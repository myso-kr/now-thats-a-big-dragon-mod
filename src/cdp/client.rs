//! JSON-RPC over a WebSocket. It delivers messages; it does not interpret them.

use serde_json::{json, Value};
use std::collections::VecDeque;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::time::{Duration, Instant};
use tungstenite::{Message, WebSocket};

pub struct Session {
    // CDP is loopback-only, so no TLS is involved, but tungstenite::connect picks
    // the wrapper type from the scheme — so we take the type it hands back.
    ws: WebSocket<tungstenite::stream::MaybeTlsStream<TcpStream>>,
    next_id: u64,
    /// Set once the far end has gone. The game exiting is a normal end, not a
    /// failure, and the caller needs to be able to tell the two apart.
    closed: bool,
    /// Events that arrived while a command was waiting for its reply.
    ///
    /// They must be kept, not dropped. Serving one large asset means several
    /// round-trips, and every request the page makes in the meantime arrives as an
    /// event here. Discarding those leaves them paused forever, and the page dies
    /// waiting on assets that will never be answered — with the launcher reporting
    /// nothing but success.
    events: VecDeque<Value>,
}

/// Poll `/json/list` until the page target's WebSocket URL appears.
/// This is loopback: no TLS, no redirects — minimal HTTP is enough.
pub fn wait_for_page(port: u16, timeout: Duration) -> Result<String, String> {
    let deadline = Instant::now() + timeout;
    let mut last = String::new();
    while Instant::now() < deadline {
        match http_get(port, "/json/list") {
            Ok(body) => {
                if let Ok(v) = serde_json::from_str::<Value>(&body) {
                    if let Some(url) = v
                        .as_array()
                        .and_then(|a| a.iter().find(|t| t["type"] == "page"))
                        .and_then(|t| t["webSocketDebuggerUrl"].as_str())
                    {
                        return Ok(url.to_owned());
                    }
                }
            }
            Err(e) => last = e,
        }
        std::thread::sleep(Duration::from_millis(250));
    }
    Err(format!(
        "the CDP endpoint (:{port}) did not come up within {}s. {last}",
        timeout.as_secs()
    ))
}

/// How many more bytes of body to read, given the response headers.
///
/// Reading to EOF is not an option: the DevTools endpoint ignores `Connection: close`
/// and holds the socket open, so a read-to-end blocks until the read timeout and then
/// throws away everything it had. That is what made the launcher unable to attach at
/// all — it looked exactly like the port never coming up.
fn body_length(headers: &str) -> Option<usize> {
    for line in headers.split("\r\n") {
        let Some((k, v)) = line.split_once(':') else {
            continue;
        };
        if k.trim().eq_ignore_ascii_case("content-length") {
            return v.trim().parse().ok();
        }
    }
    None
}

fn http_get(port: u16, path: &str) -> Result<String, String> {
    let mut s = TcpStream::connect(("127.0.0.1", port)).map_err(|e| e.to_string())?;
    s.set_read_timeout(Some(Duration::from_secs(5))).ok();
    // The port has to be in the Host header. DevTools builds webSocketDebuggerUrl out
    // of whatever Host it was given, so sending a bare address yields a portless
    // ws:// URL that then cannot be connected to.
    write!(s, "GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n\r\n")
        .map_err(|e| e.to_string())?;

    // Read until the headers are complete, then exactly as much body as they promise.
    let mut buf: Vec<u8> = Vec::with_capacity(8192);
    let mut chunk = [0u8; 4096];
    let mut split = None;
    while split.is_none() {
        let n = s.read(&mut chunk).map_err(|e| e.to_string())?;
        if n == 0 {
            return Err("the connection closed before the headers were complete".into());
        }
        buf.extend_from_slice(&chunk[..n]);
        split = buf.windows(4).position(|w| w == b"\r\n\r\n").map(|i| i + 4);
    }
    let at = split.unwrap();
    let headers = String::from_utf8_lossy(&buf[..at]).into_owned();
    let want = body_length(&headers).ok_or("the response has no content-length")?;

    while buf.len() - at < want {
        let n = s.read(&mut chunk).map_err(|e| e.to_string())?;
        if n == 0 {
            return Err("the connection closed mid-body".into());
        }
        buf.extend_from_slice(&chunk[..n]);
    }
    String::from_utf8(buf[at..at + want].to_vec()).map_err(|e| e.to_string())
}

/// What an incoming protocol message is, relative to the command we are waiting on.
#[derive(Debug, PartialEq)]
pub enum Incoming {
    /// The reply to our request.
    Reply,
    /// Something the page is telling us. It has to be kept: a request paused while a
    /// command is in flight stays paused until we answer it.
    Event,
    /// A reply to some other request. Nothing needs it.
    Other,
}

pub fn classify(msg: &Value, waiting_for: u64) -> Incoming {
    if msg.get("id").and_then(Value::as_u64) == Some(waiting_for) {
        return Incoming::Reply;
    }
    if msg.get("method").is_some() {
        return Incoming::Event;
    }
    Incoming::Other
}

impl Session {
    pub fn open(ws_url: &str) -> Result<Self, String> {
        let (ws, _) =
            tungstenite::connect(ws_url).map_err(|e| format!("could not connect to CDP: {e}"))?;
        Ok(Self {
            ws,
            next_id: 0,
            closed: false,
            events: VecDeque::new(),
        })
    }

