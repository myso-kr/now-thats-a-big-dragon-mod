//! Reads a minified JavaScript value literal into a `serde_json::Value`.
//!
//! The game's i18n tables are object literals, not JSON: keys are usually bare
//! identifiers, strings may use single quotes, and one table wraps its contents in
//! ``JSON.parse(`…`)``. There is no JS engine here to evaluate them with, so this
//! parses them directly.
//!
//! It covers more than the shipped bundle currently uses — escapes, numbers, arrays,
//! booleans — because a game update could introduce any of them. What it will not do
//! is guess: anything it does not understand is an error, never a best effort. A
//! silently mis-parsed table would be written straight back into the bundle.

use serde_json::{Map, Value};

pub fn parse(src: &str) -> Result<Value, String> {
    let mut p = P {
        b: src.as_bytes(),
        s: src,
        i: 0,
    };
    p.ws();
    let v = p.value()?;
    p.ws();
    if p.i != p.b.len() {
        return Err(format!("trailing input at byte {}", p.i));
    }
    Ok(v)
}

struct P<'a> {
    b: &'a [u8],
    s: &'a str,
    i: usize,
}

impl<'a> P<'a> {
    fn ws(&mut self) {
        while self.i < self.b.len() && (self.b[self.i] as char).is_ascii_whitespace() {
            self.i += 1;
        }
    }

    fn peek(&self) -> Option<u8> {
        self.b.get(self.i).copied()
    }

    fn eat(&mut self, c: u8) -> Result<(), String> {
        if self.peek() == Some(c) {
            self.i += 1;
            Ok(())
        } else {
            Err(format!(
                "expected '{}' at byte {}, found {:?}",
                c as char,
                self.i,
                self.peek().map(|x| x as char)
            ))
        }
    }

    fn starts_with(&self, s: &str) -> bool {
        self.s[self.i..].starts_with(s)
    }

    fn value(&mut self) -> Result<Value, String> {
        self.ws();
        match self.peek() {
            Some(b'{') => self.object(),
            Some(b'[') => self.array(),
            Some(b'"') | Some(b'\'') | Some(b'`') => Ok(Value::String(self.string()?)),
            Some(b'!') => {
                // Minifiers emit `!0` for true and `!1` for false.
                self.i += 1;
                match self.peek() {
                    Some(b'0') => {
                        self.i += 1;
                        Ok(Value::Bool(true))
                    }
                    Some(b'1') => {
                        self.i += 1;
                        Ok(Value::Bool(false))
                    }
                    _ => Err(format!("unsupported '!' expression at byte {}", self.i)),
                }
            }
            // A leading `.` is a number in JS: minifiers write `.7` for `0.7`, and the
            // upgrade tree does. Reaching `number()` only on a digit meant the whole
            // tree failed to parse and autoplay lost its unlock signals.
            Some(c) if c == b'-' || c == b'.' || c.is_ascii_digit() => self.number(),
            Some(_) => {
                if self.starts_with("JSON.parse(") {
                    return self.json_parse();
                }
                for (word, v) in [
                    ("true", Value::Bool(true)),
                    ("false", Value::Bool(false)),
                    ("null", Value::Null),
                    ("void 0", Value::Null),
                    ("undefined", Value::Null),
                ] {
                    if self.starts_with(word) {
                        self.i += word.len();
                        return Ok(v);
                    }
                }
                Err(format!(
                    "unsupported expression at byte {}: {:?}",
                    self.i,
                    &self.s[self.i..(self.i + 24).min(self.s.len())]
                ))
            }
            None => Err("unexpected end of input".into()),
        }
    }

    /// ``JSON.parse(`{…}`)`` — the inner text is plain JSON, so hand it to serde.
    fn json_parse(&mut self) -> Result<Value, String> {
        self.i += "JSON.parse(".len();
        self.ws();
        let text = self.string()?;
        self.ws();
        self.eat(b')')?;
        serde_json::from_str(&text).map_err(|e| format!("JSON.parse argument is not JSON: {e}"))
    }

    fn object(&mut self) -> Result<Value, String> {
        self.eat(b'{')?;
        let mut map = Map::new();
        loop {
            self.ws();
            if self.peek() == Some(b'}') {
                self.i += 1;
                return Ok(Value::Object(map));
            }
            let key = match self.peek() {
                Some(b'"') | Some(b'\'') => self.string()?,
                Some(c) if c.is_ascii_alphanumeric() || c == b'_' || c == b'$' => self.ident(),
                _ => return Err(format!("bad object key at byte {}", self.i)),
            };
            self.ws();
            self.eat(b':')?;
            let v = self.value()?;
            map.insert(key, v);
            self.ws();
            match self.peek() {
                Some(b',') => {
                    self.i += 1;
                }
                Some(b'}') => {}
                _ => return Err(format!("expected ',' or '}}' at byte {}", self.i)),
            }
        }
    }

