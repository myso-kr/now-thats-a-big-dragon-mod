//! Patches a real game bundle and checks the result, end to end.
//!
//! The unit tests all run against hand-written fixtures, which is the only way to
//! state a case precisely — but it also means none of them would notice if the real
//! bundle stopped matching an anchor. This test closes that gap.
//!
//! It needs a decrypted bundle, which cannot be committed (it is the game's own
//! code), so it skips itself unless one is pointed at:
//!
//!   node tools/dry-run.js
//!   BD_BUNDLE_JS=%TEMP%/bd-dryrun/original-index-C5vCJZoP.js cargo test --test bundle
//!
//! When the game updates, running this against the new bundle is what tells you
//! which anchor moved.

use std::path::PathBuf;

/// The bundle to test against, or None when the environment does not name one.
fn bundle() -> Option<(String, PathBuf)> {
    let p = PathBuf::from(std::env::var("BD_BUNDLE_JS").ok()?);
    let src = std::fs::read_to_string(&p).ok()?;
    Some((src, p))
}

/// The language to patch in. Korean by default; BD_LANG points the whole file at
/// another one, which is what the byte-for-byte comparison needs when the Node
/// dry-run was produced for a different language.
fn lang() -> String {
    std::env::var("BD_LANG").unwrap_or_else(|_| "ko".to_owned())
}

fn ko_tables() -> serde_json::Value {
    bigdragon::assets::tables(&lang()).expect("the bundled translation")
}

/// A plan that patches the language in, the way that system would get it.
fn korean_plan() -> bigdragon::patch::Plan {
    let cat = bigdragon::assets::catalogue().expect("locale/languages.json");
    let code = lang();
    let def = cat
        .languages
        .get(&code)
        .expect("the catalogue entry")
        .clone();
    // The list and its order come from the launcher itself, so the test cannot drift
    // away from what ships.
    let carried = bigdragon::patch::carry(&cat, &code);
    bigdragon::patch::Plan {
        language: Some((code, def)),
        cheat: true,
        autoplay: true,
        tables: Some(ko_tables()),
        carried,
    }
}

macro_rules! skip_unless_bundle {
    () => {
        match bundle() {
            Some(x) => x,
            None => {
                eprintln!("skipped: set BD_BUNDLE_JS to a decrypted bundle to run this");
                return;
            }
        }
    };
}

#[test]
fn finds_every_i18n_namespace_in_the_real_bundle() {
    let (src, _) = skip_unless_bundle!();
    let ids = bigdragon::patch::i18n::table_ids(&src).expect("the en table map");
    for ns in bigdragon::patch::i18n::NAMESPACES {
        assert!(ids.iter().any(|(k, _)| k == ns), "namespace {ns} not found");
    }
}

#[test]
fn translates_the_same_number_of_strings_the_node_patcher_does() {
    let (src, _) = skip_unless_bundle!();
    let (_, rep) = bigdragon::patch::i18n::patch(&src, &ko_tables()).expect("patch");
    assert_eq!(
        rep.replaced.len(),
        bigdragon::patch::i18n::NAMESPACES.len(),
        "every table should be replaced"
    );
    // Both numbers move on their own: `total` grows when the game adds strings (572
    // in 1.0.5, 621 with the artifacts namespace), and `translated` grows when a
    // translation does. Pinning either to a literal only buys a test that has to be
    // edited every time real work happens — and the byte-for-byte comparison below
    // already proves Rust and Node counted the same tables the same way, which is
    // what pinning was for. What is asserted here is that nothing collapsed.
    assert!(
        rep.total >= 572,
        "only {} strings found; the tables look truncated",
        rep.total
    );
    assert!(
        rep.translated > rep.total / 2,
        "only {} of {} strings translated; the table looks like it was not applied",
        rep.translated,
        rep.total
    );
}

