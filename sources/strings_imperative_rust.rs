use std::fs::File;
use std::io::prelude::*;


pub fn test(contents: &str) -> i32 {
    let mut m = 0;
    for item in contents.split(",") {
       if let Ok(x) = item.trim().parse::<i32>() {
         if x < 100 {
           m += x;
         }
       }
    }
    m
}

fn main() {
    let mut file = File::open("./numbers.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    println!("Result: {}", test(&contents));
}
