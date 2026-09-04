//! Find the game installation and read its version. It does nothing else.

use super::Install;
use std::path::{Path, PathBuf};

const EXE: &str = "now-thats-a-big-dragon.exe";

/// Standard install-path candidates, tried top to bottom.
fn candidates() -> Vec<PathBuf> {
    let mut v = Vec::new();
    for root in ["C:\\Program Files (x86)\\Steam", "C:\\Program Files\\Steam"] {
        v.push(Path::new(root).join("steamapps/common/Now THAT'S a Big Dragon!"));
    }
    // Libraries on another drive are common too
    for d in ['D', 'E', 'F'] {
        v.push(PathBuf::from(format!(
            "{d}:\\SteamLibrary\\steamapps\\common\\Now THAT'S a Big Dragon!"
        )));
    }
    v
}

pub fn find(explicit: Option<&Path>) -> Result<Install, String> {
    if let Some(d) = explicit {
        return load(d).map_err(|e| format!("no game at the path given: {}\n  {e}", d.display()));
    }
    for d in candidates() {
        if let Ok(i) = load(&d) {
            return Ok(i);
        }
    }
    Err(format!(
        "Game not found. Pass --game-dir, or set BIG_DRAGON_DIR.\n\
         Looked in:\n{}",
        candidates()
            .iter()
            .map(|p| format!("  {}", p.display()))
            .collect::<Vec<_>>()
            .join("\n")
    ))
}

fn load(dir: &Path) -> Result<Install, String> {
    let exe = dir.join(EXE);
    if !exe.is_file() {
        return Err(format!("no {EXE} here"));
    }
    let pkg = dir.join("resources/app/package.json");
    let version = std::fs::read_to_string(&pkg)
        .ok()
        .and_then(|s| serde_json::from_str::<serde_json::Value>(&s).ok())
        .and_then(|v| v.get("version")?.as_str().map(str::to_owned))
        .unwrap_or_else(|| "unknown".into());
    Ok(Install {
        dir: dir.to_path_buf(),
        exe,
        version,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fails_when_the_executable_is_missing() {
        assert!(load(Path::new("Z:\\no-such-path")).is_err());
    }

    #[test]
    fn the_candidate_list_is_not_empty() {
        assert!(!candidates().is_empty());
    }
}