#[test]
fn every_anchor_still_matches() {
    let (src, _) = skip_unless_bundle!();
    let plan = korean_plan();
    let (out, rep) = bigdragon::patch::bundle(&src, &plan).expect("bundle patch");

    assert_eq!(
        rep.namespaces.len(),
        bigdragon::patch::i18n::NAMESPACES.len(),
        "A1 i18n tables"
    );
    assert!(rep.time_scale, "A2 time units");
    assert!(rep.stores_wrapped.is_some(), "A3 store factory");
    assert!(rep.dispatch.is_some(), "A4 dispatch");
    assert!(rep.stats.is_some(), "A5 stats table");
    assert!(
        rep.stores_found.contains(&"__slots".to_string()),
        "A6 slot registry"
    );

    // The languages went into the game's own list rather than over the English one.
    let added = rep.added.as_ref().expect("the settings integration");
    assert_eq!(
        added.resources,
        added.langs.len(),
        "every language in the bundle"
    );
    assert!(added.supported, "A7 supported-language list");
    assert!(added.flag, "A8 flag map");
    assert!(added.labels > 0, "A9 language names");
    assert!(added.fallback, "A10 i18next fallbackLng");
    assert!(added.default, "A11 fresh-profile default");
    assert!(
        added.langs.contains(&lang()),
        "the selected language is in the list"
    );
    assert!(
        out.contains(r#"languages:{en:"English""#),
        "English is added to, never overwritten"
    );

    // Every bridge has to be present in the emitted code, not merely reported.
    for needle in [
        "window.__bd_dispatch=",
        "window.__bd_stats=",
        "window.__bd_stores",
        "window.__bd_slotStores=",
    ] {
        assert!(
            out.contains(needle),
            "{needle} missing from the patched bundle"
        );
    }
}

#[test]
fn the_patched_bundle_is_still_parseable_javascript() {
    let (src, _) = skip_unless_bundle!();
    let plan = korean_plan();
    let (out, _) = bigdragon::patch::bundle(&src, &plan).expect("bundle patch");

    let dir = std::env::temp_dir().join("bd-rust-patch");
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("patched.js");
    std::fs::write(&path, &out).unwrap();

    // `node --check` is the only honest syntax check available here. Without node on
    // PATH the test says so rather than passing quietly.
    let out = std::process::Command::new("node")
        .arg("--check")
        .arg(&path)
        .output();
    match out {
        Ok(o) => assert!(
            o.status.success(),
            "the patched bundle is not valid JavaScript:\n{}",
            String::from_utf8_lossy(&o.stderr)
        ),
        Err(e) => eprintln!("skipped the syntax check: node is not runnable ({e})"),
    }
}

#[test]
fn korean_actually_reaches_the_output() {
    let (src, _) = skip_unless_bundle!();
    let ko = ko_tables();
    let (out, _) = bigdragon::patch::i18n::patch(&src, &ko).expect("patch");
    // Pick a real translated string out of the locale file and look for it.
    let sample = ko["common"]["wishlistNow"].as_str();
    if let Some(s) = sample {
        assert!(
            out.contains(s),
            "translated string {s:?} is not in the output"
        );
    }
    let (out, patched) = bigdragon::patch::i18n::patch_time_scale(&out, &ko);
    assert!(patched, "the time scale was not rewritten");
    assert!(
        !out.contains("{seconds:1,minutes:60"),
        "the English scale is still there"
    );
}

/// The two implementations have to produce the same bytes, not merely both work.
///
/// Node is the reference: it is the one that gets edited first when an anchor moves,
/// and the Rust launcher is what ships. A divergence here is the failure that would
/// otherwise show up only as a subtly different game.
///
///   node tools/dry-run.js
///   BD_BUNDLE_JS=%TEMP%/bd-dryrun/original-index-C5vCJZoP.js ///     BD_NODE_JS=%TEMP%/bd-dryrun/index-C5vCJZoP.js cargo test --test bundle
#[test]
fn the_rust_output_matches_the_node_output_byte_for_byte() {
    let (src, _) = skip_unless_bundle!();
    let Ok(p) = std::env::var("BD_NODE_JS") else {
        eprintln!("skipped: set BD_NODE_JS to the Node dry-run output to run this");
        return;
    };
    let want = std::fs::read_to_string(&p).expect("the Node output");
    let (got, _) = bigdragon::patch::bundle(&src, &korean_plan()).expect("bundle patch");

    if got == want {
        return;
    }
    // Report where they part company rather than dumping eight megabytes.
    let at = got
        .as_bytes()
        .iter()
        .zip(want.as_bytes())
        .position(|(a, b)| a != b)
        .unwrap_or_else(|| got.len().min(want.len()));
    // Slicing a &str at an arbitrary byte offset panics mid-character, and the
    // translations are full of multi-byte ones — so every edge is walked back to a
    // boundary first.
    let floor = |s: &str, mut i: usize| {
        while i > 0 && !s.is_char_boundary(i) {
            i -= 1;
        }
        i
    };
    let window = |s: &str, from: usize, len: usize| {
        let a = floor(s, from.min(s.len()));
        let b = floor(s, (a + len).min(s.len()));
        s[a..b].to_owned()
    };
    panic!(
        "rust and node diverge at byte {at} (rust {} bytes, node {} bytes)
  before: {}
  rust:   {}
  node:   {}",
        got.len(),
        want.len(),
        window(&got, at.saturating_sub(80), 80),
        window(&got, at, 120),
        window(&want, at, 120),
    );
}

/// The same byte-for-byte check for the stylesheet.
///
/// The bundle comparison would not have caught it: the CSS is patched by a different
/// module, and the two drifted apart over a language that replaces only one of the
/// game's two font slots.
///
///   node tools/dry-run.js --lang=ru
///   BD_LANG=ru BD_CSS=%TEMP%/bd-dryrun/original-style-CCeH8nWv.css ///     BD_NODE_CSS=%TEMP%/bd-dryrun/style-CCeH8nWv.css cargo test --test bundle
#[test]
fn the_rust_css_matches_the_node_css_byte_for_byte() {
    let (Ok(src), Ok(want)) = (std::env::var("BD_CSS"), std::env::var("BD_NODE_CSS")) else {
        eprintln!("skipped: set BD_CSS and BD_NODE_CSS to the dry-run stylesheets");
        return;
    };
    let src = std::fs::read_to_string(&src).expect("the original stylesheet");
    let want = std::fs::read_to_string(&want).expect("the Node stylesheet");
    let plan = korean_plan();
    let (got, rep) = bigdragon::patch::css::patch(&src, plan.fonts(), plan.fallback());

    assert!(rep.stacks > 0, "no font stack was rewritten at all");
    if got == want {
        return;
    }
    let at = got
        .as_bytes()
        .iter()
        .zip(want.as_bytes())
        .position(|(a, b)| a != b)
        .unwrap_or_else(|| got.len().min(want.len()));
    let floor = |s: &str, mut i: usize| {
        while i > 0 && !s.is_char_boundary(i) {
            i -= 1;
        }
        i
    };
    let window = |s: &str, from: usize, len: usize| {
        let a = floor(s, from.min(s.len()));
        let b = floor(s, (a + len).min(s.len()));
        s[a..b].to_owned()
    };
    panic!(
        "rust and node css diverge at byte {at} (rust {} bytes, node {} bytes)
  before: {}
  rust:   {}
  node:   {}",
        got.len(),
        want.len(),
        window(&got, at.saturating_sub(80), 80),
        window(&got, at, 120),
        window(&want, at, 120),
    );
}

/// The two launchers have to hand the renderer the same dialogue option labels.
///
/// Autoplay picks an option by where it sits in the .ink file and finds it on screen by
/// its label. If Rust's table disagreed with Node's, autoplay would choose the wrong
/// option in silence - paying a ransom instead of defending, say - and no log line
/// would say so.
///
///   node tools/dialog-choices.js > %TEMP%/choices.json
///   BD_NODE_CHOICES=%TEMP%/choices.json cargo test --test bundle
#[test]
fn the_rust_dialogue_choices_match_the_node_ones() {
    let Ok(p) = std::env::var("BD_NODE_CHOICES") else {
        eprintln!("skipped: set BD_NODE_CHOICES to the output of tools/dialog-choices.js");
        return;
    };
    let want: serde_json::Value =
        serde_json::from_str(&std::fs::read_to_string(&p).expect("the Node output"))
            .expect("valid JSON");
    let langs = want.as_object().expect("an object per language");
    assert!(!langs.is_empty(), "no languages in the Node output");

    for (lang, table) in langs {
        let got = bigdragon::ink::choice_table_for(lang);
        assert_eq!(&got, table, "{lang}: the option labels differ");
    }
}
