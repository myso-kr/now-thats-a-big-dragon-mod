//! Chrome DevTools Protocol. The only channel we have to the game.
//!
//!   client  JSON-RPC over a WebSocket; pairs requests with responses
//!   fetch   the loop that intercepts responses through the Fetch domain

pub mod client;
pub mod fetch;

pub use client::Session;

/// Wait for the endpoint to come up, then attach to the page target.
pub fn connect(port: u16) -> Result<Session, Box<dyn std::error::Error>> {
    let url = client::wait_for_page(port, std::time::Duration::from_secs(30))?;
    let s = Session::open(&url)?;
    crate::log!("attached to the page target");
    Ok(s)
}

/// A second, independent session on the same page.
///
/// The socket is synchronous and `fetch::serve` blocks on it forever, so anything
/// that has to run at the same time - the watchdog - needs its own connection rather
/// than sharing this one.
pub fn connect_again(port: u16) -> Result<Session, Box<dyn std::error::Error>> {
    let url = client::wait_for_page(port, std::time::Duration::from_secs(10))?;
    Ok(Session::open(&url)?)
}
