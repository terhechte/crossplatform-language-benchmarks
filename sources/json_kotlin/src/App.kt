import kotlinx.serialization.*
import kotlinx.serialization.json.*
import kotlinx.cinterop.*
import platform.posix.*

fun process(contents: String) {
    val obj = Json.parse(Media.serializer().list, contents)
    println(obj.map({ media -> media.author.username }))
}

@Serializable
data class User(val username: String)

@Serializable
data class Comment(val author: User, val text: String, val likes: Array<User>)

@Serializable
data class Media(val author: User, val likes: Array<User>, val comments: Array<Comment>, val images: Map<String, String>, val description: String)

fun main(args: Array<String>) {
    // For the life of me, I could not figure out how to open and read a file with Kotlin Native without
    // going back to C libraries.. This is based on Kotlin Native Sample Code
    val file = fopen("./test.json", "r")
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
            process(result)
        }
    } finally {
        fclose(file)
    }
}
