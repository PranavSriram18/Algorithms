
"""
Source: https://leetcode.com/problems/valid-word-abbreviation
Level: LC Easy
"""

class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        self.word = word
        self.w_len = len(word)
        self.abbr = abbr
        self.a_len = len(abbr)
        return self.check(0, 0)
        
    def check(self, w_pos, a_pos):
        if w_pos >= self.w_len or a_pos >= self.a_len:
            return (a_pos == self.a_len) and (w_pos == self.w_len)
        
        abbr_ch = self.abbr[a_pos]
        if abbr_ch.isalpha():
            return self.word[w_pos] == abbr_ch and self.check(
                w_pos+1, a_pos+1)

        # check if num has leading 0s
        if self.abbr[a_pos] == '0':
            return False
        
        last_digit_pos = a_pos
        while last_digit_pos+1 < self.a_len and self.abbr[
            last_digit_pos+1].isdigit():
            last_digit_pos += 1
        num = int(self.abbr[a_pos:last_digit_pos+1])
        
        return self.check(w_pos+num, last_digit_pos+1)
    