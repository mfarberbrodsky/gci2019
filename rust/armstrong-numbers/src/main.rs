use std::io;

fn main() {
    loop {
        println!("Enter a number: ");

        let mut n = String::new();
        io::stdin().read_line(&mut n).expect("Failed to read line");
        let n: u32 = match n.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        if is_armstrong_num(n) {
            print!("{} is an Armstrong number, because {} = ", n, n);
        } else {
            print!("{} is not an Armstrong number, because {} != ", n, n);
        }
        print_armstrong_calculation(n);

        println!("Would you like to enter another number? (Y/n)");
        let mut yes_or_no = String::new();
        io::stdin()
            .read_line(&mut yes_or_no)
            .expect("Failed to read line");
        if yes_or_no.trim() == "n" {
            break;
        }
    }
}

fn is_armstrong_num(n: u32) -> bool {
    let numdig = num_digits(n);
    let mut s: u32 = 0;

    let mut temp = n;
    while temp > 0 {
        s += (temp % 10).pow(numdig);
        temp /= 10;
    }

    return n == s;
}

fn print_armstrong_calculation(n: u32) {
    let numdig = num_digits(n);
    let mut s: u32 = 0;
    let mut temp = n;
    while temp > 0 {
        let digit = temp % 10;
        s += digit.pow(numdig);
        temp /= 10;

        print!("{}^{}", digit, numdig);
        if temp > 0 {
            print!(" + ");
        }
    }
    println!(" = {}.", s);
}

fn num_digits(n: u32) -> u32 {
    if n != 0 {
        return (n as f64).log10() as u32 + 1;
    }
    return 1;
}
