#pragma once

/**
 * This class includes functions for solving various problems involving 
 * bit manipulation.
*/
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

    /**
     * Given an integer x, returns the number of integers a in [1, x-1]
     * that satisfy a ^ x > x.
     * 
     * Full problem description:
     * https://www.hackerrank.com/challenges/the-great-xor/problem?isFullScreen=true
     * 
     * Level: Medium
     * 
     * Basic idea: Consider the position of the msb of a. That needs to be a 0
     * in the binary representation of x. Once that is fixed, the bits to its 
     * right can be anything. So just loop over 0-bits of x and add 2^bit for 
     * each of those.
    */
    long theGreatXor(long x) {
        long total = 0;
        long mask = 1l;
        while (mask <= x) {
            total += ((x & mask) == 0) * mask;
            mask <<= 1;
        }
        return total;
    }

};  // class BitManipulator
