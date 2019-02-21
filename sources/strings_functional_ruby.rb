def test(contents)
  contents.split(",")
    .map{|m| m.strip()}
    .map{|i| i.to_i}
    .reject{|i| i >= 100}
    .reduce(:+)
end

def main()
  puts test(IO.read("./numbers.txt"))
end
main()

