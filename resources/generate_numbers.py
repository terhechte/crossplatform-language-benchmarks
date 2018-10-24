import random
import sys

for x in range(0, 7000000):
  c = random.randint(0, 120)
  sys.stdout.write(str(c))
  if random.randint(0, 5) > 3:
    for x in range(0, random.randint(0, 10)):
        sys.stdout.write(" ")
  sys.stdout.write(",")
  if random.randint(0, 5) > 3:
    for x in range(0, random.randint(0, 10)):
        sys.stdout.write(" ")
