import Foundation

func test(_ contents: String) -> Int {
    let strings = contents.split(separator: ",")
    var sum = 0
    for string in strings {
      let trimmed = string.trimmingCharacters(in: .whitespaces)
      guard let number = Int(trimmed) else { continue }
      if number < 100 {
        sum += number
      }
    }
    return sum
}

func main() {
  let contents = try! String(contentsOfFile: "./numbers.txt")
  print(test(contents))
}

main()
