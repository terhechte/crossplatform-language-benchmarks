#include <iostream> 

using std::cout;

bool is_prime(int number) {
  // C++ does not have a range struct
  // so this is obvously not a useful comparison.
  if (number <= 1) return false;
  for (int i=2; i<number; i++) {
    if (number % i == 0) return false;
  }
  return true;
}

int main (int argc, char *argv[]) {
  int a = 0;
  for (int i=0; i<=100000; i++) {
    if (is_prime(i)) {
      a += 1;
    }
  }
  cout << "\n" << a << "\n";
}
