func isPrime(_ number: Int) -> Bool {
    return number > 1 && !(2..<number).contains { number % $0 == 0 }
}

func main() {
  var a = 0
  for i in 0..<100000 {
    if isPrime(i) { a += 1 }
  } 
  print(a)
}
main()
