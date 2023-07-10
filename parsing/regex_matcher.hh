#include <string>
#include <vector>

/*
Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:
'.' Matches any single character.​​​​
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).

Full problem description: 
https://leetcode.com/problems/regular-expression-matching/
Level: Leetcode Hard

Basic idea: state is positions in s and p. Recursion with a cache. The casework
is a bit tricky.
*/

class RegexMatcher {
public:
    bool isMatch(std::string s, std::string p) {
        slen_ = s.size();
        plen_ = p.size();
        cache_ = std::vector<std::vector<int>>(
			slen_ + 1, std::vector<int>(plen_ + 1, -1)
		);
        return isMatch(0, 0, s, p);
    }
    
private:
    static const char kNullChar = '!';
    
    bool isMatch(int sPos, int pPos, std::string& s, std::string& p) {
        int& result = cache_[sPos][pPos];
        if (result != -1) return result;
        bool sTerm = sPos >= slen_;
        if (sTerm && pPos == plen_) return result = true;
        if (pPos == plen_) return result = false;
        
        // non-p-terminal cases
        char sch = sTerm ? kNullChar : s[sPos];
        char pch = p[pPos];
        bool currIsDot = pch == '.';
        bool nextIsStar = (pPos != plen_ -1 && p[pPos+1] == '*');
        bool currMatches = (sch == pch || (currIsDot && !sTerm));
        
        // case 0
        if (!nextIsStar) {
            return result = currMatches && isMatch(sPos+1, pPos+1, s, p);
        }
        
        // case 1: advance both
        if (currMatches && isMatch(sPos+1, pPos + 2, s, p)) return result = true;
        
        // case 2: advance s only
        if (currMatches && isMatch(sPos+1, pPos, s, p)) return result = true;
        
        // case 3: advance p only
        return result = isMatch(sPos, pPos+2, s, p);
    }
    
    int slen_;
    int plen_;
    std::vector<std::vector<int>> cache_;
};