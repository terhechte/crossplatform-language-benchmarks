import kotlinx.cinterop.*
import platform.posix.*

fun test(contents: String): Int {
    return contents.split(",").asSequence()
            .map({ string -> string.trim() })
            .map({ string -> string.toIntOrNull() })
            .filterNotNull()
            .filter({ number -> number < 100 })
            .fold(0, { a, b -> a + b})
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
