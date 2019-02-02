# Mobile Language Benchmarks

I wrote this benchmark for a talk at Mobilization Conf 2018. It tries to compare modern languages aspiring to become go-to solutions for sharing code between iOS, Android and possibly other targets. The benchmark implements several short problems in Swift, Rust and Kotlin Native, C++ and C.

This benchmark tries to inspect three properties of aforementioned modern languages:

- Similarity of code
- Compile time performance [1]
- Runtime performance

[1] *Compile times are measured because fast recompiling is a significant part of developer happiness and language usefulness. Nobody wants a codebase where a single change causes a 30min compile time.*

Meaning, it tries to identify the performance differences between similar looking code in modern languages. Take the following simple prime number algorithm as an example:

### Kotlin:
``` kotlin
(number > 1) && !((2 until number).any({ n -> number % n == 0 }))
``` 

### Swift
``` Swift
number > 1 && !(2..<number).contains { number % $0 == 0 }
``` 

### Rust
``` Rust
number > 1 && !(2..number).any(|n| number % n == 0)
``` 

You can already see, that the implementation of the algorithm looks very similar, the main difference is in naming things (i.e. `any` vs `contains`). This is possible, because all three languages above share a `Range` structure and offer functional operations (such as `any` or `contains`) with closures on them.
C++ on the other hand, would require different code, as it does (currently, without external libraries, such as boost) not offer a `Range` structure, and also does not offer easy functional operations as part of its standard library (there is `std::transform`, `std::filter_if` or `std::reduce` but they compose not as easily as above).

So, in short, what this benchmark tries to answer is:

## How different is the performance for almost similar languages between Kotlin, Swift, and Rust

C++ and C are sometimes (where appropriate) added as comparisons for speed purposes (and sometimes also just to see how much more involved it is to implement the same code in C++).

There's probably a ton wrong here. If you find something that you deem not good, please file an issue, **OR*** (even better) create a PR. I've been working on this benchmark because I'm genuinely interested on the differences between the languages that can be used for sharing code across multiple mobile platforms. Consider this a first draft.

Also, I'm by far no expert in C++ or C. So, if any of my writing about C++ here is wrong, please don't become enraged and instead help out by creating a pull request.

Finally, all binaries are compiled with all optimizations on.

# The Numbers

## Benchmarks for macOS X 10.14.2 on a Mac Mini 3.2 GHz Core i7 32GB RAM

[A nicer, HTML Bar Chart, representation can be found here]()

JSON / NUMBERS files into resources, generators into resources

# Principles

This benchmark tries to adhere to the following principles. However, I do understand that benchmarking is hard and always biased. I tried as much as possible to choose problems that can be implemented in a very similar manner across the selected languages (with the exception of C, which is just in for the lolz). 

- Code should be idiomatic. Examples:
  - If the language has a idiomatic way of accessing array slices, use that (i.e. Swift)
  - If the language has a idiomatic way of using lazy sequences, use that
- Code should not perform crazy optimizations
- The solutions in the different languages should be easily comparable:
  - Use `map`, `filter`, and their equivalents in the same manner when possible
  - Use for loops in the same way
  - If, say, structs are useful for a solution, use structs, even though Kotlin doesn't support them. If the solution requires a pointer to a struct, use classes and Box<Struct> in Rust
- Bench the compile time too (because we native developers are always looking at React Native and their instant reload. Faster compile times certainly help her)
- If the code requires external dependencies, don't bench their compile time (because they don't change after the first compile and thus are nothing that needs to be compiled constantly).
- If something takes longer than 5min (compiling, or running) it is killed


# The Benchmarks

Some benchmarks are implemented in two manners. The first being in functional style, such as:

``` swift
0..<100.filter({ $0 % 2 == 0 }).map(String.init)
```

The other in imperative style:

```swift
var results = [String]()
for i in 0..<100 {
  guard i % 2 == 0 else { continue }
  results.append(String(i))
}
```

The reason for this is to see if the usage of functional constructs has any overhead in the language (i.e. whether the language supports zero-overhead-abstractions).

## Strings

