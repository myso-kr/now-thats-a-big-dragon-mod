//! Command-line argument parsing only. Knows nothing about the game or CDP.

use std::path::PathBuf;

pub const USAGE: &str = "\
Usage:
  bigdragon                  launch the game and attach to it
  bigdragon --attach         attach to a game already running with --remote-debugging-port

  --no-translate             leave the game in its own language
  --lang <code>              force a language instead of following the system
  --no-cheat                 disable the cheat widget (F8)
  --no-auto                  disable autoplay (F9)
  --no-watchdog              disable the external watchdog

  --port <number>            CDP port (default 9223)
  --game-dir <path>          game install directory (default: the standard Steam path)
  -h, --help                 this help";

#[derive(Debug, Clone)]
pub struct Options {
    pub attach: bool,
    /// Apply a translation at all. Which one is decided from the system locale.
    pub translate: bool,
    /// An explicit language, overriding the system locale.
    pub lang: Option<String>,
    pub cheat: bool,
    pub autoplay: bool,
    pub watchdog: bool,
    pub port: u16,
    pub game_dir: Option<PathBuf>,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            attach: false,
            translate: true,
            lang: None,
            cheat: true,
            autoplay: true,
            watchdog: true,
            port: 9223,
            game_dir: None,
        }
    }
}

pub enum Parsed {
    Run(Options),
    Help,
}

pub fn parse<I: IntoIterator<Item = String>>(args: I) -> Result<Parsed, String> {
    let mut o = Options::default();
    // Environment variables only move the defaults. An explicit argument always wins.
    if let Ok(p) = std::env::var("BIG_DRAGON_PORT") {
        o.port = p
            .parse()
            .map_err(|_| format!("BIG_DRAGON_PORT is not a number: {p}"))?;
    }
    if let Ok(d) = std::env::var("BIG_DRAGON_DIR") {
        o.game_dir = Some(PathBuf::from(d));
    }

    let mut it = args.into_iter();
    while let Some(a) = it.next() {
        match a.as_str() {
            "-h" | "--help" => return Ok(Parsed::Help),
            "--attach" => o.attach = true,
            "--no-ko" | "--no-translate" => o.translate = false,
            "--lang" => {
                let v = it.next().ok_or("--lang needs a language code after it")?;
                o.lang = Some(v);
            }
            "--no-cheat" => o.cheat = false,
            "--no-auto" => o.autoplay = false,
            "--no-watchdog" => o.watchdog = false,
            "--port" => {
                let v = it.next().ok_or("--port needs a number after it")?;
                o.port = v
                    .parse()
                    .map_err(|_| format!("port is not a number: {v}"))?;
            }
            "--game-dir" => {
                let v = it.next().ok_or("--game-dir needs a path after it")?;
                o.game_dir = Some(PathBuf::from(v));
            }
            other => return Err(format!("unknown argument: {other}")),
        }
    }
    Ok(Parsed::Run(o))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn run(a: &[&str]) -> Options {
        match parse(a.iter().map(|s| s.to_string())).unwrap() {
            Parsed::Run(o) => o,
            Parsed::Help => panic!("expected a run, not help"),
        }
    }

    #[test]
    fn everything_is_on_by_default() {
        let o = run(&[]);
        assert!(o.translate && o.cheat && o.autoplay && o.watchdog);
        assert_eq!(
            o.lang, None,
            "the system locale decides unless told otherwise"
        );
        assert!(!o.attach);
    }

    #[test]
    fn features_can_be_disabled_individually() {
        let o = run(&["--no-ko", "--no-auto"]);
        assert!(!o.translate && !o.autoplay);
        assert!(o.cheat, "what was not named should stay as it was");
    }

    #[test]
    fn takes_a_language() {
        assert_eq!(run(&["--lang", "ja"]).lang.as_deref(), Some("ja"));
        assert!(
            run(&["--lang", "ja"]).translate,
            "naming one implies wanting it"
        );
    }

    #[test]
    fn no_translate_is_the_same_as_the_old_no_ko() {
        assert!(!run(&["--no-translate"]).translate);
        assert!(!run(&["--no-ko"]).translate);
    }

    #[test]
    fn a_language_with_no_code_after_it_is_an_error() {
        assert!(parse(["--lang".to_string()]).is_err());
    }

    #[test]
    fn takes_a_port() {
        assert_eq!(run(&["--port", "9333"]).port, 9333);
    }

    #[test]
    fn an_unknown_argument_does_not_pass_silently() {
        assert!(parse(["--nope".to_string()]).is_err());
    }

    #[test]
    fn a_non_numeric_port_is_an_error() {
        assert!(parse(["--port".into(), "abc".into()]).is_err());
    }
}
