import os, sys, platform, time, subprocess, csv, pickle
from os.path import join, abspath
from shutil import copyfile
from collections import OrderedDict
import ConfigParser

CONFIG_FILE = "bench.cfg"

class BenchConfig:
    class SectionWrapper:
        def __init__(self, name, config):
            self.name = name
            self.config = config
        def __getattr__(self, key):
            if self.name == "active":
                return self.config.getboolean(self.name, key)
            else:
                return self.config.get(self.name, key)
    def __init__(self, config_file):
        self.config = ConfigParser.ConfigParser()
        self.config.read(abspath(config_file))
        self.sections = {
            "general": BenchConfig.SectionWrapper("general", self.config),
            "active": BenchConfig.SectionWrapper("active", self.config),
            "titles": BenchConfig.SectionWrapper("titles", self.config),
            "directories": BenchConfig.SectionWrapper("directories", self.config)
        }

    def __getattr__(self, key):
        return self.sections[key]

class BuildSystem:
    # The name of this system
    name = None
    # This is an input parameter
    infile = None
    # This is generated by the build system
    outfile = None
    # This is an input parameter
    source_directory = None
    # This is an input parameter
    out_directory = None
    def __init__(self, infile, source_directory, out_directory):
        self.infile = infile
        self.source_directory = source_directory
        self.out_directory = out_directory
    def clean(self): pass
    def prebuild(self): pass
    def build_cwd(self): return os.path.curdir
    def build(self): pass
    def postbuild(self): pass
    def run(self):
        return abspath(join(self.out_directory, self.outfile))
    def execute(self, command):
        p = subprocess.Popen(command.split(), stderr=subprocess.STDOUT, cwd=self.build_cwd())
        p.wait()

class SwiftBuildSystem (BuildSystem):
    name = "Swift"
    def build(self):
        self.outfile = self.infile.replace(".swift", "")
        return "%s -O %s -o %s" % (config.general.binary_swift, abspath(join(self.source_directory, self.infile)), abspath(join(self.out_directory, self.outfile)))

class RustBuildSystem (BuildSystem):
    name = "Rust"
    def build(self):
        self.outfile = self.infile.replace(".rs", "")
        return "%s -O %s -o %s" % (config.general.binary_rust, abspath(join(self.source_directory, self.infile)), abspath(join(self.out_directory, self.outfile)))

class KotlinBuildSystem (BuildSystem):
    name = "Kotlin"
    def build(self):
        outfile = self.infile.replace(".kt", "")
        self.outfile = outfile + ".kexe"
        return "%s -opt %s -o %s" % (config.general.binary_kotlin, abspath(join(self.source_directory, self.infile)), abspath(join(self.out_directory, self.outfile)))

class CBuildSystem (BuildSystem):
    name = "C"
    def build(self):
        self.outfile = self.infile.replace(".c", "")
        return "%s -O2 %s -o %s" % (config.general.binary_clang, abspath(join(self.source_directory, self.infile)), abspath(join(self.out_directory, self.outfile)))

class CargoBuildSystem (BuildSystem):
    name = "Rust"
    def perform_in_cargo(self, command, ret = False):
        if ret:
            return command
        else:
            self.execute(command)

    def build_cwd(self):
        return abspath(join(self.source_directory, self.infile))

    def clean(self):
        self.perform_in_cargo("%s clean" % (config.general.binary_cargo))

    def prebuild(self):
        self.perform_in_cargo("%s build-deps" % (config.general.binary_cargo))

    def build(self):
        self.outfile = self.infile
        return self.perform_in_cargo("%s build --release" % (config.general.binary_cargo), ret = True)

    def postbuild(self):
        source_path = abspath(join(self.source_directory, self.infile, join("target", "release"), self.outfile))
        target_path = abspath(join(self.out_directory, self.infile))
        os.system("cp %s %s" % (source_path, target_path))

