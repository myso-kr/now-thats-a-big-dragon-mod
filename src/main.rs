//! Entry point. It reads the arguments and assembles the run order — nothing else.
//!
//! No policy and no parsing live here. Reading this file alone should tell you what
//! gets called, and in what order. Everything it calls lives in `lib.rs`.

use bigdragon::{cdp, cli, game, log, patch, warn, watchdog};
use std::process::ExitCode;

fn main() -> ExitCode {
    let opt = match cli::parse(std::env::args().skip(1)) {
        Ok(cli::Parsed::Run(o)) => o,
        Ok(cli::Parsed::Help) => {
            println!("{}", cli::USAGE);
            return ExitCode::SUCCESS;
        }
        Err(e) => {
            warn!("bad argument: {e}");
            eprintln!("{}", cli::USAGE);
            return ExitCode::from(2);
        }
    };

    match run(&opt) {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            warn!("{e}");
            ExitCode::FAILURE
        }
    }
}

fn run(opt: &cli::Options) -> Result<(), Box<dyn std::error::Error>> {
    let install = game::locate::find(opt.game_dir.as_deref())?;
    log!("game {} at {}", install.version, install.dir.display());

    // If the game is already up, Electron's single-instance lock makes a new process
    // hand its arguments over and exit. --remote-debugging-port never takes effect,
    // yet the launcher still looks like it attached — so block it up front.
    let _child = if opt.attach {
        log!("attaching to the running game (port {})", opt.port);
        None
    } else {
        Some(game::process::launch(&install, opt.port)?)
    };

    let (plan, why) = patch::Plan::build(opt)?;
    match plan.lang() {
        Some(code) => log!("language: {code} - {why}"),
        None => log!("no language patch - {why}"),
    }
    let mut session = cdp::connect(opt.port)?;

    // The watchdog gets its own connection and its own thread. The socket is
    // synchronous and serve() blocks on it for the life of the run, so a watchdog
    // sharing this session would never get a turn - which is exactly what used to
    // happen: the call sat after serve() and was never reached at all.
    if opt.watchdog {
        let port = opt.port;
        std::thread::spawn(move || match cdp::connect_again(port) {
            Ok(mut s) => {
                if let Err(e) = watchdog::run(&mut s) {
                    warn!("watchdog stopped: {e}");
                }
            }
            Err(e) => warn!("watchdog could not attach: {e}"),
        });
    }

    // Returns when the game exits, which ends the run.
    cdp::fetch::serve(&mut session, &plan)?;
    Ok(())
}