String processing is a very common operation that can quickly become expensive. The inclusion of proper unicode support in modern languages makes string operations even more expensive. This problem benches file IO, string processing, and optionals. It consists out of the following steps:

1. Read a particularly long file which contains numbers, divided by commata, interspersed with whitespace: `4  , 32 ,    8,   9   ,177` [...]
2. Split the string by commata into a list of strings
3. Remove the whitespace in each entry on the left and right (trim)
4. Convert each entry to integer. If that fails, return `null` or an `optional` (if the language has such a construct)
5. Flatten the resulting list of optionals or null (removing all invalid entries)
6. Filter out all numbers that are bigger than 100
7. Sum up the remaining numbers

The **functional** benchmark is implemented in [Swift](sources/strings_functional_swift.swift), [Rust](sources/strings_functional_rust.rs), [Kotlin](sources/strings_functional_kotlin.kt) and [C++](sources/strings_functional_cpp.cpp).

The **imperative** benchmark is implemented in [Swift](sources/strings_imperative_swift.swift), [Rust](sources/strings_imperative_rust.rs), [Kotlin](sources/strings_imperative_kotlin.kt) and [C++](sources/strings_imperative_cpp.cpp).

### Notes
- File IO seems to make quite a difference here. I created some versions where the string was inlined in the source file and it did indeed change the results, but the resulting 7MB `.swift` and `.kt` files were unwieldy to handle. Also, benching file IO is useful.
- Swift has a very slow implementation of `trim`. Swift strings are converted to Objective-C strings, then they're trimmed, then they're converted back to Swift Strings. This leads to sub-par performance. When replacing the standard libraries trim with a custom implementation, the Swift benchmark improves dramatically.
- The C++ version is not entirely functional. It is a mix of functional and imperative, but it is the best I could come up with.
- I must be doing something wrong with C++, though I don't know what. The Rust version performs dramatically better than the C++ version.

## Prime Numbers

This problem benches the implementation of a very simple algorithm. The idea is to see whether we can find performance differences for very small and local chunks of code.

1. Go through the range of numbers from 0 to 100000
2. For each number N1, identify whether it is prime by:
3. Testing whether N1 is > 1
4. Testing whether the range of 2 until N1 contains any N2 such that the modulus of N1 and N2 is zero

The benchmark is implemented in [Rust](sources/prime_rust.rs), [Swift](sources/prime_swift.swift), [Kotlin](sources/prime_kotlin.kt) and [C++](sources/prime_cpp.cpp)

### Notes
- The C++ version is imperative, as a functional version would have required the addition of `Boost`

## Chunks

This problem measures functional array processing and dynamic array handling. It requires creating arrays, chunking of arrays, summing of arrays, and iterating over arrays.

1. Create an array of 1000000 * 256 integers in memory `[1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]` [...]
2. Iterate over this array in chunks of 8 integers C1 `[[1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]]` [...]
3. For each chunk C1, iterate again, in chunks of 2 integers C2 `[[[1, 2], [3, 4], [5, 6], [7, 8]], [[1, 2], [3, 4], [5, 6], [7, 8]]]` [...]
4. For each chunk C2, sum up the contents `[[3, 7, 11, 15], [3, 7, 11, 15]]` [...]
5. Flatten the resulting array of arrays `[3, 7, 11, 15, 3, 7, 11, 15]` [...]
6. Sum the resulting arrays `72`
7. Do the same with other chunk sizes (32, 8) and (16, 4)

The **functional** benchmark is implemented in [Swift](sources/chunks_functional_swift.swift), [Rust](sources/chunks_functional_rust.rs) and [Kotlin](sources/chunks_functional_kotlin.kt)
The **imperative** benchmark is implemented in [Swift](sources/chunks_imperative_swift.swift), [Rust](sources/chunks_imperative_rust.rs), [Kotlin](sources/chunks_imperative_kotlin.kt) and [C](sources/chunks_imperative_c.c)

