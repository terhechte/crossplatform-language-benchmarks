fn is_prime(number: i32) -> bool {
    number > 1 && !(2..number).any(|n| number % n == 0)
}

fn main() {
  let mut a = 0;
  for i in 0..=100000 {
    if is_prime(i) { a += 1 }
  }
  println!("{}", a);
}
