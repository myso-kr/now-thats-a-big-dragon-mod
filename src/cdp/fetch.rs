//! Intercepts the game's asset requests through the Fetch domain.
//!
//! What to change, and how, is decided by patch::Plan. This file only intercepts,
//! asks, and answers.

use crate::cdp::Session;
use crate::patch::Plan;
use base64::{engine::general_purpose::STANDARD as B64, Engine};
use serde_json::json;

/// The requests we care about. The ones we rewrite have to be caught at the Response
/// stage, which is the only way to get the original body in hand.
const PATTERNS: &[(&str, &str)] = &[
    ("*/assets/index-*.js*", "Response"),
    ("*/assets/style-*.css*", "Response"),
    ("*/dialogs/*.ink*", "Request"),
    ("*/fonts/bd-*", "Request"),
    ("*/flags/*", "Request"),
];

pub fn serve(s: &mut Session, plan: &Plan) -> Result<(), Box<dyn std::error::Error>> {
    let patterns: Vec<_> = PATTERNS
        .iter()
        .map(|(u, stage)| json!({ "urlPattern": u, "requestStage": stage }))
        .collect();
    s.send("Fetch.enable", json!({ "patterns": patterns }))?;
    inject_scripts(s, plan)?;
    s.send("Page.reload", json!({ "ignoreCache": true }))?;
    crate::log!("ready. Close this window and the patch is gone.");

    loop {
        let msg = match s.next_event() {
            Ok(m) => m,
            // The game exiting closes the socket. That is how a run normally ends,
            // not a failure, and the launcher has to stop with it rather than linger.
            Err(_) if s.closed() => {
                crate::log!("the game exited. Closing the launcher.");
                return Ok(());
            }
            Err(e) => return Err(e.into()),
        };
        if msg.get("method").and_then(|m| m.as_str()) != Some("Fetch.requestPaused") {
            continue;
        }
        let p = &msg["params"];
        let id = p["requestId"].as_str().unwrap_or_default().to_owned();
        let url = p["request"]["url"].as_str().unwrap_or_default().to_owned();
        // Carried through to fulfillRequest for the rewritten assets. Replacing the
        // original headers with a bare content-type is enough to make the game
        // refuse the response entirely.
        let headers = p["responseHeaders"].clone();
        // A gemshell:// response carries no HTTP status, so this arrives as 0 or not
        // at all. Echoing a 0 back makes the renderer reject the response outright:
        // the script never runs, the game shows its "something went wrong" page, and
        // nothing anywhere says why.
        let status = match p["responseStatusCode"].as_u64() {
            Some(n) if n >= 100 => n,
            _ => 200,
        };
        if let Err(e) = handle(s, plan, &id, &url, &headers, status) {
            crate::warn!("could not handle {url}: {e}");
            let _ = s.send("Fetch.continueRequest", json!({ "requestId": id }));
        }
    }
}

/// Keep the original response headers, minus content-length (we recompute it), and
/// make sure a content-type is present.
fn headers_for(original: &serde_json::Value, fallback_mime: &str) -> serde_json::Value {
    let mut out: Vec<serde_json::Value> = Vec::new();
    let mut has_type = false;
    if let Some(list) = original.as_array() {
        for h in list {
            let name = h["name"].as_str().unwrap_or_default();
            if name.eq_ignore_ascii_case("content-length") {
                continue;
            }
            if name.eq_ignore_ascii_case("content-type") {
                has_type = true;
            }
            out.push(h.clone());
        }
    }
    if !has_type {
        out.push(json!({ "name": "Content-Type", "value": fallback_mime }));
    }
    serde_json::Value::Array(out)
}

