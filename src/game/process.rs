//! Start the game process, and refuse to start a second one.

use super::Install;
use std::process::{Child, Command};

/// PIDs of already-running processes with this name.
///
/// Electron holds a single-instance lock, so if the game is already up, a new
/// process hands its arguments to the existing one and exits immediately.
/// `--remote-debugging-port` never reaches the surviving instance, yet the
/// launcher still looks like it attached successfully — so this has to be
/// checked before launching, not after.
pub fn running(exe_name: &str) -> Vec<String> {
    let out = Command::new("tasklist")
        .args([
            "/FI",
            &format!("IMAGENAME eq {exe_name}"),
            "/FO",
            "CSV",
            "/NH",
        ])
        .output();
    let Ok(out) = out else { return Vec::new() };
    String::from_utf8_lossy(&out.stdout)
        .lines()
        .filter_map(parse_pid)
        .collect()
}

/// Pull just the PID out of `"name.exe","1234","Console",...`.
fn parse_pid(line: &str) -> Option<String> {
    let mut fields = line.split("\",\"");
    let _name = fields.next()?;
    let pid = fields.next()?.trim_matches('"');
    pid.chars()
        .all(|c| c.is_ascii_digit())
        .then(|| pid.to_owned())
}

/// How long to give a closing game before deciding it is still up.
const EXIT_GRACE: std::time::Duration = std::time::Duration::from_secs(10);

/// Wait for the game to be gone, and to stay gone.
///
/// A closing game leaves the process list before it lets go of the single-instance
/// lock. Launching into that window looks like it worked — the new process hands its
/// arguments to the dying one and exits, so nothing is patched and the launcher then
/// waits on a page that never loads. Two clear readings a moment apart tell the
/// difference, and someone who has just closed the game should not have to run the
/// command twice either.
fn wait_until_gone(exe_name: &str) -> Vec<String> {
    let start = std::time::Instant::now();
    let mut announced = false;
    loop {
        if running(exe_name).is_empty() {
            std::thread::sleep(std::time::Duration::from_millis(400));
            if running(exe_name).is_empty() {
                return Vec::new();
            }
        }
        if start.elapsed() >= EXIT_GRACE {
            return running(exe_name);
        }
        if !announced {
            crate::log!("the game is still closing; waiting for it to let go");
            announced = true;
        }
        std::thread::sleep(std::time::Duration::from_millis(400));
    }
}

pub fn launch(install: &Install, port: u16) -> Result<Child, String> {
    let exe_name = install
        .exe
        .file_name()
        .and_then(|s| s.to_str())
        .unwrap_or_default();
    let pids = wait_until_gone(exe_name);
    if !pids.is_empty() {
        return Err(format!(
            "The game is already running (PID {}).\n\
             Because of the single-instance lock, launching now would not apply the patch.\n\
             Close the game completely and run again, or use --attach.\n\
             (--attach needs the game to be running with --remote-debugging-port={port})",
            pids.join(", ")
        ));
    }

    crate::log!("launching the game (CDP port {port})");
    Command::new(&install.exe)
        .arg(format!("--remote-debugging-port={port}"))
        .current_dir(&install.dir)
        .spawn()
        .map_err(|e| format!("could not launch the game: {e}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pulls_a_pid_out_of_a_tasklist_line() {
        let line = "\"now-thats-a-big-dragon.exe\",\"24320\",\"Console\",\"1\",\"301,028 K\"";
        assert_eq!(parse_pid(line).as_deref(), Some("24320"));
    }

    #[test]
    fn the_no_matches_notice_is_not_a_pid() {
        // tasklist prints this in the OS display language; Korean Windows shown here.
        let line = "정보: 지정한 조건에 맞는 작업이 실행되고 있지 않습니다.";
        assert_eq!(parse_pid(line), None);
        assert_eq!(
            parse_pid("INFO: No tasks are running which match the specified criteria."),
            None
        );
    }

    #[test]
    fn a_blank_line_is_not_a_pid() {
        assert_eq!(parse_pid(""), None);
    }
}
