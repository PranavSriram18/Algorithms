#pragma once

/*

Problem Link: 
https://leetcode.com/problems/maximum-balanced-subsequence-sum/

Level: Leetcode Hard

Scratch:

x0, x1, x2, ..., x_{n-1}

Let f(k) be the max sum of elements with idx >= k, having chosen x_k
Let f(k) be the max sum of elements with idx >= k, having NOT chosen x_k
max(f(0), g(0)) is the value I seek



f(k) = x_k + max_{j satisfies balance} (f(j))

Let n(k) be next index after k that is balanced
f(k) = x_k + max (f(n(k)), g(n(k)))
g(k) = max(g(k+1), f(k+1))
*/

class Solution {

public:
    long long maxBalancedSubsequenceSum(vector<int>& nums) {
        n_ = nums.size();
        nums_ = nums;
        // Handle all-negative edge case
        if (all_of(
            nums.begin(),
            nums.end(),
            [](int x) { return x <= 0; }
        )) {
            return *max_element(nums.begin(), nums.end());
        }
        buildSegmentTree();
        buildTables();
        return max(f_[0], g_[0]);
    }

private:
    void buildTables() {
        f_.resize(n_);
        g_.resize(n_);
        f_[n_-1] = nums[n_-1];
        g_[n_-1] = 0;

        for (int i = n_-2; i >= 0; --i) {
            f_[i] = nums[i] + max(f_[next(i)], g_[next(i)]);
            g_[i] = max(g_[i+1], f_[i+1]);
        }
        return;
    }

    buildSegmentTree() {
        // TODO - complete
        vector<int> modifiedNums = nums_;
        for (int i = 0; i < n_; ++i) {
            modifiedNums[i] -= i;
        }
        stree_ = SegmentTree(modifiedNums);
    }

    int next(int i) {
        return stree_.next(i);
    }

    int n_;
    vector<int> nums_;
    vector<int64_t> f_;
    vector<int64_t> g_;
    SegmentTree stree_;
};