fn handle(
    s: &mut Session,
    plan: &Plan,
    id: &str,
    url: &str,
    headers: &serde_json::Value,
    status: u64,
) -> Result<(), String> {
    // Fonts: hand back the bytes we shipped inside the binary. Only the URLs this
    // language planted in the CSS are ours to answer.
    if let Some((_, bytes)) = crate::assets::font_for(url, plan.fonts()) {
        return fulfill_bytes(s, id, "font/woff2", bytes);
    }

    // Flags: the settings screen shows one per language, including the ones the
    // player has not picked, so every carried language's file has to be served.
    // The game's own five keep their own files and fall through.
    if url.contains("/flags/") {
        if let Some(bytes) = crate::assets::flag_for(url, &plan.carried) {
            return fulfill_bytes(s, id, "image/png", bytes);
        }
        return cont(s, id);
    }

    // Dialogue. Which folder the game asks for depends on the language it is running
    // in, and adding our language to its settings means it now asks for ours —
    // `dialogs/ko/intro.ink`, a path the game's own assets do not have. Answering
    // only the `en` folder left the game to its own handler, which returned the
    // string "Not found" and the game typed that out as the dialogue.
    if url.contains("/dialogs/") {
        if let Some((folder, id_str)) = dialog_path(url) {
            // A request for a language we carry is served in that language. A request
            // for `en` is served in the applied one, which is the path taken when the
            // settings integration failed and the translation went over the en slot.
            let lang = if crate::assets::available().contains(&folder) {
                Some(folder)
            } else if folder == "en" {
                plan.lang().map(str::to_owned)
            } else {
                None
            };
            if let Some(lang) = lang {
                if let Some(text) = crate::assets::dialogs(&lang).get(id_str.as_str()) {
                    return fulfill_text(s, id, "text/plain; charset=utf-8", text);
                }
            }
        }
        return cont(s, id);
    }

    // The bundle and the stylesheet are rewritten from their real responses, so both
    // are caught at the Response stage - the original body is the input.
    if url.contains("/assets/index-") && url.contains(".js") {
        let src = response_body(s, id)?;
        let (code, rep) = crate::patch::bundle(&src, plan)?;
        rep.report(plan);
        crate::log!("bundle {} -> {} bytes", src.len(), code.len());
        return fulfill(
            s,
            id,
            status,
            &headers_for(headers, "application/javascript"),
            code.as_bytes(),
        );
    }
    if url.contains("/assets/style-") && url.contains(".css") && plan.lang().is_some() {
        let src = response_body(s, id)?;
        let (css, rep) = crate::patch::css::patch(&src, plan.fonts(), plan.fallback());
        // A language may bundle no font at all — Spanish and Thai do, because the
        // game's own font already draws Spanish and no pixel font draws Thai. Then
        // zero @font-face rules is the correct outcome, and what still has to happen
        // is the system fallback going onto both stacks.
        let want = plan.fonts().len();
        crate::log::probe(
            "fonts",
            rep.faces == want && rep.stacks > 0,
            &format!(
                "{}/{} faces, {} stacks{}",
                rep.faces,
                want,
                rep.stacks,
                if want == 0 {
                    " (system font by design)"
                } else {
                    ""
                }
            ),
        );
        return fulfill(
            s,
            id,
            status,
            &headers_for(headers, "text/css"),
            css.as_bytes(),
        );
    }

    cont(s, id)
}

/// The original response body of a paused request, as text.
///
/// Only available at the Response stage; at the Request stage there is no body yet,
/// which is why the two rewritten assets are intercepted there and not earlier.
fn response_body(s: &mut Session, id: &str) -> Result<String, String> {
    let r = s.send("Fetch.getResponseBody", json!({ "requestId": id }))?;
    let body = r["body"].as_str().unwrap_or_default();
    if r["base64Encoded"].as_bool().unwrap_or(false) {
        let raw = B64
            .decode(body)
            .map_err(|e| format!("body is not valid base64: {e}"))?;
        String::from_utf8(raw).map_err(|e| format!("body is not valid UTF-8: {e}"))
    } else {
        Ok(body.to_owned())
    }
}

