#include "special_binary_string.hh"

#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, std::string> expectedResults;
    std::string s0 = "11011000";
    expectedResults[s0] = "11100100";

    std::string s1 = "110110101111000000";
    expectedResults[s1] = "111111000010100100";

    std::string s2 = "1010";
    expectedResults[s2] = "1010";

    SpecialBinaryString specialBinaryString;

    for (const auto& [str, val] : expectedResults) {
        assert(val == specialBinaryString.makeLargestSpecial(str));
    }

    std::cout << "Success!" << std::endl;

    return 0;
}