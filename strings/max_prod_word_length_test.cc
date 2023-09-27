#include <cassert>
#include <chrono>
#include <iostream>
#include <cmath>

#include "max_prod_word_length.hh"

int main() {
    // TODO - additional tests and timing
    std::vector<std::string> strings {"a", "bc", "abdef", "fg"};
    int expectedResult = 4;
    MaxProdWordLength solver;
    assert(solver.solve(strings) == expectedResult);
    std::cout << "Success" << std::endl;
    return 0;
}