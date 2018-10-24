import kotlinx.cinterop.*
import platform.posix.*

fun test(contents: String): Int {
    val strings = contents.split(",")
    var result = 0
    for (string in strings) {
        val trimmed = string.trim()
        val asNumber = trimmed.toIntOrNull()
        if (asNumber != null) {
            if (asNumber < 100) {
               result += asNumber
            }
        }
    }
    return result
}

fun main(args: Array<String>) {
    // For the life of me, I could not figure out how to open and read a file with Kotlin Native without
    // going back to C libraries.. This is based on Kotlin Native Sample Code
    val file = fopen("./numbers.txt", "r")
    if (file == null) {
        return
    }
    try {
        memScoped {
            val bufferLength = 64 * 1024
            val buffer = allocArray<ByteVar>(bufferLength)
            var result = ""
            while (true) {
                val nextLine = fgets(buffer, bufferLength, file)?.toKString()
                if (nextLine == null || nextLine.isEmpty()) break
                result += nextLine
            }
            println(test(result))
        }
    } finally {
        fclose(file)
    }
}
