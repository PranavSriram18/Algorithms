#pragma once 

#include <set>

/**
 * Problem Link: 
 * https://leetcode.com/problems/count-integers-in-intervals/description/
 * 
 * Level: Leetcode Hard
 * 
 * Problem Description:
 * Given an empty set of intervals, implement a data structure that can:
 * Add an interval to the set of interval
 * Count the number of integers that are present in at least one interval.
*/
class IntervalCounter {

public:
    struct Interval {
        int left;
        int right;
        Interval(int l, int r) : left(l), right(r) {}

        int elems() const {
            return right - left + 1;
        }

        // Intervals I1, I2 satisfy I1 < I2 iff they are disjoint and I1 comes
        // strictly before I2
        bool operator<(const Interval& other) const {
            return right < other.left;
        }
    };  // struct Interval

    /**
     * Adds the interval [left, right].
    */
    void add(int left, int right) {
        Interval interval(left, right);

        // Find leftmost interval that is >= interval. There are 3 cases:
        // 1. No such interval exists
        // 2. *leftIt is strictly to the right of interval
        // 3. *leftIt intersects interval
        auto leftIt = intervals_.lower_bound(interval);

        // Cases 1 and 2 imply nothing intersects interval, so can safely insert
        if (leftIt == intervals_.end() || interval < *leftIt) {
            return insertInterval(interval);
        }

        // Get rightIt, the LAST interval NOT strictly to the right of interval
        auto farRightIt = intervals_.upper_bound(interval);
        auto rightIt = farRightIt;
        --rightIt;

        // Because we're in Case 3, i.e. *leftIt intersects interval, we know
        // that rightIt must as well (it could be that rightIt == leftIt). 
        // Hence, we need to delete everything in [leftIt, farRightIt) and
        // replace with merged(*leftIt, interval, *rightIt)
        Interval merged(
            std::min(leftIt->left, interval.left),
            std::max(rightIt->right, interval.right)
        );
        for (auto it = leftIt; it != farRightIt; ++it) {
            count_ -= it->elems();
        }
        intervals_.erase(leftIt, farRightIt);
        insertInterval(merged);
    }
    
    int count() {
        return count_;
    }

private:
    void insertInterval(Interval interval) {
        intervals_.insert(interval);
        count_ += interval.elems();
    }

    std::set<Interval> intervals_;
    int count_ = 0;  // total covered integers
};  // class IntervalCounter
