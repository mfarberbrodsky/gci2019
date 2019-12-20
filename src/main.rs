use image;
use reqwest;
use select::{
    document::Document,
    predicate::{Attr, Name},
};
use std::{env, fs, fs::File, io};
use std::{path::Path, str::from_utf8};
use url::Url;

fn main() {
    let args: Vec<String> = env::args().collect();

    let mut url = "https://c.xkcd.com/random/comic".to_string();
    if args.len() > 1 {
        println!("Displaying comic number {}...", &args[1]);
        url = format!("https://xkcd.com/{}", &args[1]).to_string();
    } else {
        println!("Displaying random comic...");
    }

    let response = reqwest::get(&url).unwrap();
    let document = Document::from_read(response).expect("Failed to read document");
    let img = document
        .find(Attr("id", "comic"))
        .next()
        .unwrap()
        .find(Name("img"))
        .next()
        .unwrap();

    let img_url = format!("https:{}", img.attr("src").unwrap());
    let img_parsed_url = Url::parse(&img_url).expect("Failed to parse url");
    let img_file_name = img_parsed_url
        .path_segments()
        .and_then(|segments| segments.last())
        .unwrap();

    let mut img_response = reqwest::get(&img_url).expect("Failed to download image");
    let mut img_file = File::create(img_file_name).expect("Failed to create file");
    io::copy(&mut img_response, &mut img_file).expect("Failed to copy image to file");

    print_ascii_art(img_file_name);

    fs::remove_file(img_file_name).expect("Failed to delete temp file");
}

// Code taken from https://github.com/edelsonc/asciify
fn print_ascii_art(file: &str) {
    let img = match image::open(&Path::new(file)) {
        Ok(p) => p,
        Err(_e) => panic!("Not a valid image path or could no open image"),
    };
    let img = img.resize(80u32, 40u32, image::FilterType::Nearest);

    // convert to LUMA and change each greyscale pixel into a character
    let imgbuf = img.to_luma();
    let ascii_art = imgbuf
        .pixels()
        .map(|p| intensity_to_ascii(&p[0]))
        .fold(String::new(), |s, p| s + p);

    // we have one long string, but we need to chunk it by line
    let subs = ascii_art
        .as_bytes()
        .chunks(imgbuf.width() as usize)
        .map(from_utf8)
        .collect::<Result<Vec<&str>, _>>()
        .unwrap();
    for s in subs {
        println!("{}", s);
    }
}

fn intensity_to_ascii(value: &u8) -> &str {
    // changes an intensity into an ascii character
    // this is a central step in creating the ascii art
    let ascii_chars = [
        " ", ".", "^", ",", ":", "_", "=", "~", "+", "O", "o", "*", "#", "&", "%", "B", "@", "$",
    ];

    let n_chars = ascii_chars.len() as u8;
    let step = 255u8 / n_chars;
    for i in 1..(n_chars - 1) {
        let comp = &step * i;
        if value < &comp {
            let idx = (i - 1) as usize;
            return ascii_chars[idx];
        }
    }

    ascii_chars[(n_chars - 1) as usize]
}
