//! Patching the bundle. Each submodule owns exactly one anchor.
//!
//!   scan    brace-balance scanner (knows nothing about JS meaning)
//!   jsval   reads a JS value literal into a serde_json::Value
//!   i18n    find the English tables, merge a translation in
//!   locale  add a language to the game's own list, so settings can offer it
//!   css     inject @font-face
//!   bridge  inject the store / dispatch / stats bridges

pub mod bridge;
pub mod css;
pub mod i18n;
pub mod jsval;
pub mod locale;
pub mod scan;
pub mod tree;

use crate::cli::Options;

/// One language this binary can offer in the settings screen.
pub struct Carried {
    pub code: String,
    /// The language's own name for itself, which is what the button says.
    pub label: String,
    pub flag_file: String,
    pub tables: serde_json::Value,
}

/// Every language to offer, the selected one first.
///
/// The order matters: each locale is inserted at the same anchor, so the order they
/// go in is the order they appear in the settings screen — and the Node reference
/// builds the same list the same way. Anything that needs this list has to call
/// *this*, not rebuild it; two copies of an ordering rule is one copy too many.
///
/// A language with no catalogue entry, or none bundled, is simply not offered.
pub fn carry(cat: &crate::language::Catalogue, selected: &str) -> Vec<Carried> {
    let mut out = Vec::new();
    let mut push = |code: &str| {
        let (Some(def), Ok(t)) = (cat.languages.get(code), crate::assets::tables(code)) else {
            return;
        };
        out.push(Carried {
            code: code.to_owned(),
            label: def.name.clone(),
            flag_file: def.flag_file.clone(),
            tables: t,
        });
    };
    push(selected);
    for other in crate::assets::available() {
        if other != selected {
            push(&other);
        }
    }
    out
}

/// What to change and how, decided up front. The intercept loop consults only this.
pub struct Plan {
    /// The language being patched in, with its fonts. None means the game is left in
    /// whatever language it chose for itself.
    pub language: Option<(String, crate::language::Language)>,
    pub cheat: bool,
    pub autoplay: bool,
    pub tables: Option<serde_json::Value>,
    /// Every language to add to the game's own list, the selected one first.
    ///
    /// All of them go in, not just the selected one: the settings screen is a list,
    /// and a player whose saved choice is missing from it sees raw i18n keys.
    pub carried: Vec<Carried>,
}

impl Plan {
    /// Decide the language here, once, so the intercept loop never has to.
    pub fn build(opt: &Options) -> Result<(Self, String), String> {
        if !opt.translate {
            return Ok((
                Self {
                    language: None,
                    cheat: opt.cheat,
                    autoplay: opt.autoplay,
                    tables: None,
                    carried: Vec::new(),
                },
                "translation disabled".to_owned(),
            ));
        }
        let cat = crate::assets::catalogue()?;
        let choice = crate::language::resolve(
            &cat,
            opt.lang.as_deref(),
            &crate::language::system_locale(),
            &crate::assets::available(),
        );
        let language = match &choice.lang {
            Some(code) => {
                let def = cat
                    .languages
                    .get(code)
                    .ok_or_else(|| format!("locale/languages.json has no entry for {code}"))?;
                Some((code.clone(), def.clone()))
            }
            None => None,
        };
        let tables = match &choice.lang {
            Some(code) => Some(crate::assets::tables(code)?),
            None => None,
        };

        let carried = match &choice.lang {
            Some(code) => carry(&cat, code),
            None => Vec::new(),
        };

        Ok((
            Self {
                language,
                cheat: opt.cheat,
                autoplay: opt.autoplay,
                tables,
                carried,
            },
            choice.reason,
        ))
    }

    /// The language code, when one is being applied.
    pub fn lang(&self) -> Option<&str> {
        self.language.as_ref().map(|(c, _)| c.as_str())
    }

    /// The fonts to serve and to name in the CSS.
    pub fn fonts(&self) -> &[crate::language::Font] {
        self.language
            .as_ref()
            .map_or(&[], |(_, d)| d.fonts.as_slice())
    }

