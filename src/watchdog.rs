//! Watches the autoplay heartbeat from outside the renderer.
//!
//! When the renderer wedges, the supervisor inside the game wedges with it. This
//! process being outside is the only safeguard that actually holds.

use crate::cdp::Session;
use std::time::{Duration, Instant};

const STALL: Duration = Duration::from_secs(6);
const POLL: Duration = Duration::from_secs(2);

pub fn run(s: &mut Session) -> Result<(), Box<dyn std::error::Error>> {
    // A wedged renderer answers nothing, which is exactly the case this exists for.
    // Without a deadline the first read would block forever and the watch would end
    // silently.
    s.set_read_timeout(Duration::from_secs(10));

    let mut last_beat = 0f64;
    let mut last_seen = Instant::now();
    let mut recovering = false;

    crate::log!(
        "watchdog up (steps in after {}s without a heartbeat)",
        STALL.as_secs()
    );
    loop {
        std::thread::sleep(POLL);
        let beat = s
            .eval_number("window.__bd_auto_beat||0")
            .unwrap_or(f64::NAN);

        if beat.is_finite() && beat != last_beat {
            last_beat = beat;
            last_seen = Instant::now();
            recovering = false;
            continue;
        }
        if last_beat == 0.0 {
            continue; // autoplay has not started yet
        }
        if last_seen.elapsed() < STALL || recovering {
            continue;
        }
        recovering = true;
        crate::warn!(
            "no autoplay heartbeat for {}s - stopping it from outside.",
            last_seen.elapsed().as_secs()
        );
        let _ = s.eval(
            "try{window.__bd_auto&&window.__bd_auto.stop('watchdog: heartbeat stopped');\
             window.__bd_cheat&&window.__bd_cheat.setSpeed(1);}catch(e){}",
        );
        crate::log!("watchdog done (autoplay stopped, speed back to 1x)");
    }
}
