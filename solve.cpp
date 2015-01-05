#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cout << "Usage-  solve wordlist\n";
    return 1;
  }

  std::ifstream infile;
  infile.open(argv[1]);
  if (!infile.is_open()) {
    std::cout << "Could not open file \"" << argv[1] << "\"\n";
    return 1;
  }

  std::string line;
  int count = 0;
  while (getline(infile, line)) {
    count ++;
  }

  std::cout << "read " << count << " lines.\n";
  return 0;
}
