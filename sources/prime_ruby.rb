
def is_prime(number)
  return false if number <= 1
  for i in 2...number
    return false if (number % i) == 0
  end
  return true
end

a = 0
for i in 0..100000
  if is_prime(i) == true
    a += 1
  end
end
puts a
