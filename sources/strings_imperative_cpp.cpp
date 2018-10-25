#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cctype>
#include <optional>
#include <functional>
#include <numeric>

// Lifted from StackOverflow
inline std::string trim(const std::string &s) {
   auto  wsfront=std::find_if_not(s.begin(),s.end(),[](int c){return std::isspace(c);});
   return std::string(wsfront,std::find_if_not(s.rbegin(),std::string::const_reverse_iterator(wsfront),[](int c){return std::isspace(c);}).base());
}

int test(std::stringstream &s) {
  std::string item;
  std::vector<std::string> elems;
  auto sum = 0;
  while (std::getline(s, item, ',')) {
    auto trimmed = trim(item);
    try {
      auto number = std::stoi(trimmed);
      if (number < 100) {
        sum += number;
      }
    }
    catch (int ) {
      continue;
    }
  }
  return sum;
}

int main (int argc, char *argv[]) {
  std::ifstream inFile;
  inFile.open("numbers.txt");

  std::stringstream strStream;
  strStream << inFile.rdbuf();

  std::cout << "\n" << test(strStream) << "\n";
}
