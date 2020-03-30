use reqwest;
use select;
use select::document::Document;
use select::predicate::{Class, Name};
use std::io;

fn main() {
    println!("Hello! Which WCA (World Cubing Association) event results would you like to see?");
    println!("2x2 / 3x3 / 4x4 / 5x5 / 6x6 / 7x7 (enter a number 2..7)");
    let cube_n = get_num();
    assert!(
        2 <= cube_n && cube_n <= 7,
        format!("{} is an invalid number!", cube_n)
    );

    println!("How many top results?");
    let top_n = get_num() as usize;
    assert!(1 <= top_n, format!("{} is an invalid number!", cube_n));

    println!(
        "Printing top {} results for {}x{}x{} cube:\n",
        top_n, cube_n, cube_n, cube_n
    );

    let url = format!(
        "https://www.worldcubeassociation.org/results/rankings/{}{}{}",
        cube_n, cube_n, cube_n
    );
    let res = reqwest::get(&url).unwrap();
    let document = Document::from_read(res).expect("Failed to read");

    let top = document.find(Name("tr")).skip(1).take(top_n);

    for node in top {
        println!(
            "Name: {}, Result: {}",
            node.find(Class("name")).next().unwrap().text(),
            node.find(Class("result")).next().unwrap().text()
        );
    }
}

fn get_num() -> u32 {
    let mut n = String::new();
    io::stdin().read_line(&mut n).expect("Failed to read line");
    let n: u32 = match n.trim().parse() {
        Ok(num) => num,
        Err(_) => {
            eprintln!("{} is not a number, exiting", n.trim());
            std::process::exit(1);
        }
    };

    return n;
}