/// `…/dialogs/en/intro.ink` becomes `intro`. Only the en slot is replaced.
/// The language and dialogue id in `…/dialogs/<lang>/<id>.ink`.
fn dialog_path(url: &str) -> Option<(String, String)> {
    let after = url.split("/dialogs/").nth(1)?;
    let (lang, rest) = after.split_once('/')?;
    let name = rest.split(['?', '#']).next()?;
    let id = name.strip_suffix(".ink")?;
    Some((lang.to_owned(), id.to_owned()))
}

fn cont(s: &mut Session, id: &str) -> Result<(), String> {
    s.send("Fetch.continueRequest", json!({ "requestId": id }))
        .map(|_| ())
}

fn fulfill_text(s: &mut Session, id: &str, mime: &str, body: &str) -> Result<(), String> {
    fulfill_bytes(s, id, mime, body.as_bytes())
}

fn fulfill_bytes(s: &mut Session, id: &str, mime: &str, body: &[u8]) -> Result<(), String> {
    let headers = json!([{ "name": "Content-Type", "value": mime }]);
    fulfill(s, id, 200, &headers, body)
}

fn fulfill(
    s: &mut Session,
    id: &str,
    status: u64,
    headers: &serde_json::Value,
    body: &[u8],
) -> Result<(), String> {
    s.send(
        "Fetch.fulfillRequest",
        json!({
            "requestId": id,
            "responseCode": status,
            "responseHeaders": headers,
            "body": B64.encode(body),
        }),
    )
    .map(|_| ())
}

/// Plant the widget and autoplay before the document loads.
///
/// The engine modules go in ahead of engine.js. The browser has no module system,
/// so concatenation in the right order *is* the dependency wiring — engine.js reads
/// them off `window.__bd_mod`, which does not exist until they have run.
/// The concatenated source, plus the names that actually went into it.
///
/// The names are collected by the same loop that appends the bodies, so the log
/// cannot claim a module the source does not contain. It did exactly that once: the
/// line said "6 modules" while none were concatenated, and the widget failed in the
/// renderer where no log could show it.
pub fn build_injection(plan: &Plan) -> (String, Vec<&'static str>) {
    let mut src = String::new();
    let mut names = Vec::new();
    let mut add = |name: &'static str, body: &str, src: &mut String| {
        src.push_str(body);
        src.push('\n');
        names.push(name);
    };

    if plan.cheat {
        for (name, body) in crate::assets::WIDGET_MODULES {
            add(name, body, &mut src);
        }
        add("widget.js", crate::assets::CHEAT_WIDGET, &mut src);
    }
    if plan.autoplay {
        // Autoplay names a dialogue option by where it sits in the .ink file, and needs
        // the labels of the language actually in play to find that option on screen.
        // Without them it recognises nothing, holds thirty seconds on every branching
        // dialogue, and then takes whatever came first.
        let table = plan
            .lang()
            .map(crate::ink::choice_table_for)
            .unwrap_or_else(|| serde_json::Value::Object(serde_json::Map::new()));
        add(
            "dialog-choices",
            &format!("window.__bd_dialogChoices={table};"),
            &mut src,
        );
        for (name, body) in crate::assets::ENGINE_MODULES {
            add(name, body, &mut src);
        }
        add("engine.js", crate::assets::AUTOPLAY_ENGINE, &mut src);
        add("panel.js", crate::assets::AUTOPLAY_PANEL, &mut src);
    }
    (src, names)
}

