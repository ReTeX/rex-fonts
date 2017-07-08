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

fn main() {
    println!("Hi");
    let file = File::open(UNICODE_MATH_FILE).expect("Unable to open `unicode-math-table.tex`");

    let mut reader = BufReader::new(file);
    let mut points: HashSet<String> = HashSet::new();
    let mut regex = Regex::new(UNICODE_MATH_REGEX).expect("Failed to initalize regex");

    for line in reader.lines() {
        let line = line.expect("Failed to read line.");
        let caps = match regex.captures(&line) {
            Some(e) => e,
            None => {
                println!("Unable to match: {}", line);
                continue;
            }
        };

        if !points.contains(&caps["usv"]) {
            points.insert(caps["usv"].into());
        }
    }

    let mut v = points.into_iter().collect::<Vec<_>>();
    v.sort();

    for c in v {
        println!("{}", c);
    }
}