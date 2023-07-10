#pragma once

class BitManipulator {
public:
    /*
     * Determines the bitwise `and` over the range [left, right].
     *
     * Full problem description: 
     * https://leetcode.com/problems/bitwise-and-of-numbers-range/
     * 
     * Basic Idea: 
     * Identify a criterion for kth bit to be set.
     * Suppose kth bit is on in the result. Let g(k, n) be number formed by bits 
     * [0, k-1] in the integer n.
     * We must have g(k, left) + (right - left) <= 2^k - 1, so that we don't carry. 
    */
    int rangeBitwiseAnd(int l, int r) {
        int x = 0, d = r - l;
        for (int b = 0; b <= 31; ++b) {
            if ((l & (1 << b)) && (d + (l & ((1 << b) - 1)) <= (1 << b) - 1)) {
                x |= (1 << b);
            }
        }
        return x;
    }
};  // class BitManipulator
