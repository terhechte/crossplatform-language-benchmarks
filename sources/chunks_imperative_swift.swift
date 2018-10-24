func resize(image: [Int], width: Int, scale: Int) -> [Int] {
    var result = [Int]()
    result.reserveCapacity(image.count / scale)
    for i in stride(from: 0, to: image.count, by: width) {
        for i2 in stride(from: i, to: (i + width), by: scale) {
            var sum = 0
            for i3 in i2..<(i2 + scale) {
                sum += image[i3]
            }
            result.append(sum)
       }
    }
    return result
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




