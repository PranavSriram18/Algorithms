#pragma once

#include <functional>
#include <utility>
#include <vector>


template<typename T>
class SegmentTree {
public:
    using BinOp = std::function<T(T, T)>;
    
    explicit SegmentTree(const std::vector<T>& data, BinOp binOp) {
        n_ = data.size();
        while (m_ < n_) {
            m_ <<= 1;
        }
        stree_.resize(2 * m_);
        idxToSegment_.resize(m_);
        binOp_ = binOp;
        populateStree(1, data);
        populateIdxToSegment(1);
    }

    // Update data[idx] := newVal
    // Time complexity: O(log n)
    void update(int idx, T newVal) {
        assert(0 <= idx && idx < m_);
        int node = m_ + idx;
        stree_[node] = newVal;
        node = parent(node);
        while(node >= 1) {
            stree_[node] = binOp_(lc(node), rc(node));
            node = parent(node);
        }
    }

    // Get result of evaluating BinOp over data range [left, right] inclusive
    T query(int left, int right) {
        return query(1, left, right);
    }

private:
    T populateStree(int node, const std::vector<T>& data) {
        if (isLeaf(node)) {
            return stree_[node] = data[node-m_];
        }
        return stree_[node] = binOp_(
            populateStree(lc(node), data), populateStree(rc(node), data)
        );
    }

    std::pair<int, int> populateIdxToSegment(int node) {
        if (isLeaf(node)) {
            return {node - m_, node - m_};
        }
        std::pair<int, int> leftInterval = populateIdxToSegment(lc(node));
        std::pair<int, int> rightInterval = populateIdxToSegment(rc(node));
        return idxToSegment_[node] = {leftInterval.first, rightInterval.second};
    }

    // Wrapper for query, taking root of subtree containing query as 
    // additional parameter
    T query(int node, int left, int right) {
        // Base case for leaf nodes
        if (isLeaf(node)) {
            return stree_[node];
        }

        // Recursively forward queries to children
        std::pair<int, int> leftInterval = segment(lc(node));
        if (right <= leftInterval.second) {
            return query(lc(node), left, right);
        }
        std::pair<int, int> rightInterval = segment(rc(node));
        if (left >= rightInterval.first) {
            return query(rc(node), left, right);
        }

        T leftResult = query(lc(node), left, leftInterval.second);
        T rightResult = query(rc(node), rightInterval.first, right);
        return binOp_(leftResult, rightResult);
    }

    // Helpers

    std::pair<int, int> segment(int node) {
        if (isLeaf(node)) {
            return {node - m_, node - m_};
        }
        return idxToSegment_[node];
    }

    int lc(int node) {
        return 2 * node;
    }

    int rc(int node) {
        return 2 * node + 1;
    }

    int parent(int node) {
        return node / 2;
    }

    bool isLeaf(int node) {
        return node >= m_;
    }

    // Private members

    int n_;  // number of entries in input data
    int m_ = 1;  // smallest power of 2 geq n_. number of leaves in segment tree

    // array representing the segment tree
    // root is stored in index 1; total of 2*m_-1 nodes
    std::vector<T> stree_;

    // Mapping indices in stree_ to corresponding segments of data
    // Length is m_ as we don't explicitly store segments for leaves
    std::vector<std::pair<int, int>> idxToSegment_;

    BinOp binOp_;

};  // class SegmentTree
