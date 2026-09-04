//! The launcher, as a library.
//!
//! `main.rs` is only an entry point: it reads arguments and assembles the run order.
//! Everything it calls lives here, which is also what lets `tests/` drive a real
//! bundle through the patcher without going near the game.

#[macro_use]
pub mod log;

pub mod assets;
pub mod cdp;
pub mod cli;
pub mod game;
pub mod ink;
pub mod language;
pub mod patch;
pub mod watchdog;