class BenchResult:
    name = ""
    language = ""
    command = ""
    is_compile = False
    is_fail = False
    real = 0.0
    user = 0.0
    sys = 0.0
    resident_set_size = 0
    page_reclaims = 0
    children = []

    def __str__(self):
        return "%s: real: %f, user: %f, sys: %f, max resident set size: %i" % (self.name, self.real, self.user, self.sys, self.resident_set_size)

    def merge(self, items):
        self.children = items
        c = 0
        fail = False
        for item in items:
            if item.is_fail == True: 
                fail = True
                continue
            self.real += item.real
            self.user += item.user
            self.sys += item.sys
            self.resident_set_size += item.resident_set_size
            self.page_reclaims += item.page_reclaims
            c += 1
        self.fail = fail
        if c == 0: return
        self.real /= c
        self.user /= c
        self.sys /= c
        self.resident_set_size /= c
        self.page_reclaims /= c

class Bencher:
    benches = OrderedDict()
    languages = set()
    count = None

    def __init__(self, count):
        self.count = count

    def split_load(self, line, result):
        """parse the bench results into real, user, sys and apply to result"""
        comps = line.split()
        result.real = float(comps[0])
        result.user = float(comps[2])
        result.sys = float(comps[4])

    def bench_command(self, command, cwd):
        """run a command and return the timing"""
        print "\t: %s" % (command,)
        result = BenchResult()
        result.command = command
        # Make sure we don't run too long
        begin = time.time()
        process = subprocess.Popen(["time", "-l"] + command.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=cwd)
        while True:
            if process.poll() != None:
                break
            if (time.time() - begin) > int(config.general.bench_max_time):
                print "Executing %s took too long. Quitting." % (command,)
                fail_result = BenchResult()
                fail_result.is_fail = True
                return fail_result
        output = process.stdout.read()
        for line in output.split("\n"):
            if line.find("real") >= 0 or line.find("user") >= 0 or line.find("sys") >= 0:
                self.split_load(line, result)
            if line.find("maximum resident set size") >= 0:
                result.resident_set_size = int(line.split()[0])
            if line.find("page reclaims") >= 0:
                result.page_reclaims = int(line.split()[0])
        return result

    def multi_bench_command(self, command, cwd):
        new = BenchResult()
        new.merge([self.bench_command(command, cwd) for x in range(0, self.count)])
        return new

    def bench_entry(self, name, entry):
        # If benching this language is disabled, stop
        if not entry.name in config.general.active_languages:
            print "Unsupported language", entry.name
            return
        entry.clean()
        entry.prebuild()
        command = entry.build()
        print "Benching Compile: ", name, entry.name
        compile_bench = self.bench_command(command, entry.build_cwd())
        compile_bench.name = name
        compile_bench.language = entry.name
        compile_bench.is_compile = True
        lst = None
        key = "Compile: " + name
        try:
            lst = self.benches[key]
        except KeyError:
            lst = []
            self.benches[key] = lst
        lst.append(compile_bench)
        entry.postbuild()
        # if the compiling failed, we can't execute it
        bench = None
        if compile_bench.is_fail == True:
            bench = BenchResult()
            bench.is_fail = True
        else:
            print "Benching: ", name, entry.name
            run_command = entry.run()
            bench = self.multi_bench_command(run_command, abspath(config.directories.resource_directory))
        bench.name = name
        bench.language = entry.name
        self.languages.add(entry.name)
        try:
            lst = self.benches[name]
        except KeyError:
            lst = []
            self.benches[name] = lst
        lst.append(bench)

    def write_bench_pickle(self, folder):
        with open(abspath(join(folder, version_info() + ".pickle")), "w") as picklefile:
            pickle.dump(self.benches, picklefile)

    def write_bench_csv(self, folder):
        fieldnames = ["Benchmark"] + list(self.languages)
        with open(abspath(join(folder, version_info() + ".csv")), "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for bench_name in self.benches.keys():
                language_benches = self.benches[bench_name]
                values = {"Benchmark": bench_name}
                for language_bench in language_benches:
                    values[language_bench.language] = language_bench.real
                writer.writerow(values)

def version_info():
  def detect_version():
    linux = platform.linux_distribution()
    macos = platform.mac_ver()
    win = platform.win32_ver()
    if len(linux[0]) > 0: return linux
    elif len(macos[0]) > 0: return macos
    elif len(win[0]) > 0: return win
    else: return (sys.platform, ('', '', ''), platform.architecture()[0])
  version = detect_version()
  return "%s-%s-%s" % (sys.platform, version[0], version[-1])

def build_system_factory(in_dir, out_dir):
    def fn(infile):
        language = infile.split(".")[-1]
        if language == "swift": return SwiftBuildSystem(infile, in_dir, out_dir)
        elif language == "rs": return RustBuildSystem(infile, in_dir, out_dir)
        elif language == "kt": return KotlinBuildSystem(infile, in_dir, out_dir)
        elif language == "c": return CBuildSystem(infile, in_dir, out_dir)
    return fn

def clear_builds(out_dir):
    for f in os.listdir(out_dir):
        os.remove(abspath(join(out_dir, f)))

def make_benches():
    clear_builds(config.directories.build_directory)
    builder = build_system_factory(config.directories.source_directory, config.directories.build_directory)
    bencher = Bencher(int(config.general.iteration_count))
    if config.active.primes_functional:
        title = config.titles.primes_functional_title
        bencher.bench_entry(title, builder("prime_swift.swift"))
        bencher.bench_entry(title, builder("prime_rust.rs"))
        bencher.bench_entry(title, builder("prime_kotlin.kt"))
    if config.active.strings_functional:
        title = config.titles.strings_functional_title
        bencher.bench_entry(title, builder("strings_functional_swift.swift"))
        bencher.bench_entry(title, builder("strings_functional_rust.rs"))
        bencher.bench_entry(title, builder("strings_functional_kotlin.kt"))
    if config.active.strings_imperative:
        title = config.titles.strings_imperative_title
        bencher.bench_entry(title, builder("strings_imperative_swift.swift"))
        bencher.bench_entry(title, builder("strings_imperative_rust.rs"))
        bencher.bench_entry(title, builder("strings_imperative_kotlin.kt"))
    if config.active.chunks_functional:
        title = config.titles.chunks_functional_title
        bencher.bench_entry(title, builder("chunks_functional_swift.swift"))
        bencher.bench_entry(title, builder("chunks_functional_rust.rs"))
        bencher.bench_entry(title, builder("chunks_functional_kotlin.kt"))
        bencher.bench_entry(title, builder("chunks_imperative_c.c"))
    if config.active.chunks_imperative:
        title = config.titles.chunks_imperative_title
        bencher.bench_entry(title, builder("chunks_imperative_swift.swift"))
        bencher.bench_entry(title, builder("chunks_imperative_rust.rs"))
        bencher.bench_entry(title, builder("chunks_imperative_kotlin.kt"))
        bencher.bench_entry(title, builder("chunks_imperative_c.c"))
    if config.active.json:
        title = config.titles.json_title
        bencher.bench_entry(title, builder("json_swift.swift"))
        bencher.bench_entry(title, CargoBuildSystem("json_rust", config.directories.source_directory, config.directories.build_directory))

    bencher.write_bench_csv(config.directories.bench_csv_directory)
    bencher.write_bench_pickle(config.directories.bench_csv_directory)

def make_charts():
    """Goes through all the csv files, and renders them as markdown tables. Returns all."""
    def make_chart(filepath):
        name = os.path.splitext(os.path.basename(filepath))[0]
        output = []
        with open(filepath, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            fields = reader.fieldnames
            output.append(" | ".join(fields))
            longest = max(map(lambda x: len(x), fields))
            output.append(" | ".join([longest * "-" for x in range(0, len(fields))]))
            for row in reader:
                line = []
                for field in fields:
                    try:
                        line.append(str(round(float(row[field]), 2)))
                    except ValueError:
                        line.append(row[field])
                output.append(" | ".join(line))
        return "# " + name + "\n" + "\n".join(["| %s |" % (x,) for x in output])
    charts = []
    for f in os.listdir(abspath(config.directories.bench_csv_directory)):
        if f[-3:] != "csv":continue
        charts.append(make_chart(abspath(join(config.directories.bench_csv_directory, f))))
    print "\n\n".join(charts)

def usage():
    print """
    Usage:
      python ./bench.py [task]
        Tasks:
         "charts": Will render all charts in 'benches/' to markdown and print them
         "bench": Will run all activated benchmarks, and write to the 'benches/' directory
    """
    sys.exit()

config = BenchConfig(CONFIG_FILE)

if __name__ == "__main__":
    command = ""
    try:
        command = sys.argv[1]
    except IndexError:
        pass
    if command == "charts":
        make_charts()
    elif command == "bench":
        make_benches()
    else:
        usage()