    fn array(&mut self) -> Result<Value, String> {
        self.eat(b'[')?;
        let mut out = Vec::new();
        loop {
            self.ws();
            if self.peek() == Some(b']') {
                self.i += 1;
                return Ok(Value::Array(out));
            }
            out.push(self.value()?);
            self.ws();
            match self.peek() {
                Some(b',') => {
                    self.i += 1;
                }
                Some(b']') => {}
                _ => return Err(format!("expected ',' or ']' at byte {}", self.i)),
            }
        }
    }

    fn ident(&mut self) -> String {
        let start = self.i;
        while let Some(c) = self.peek() {
            if c.is_ascii_alphanumeric() || c == b'_' || c == b'$' {
                self.i += 1;
            } else {
                break;
            }
        }
        self.s[start..self.i].to_owned()
    }

    fn number(&mut self) -> Result<Value, String> {
        let start = self.i;
        if self.peek() == Some(b'-') {
            self.i += 1;
        }
        while let Some(c) = self.peek() {
            if c.is_ascii_digit() || c == b'.' || c == b'e' || c == b'E' || c == b'+' || c == b'-' {
                self.i += 1;
            } else {
                break;
            }
        }
        let text = &self.s[start..self.i];
        // `2592e3` is valid JS but serde_json reads it happily too, and Rust's `f64`
        // parser accepts a bare `.7` as well - so nothing has to be rewritten here.
        text.parse::<f64>()
            .ok()
            .and_then(serde_json::Number::from_f64)
            .map(Value::Number)
            .ok_or_else(|| format!("bad number {text:?} at byte {start}"))
    }

    /// A string in any of the three quote styles. Template substitutions are refused
    /// rather than guessed at, because their value is not knowable statically.
    fn string(&mut self) -> Result<String, String> {
        let quote = match self.peek() {
            Some(q @ (b'"' | b'\'' | b'`')) => q,
            _ => return Err(format!("expected a string at byte {}", self.i)),
        };
        self.i += 1;
        let mut out = String::new();
        loop {
            let c = match self.peek() {
                Some(c) => c,
                None => return Err("unterminated string".into()),
            };
            if c == quote {
                self.i += 1;
                return Ok(out);
            }
            if quote == b'`' && c == b'$' && self.b.get(self.i + 1) == Some(&b'{') {
                return Err(format!("template substitution at byte {}", self.i));
            }
            if c == b'\\' {
                self.i += 1;
                let e = self.peek().ok_or("string ends on a backslash")?;
                self.i += 1;
                match e {
                    b'n' => out.push('\n'),
                    b't' => out.push('\t'),
                    b'r' => out.push('\r'),
                    b'b' => out.push('\u{8}'),
                    b'f' => out.push('\u{c}'),
                    b'v' => out.push('\u{b}'),
                    b'0' => out.push('\0'),
                    b'u' => out.push(self.unicode_escape()?),
                    b'x' => out.push(self.hex_escape(2)?),
                    b'\n' => {}                       // a line continuation
                    other => out.push(other as char), // \" \' \` \\ \/ and friends
                }
                continue;
            }
            // Step over a whole UTF-8 character, not one byte.
            let ch = self.s[self.i..]
                .chars()
                .next()
                .ok_or("invalid UTF-8 in string")?;
            out.push(ch);
            self.i += ch.len_utf8();
        }
    }

    fn unicode_escape(&mut self) -> Result<char, String> {
        if self.peek() == Some(b'{') {
            self.i += 1;
            let start = self.i;
            while self.peek().is_some_and(|c| c != b'}') {
                self.i += 1;
            }
            let hex = &self.s[start..self.i];
            self.eat(b'}')?;
            let n = u32::from_str_radix(hex, 16).map_err(|_| format!("bad \\u{{{hex}}}"))?;
            return char::from_u32(n).ok_or_else(|| format!("bad code point {n}"));
        }
        let first = self.hex4()?;
        // A surrogate pair is two escapes; a lone surrogate is an error.
        if (0xD800..0xDC00).contains(&first) {
            if !self.starts_with("\\u") {
                return Err("lone high surrogate".into());
            }
            self.i += 2;
            let second = self.hex4()?;
            if !(0xDC00..0xE000).contains(&second) {
                return Err("high surrogate not followed by a low one".into());
            }
            let n = 0x10000 + ((first - 0xD800) << 10) + (second - 0xDC00);
            return char::from_u32(n).ok_or_else(|| format!("bad code point {n}"));
        }
        char::from_u32(first).ok_or_else(|| format!("bad code point {first}"))
    }

