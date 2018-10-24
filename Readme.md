# Mobile Language Benchmarks

I wrote this benchmark for a talk at Mobilization Conf 2018. It tries to compare modern languages aspiring to become go-to solutions for sharing code between iOS, Android and possibly other targets. The benchmark implements several short problems in Swift, Rust and Kotlin Native. One is also implemented in C.

There's probably a ton wrong here. If you find something that you deem not good, please file an issue, **OR*** (even better) create a PR. I've been working on this benchmark because I'm genuinely interested on the differences between the languages that can be used for sharing code across multiple mobile platforms. Consider this a first draft.

# The Numbers

[fixme: insert benchmarks]
JSON / NUMBERS files into resources, generators into resources

# The Benchmark

## Principles

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

## Things I'd like to do in the future
- Elaborate further on the `Principles`
- Add C++
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
