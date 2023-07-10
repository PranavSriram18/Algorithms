#include <cassert>
#include <iostream>

#include "regex_matcher.hh"

int main() {
    RegexMatcher regexMatcher;
    assert(regexMatcher.isMatch("aa", "a") == false);
    assert(regexMatcher.isMatch("aa", "a*"));
    assert(regexMatcher.isMatch("ab", ".*"));
    std::cout << "Success" << std::endl;
    return 0;
}