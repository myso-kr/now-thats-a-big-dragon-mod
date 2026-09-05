# -*- coding: utf-8 -*-
"""Writes the GitHub Pages site: one page per bundled language, plus the data it needs.

    python tools/build-site.py            # write docs/
    python tools/build-site.py --check    # write nothing, report drift

The language list is not repeated here. It is read from `locale/languages.json`, the
same file the launcher matches on, and a language appears on the site exactly when its
translation is bundled - so a page cannot claim a translation that does not ship.

What is written:

    docs/_data/languages.yml   the catalogue, for the layout to loop over
    docs/<code>/index.md       one page per language
    docs/index.md              English, and the hreflang x-default

The prose is here rather than in the pages because every page says the same few things
and the only thing that changes is the language. Keeping it in one table is what makes
twenty-two pages maintainable, and what stops one of them quietly going stale.
"""
import argparse
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://myso-kr.github.io/now-thats-a-big-dragon-mod"

# The site's own chrome, in every language, lives in tools/site_strings.py - the same
# shape as translations/<lang>/strings.py, so there is one convention rather than two.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_strings import S as COPY  # noqa: E402
from site_safety import SAFETY  # noqa: E402
from site_faq import Q as QUESTIONS, ANSWERS  # noqa: E402
from site_howto import H as STEPS  # noqa: E402

# The four warnings live in their own table because they are the ones that can cost
# somebody something. Merged here so the layout sees one set of strings.
for _code, _warnings in SAFETY.items():
    COPY.setdefault(_code, {}).update(_warnings)

# The questions answer engines ask. Their answers are the page's own sentences, paired
# by tools/site_faq.py, so a quoted answer cannot drift from the page it came out of.
for _code, _questions in QUESTIONS.items():
    COPY.setdefault(_code, {}).update(_questions)

# And the install steps, which the layout publishes as schema.org/HowTo.
for _code, _steps in STEPS.items():
    COPY.setdefault(_code, {}).update(_steps)


def catalogue():
    return json.loads(io.open(ROOT / "locale" / "languages.json", encoding="utf-8").read())


def bundled():
    """The languages that actually ship, in the order the README lists them."""
    cat = catalogue()["languages"]
    out = []
    for code, e in cat.items():
        if not (ROOT / "locale" / f"i18n.{code}.json").exists():
            continue
        fonts = [f for f in e.get("fonts", []) if f.get("replaces") == "everyday_standard"]
        body = fonts[0]["file"] if fonts else None
        out.append({
            "code": code,
            "name": e["name"],
            "english": e["english"],
            "share": e.get("steamShare", 0),
            "status": e.get("status", "draft"),
            # Which font draws it, which is the one thing a reader of that page cannot
            # find out for themselves.
            "drawn": body is None or body.startswith("Everyday_Standard"),
            "dialogs": len(list((ROOT / "locale" / "dialogs" / code).glob("*.ink"))),
        })
    out.sort(key=lambda x: -x["share"])
    return out


def yaml_of(langs):
    lines = ["# Written by tools/build-site.py from locale/languages.json.",
             "# One list, not two: this is the same catalogue the launcher matches on.",
             ""]
    for l in langs:
        lines.append(f"- code: \"{l['code']}\"")
        lines.append(f"  name: \"{l['name']}\"")
        lines.append(f"  english: \"{l['english']}\"")
        lines.append(f"  share: {l['share']}")
        lines.append(f"  status: \"{l['status']}\"")
        lines.append(f"  drawn: {'true' if l['drawn'] else 'false'}")
        lines.append(f"  dialogs: {l['dialogs']}")
    return "\n".join(lines) + "\n"


