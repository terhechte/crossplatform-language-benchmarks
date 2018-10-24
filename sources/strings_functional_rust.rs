use std::fs::File;
use std::io::prelude::*;

pub fn test(contents: &str) -> i32 {
    contents.split(",")
    .map(|s| { s.trim() })
    .filter_map(|s| { s.parse().ok() })
    .filter(|number: &i32| { *number < 100 })
    .fold(0, |acc, x| acc + x)
}

fn main() {
  let mut f = File::open("./numbers.txt").unwrap();
  let mut contents = String::new();
  f.read_to_string(&mut contents).unwrap();
  println!("Result: {}", test(&contents));
}
