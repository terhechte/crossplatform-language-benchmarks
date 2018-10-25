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
std::vector<std::string> split(const std::string &s, char delim) {
  std::stringstream ss(s);
  std::string item;
  std::vector<std::string> elems;
  while (std::getline(ss, item, delim)) {
    elems.push_back(std::move(item));
  }
  return elems;
}

// Lifted from StackOverflow
inline std::string trim(const std::string &s) {
   auto  wsfront=std::find_if_not(s.begin(),s.end(),[](int c){return std::isspace(c);});
   return std::string(wsfront,std::find_if_not(s.rbegin(),std::string::const_reverse_iterator(wsfront),[](int c){return std::isspace(c);}).base());
}

inline std::optional<int> operate(const std::string &s) {
  auto trimmed = trim(s);
  try {
    auto number = std::stoi(trimmed);
    return number;
  }
  catch (int ) {
    return {};
  }
}

int test(std::string str) {
  // I found it tricky to use a fully functional C++ version without external libraries such as
  // boost.
  // So, instead, enjoy this half-hearted attempt
  auto contents = split(str, ',');
  std::vector<std::optional<int>> converted; 
  converted.resize(contents.size());
  std::transform(contents.begin(), contents.end(), converted.begin(), operate);
  auto sum = 0;
  for (std::optional<int> n: converted) {
    if (n.has_value() ) {
      if (n.value() < 100) {
        sum += n.value();
      }
    }
  }
  return sum;
}

int main (int argc, char *argv[]) {
  std::ifstream inFile;
  inFile.open("numbers.txt");

  std::stringstream strStream;
  strStream << inFile.rdbuf();
  std::string str = strStream.str();

  std::cout << "\n" << test(str) << "\n";
}