    /// The system font stack to put behind ours.
    pub fn fallback(&self) -> &[String] {
        self.language
            .as_ref()
            .map_or(&[], |(_, d)| d.fallback.as_slice())
    }
}

/// A tick or a cross, for a log line that reports several booleans at once.
fn tick(ok: bool) -> &'static str {
    if ok {
        "✔"
    } else {
        "✘"
    }
}

/// What one bundle patch actually did. Printed once, so a silent no-op is visible.
#[derive(Debug, Default)]
pub struct Applied {
    pub namespaces: Vec<String>,
    pub translated: usize,
    pub total: usize,
    pub time_scale: bool,
    pub dispatch: Option<String>,
    pub stats: Option<String>,
    pub stores_wrapped: Option<String>,
    pub stores_found: Vec<String>,
    /// The identifier the dungeon's scene has in the bundle, when it was found.
    pub dungeon_scene: Option<String>,
    /// How many upgrade tree nodes were read out of the bundle. Zero means autoplay
    /// cannot send the unlock signals, and stalls at twelve of the eighty-eight.
    pub tree_nodes: usize,
    /// Set when the languages went into the game's own list rather than over `en`.
    pub added: Option<locale::AddedAll>,
}

/// Apply every bundle edit in one pass: Korean tables, the time scale, and the three
/// bridges.
///
/// Order matters only in that the i18n replacement changes byte offsets, so it runs
/// first and every bridge searches the already-rewritten source.
pub fn bundle(src: &str, plan: &Plan) -> Result<(String, Applied), String> {
    let mut out = src.to_owned();
    let mut rep = Applied::default();

    if let Some(ko) = &plan.tables {
        // Preferred: add the languages to the game's own list, so English stays
        // English and the player can switch in the settings screen. Everything is
        // built against the untouched source, because add_locale inserts whole
        // locales rather than rewriting the English tables in place.
        let mut merged = Vec::with_capacity(plan.carried.len());
        for c in &plan.carried {
            match i18n::merged(&out, &c.tables) {
                Ok((tables, r)) => {
                    // The selected language is the one whose counts get reported.
                    if c.code == plan.lang().unwrap_or_default() {
                        rep.namespaces = r.replaced;
                        rep.translated = r.translated;
                        rep.total = r.total;
                    }
                    merged.push((tables, i18n::time_units(&c.tables)));
                }
                Err(e) => return Err(e),
            }
        }

        let bundled: Vec<locale::Bundled> = plan
            .carried
            .iter()
            .zip(merged.iter())
            .map(|(c, (tables, units))| locale::Bundled {
                lang: &c.code,
                label: &c.label,
                flag_file: &c.flag_file,
                tables,
                units: units.as_deref(),
            })
            .collect();

        match locale::add_languages(&out, &bundled, plan.lang()) {
            Some((code, added)) => {
                out = code;
                rep.time_scale = added.time_scale > 0;
                rep.added = Some(added);
            }
            None => {
                // Fall back to overwriting the en slot, which needs only the table
                // anchors. A game update that moves the settings UI then costs the
                // settings integration, not the translation.
                let (code, r) = i18n::patch(&out, ko)?;
                out = code;
                rep.namespaces = r.replaced;
                rep.translated = r.translated;
                rep.total = r.total;

                let (code, patched) = i18n::patch_time_scale(&out, ko);
                out = code;
                rep.time_scale = patched;
            }
        }
    }

    // Autoplay needs dispatch to issue real game commands; the cheat widget needs the
    // stores to reach real state. The stats table is read by both.
    if plan.autoplay {
        let d = bridge::inject_dispatch(&out);
        out = d.code;
        rep.dispatch = d.id;

        let s = bridge::inject_stats(&out);
        out = s.code;
        rep.stats = s.id;
    }
    if plan.autoplay || plan.cheat {
        let b = bridge::inject_stores(&out);
        out = b.code;
        rep.stores_wrapped = b.wrapped;
        rep.stores_found = b.found;
    }

    // The dungeon's Babylon scene, which is otherwise reachable from nowhere.
    let d = bridge::inject_dungeon(&out);
    out = d.code;
    rep.dungeon_scene = d.id;

    // Three things the injected scripts read off `window`, put in front of the bundle
    // rather than into the prelude: the tree is read from this very source, so it
    // cannot be known before the bundle arrives, and the names come from the tables
    // merged above. All three are read lazily in the renderer, so the prelude running
    // first is not a problem. Each is optional - a missing piece costs one feature.
    let upgrade_tree = tree::extract(src);
    rep.tree_nodes = tree::count_nodes(upgrade_tree.as_ref());
    let mut prologue = String::new();
    if let Some(t) = &upgrade_tree {
        prologue.push_str(&format!("window.__bd_upgradeTree={t};"));
    }
    prologue.push_str(&format!(
        "window.__bd_upgradeNames={};",
        upgrade_titles(plan.tables.as_ref())
    ));
    prologue.push_str(&format!(
        "window.__bd_levelNames={};",
        plan.tables
            .as_ref()
            .and_then(|t| t.get("levels"))
            .and_then(|l| l.get("names"))
            .cloned()
            .unwrap_or_else(|| serde_json::Value::Object(serde_json::Map::new()))
    ));
    Ok((prologue + &out, rep))
}

