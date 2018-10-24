import Foundation

func test(_ contents: String) -> Int {
    let numbers: [Int] = contents.split(separator: ",")
        .lazy
        .map({ $0.trimmingCharacters(in: .whitespaces) })
        .compactMap({ Int($0) })
        .filter({ $0 < 100 })
        return numbers.reduce(0, { (result, value) -> Int in return result + value })
}

func main() {
  let contents = try! String(contentsOfFile: "./numbers.txt")
  print(test(contents))
}

main()

