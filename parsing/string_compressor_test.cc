#include <cassert>
#include <chrono>
#include <iostream>

#include "string_compressor.hh"

#include "../utils/string_utils.hh"

int main() {
    StringCompressor compressor;
    std::string test = "aaabbbbcdde";
    std::string expectedResult = "a3b4cd2e";
    std::vector<char> testVec = utils::str2vec(test);
    compressor.compress(testVec);
    std::string result = utils::vec2str(testVec);
    assert(utils::startsWith(result, expectedResult));
    std::cout << "Success!" << std::endl;
    return 0;
}