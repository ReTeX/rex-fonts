extern crate regex;

use std::io::BufReader;
use std::io::BufRead;
use std::io::Read;
use std::fs::File;
use std::collections::HashSet;

use regex::Regex;

static UNICODE_MATH_FILE: &str = "unicode-math-table.tex";
static UNICODE_MATH_REGEX: &str = r#"(?x)
    ^\\UnicodeMathSymbol
    \{"(?P<usv>[\dA-F]{5})\}
    \{\\(?P<cmd>[A-Za-z]+)\s*\}
    \{\\math(?P<atom>[a-z]+)\}
    \{(?P<name>[^\}]+)\}"#;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Atom {
    Accent,
    AccentWide,
    Alpha,
    Bin,
    BotAccent,
    BotAccentWide,
    Close,
    Fence,
    Op,
    Open,
    Ord,
    Over,
    Punct,
    Rel,
    Under
}

impl Atom {
    fn from_str(s: &str) -> Atom {
        match s {
            "accent" => Atom::Accent,
            "accentwide" => Atom::AccentWide,
            "alpha" => Atom::Alpha,
            "bin" => Atom::Bin,
            "botaccent" => Atom::BotAccent,
            "botaccentwide" => Atom::BotAccentWide,
            "close" => Atom::Close,
            "fence" => Atom::Fence,
            "op" => Atom::Op,
            "open" => Atom::Open,
            "ord" => Atom::Ord,
            "over" => Atom::Over,
            "punct" => Atom::Punct,
            "rel" => Atom::Rel,
            "under" => Atom::Under,
            _ => panic!("unrecognized atom `{}`", s),
        }
    }
}

fn main() {
    let file = File::open(UNICODE_MATH_FILE)
        .expect("Unable to open `unicode-math-table.tex`");

    let mut reader = BufReader::new(file);
    let mut atoms: HashSet<String> = HashSet::new();
    let mut regex = Regex::new(UNICODE_MATH_REGEX)
        .expect("Failed to initalize regex");
}