### Notes
- The additional chunking into slices of 2 is purely to complicate the problem
- The Swift version uses array slicing which are a clear performance improvement. It could be argued whether this is still idiomatic Swift as they're not a commonly used abstraction in end user Swift code (they're used a lot in the standard library though)
- The Rust version also uses slices (`&[usize]`), however this is clearly idiomatic Rust, even `Clippy` points this out.
- The functional Kotlin never finished for me (that is, I always gave up after 25min of waiting)

## JSON

It was famously once quipped, that mobile apps are nothing more than glorified JSON stylesheets. As many apps indeed resolve heavily around JSON processing, it makes sense to also test the JSON deserialization performance of the varous languages. As not all languages come with a JSON parser in the standard library, the canonical library was picked (if there was such a thing). One important addition here is the requirement to parse the JSON directly into the correct datatype, not just a JSON object or value. In this example, the JSON is for a fictional posting of a new image to an image service.

1. Read a large JSON file (27MB)
2. Define structures that auto-deserialize from JSON
3. Parse the JSON into the structures
4. Map over all parsed entities and print the image author's username

[Here's an example of the JSON that doesn't require you to download the full 27MB file](resources/json_bench_example.json)

The benchmark is implemented in [Swift](sources/json_swift.swift), [Kotlin](sources/json_kotlin/src/App.kt] and [Rust](sources/json_rust/src/main.rs)

### Notes
- This Benchmark was not implemented for Kotlin Native, as I could not find a way to deserialize JSON into types with Kotlin Native (see issues)
- This Benchmark was not (yet) implemented for C++. I'm planning to do so.
- The default JSON parser for Rust is an external package / crate (`serde`)
- There is no serialization benchmark (yet)

# Issues
- Elaborate further on the `Principles`
- Add C++
- Should boost be allowed for C++?
- Add more examples
- Add Kotlin JVM (i.e. the non-native version)
- Run on more operating systems / architectures
- Add Windows support (bench.py uses multiple unix conventions)
- I couldn't get JSON deserialization into classes to work for Kotlin Native (see https://github.com/Kotlin/kotlinx.serialization/blob/master/json/README.md)
- Maybe add Go
- Maybe use internally https://pypi.org/project/psutil/
- Maybe use internally https://pypi.org/project/bench/

# Contributing

There're multiple ways to contribue. I'll just list some of them:
- Look at the examples if anything is not idiomatic, create a PR. Please follow the principles stated above.
- Run the tests on your machine, commit the resulting CSV
- Run the tests on an Android / Windows device, commit the resulting CSV
- Run the tests on Linux, commit the resulting CSV
- Improve the bench.py (it was a quick hack)
- Look at the open issues

# Running it

There's a benchmark runner included. Make sure that your system fulfills all the requirements (see below), then edit the `bench.cfg` file to your needs. The config file is documented.

Finally, just run it like this:

``` bash
python ./bench.py bench
```

**Warning**, this can take a long time.

It will render the benchmarks into `csv` files into the `benches/` directory.

If you desire to generate markdown charts, simply run:

```bash
python ./bench.py charts
```

You can also generate kinda fancy HTML charts via

``` bash
python ./bench.py html_charts
```

(warning, the code for this is *messy*)

# Requirements:

If you don't fulfill any of these requirements, you can disable them in the `bench.cfg` (except for Python, obviously).

## Python
Python 2.7+

## Rust

### Rustup:
https://rustup.rs/
This will install `rust`, `rustc`, and `cargo`

### Cargo Build Deps
This benchmark needs:
https://crates.io/crates/cargo-build-deps

In order to install it, once `rust` / `cargo` is installed, run:
``` bash
cargo install cargo-build-deps
```
### Swift
Follow the guides on:
https://swift.org/getting-started/

### Kotlin Native
I installed it from the releases on their GitHub page here:
https://github.com/JetBrains/kotlin-native

### C
If you use Xcode, Rust, or Swift, chances are high you already have it installed, otherwise ask a package manager of your choice, or look here:
https://clang.llvm.org/

# Resources

There're two Python scripts that generate the JSON and the number string for the `JSON` and the `Strings` test. If you run them, they will print the generated code to the console, so run them like this (if you intend to change the contents of the file):

``` bash
python ./gen_numbers.py > ./numbers.txt
```
