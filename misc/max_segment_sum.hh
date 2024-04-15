#pragma once

#include "../utils/counter.hh"
#include <map>
#include <set>
#include <vector>

/**
 * Problem link: 
 * https://leetcode.com/problems/maximum-segment-sum-after-removals/description/
 * 
 * Level: Leetcode Hard
 * 
 * Description:
 * You are given two 0-indexed integer arrays nums and removeQueries, both of 
 * length n. For the ith query, the element in nums at the index 
 * removeQueries[i] is removed, splitting nums into different segments.
 * A segment is a contiguous sequence of positive integers in nums. A segment 
 * sum is the sum of every element in a segment.
 * Return an integer array answer, of length n, where answer[i] is the maximum
 * segment sum after applying the ith removal.
 * 
 * Basic idea:
 * Store sorted list of segments (std::set)
 * For each query:
 *  find the relevant segment
 *  remove the segment from the set
 *  split the segment into 0-2 new pieces that get added back to the set
 * 
 * We also need to keep track of the sums of the segments
 * Use a 2nd Counter for storing the multiset of segment sums
*/
class MaxSegmentSum {
public:
    std::vector<long long> maximumSegmentSum(
        std::vector<int>& nums, std::vector<int>& removeQueries) {
        n_ = nums.size();
        nums_ = nums;
        queries_ = removeQueries;
        result_.reserve(n_);
        intervals_.insert({0, n_-1});
        buildPrefixSums();
        counter_.increment(pfx_.back());
        for (int q : queries_) {
            processQuery(q);
        }
        return result_;
    }

private:
    // represents the inclusive range [left, right]
    struct Interval {
        int left;
        int right;
        Interval(int l, int r) : left(l), right(r) {}

        bool operator<(const Interval& other) const {
            return right < other.left;
        }

        operator bool() const {
            return right >= left;
        }
    };  // struct Interval

    void buildPrefixSums() {
        pfx_.resize(n_+1);
        for (int i = 1; i <= n_; ++i) {
            pfx_[i] = pfx_[i-1] + nums_[i-1];
        }
    }

    void processQuery(int q) {
        // Find relevant segment (it's guaranteed to exist) and build the 
        // resulting new segments
        auto it = intervals_.lower_bound({q, q});
        Interval leftInterval(it->left, q-1);
        Interval rightInterval(q+1, it->right);

        // Update intervals_ and counter_
        counter_.decrement(segmentSum(*it));
        intervals_.erase(it);
        if (leftInterval) {
            intervals_.insert(leftInterval);
            counter_.increment(segmentSum(leftInterval));
        }
        if (rightInterval) {
            intervals_.insert(rightInterval);
            counter_.increment(segmentSum(rightInterval));
        }

        // Update result
        result_.push_back(counter_.firstKey());
    }

    inline long long segmentSum(const Interval& interval) {
        return pfx_[interval.right+1] - pfx_[interval.left];
    }

    int n_;  // number of data elements and number of queries
    std::vector<int> nums_;  // data array
    std::vector<int> queries_;  // queries
    std::vector<long long> pfx_;  // pfx_[i] = sum(nums[0...(i-1)])
    std::set<Interval> intervals_;  // current set of segments
    // For tracking sums of segments. Note we store keys in desc order
    Counter<long long, int, std::greater<long long>> counter_;
    std::vector<long long> result_;  // the results of the n_ queries
};