fn inject_scripts(s: &mut Session, plan: &Plan) -> Result<(), String> {
    let (src, names) = build_injection(plan);
    if src.is_empty() {
        return Ok(());
    }
    s.send("Page.enable", json!({}))?;
    s.send(
        "Page.addScriptToEvaluateOnNewDocument",
        json!({ "source": src }),
    )?;
    crate::log!(
        "injecting {} files, {} KB: {}",
        names.len(),
        src.len() / 1024,
        names.join(", ")
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_folder_and_the_id_both_come_out_of_the_url() {
        // The folder matters: once our language is in the game's settings, the game
        // asks for `dialogs/ko/…`, not `dialogs/en/…`.
        assert_eq!(
            dialog_path("gemshell://x/dialogs/en/intro.ink"),
            Some(("en".into(), "intro".into()))
        );
        assert_eq!(
            dialog_path("gemshell://x/dialogs/ko/intro.ink"),
            Some(("ko".into(), "intro".into()))
        );
        assert_eq!(
            dialog_path("gemshell://x/dialogs/zh-Hant/king_dungeon_2.ink"),
            Some(("zh-Hant".into(), "king_dungeon_2".into()))
        );
    }

    #[test]
    fn the_query_string_is_stripped() {
        assert_eq!(
            dialog_path("x/dialogs/en/a.ink?v=2"),
            Some(("en".into(), "a".into()))
        );
    }

    #[test]
    fn every_language_we_carry_can_answer_the_folder_the_game_asks_for() {
        // A language in the settings list whose dialogue folder we cannot answer
        // leaves the game to its own handler, which has no such folder and returns
        // the string "Not found" — which the game then types out as the dialogue.
        for lang in crate::assets::available() {
            let url = format!("gemshell://x/dialogs/{lang}/intro.ink");
            let (folder, id) = dialog_path(&url).expect("parsed");
            assert_eq!(folder, lang);
            assert!(
                crate::assets::dialogs(&lang).contains_key(id.as_str()),
                "{lang}: no intro.ink bundled"
            );
        }
    }

    fn plan(cheat: bool, autoplay: bool) -> Plan {
        Plan {
            language: None,
            cheat,
            autoplay,
            tables: None,
            carried: Vec::new(),
        }
    }

    #[test]
    fn the_widget_modules_go_in_ahead_of_widget_js() {
        let (src, names) = build_injection(&plan(true, false));
        let widget = names
            .iter()
            .position(|n| *n == "widget.js")
            .expect("widget.js");
        assert!(widget > 0, "widget.js must not be first");
        assert_eq!(
            widget,
            names.len() - 1,
            "and it must come after every module"
        );
        // The registrations have to be in the text, not merely counted in the log.
        assert!(
            src.contains("__bd_cheat_mod"),
            "no widget module was concatenated"
        );
    }

    #[test]
    fn the_engine_modules_go_in_ahead_of_engine_js() {
        let (src, names) = build_injection(&plan(false, true));
        let engine = names
            .iter()
            .position(|n| *n == "engine.js")
            .expect("engine.js");
        assert!(engine > 0, "engine.js must not be first");
        assert_eq!(
            names.last().copied(),
            Some("panel.js"),
            "the panel goes last"
        );
        assert!(
            src.contains("__bd_mod"),
            "no engine module was concatenated"
        );
    }

    #[test]
    fn what_is_reported_is_what_was_concatenated() {
        let (src, names) = build_injection(&plan(true, true));
        assert_eq!(
            names.len(),
            crate::assets::WIDGET_MODULES.len() + crate::assets::ENGINE_MODULES.len() + 4,
            "every module, plus dialog-choices, widget.js, engine.js and panel.js"
        );
        assert!(
            src.contains("window.__bd_dialogChoices="),
            "autoplay was injected with no dialogue option labels"
        );
        for (name, body) in crate::assets::WIDGET_MODULES {
            assert!(names.contains(name), "{name} was reported but not added");
            assert!(src.contains(body), "{name} is missing from the source");
        }
        for (name, body) in crate::assets::ENGINE_MODULES {
            assert!(names.contains(name), "{name} was reported but not added");
            assert!(src.contains(body), "{name} is missing from the source");
        }
    }

    #[test]
    fn nothing_is_injected_when_both_are_off() {
        let (src, names) = build_injection(&plan(false, false));
        assert!(src.is_empty());
        assert!(names.is_empty());
    }

    #[test]
    fn anything_but_ink_is_ignored() {
        assert_eq!(dialog_path("x/dialogs/en/a.txt"), None);
    }
}