    pub fn send(&mut self, method: &str, params: Value) -> Result<Value, String> {
        self.next_id += 1;
        let id = self.next_id;
        let msg = json!({ "id": id, "method": method, "params": params });
        if let Err(e) = self.ws.send(Message::Text(msg.to_string())) {
            self.closed = true;
            return Err(format!("could not send {method}: {e}"));
        }
        loop {
            let got = self.recv()?;
            if classify(&got, id) == Incoming::Reply {
                if let Some(err) = got.get("error") {
                    return Err(format!("{method}: {err}"));
                }
                return Ok(got.get("result").cloned().unwrap_or(Value::Null));
            }
            if classify(&got, id) == Incoming::Event {
                self.events.push_back(got);
            }
        }
    }

    /// True once the connection has gone, whichever way it went. The game exiting is
    /// how a run normally ends, and the caller has to tell that from a real failure.
    pub fn closed(&self) -> bool {
        self.closed
    }

    /// Give reads a deadline.
    ///
    /// A wedged renderer keeps the socket open and stops answering. Without this, a
    /// blocking read waits forever and whatever was watching quietly stops watching —
    /// which is the one thing a watchdog must not do.
    pub fn set_read_timeout(&mut self, d: Duration) {
        let stream = match self.ws.get_mut() {
            tungstenite::stream::MaybeTlsStream::Plain(s) => s,
            _ => return,
        };
        let _ = stream.set_read_timeout(Some(d));
    }

    /// The next protocol message, taking anything queued while a command was in
    /// flight before going back to the socket.
    pub fn next_event(&mut self) -> Result<Value, String> {
        if let Some(v) = self.events.pop_front() {
            return Ok(v);
        }
        self.recv()
    }

    /// How many events are waiting. Only for diagnostics.
    pub fn queued(&self) -> usize {
        self.events.len()
    }

    pub fn recv(&mut self) -> Result<Value, String> {
        loop {
            let msg = match self.ws.read() {
                Ok(m) => m,
                Err(e) => {
                    self.closed = true;
                    return Err(format!("CDP read failed: {e}"));
                }
            };
            match msg {
                Message::Text(t) => {
                    return serde_json::from_str(&t)
                        .map_err(|e| format!("could not parse the CDP response: {e}"))
                }
                Message::Close(_) => {
                    self.closed = true;
                    return Err("the CDP connection closed".into());
                }
                _ => continue,
            }
        }
    }

    pub fn eval(&mut self, expr: &str) -> Result<Value, String> {
        self.send(
            "Runtime.evaluate",
            json!({ "expression": expr, "returnByValue": true, "awaitPromise": true }),
        )
    }

    pub fn eval_number(&mut self, expr: &str) -> Option<f64> {
        self.eval(expr).ok()?.get("result")?.get("value")?.as_f64()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn our_reply_is_recognised() {
        let m = json!({"id": 7, "result": {}});
        assert_eq!(classify(&m, 7), Incoming::Reply);
    }

    #[test]
    fn an_event_arriving_mid_command_is_kept_not_dropped() {
        // This is the bug that made the launcher unusable: a Fetch.requestPaused that
        // arrived while a large asset was being fetched was discarded, so that request
        // stayed paused forever and the page died waiting on it.
        let m = json!({"method": "Fetch.requestPaused", "params": {"requestId": "x"}});
        assert_eq!(classify(&m, 7), Incoming::Event);
    }

    #[test]
    fn someone_elses_reply_is_neither() {
        let m = json!({"id": 8, "result": {}});
        assert_eq!(classify(&m, 7), Incoming::Other);
    }

    #[test]
    fn an_error_reply_is_still_our_reply() {
        let m = json!({"id": 7, "error": {"message": "no"}});
        assert_eq!(classify(&m, 7), Incoming::Reply);
    }

    #[test]
    fn reads_the_content_length() {
        let h = "HTTP/1.1 200 OK\r\nContent-Length: 42\r\nContent-Type: application/json\r\n\r\n";
        assert_eq!(body_length(h), Some(42));
    }

    #[test]
    fn the_header_name_is_case_insensitive() {
        assert_eq!(
            body_length("HTTP/1.1 200 OK\r\ncontent-length: 7\r\n\r\n"),
            Some(7)
        );
        assert_eq!(
            body_length("HTTP/1.1 200 OK\r\nCONTENT-LENGTH: 7\r\n\r\n"),
            Some(7)
        );
    }

    #[test]
    fn a_missing_length_is_none_rather_than_a_guess() {
        // Reading to EOF instead would block until the read timeout, which is exactly
        // the bug this replaced.
        assert_eq!(
            body_length("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"),
            None
        );
    }

    #[test]
    fn a_header_that_merely_contains_the_word_is_not_matched() {
        assert_eq!(
            body_length("HTTP/1.1 200 OK\r\nX-Content-Length-Hint: 9\r\n\r\n"),
            None
        );
    }

    #[test]
    fn a_non_numeric_length_is_not_accepted() {
        assert_eq!(
            body_length("HTTP/1.1 200 OK\r\nContent-Length: abc\r\n\r\n"),
            None
        );
    }
}