def quote(v):
    """A YAML double-quoted scalar. The strings carry apostrophes and colons."""
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def i18n_yaml():
    """Every string the layout says, keyed by language, English first as the fallback."""
    lines = ["# Written by tools/build-site.py from tools/site_strings.py.",
             "# The layout looks these up by the page's language and falls back to English,",
             "# so a page is localised rather than an English page with a translated headline.",
             ""]
    for code in ["en"] + [c for c in COPY if c != "en"]:
        lines.append(f"{quote(code)}:")
        for key, value in COPY[code].items():
            lines.append(f"  {key}: {quote(value)}")
    return "\n".join(lines) + "\n"


def faq_yaml():
    """Which string asks each question and which one answers it.

    The layout walks this to build both the visible question-and-answer list and the
    FAQPage structured data, from the same pair - so what a reader sees and what an
    answer engine quotes are the same sentence.
    """
    lines = ["# Written by tools/build-site.py from tools/site_faq.py.",
             "# question: the key that asks it. answer: the key that already answers it.",
             ""]
    for q, a in ANSWERS.items():
        lines.append(f"- question: {quote(q)}")
        lines.append(f"  answer: {quote(a)}")
    return chr(10).join(lines) + chr(10)


def body_of(path):
    """Whatever a page already says below its front matter.

    The generator owns the front matter and nothing else. English and Korean carry pages
    somebody sat down and wrote - install steps, the debugging-port warning, the takedown
    address - and an earlier version of this file replaced both with a stub. Five hundred
    lines of safety notice are not the generator's to throw away.
    """
    if not path.exists():
        return ""
    text = io.open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return "" if end < 0 else text[end + 4:].lstrip("\n")


def page_of(l, body=""):
    """One language's page: front matter from the catalogue, body left as it was."""
    code = l["code"]
    c = COPY[code]
    front = f"""---
layout: default
lang: {quote(code)}
code: {quote(code)}
title: {quote(c['title'])}
description: {quote(c['description'])}
native: {quote(l['name'])}
english: {quote(l['english'])}
share: {l['share']}
status: {quote(l['status'])}
drawn: {'true' if l['drawn'] else 'false'}
dialogs: {l['dialogs']}
---
"""
    return front + ("\n" + body if body.strip() else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="write nothing, report drift")
    args = ap.parse_args()

    langs = bundled()
    missing = [l["code"] for l in langs if l["code"] not in COPY]
    if missing:
        sys.exit(f"no site copy written for: {', '.join(missing)}")
    # A page that is missing one of these is a page that failed to warn somebody.
    keys = set(COPY["en"])
    for l in langs:
        gaps = sorted(keys - set(COPY[l["code"]]))
        if gaps:
            sys.exit(f"{l['code']} is missing site strings: {', '.join(gaps)}")

    wrote, drift = [], []
    def put(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        old = io.open(path, encoding="utf-8").read() if path.exists() else None
        if old == text:
            return
        if args.check:
            drift.append(str(path.relative_to(ROOT)))
            return
        io.open(path, "w", encoding="utf-8", newline="\n").write(text)
        wrote.append(str(path.relative_to(ROOT)))

    put(DOCS / "_data" / "languages.yml", yaml_of(langs))
    put(DOCS / "_data" / "i18n.yml", i18n_yaml())
    put(DOCS / "_data" / "faq.yml", faq_yaml())
    english = {"code": "en", "name": "English", "english": "English", "share": 0,
               "status": "source", "drawn": True, "dialogs": 32}
    root = DOCS / "index.md"
    put(root, page_of(english, body_of(root)))
    for l in langs:
        if l["code"] == "en":
            continue
        page = DOCS / l["code"] / "index.md"
        put(page, page_of(l, body_of(page)))

    total = sum(l["share"] for l in langs)
    print(f"{len(langs)} languages, {total:.2f}% of Steam")
    if args.check:
        if drift:
            print("out of date:")
            for d in drift:
                print(f"  {d}")
            return 1
        print("the site is up to date")
        return 0
    for w in wrote:
        print(f"  wrote {w}")
    if not wrote:
        print("  nothing to do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
