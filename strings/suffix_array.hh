#pragma once

#include <string>
#include <vector>

/**
 * string s, with n characters
 * s = "babaac"
 * suffixes: ["c", "ac", "aac", "baac", "abaac", "babaac"]
 * suffix array (full suffixes): ["aac", "abaac", "ac", "baac", "babaac", "c"]
 * suffix array: [3, 1, 4, 2, 0, 5]
 * 
 * Problem: construct suffix array from the string s
 * 
 * Naive algorithm:
 * create array of suffixes and sort it
 * Time complexity: 
 * - create suffix array: O(n^2)
 * - sorting it: O(nlogn) comparisons; e.g. comparison is O(n)
 * - sorting total: O(n^2 log n)
 * 
 * s = "babaac$"
 * "babaac$"
 * "abaac$b"
 * "baac$ba"
 * "aac$bab"
 * "ac$baba"
 * "c$babaa"
 * "$babaac" (ignore)
 * 
 * sorted cyclic shifts:
 * [aac$bab, abaac$b, ac$baba, baac$ba, babaac$, c$babaa]
 * 
 * --> to compute suffix array, sufficient to compute cyclic shift array
 * 
 * Define f(i, k) to be length k cyclic substring starting at i of length k
 * 
 * for example, f(4, 4) = "ac$b", f(3, 6) = "aac$ba"
 * 
 * Idea:
 * Start by sorting f(i, 1) for each i
 * Then sort f(i, 2) for each i
 * Then sort f(i, 4) for each i
 * Then sort f(i, 8) for each i
 * 
 * indices:
 * [[6] ... [1, 3, 4] [0, 2] [5] ... _]
 *    [6, 1, 3, 4, 0, 2, 5]
 * -> [(2, 0), (1, 0), (2, 1), (1, 1), (1, 2), (3, 0), (0, 0)]
 * 
 * eq group:
 *   [2, 1, 2, 1, 1, 3, 0]
 * 
 * f(i, 2^j+1) = (f(i, 2^j), f(i+2^j, 2^j))
 * 
 * E.g. suppose I want to compare f(3, 2) and f(5, 2)
 * f(3, 2) = (f(3, 1), f(4, 1))
 * f(5, 2) = (f(5, 1), f(6, 1))
 * 
 * Suppose I want to compare f(3, 2) and f(4, 2)
 * f(3, 2) = (f(3, 1), f(4, 1))
 * f(4, 2) = (f(4, 1), f(5, 1))
 * 
 * f(i, 2^j+1) = (f(i, 2^j), f(i+2^j, 2^j)) -> (a, b)
 * f(k, 2^j+1) = (f(k, 2^j), f(k+2^j, 2^j)) -> (c, d)
 * 
 * s = "babaac$"
 * f(*, 1):
 * [(2, 0), (1, 0), (2, 1), (1, 1), (1, 2), (3, 0), (0, 0)]
 * 
 * f(*, 2):
 * f(0, 2): f(0, 1) + f(1, 1)
 * 
 * 
 * For each new substring, have 4 parameters:
 * p0, the global sorted position of the first half
 * c0, the eq class of the first half
 * p1, the global sorted position of the second half
 * c1, the eq of the second half
 * 
 * Put these in buckets based on c0
 * Within each bucket sort by c1
*/
class SuffixArray {
public:
    explicit SuffixArray(const std::string& s) : s_(s), n_(s_.size()) {
        buildSortedIndices();
    }

    std::vector<int> get() const {
        return sortedIndices_;
    }

private:
    void buildSortedIndices() {
        // sort f(i, 1) for each i
        vector<vector<int>> indices;

        for (int i = 0; i < n_; ++i) {
            char ch = s_[i];
            indices[ch].push_back(i);
        }
        std::vector<int> result;
        for (auto& v: indices) {
            for (int idx : v) {
                result.push_back(idx);
            }
        }
    }

    std::string s_;
    int n_;

    std::vector<int> sortedIndices_;

};  // class SuffixArray
