//! Log prefix lives in one place. No other file needs to know the format.
//!
//! Every line is flushed. Rust block-buffers stdout when it is not a terminal, so a
//! launcher redirected to a file shows nothing until the buffer fills — which for a
//! process that runs for hours means the log is useless exactly when it is needed.

use std::io::Write;

pub fn line(s: &str) {
    let out = std::io::stdout();
    let mut h = out.lock();
    let _ = writeln!(h, "[launcher] {s}");
    let _ = h.flush();
}

pub fn warn_line(s: &str) {
    let err = std::io::stderr();
    let mut h = err.lock();
    let _ = writeln!(h, "[launcher] ! {s}");
    let _ = h.flush();
}

#[macro_export]
macro_rules! log {
    ($($t:tt)*) => { $crate::log::line(&format!($($t)*)) };
}

#[macro_export]
macro_rules! warn {
    ($($t:tt)*) => { $crate::log::warn_line(&format!($($t)*)) };
}

/// One line of the anchor checklist. Keeps the check/cross marks consistent.
pub fn probe(name: &str, ok: bool, detail: &str) {
    let mark = if ok { "ok " } else { "FAIL" };
    if detail.is_empty() {
        line(&format!("  {mark} {name}"));
    } else {
        line(&format!("  {mark} {name} - {detail}"));
    }
}
