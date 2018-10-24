fun isPrime(number: Int): Boolean {
    return (number > 1) && !((2 until number).any({ n -> number % n == 0 }))
}

fun main(args: Array<String>) {
    var a = 0
    for (i in 0..100000) {
        if (isPrime(i)) { a += 1 }
    }
    println(a)
}
