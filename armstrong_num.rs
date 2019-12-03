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

fn num_digits(n: u32) -> u32 {
    if n != 0 {
        return (n as f64).log10() as u32 + 1;
    }
    return 1;
}
