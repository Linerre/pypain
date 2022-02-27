#include <iostream>
#include <fstream>
#include <string>
#include <vector>


int main()
{
  // Use abpath if the file should be placed in another directory
  // that is different from $(cwd)
  std::ifstream inf{ "sample.txt" };
  if(!inf) {
    std::cerr << "test.txt could not be open for reading.\n";
    return 1;
  }

  // Read the file line by line and put the lines in a vector
  std::vector<std::string> raw_lines;
  std::vector<std::string> new_lines;
  int line_num = 0;

  while(inf) {
    std::string str_input;
    // getline() will read but NOT include
    // the "\n" at the end of each line
    std::getline(inf, str_input);
    if (!str_input.empty()) {
      line_num++;
      raw_lines.push_back(str_input);
    }
  }

  // line_num is run-time variable, not a compile-time const!
  std::cout << "There are "
            << line_num
            << " non-empty lines in total."
            << std::endl;

  std::fstream of;

  // Replace the '@' in each line with two newline chars
  for (int i = 0; i < line_num; i++) {
    std::string line = raw_lines[i];
    std::size_t found_at_char = line.find_first_of("@");

    while (found_at_char != std::string::npos) {
      line.replace(line.find_first_of("@"), 1, "\n\n");
      found_at_char = line.find_first_of("@");
    }
    new_lines.push_back(line);
  }

  of.open("result.txt", std::fstream::out);
  for (int i = 0; i < line_num; i++) {
    of << new_lines[i] << " ";
  }
  of.close();

  return 0;
}
