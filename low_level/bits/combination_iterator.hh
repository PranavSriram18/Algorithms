#pragma once

#include <string>

/**
 * Implements a lexicographic iterator over k-combinations of characters from a
 * string of unique characters.
 * 
 * Full problem description: 
 * https://leetcode.com/problems/iterator-for-combination/
 * 
 * Level: Medium
 * 
 * **Basic idea**
 * Use a bitmask to represent the state. In each step, we:
 * (i) find the leftmost on bit that can move 1 step to the left,
 * (ii) move this bit 1 step to the left, and
 * (iii) move all on bits to this bit’s left (if any) to the right, all the way
 * up to the bit. Examples help illustrate this.
 * 
 * Starting with the mask 00111 would produce the chain:
 * 00111 --> 01011 --> 10011 --> 01101
 * 
 * Initially the msb moves left freely. Once it's stuck at the left wall, the
 * next bit starts moving left, and the msb moves right as far as possible.
 * 
 * Another example of the shift pattern:
 * 11000101 --> 00111001
*/
class CombinationIterator {
public:
    CombinationIterator(std::string characters, int combinationLength) {
        s_ = characters;
        n_ = s_.size();
        k_ = combinationLength;
        mask_ = 0; 
    }
    
    std::string next() {
        updateState();
        return toString();
    }
    
    bool hasNext() {
        return mask_ != (((1 << k_) - 1) << (n_ - k_));
    }
    
private:
    void updateState() {
        if (mask_ == 0) {
            mask_ = ((1 << k_) - 1);
            return;
        }
        
        // search for the leftmost 1 that can move left
        int count = 0;
        int bit = -1;
        for (int i = n_ - 1; i >= 0; --i) {
            if ((mask_ & (1 << i)) == 0) continue;
            count++;
            if (i < n_ - 1 && ((mask_ & (1 << (i+1))) == 0)) {
                bit = i; 
                break;
            }
        }
        // unset everything from left up till and including
        // bit, and set next count bits
        mask_ = mask_ & ((1 << bit) - 1) | (((1 << count) - 1) << (bit+1));
    }
    
    std::string toString() {
        std::string res;
        for (int i = 0; i < n_; ++i) {
            if (mask_ & (1 << i)) {
                res += s_[i];
            }
        }
        return res;
    }
    
    int n_;
    std::string s_;
    int k_;
    int mask_;
};
