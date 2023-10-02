#pragma once

#include <string>
#include <vector>

namespace utils {
std::vector<char> str2vec(const std::string& s) {
    std::vector<char> v;
    v.reserve(s.size());
    for (char ch : s) {
        v.push_back(ch);
    }
    return v;
}

std::string vec2str(const std::vector<char>& v) {
    std::string s;
    for (char ch : v) {
        s += ch;
    }
    return s;
}

// Whether s1 starts with s2
bool startsWith(const std::string& s1, const std::string& s2) {
    return (s2.size() <= s1.size()) && (s1.substr(0, s2.size()) == s2);
}
}  // namespace utils 