/// `{"carpalCure":"Carpal Cure",...}` - what the cheat widget calls each upgrade.
fn upgrade_titles(tables: Option<&serde_json::Value>) -> serde_json::Value {
    let mut out = serde_json::Map::new();
    if let Some(details) = tables
        .and_then(|t| t.get("upgrades"))
        .and_then(|u| u.get("details"))
        .and_then(serde_json::Value::as_object)
    {
        for (id, v) in details {
            if let Some(title) = v.get("title").and_then(serde_json::Value::as_str) {
                out.insert(id.clone(), serde_json::Value::String(title.to_owned()));
            }
        }
    }
    serde_json::Value::Object(out)
}

impl Applied {
    /// One line per anchor, so a failure names itself instead of being inferred from
    /// the game behaving oddly later.
    pub fn report(&self, plan: &Plan) {
        if plan.lang().is_some() {
            crate::log::probe(
                "i18n tables",
                self.namespaces.len() == i18n::NAMESPACES.len(),
                &format!(
                    "{}/{} namespaces, {} of {} strings translated",
                    self.namespaces.len(),
                    i18n::NAMESPACES.len(),
                    self.translated,
                    self.total
                ),
            );
            crate::log::probe("time units", self.time_scale, "");

            // Which of the two paths was taken. Overwriting `en` still translates the
            // game, but the settings screen then offers no way back to English, so it
            // is worth saying out loud rather than looking identical in the log.
            match &self.added {
                Some(a) => crate::log::probe(
                    "settings languages",
                    a.supported && a.flag && a.labels > 0,
                    &format!(
                        "{} · list {} · flags {} · labels {} · scale {}/{} · fallback {} · default {}",
                        a.langs.join(", "),
                        tick(a.supported),
                        tick(a.flag),
                        a.labels,
                        a.time_scale,
                        a.langs.len(),
                        tick(a.fallback),
                        tick(a.default),
                    ),
                ),
                None => crate::log::probe(
                    "settings languages",
                    false,
                    "settings anchors moved; translated over the English slot instead",
                ),
            }
        }
        if plan.autoplay {
            crate::log::probe(
                "dispatch bridge",
                self.dispatch.is_some(),
                self.dispatch.as_deref().unwrap_or("autoplay will not work"),
            );
            crate::log::probe(
                "stats table",
                self.stats.is_some(),
                self.stats.as_deref().unwrap_or("decisions will be poorer"),
            );
        }
        if plan.autoplay || plan.cheat {
            crate::log::probe(
                "store bridge",
                self.stores_wrapped.is_some(),
                &format!("{} stores", self.stores_found.len()),
            );
        }
    }
}
