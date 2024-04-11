
class Solution {
/*
Problem description: https://leetcode.com/problems/magical-string/description/
Level: LC Medium

Scratch:
1 2 2 1 1 2 1 2 2 1 2 2

Idea: 
Just generate the string and count. 

Maintain an index of where we are currently reading from. 
This tells us the current block size.

*/
public:
    int magicalString(int n) {
        vector<int> result {1};
        result.reserve(n);
        int readPos = 0;
        int currWritten = 1;
        int currValue = 1;
        int blockSize;
        int numOnes = 1;

        while (result.size() < n) {
            blockSize = ((readPos < result.size()) ? result[readPos] : currValue);
            while (currWritten < blockSize && result.size() < n) {
                result.push_back(currValue);
                numOnes += (2 - currValue);
                ++currWritten;
            } 
            ++readPos;
            currWritten = 0;
            currValue = 3 - currValue;
        }
        return numOnes;
    }
};
