#pragma once

#include <vector>


/**
Full problem description: 
https://leetcode.com/problems/maximize-value-of-function-in-a-ball-passing-game/description/

Level: Leetcode Hard

Basic idea: power of 2 iteration. 

Let g(i, node) = where we land after 2^i steps from node
Let s(i, node) = sum from node with 2^i steps, excluding node

Note that we exclude node itself from s to avoid double counting
in the recurrence.

We have the following recurrences for s and g:
    g(i, node) = g(i-1, g(i-1, node))
    s(i, node) = s(i-1, node) + s(i-1, g(i-1, node))

Let f(k, node) denote sum from node with k steps, again excluding node itself.
Let 2^b be the highest power of 2 less than or equal to k.
    f(k, node) = f(k - 2^b, g(b, node))

The final result is max_{node} (node + f(k, node)).
*/
class Solution {
public:
    long long getMaxFunctionValue(std::vector<int>& receiver, long long k) {
        n_ = receiver.size();
        kSigBits_ = sizeof(long long) * CHAR_BIT - __builtin_clzll(k);
        buildJumpTables(receiver);
        return bestScore(k);
    }

private:
    void buildJumpTables(std::vector<int>& receiver) {
        g_ = std::vector<std::vector<int64_t>>(
            kSigBits_+1, std::vector<int64_t>(n_)
        );
        s_ = g_;

        // g(0, node) = s(0, node) = receiver[node]
        for (int node = 0; node < n_; ++node) {
            g_[0][node] = receiver[node];
        }
        s_[0] = g_[0];

        for (int i = 1; i <= kSigBits_; ++i) {
            for (int node = 0; node < n_; ++node) {
                int halfwayNode = g_[i-1][node];
                g_[i][node] = g_[i-1][halfwayNode];
                s_[i][node] = s_[i-1][node] + s_[i-1][halfwayNode];
            }
        }
    }

    long long bestScore(long long k) {
        // get score after k steps for each node
        int64_t best = 0;
        for (int node = 0; node < n_; ++node) {
            best = std::max(best, f(k, node) + node);
        }
        return best;
    }

    // f excludes contribution from node itself
    // f(node, j) = s(b1, node) + f(k - 2^b1, g(b1, node))
    int64_t f(long long j, int node) {
        if (j == 0) return 0;
        int highestPow = sizeof(long long) * CHAR_BIT - __builtin_clzll(j) - 1;
        return s_[highestPow][node] + f(j - (1ll << highestPow), g_[highestPow][node]);
    }

    int n_;  // number of nodes
    int kSigBits_;  // number of significant bits in k  
    
    // (i, node) --> node after 2^i steps
    std::vector<std::vector<int64_t>> g_;

    // (i, node) --> score after 2^i steps
    std::vector<std::vector<int64_t>> s_;
};
