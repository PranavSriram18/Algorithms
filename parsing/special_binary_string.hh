#pragma once

#include <algorithm>
#include <numeric>
#include <string>
#include <vector>

/*
Special binary strings are binary strings with the following two properties:

The number of 0's is equal to the number of 1's.
Every prefix of the binary string has at least as many 1's as 0's.

You are given a special binary string s. A move consists of choosing two 
consecutive, non-empty, special substrings of s, and swapping them. 

Return the lexicographically largest resulting string possible after applying
the mentioned operations on the string.

Full problem description: 
https://leetcode.com/problems/special-binary-string/

Level: Leetcode Hard.

Basic idea: recursion. Consider the first 0 that "matches" the starting 1, i.e.
the first point at which the number of 1s and 0s encountered so far are equal.
There are 2 cases:
(i) This 0 is the last character. 
    Then, s = 1s'0 and we recurse on s'.
(ii) This 0 is not the last character. Let s = s1s2...sk,
     recurse on each of the si's, and sort them.
 */
class SpecialBinaryString {
public:
    std::string makeLargestSpecial(std::string s) {
        return solve(s, 0, s.size()-1);
    }

private:
    /**
     * Returns the lexicographically largest possible substring that can be 
     * created from the substring [s[start]...s[end]].
    */
    std::string solve(std::string& s, int start, int end) {
        if (end <= start) return "";

        // First break into substrings
        std::vector<std::string> substrings;
        getSubstrings(s, start, end, substrings);

        // Case (i): only 1 substring. s = 1s'0 and recurse on s'.
        if (substrings.size() == 1) {
            return "1" + solve(s, start+1, end-1) + "0";
        } 

        // Case (ii): solve each piece
        std::vector<std::string> sortedSubstrings;
        for (auto& substring : substrings) {
            std::string sortedSubstring = solve(
                substring, 0, substring.size()-1);
            sortedSubstrings.push_back(sortedSubstring);
        }

        // Sort the solved pieces
        std::sort(
            sortedSubstrings.begin(),
            sortedSubstrings.end(),
            [](const std::string& s1, const std::string& s2) { 
                return s1 > s2;
            }
        );

        // Concatenate into a single string
        return std::accumulate(
            sortedSubstrings.begin(), sortedSubstrings.end(), std::string()
        );
    }

    /** Chunks s into special substrings. */
    void getSubstrings(
        std::string& s, int start, int end, std::vector<std::string>& substrings
    ) {
        if (start >= end) return;
        int count = 0;
        int j = start;
        for (; j <= end; ++j) {
            count += ((s[j] == '1') ? 1 : -1);
            if (count == 0) {
                substrings.push_back(s.substr(start, j-start+1));
                break;
            }
        }
        getSubstrings(s, j+1, end, substrings);
    }
};  // class SpecialBinaryString
