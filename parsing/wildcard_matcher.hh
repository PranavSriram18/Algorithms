#pragma once

#include <string>
#include <vector>

/*
Wildcard Matching
Level: LC Hard
Problem link: https://leetcode.com/problems/wildcard-matching/description/
Problem statement:
Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*' where:
'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial).
*/

/**
Scratch:
s = "aababac" --> string
p = "*" --> regex that matches anything
p = "aa?a*c"  --> matches s
p = a*?c --> matches s
p = a?a*c --> doesn't match s

D1 = "biology_homework1"
D2 = "biology_homework2_answers"
D3 = "math_homework4"
D4 = "math_olympiad7"

p = "*homework*"

s = "aababac"
p = "a?a*c"

Q. What if p doesn't have * ?
for i = 0:n-1 :
    check if s[i] == p[i] OR p[i] is '?'

If p = (_) * (_)

Assume:
1. p starts with a *
2. p contains at least 2 *s

s "aababacaacbacaaccaabaa"
p = *ba(*ac*aa)

if k = 2:
    s' = bacaacbacaaccaaba
    p' = *ac*aa
    if k' = 1:
        s'' = aacbacaaccaaba

State:
    position in s
    position in p

Let f(i, j) be defined as follows:
    s[i...n-1] matches p[j...n-1]

let [k0, k1, ..., k_q] be our choices for how many characters to match with first * in p
let t be number of characters after this * in p before next star
f(i, j) = max_{k_l}(f(i+k_l+t, j+t+1))

*/
class WildcardMatcher {
public:
    bool isMatch(std::string s, std::string p) {

    }

};  // class WildcardMatcher