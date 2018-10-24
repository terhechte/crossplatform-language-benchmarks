extern crate serde;
extern crate serde_json;
#[macro_use]
extern crate serde_derive;

use std::fs;
use std::collections::HashMap;

#[derive(Deserialize)]
struct User {
    username: String
}

#[derive(Deserialize)]
struct Comment {
    author: User,
    text: String,
    likes: Vec<User>
}

#[derive(Deserialize)]
struct Media {
    author: User,
    likes: Vec<User>,
    comments: Vec<Comment>,
    images: HashMap<String, String>,
    description: String
}

fn main() -> Result<(), Box<std::error::Error>>  {
    let media: Vec<Media> = serde_json::from_str(&fs::read_to_string("./test.json")?)?;
    println!("{:?}", media.into_iter().map(|x|x.author.username).collect::<Vec<String>>());
    Ok(())
}
