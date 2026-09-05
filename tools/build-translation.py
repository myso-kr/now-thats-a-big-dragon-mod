# -*- coding: utf-8 -*-
"""Builds one language's translation from its source under translations/.

    python tools/build-translation.py vi
    python tools/build-translation.py vi --strings
    python tools/build-translation.py --all --check

A language is authored as plain data - `translations/<lang>/strings.py` defines a
dict `T` keyed the way the game keys its i18n tables, and `translations/<lang>/dialogs.py`
defines a dict `F` of `<name>.ink` to file body. Neither file reads argv, opens
anything or knows where the output goes; this driver does that once for all of them.

The strings go out through `translate.js import`, so the worksheet round-trip, the
placeholder checks and the plural handling stay in the one implementation that the
tests already cover.
"""
import argparse
import importlib.util
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "translations"
DIALOGS = ROOT / "locale" / "dialogs"

# Notation glued to a number - it reads the same in every language, so it is carried
# across rather than left to fall back to English and look untranslated in a diff.
# The empty string is here for the same reason: `fullChests.prefix` is blank in the
# English, so there is nothing for a table to say about it.
PASS_THROUGH = ("", "+", "-", "x", "%", "k", "//")


def load(lang, kind):
    """Import translations/<lang>/<kind>.py without it being on sys.path."""
    path = SRC / lang / f"{kind}.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"bd_{lang}_{kind}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def node(*args):
    out = subprocess.run(
        ["node", str(ROOT / "tools" / "translate.js"), *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode:
        sys.exit(out.stderr.strip() or f"translate.js {' '.join(args)} failed")
    return out.stdout


def strings(lang, check):
    """Fill the exported worksheet from `T` and hand it back to translate.js.

    Under --check nothing is written and the result is compared against the JSON that
    ships instead. That is the guard that keeps the table and the file it generates
    from drifting apart the way they did once already: a string edited in the
    worksheet and never carried back here would silently be undone by the next build.
    """
    mod = load(lang, "strings")
    if mod is None:
        return None
    table = mod.T
    filled, missing = [], []
    for line in node("export", lang).split("\n"):
        if not line.strip():
            continue
        if line.startswith("#"):
            filled.append(line)
            continue
        key, english = line.split("\t")[:2]
        text = table.get(key)
        if text is None and english in PASS_THROUGH:
            text = english
        if text is None:
            # Untranslated keeps the English, which is what i18next would fall back
            # to anyway - but it has to be visible here, not silent.
            missing.append((key, english))
            text = ""
        filled.append(f"{key}\t{english}\t{text}")

    work = ROOT / "target" / "translations"
    work.mkdir(parents=True, exist_ok=True)
    tsv = work / f"{lang}.tsv"
    io.open(tsv, "w", encoding="utf-8", newline="\n").write("\n".join(filled) + "\n")
    shipped = ROOT / "locale" / f"i18n.{lang}.json"
    if not check:
        sys.stdout.write(node("import", lang, str(tsv)))
        return len(table), missing, None

    # translate.js owns the shape of the file, so the only honest way to learn what
    # this table would produce is to let it write, compare, and put the file back.
    before = shipped.read_bytes() if shipped.exists() else b""
    node("import", lang, str(tsv))
    after = shipped.read_bytes()
    if after != before:
        shipped.write_bytes(before)
    return len(table), missing, None if after == before else first_difference(before, after)


def flatten(node, prefix=""):
    for key, value in node.items():
        if isinstance(value, dict):
            yield from flatten(value, f"{prefix}{key}.")
        else:
            yield f"{prefix}{key}", value


def first_difference(before, after):
    """Name the key whose text would change, rather than a byte offset."""
    was = dict(flatten(json.loads(before or b"{}")))
    now = dict(flatten(json.loads(after)))
    for key in sorted(set(was) | set(now)):
        if was.get(key) != now.get(key):
            return f"{key}: ships {was.get(key)!r}, table gives {now.get(key)!r}"
    return "the files differ but no key does"


def dialogs(lang, check):
    """Write the .ink files, or under --check name the ones that would change."""
    mod = load(lang, "dialogs")
    if mod is None:
        return None, []
    out = DIALOGS / lang
    if check:
        stale = [
            name for name, body in mod.F.items()
            if not (out / name).exists()
            or io.open(out / name, encoding="utf-8", newline="").read() != body
        ]
        extra = [p.name for p in out.iterdir() if p.name not in mod.F] if out.is_dir() else []
        return len(mod.F), sorted(stale + extra)
    out.mkdir(parents=True, exist_ok=True)
    for name, body in mod.F.items():
        io.open(out / name, "w", encoding="utf-8", newline="\n").write(body)
    return len(mod.F), []


def languages():
    known = json.loads(io.open(ROOT / "locale" / "languages.json", encoding="utf-8").read())
    return [c for c in known["languages"] if (SRC / c).is_dir()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--strings", action="store_true", help="skip the dialogues")
    ap.add_argument("--dialogs", action="store_true", help="skip the strings")
    ap.add_argument("--check", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    todo = languages() if args.all else [args.lang] if args.lang else []
    if not todo:
        sys.exit("usage: build-translation.py <lang> | --all")

    # The string half of the check compares each table against the game's own English
    # text, and that file is the one thing this repository deliberately does not carry -
    # it is the game's words. So on a machine without the game the strings cannot be
    # checked at all, and dying here would mean CI could never run this at any depth.
    # The dialogue half needs nothing but the repository, so that still runs, and what
    # was skipped is said out loud rather than passing quietly.
    if not args.dialogs and not (ROOT / "generated" / "i18n.en.json").exists():
        print("generated/i18n.en.json is not here, so the strings cannot be compared - "
              "checking the dialogues only. Run `node tools/extract-i18n.js` with the "
              "game installed to check the strings too.", file=sys.stderr)
        args.dialogs = True

    incomplete = 0
    for lang in todo:
        if not (SRC / lang).is_dir():
            sys.exit(f"no source under translations/{lang}")
        line = [lang]
        if not args.dialogs:
            got = strings(lang, args.check)
            if got is None:
                line.append("strings: source is the JSON")
            else:
                total, missing, drift = got
                line.append(f"strings: {total}" + (f", {len(missing)} left" if missing else ""))
                for key, english in missing[:20]:
                    print(f"  MISSING {key} | {english}", file=sys.stderr)
                if drift:
                    line.append(f"DRIFTED - {drift}")
                    incomplete += 1
        if not args.strings:
            count, stale = dialogs(lang, args.check)
            line.append(f"dialogs: {count}" if count else "dialogs: none")
            if stale:
                line.append(f"DRIFTED - {', '.join(stale)}")
                incomplete += 1
        print(" · ".join(line))

    if args.check and incomplete:
        sys.exit(1)


main()
