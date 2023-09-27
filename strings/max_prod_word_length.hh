#pragma once

#include <string>
#include <vector>


/*
Problem:
Given a list of words, return the maximum value of 
length(word[i]) * length(word[j]) where the two words do not share common
letters.

Full problem description: https://leetcode.com/problems/maximum-product-of-word-lengths/description/
Level: Leetcode Medium

Basic idea:
Naive brute forcing gives O(n^2 L) where k is length of longest string.
We can instead reduce to O(n^2 m) where m is alphabet size (26 in our case)
by precomputing "fingerprints", i.e. sets of chars that the words contain.
We can do this efficiently with bitsets.
*/

class MaxProdWordLength {
public:
    using Fingerprint = int32_t;

    int solve(std::vector<std::string>& words) {
        n_ = words.size();
        buildFingerprints(words);
        int best = 0;
        for (int i = 0; i < n_; ++i) {
            Fingerprint fi = fingerprints_[i];
            int size_i = sizes_[i];
            for (int j = i+1; j < n_; ++j) {
                if (!(fi & fingerprints_[j])) {
                    best = std::max(size_i * sizes_[j], best);
                }
            }
        }
        return best; 
    }

private:
    void buildFingerprints(std::vector<std::string>& words) {
        sizes_.reserve(n_);
        fingerprints_.reserve(n_);
        for (auto& word : words) {
            sizes_.push_back(word.size());
            fingerprints_.emplace_back(buildFingerprint(word));
        }
    }

    Fingerprint buildFingerprint(std::string& word) {
        Fingerprint f = 0;
        for (char ch : word) {
            f |= (1 << (ch - 'a'));
        }
        return f;
    }

    int n_;  // number of words
    std::vector<int> sizes_;
    std::vector<Fingerprint> fingerprints_;
};
