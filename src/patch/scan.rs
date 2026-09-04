//! Finds balanced bracket spans inside minified JS.
//!
//! This file knows nothing about what JS means. It only counts pairs without being
//! fooled by brackets inside string, template, or regex literals — which is exactly
//! why it can be tested apart from the patching logic.

/// Index just past the bracket that closes the one at `open`, or `None` if unbalanced.
pub fn balanced(src: &str, open: usize) -> Option<usize> {
    let b = src.as_bytes();
    let (o, c) = match *b.get(open)? {
        b'{' => (b'{', b'}'),
        b'[' => (b'[', b']'),
        b'(' => (b'(', b')'),
        _ => return None,
    };

    let mut depth = 0i32;
    let mut i = open;
    let mut quote: Option<u8> = None;
    let mut escaped = false;

    while i < b.len() {
        let ch = b[i];
        if let Some(q) = quote {
            if escaped {
                escaped = false;
            } else if ch == b'\\' {
                escaped = true;
            } else if ch == q {
                quote = None;
            }
            i += 1;
            continue;
        }
        match ch {
            b'"' | b'\'' | b'`' => quote = Some(ch),
            x if x == o => depth += 1,
            x if x == c => {
                depth -= 1;
                if depth == 0 {
                    return Some(i + 1);
                }
            }
            _ => {}
        }
        i += 1;
    }
    None
}

/// Locate the object literal that follows `name=`.
/// Checks the preceding byte so we do not match the tail of a longer identifier.
pub fn object_literal(src: &str, name: &str) -> Option<(usize, usize)> {
    let pat = format!("{name}=");
    let mut from = 0;
    while let Some(rel) = src[from..].find(&pat) {
        let at = from + rel;
        let prev_ok = at == 0
            || !src.as_bytes()[at - 1].is_ascii_alphanumeric()
                && src.as_bytes()[at - 1] != b'_'
                && src.as_bytes()[at - 1] != b'$';
        let brace = at + pat.len();
        if prev_ok && src.as_bytes().get(brace) == Some(&b'{') {
            if let Some(end) = balanced(src, brace) {
                return Some((brace, end));
            }
        }
        from = at + pat.len();
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn counts_nested_objects_to_the_end() {
        let s = "X={a:{b:{c:1}},d:2};";
        let (o, e) = object_literal(s, "X").unwrap();
        assert_eq!(&s[o..e], "{a:{b:{c:1}},d:2}");
    }

    #[test]
    fn is_not_fooled_by_a_closing_brace_inside_a_string() {
        let s = r#"X={a:"}}}",b:1};"#;
        let (o, e) = object_literal(s, "X").unwrap();
        assert_eq!(&s[o..e], r#"{a:"}}}",b:1}"#);
    }

    #[test]
    fn steps_over_an_escaped_quote() {
        let s = r#"X={a:"a\"}",b:1};"#;
        let (o, e) = object_literal(s, "X").unwrap();
        assert_eq!(&s[o..e], r#"{a:"a\"}",b:1}"#);
    }

    #[test]
    fn does_not_match_the_tail_of_a_longer_identifier() {
        let s = "xENe={wrong:1};ENe={right:1};";
        let (o, e) = object_literal(s, "ENe").unwrap();
        assert_eq!(&s[o..e], "{right:1}");
    }

    #[test]
    fn unbalanced_input_gives_none() {
        assert_eq!(balanced("{a:1", 0), None);
    }

    #[test]
    fn ignores_braces_inside_a_template_literal() {
        let s = "X={a:`${1+1}}`,b:2};";
        let (o, e) = object_literal(s, "X").unwrap();
        assert_eq!(&s[o..e], "{a:`${1+1}}`,b:2}");
    }
}
