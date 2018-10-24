extension BidirectionalCollection {
    func chunks(size: Int) -> [SubSequence] {
        return stride(from: 0, to: self.count, by: size)
          .map { (index) -> SubSequence in
            return self[self.index(self.startIndex, offsetBy: index)
                          ..<
                            self.index(self.startIndex, offsetBy: index + size)]
        }
    }
}

func resize_chunk(slice: ArraySlice<Int>, scale: Int) -> [Int] {
    return slice.chunks(size: scale).map { (slice) -> Int in
        return slice.reduce(into: 0, { (result, value) in
                                result += value
                            })
    }
}

func resize(image: [Int], width: Int, scale: Int) -> [Int] {
    return image.chunks(size: width)
      .map { resize_chunk(slice: $0, scale: scale) }
      .reduce(into: [Int](), { (result, values) in
                  result.append(contentsOf: values)
              })
}

func generate() -> [Int] {
    let image = [
        1, 0, 0, 4, 4, 0, 0, 1,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        4, 9, 9, 9, 9, 9, 9, 4,
        4, 9, 9, 9, 9, 9, 9, 4,
        0, 0, 0, 9, 9, 0, 0, 0,
        0, 0, 0, 9, 9, 0, 0, 0,
        1, 0, 0, 4, 4, 0, 0, 1
        ]
    let nr = 1000000
    var result = [Int]()
    result.reserveCapacity(nr * image.count)
    for _ in 0..<nr {
        result.append(contentsOf: image)
    }
    return result
}

func main()  {
    let image = generate()

    let result1 = resize(image: image, width: 8, scale: 2)
    let result2 = resize(image: image, width: 32, scale: 8)
    let result3 = resize(image: image, width: 16, scale: 4)

    let fr1 = result1.reduce(0, +) / result1.count
    let fr2 = result2.reduce(0, +) / result2.count
    let fr3 = result3.reduce(0, +) / result3.count

    print(result1.count, result2.count, result3.count)
    print(fr1, fr2, fr3)

}
main()