    fn hex4(&mut self) -> Result<u32, String> {
        let c = self.hex_escape(4)?;
        Ok(c as u32)
    }

    fn hex_escape(&mut self, n: usize) -> Result<char, String> {
        let end = (self.i + n).min(self.s.len());
        let hex = &self.s[self.i..end];
        if hex.len() != n {
            return Err("truncated hex escape".into());
        }
        self.i = end;
        let v = u32::from_str_radix(hex, 16).map_err(|_| format!("bad hex escape {hex:?}"))?;
        // Surrogate halves are handled by the caller; keep the raw value here.
        Ok(char::from_u32(v).unwrap_or('\u{fffd}'))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn reads_bare_and_quoted_keys() {
        let v = parse(r#"{a:"1","b":"2"}"#).unwrap();
        assert_eq!(v, json!({"a":"1","b":"2"}));
    }

    #[test]
    fn reads_both_quote_styles() {
        assert_eq!(parse(r#"{a:'x'}"#).unwrap(), json!({"a":"x"}));
    }

    #[test]
    fn nests() {
        let v = parse(r#"{a:{b:{c:"d"}}}"#).unwrap();
        assert_eq!(v["a"]["b"]["c"], "d");
    }

    #[test]
    fn a_brace_inside_a_string_is_not_structure() {
        let v = parse(r#"{a:"}{",b:"c"}"#).unwrap();
        assert_eq!(v, json!({"a":"}{","b":"c"}));
    }

    #[test]
    fn handles_escapes() {
        let v = parse(r#"{a:"x\"y",b:"l\nr",c:'it\'s',d:"é",e:"a\\b"}"#).unwrap();
        assert_eq!(v["a"], "x\"y");
        assert_eq!(v["b"], "l\nr");
        assert_eq!(v["c"], "it's");
        assert_eq!(v["d"], "é");
        assert_eq!(v["e"], "a\\b");
    }

    #[test]
    fn handles_a_surrogate_pair() {
        let v = parse(r#"{a:"😀"}"#).unwrap();
        assert_eq!(v["a"], "😀");
    }

    #[test]
    fn reads_non_ascii_directly() {
        let v = parse(r#"{a:"한국어"}"#).unwrap();
        assert_eq!(v["a"], "한국어");
    }

    #[test]
    fn reads_the_json_parse_form_the_upgrades_table_uses() {
        let v = parse("{details:JSON.parse(`{\"x\":{\"title\":\"T\"}}`),other:\"o\"}").unwrap();
        assert_eq!(v["details"]["x"]["title"], "T");
        assert_eq!(v["other"], "o");
    }

    #[test]
    fn a_leading_dot_is_a_number() {
        // How a minifier writes 0.7, and how the game's upgrade tree writes it.
        let v = parse("{a:.7,b:-.5,c:1.5}").expect("parses");
        assert_eq!(v["a"], 0.7);
        assert_eq!(v["b"], -0.5);
        assert_eq!(v["c"], 1.5);
    }

    #[test]
    fn reads_numbers_booleans_and_arrays() {
        let v = parse(r#"{n:2592e3,m:-1.5,t:!0,f:!1,z:null,a:[1,"x"]}"#).unwrap();
        assert_eq!(v["n"], 2592000.0);
        assert_eq!(v["m"], -1.5);
        assert_eq!(v["t"], true);
        assert_eq!(v["f"], false);
        assert!(v["z"].is_null());
        assert_eq!(v["a"][1], "x");
    }

    #[test]
    fn tolerates_a_trailing_comma() {
        assert_eq!(parse(r#"{a:"1",}"#).unwrap(), json!({"a":"1"}));
    }

    #[test]
    fn reads_an_empty_object() {
        assert_eq!(parse("{}").unwrap(), json!({}));
    }

    #[test]
    fn refuses_a_template_substitution_rather_than_guessing() {
        let err = parse("{a:`x${y}z`}").unwrap_err();
        assert!(err.contains("substitution"), "{err}");
    }

    #[test]
    fn refuses_an_expression_it_does_not_understand() {
        assert!(parse("{a:someFn()}").is_err());
        assert!(parse("{a:1+2}").is_err());
    }

    #[test]
    fn refuses_unbalanced_input() {
        assert!(parse(r#"{a:"1""#).is_err());
        assert!(parse(r#"{a:"unterminated}"#).is_err());
    }

    #[test]
    fn refuses_trailing_junk() {
        assert!(parse(r#"{a:"1"} extra"#).is_err());
    }
}
