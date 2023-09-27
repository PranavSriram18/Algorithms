#pragma once

#include <vector>
#include <string>

/*
Problem:
Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be 
stored in the input character array chars. Note that group lengths that are 10
or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

Full problem description: https://leetcode.com/problems/string-compression/
Level: Leetcode Medium

Basic idea:
This is an exercise in managing state and invariants. We can encapsulate the 
salient state into 5 parameters: where to read from, where to write to, the
previous and current characters, and the length of the current block of
consecutive characters. It also helps to (virtually) pad the input string
with a sentinel so that we process the last block. The update rules are
as follows:
1. (prevChar, nextChar) -> (nextChar, chars[readPos])
2. readPos is incremented on every read (except the last)
3. writePos is incremented on each character write
4. runLength is either incremented or reset to 1
*/
class StringCompressor {
public:
    static constexpr char kSentinel =  '\xFF';

    int compress(std::vector<char>& chars) {
        int n = chars.size();
        
        int readPos = 1;  // position to read next
        int writePos = 0;  // position to write next
        char prevChar = kSentinel;  // placeholder
        char nextChar = chars[0];  // at start, we have read the 1st char
        int runLength = 1;  // length of current block

        while(nextChar != kSentinel) {
            prevChar = nextChar;
            nextChar = readPos < n ? chars[readPos++] : kSentinel;
            if (prevChar == nextChar) {
                runLength++;
            } else {
                chars[writePos++] = prevChar;
                if (runLength > 1) {
                    std::string lenStr = std::to_string(runLength);
                    for (char digit : lenStr) {
                        chars[writePos++] = digit;
                    }
                }
                runLength = 1;
            }
        }
        return writePos;
    }
};  // class StringCompressor
