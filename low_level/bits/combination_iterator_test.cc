#include <iostream>
#include <string>

#include "combination_iterator.hh"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: program_name <chars> <combination_length>" << std::endl;
        return 1;
    }

    std::string chars = argv[1];
    int combinationLength = std::stoi(argv[2]);
    CombinationIterator iterator(chars, combinationLength);
    while(iterator.hasNext()) {
        std::cout << iterator.next() << std::endl;
    }

    return 0;
}
