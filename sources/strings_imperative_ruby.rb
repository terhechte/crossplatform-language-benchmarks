def test(contents)
  res = 0
  ar = contents.split(",")
  ar.each do |x|
    num = x.strip().to_i
    if num < 100
      res += num
    end
  end
  res
end

def main()
  puts test(IO.read("./numbers.txt"))
end
main()

