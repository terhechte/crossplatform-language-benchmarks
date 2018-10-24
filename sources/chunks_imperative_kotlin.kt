import kotlinx.cinterop.*
import platform.posix.*

fun resize_image(image: IntArray, width: Int, scale: Int): IntArray {
    val result = IntArray(image.size / scale)
    var pos = 0
    for (i in 0 until image.size step width) {
        for (i2 in i until (i + width) step scale) {
            var sum = 0
            for (i3 in i2 until (i2 + scale)) {
                sum += image[i3]
            }
            result[pos] = sum
            pos += 1
        }
    }
    return result
}

fun generate(): IntArray {
    val image = arrayOf(
            1, 0, 0, 4, 4, 0, 0, 1,
            0, 0, 0, 9, 9, 0, 0, 0,
            0, 0, 0, 9, 9, 0, 0, 0,
            4, 9, 9, 9, 9, 9, 9, 4,
            4, 9, 9, 9, 9, 9, 9, 4,
            0, 0, 0, 9, 9, 0, 0, 0,
            0, 0, 0, 9, 9, 0, 0, 0,
            1, 0, 0, 4, 4, 0, 0, 1)
    val nr = 1000000;
    val result = IntArray(nr * image.size)
    var pos = 0
    for (i1 in 0 until nr) {
        for (item in image) {
            result[pos] = item
            pos += 1
        }
    }
    return result
}

fun main(args: Array<String>) {
    val image = generate()
    val result1 = resize_image(image, 8, 2)
    val result2 = resize_image(image, 32, 8)
    val result3 = resize_image(image, 16, 4)

    val fr1 = result1.sum() / result1.size
    val fr2 = result2.sum() / result2.size
    val fr3 = result3.sum() / result3.size

    println("${result1.size} ${result2.size} ${result3.size}")
    println("${fr1} ${fr2} ${fr3}")
}
