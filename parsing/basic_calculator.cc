#include <iostream>

#include "basic_calculator.hh"

int main() {
    BasicCalculator calculator;
    std::string s0 = "(1+(4+5+2)-3)+(6+8)";
    std::string s1 = "123 - 45 + 67";
    std::string s2 = "12 - 34 + (56 - 718) + 2";

    for (auto& s : {s0, s1, s2}) {
        std::cout << s << " evaluates to " << calculator.calculate(s) << std::endl;
    }
    return 0;
}
