#pragma once

#include <cassert>
#include <functional>
#include <utility>
#include <vector>

/**
 * Implements a segment tree.
 * https://cp-algorithms.com/data_structures/segment_tree.html
 * \tparam T the datatype of elements of the underlying data array.
*/
template<typename T>
class SegmentTree {
public:
    using BinOp = std::function<T(T, T)>;
    // Represents an inclusive [left, right] interval of the data array
    using Interval = std::pair<int, int>; 
    
    /**
     * Constructor.
     * \param data The underlying data array whose segments the SegmentTree
     * represents
     * \param binOp The associative binary operation clients will query on
     * intervals of the data array.
    */
    explicit SegmentTree(const std::vector<T>& data, BinOp binOp) {
        n_ = data.size();
        while (m_ < n_) {
            m_ <<= 1;
        }
        data_ = data;
        data_.resize(m_);
        stree_.resize(2 * m_);
        idxToSegment_.resize(m_);
        binOp_ = binOp;
        populateStree(1);
        populateIdxToSegment(1);
    }

    // Update data_[idx] := newVal
    // Time complexity: O(log n)
    void update(int idx, T newVal) {
        assert(0 <= idx && idx < m_);
        int node = m_ + idx;
        stree_[node] = newVal;
        node = parent(node);
        while(node >= 1) {
            stree_[node] = binOp_(stree_[lc(node)], stree_[rc(node)]);
            node = parent(node);
        }
    }

    // Get result of evaluating BinOp over data range [left, right] inclusive
    T query(int left, int right) {
        return query(1, left, right);
    }

private:
    T populateStree(int node) {
        if (isLeaf(node)) {
            return stree_[node] = data_[node-m_];
        }
        return stree_[node] = binOp_(
            populateStree(lc(node)), populateStree(rc(node))
        );
    }

    Interval populateIdxToSegment(int node) {
        if (isLeaf(node)) {
            return {node - m_, node - m_};
        }
        auto [leftLeft, leftRight] = populateIdxToSegment(lc(node));
        auto [rightLeft, rightRight] = populateIdxToSegment(rc(node));
        return idxToSegment_[node] = {leftLeft, rightRight};
    }

    // Wrapper for query, taking root of subtree containing query as 
    // additional parameter
    T query(int node, int qLeft, int qRight) {
        auto [leftLeft, rightRight] = segment(node);
        // Terminate recursion on perfect overlap
        if (qLeft == leftLeft && qRight == rightRight) {
            return stree_[node];
        }

        // 3 other cases: query contained in left subtree, 
        // query contained in right subtree, and query overlaps both subtrees
        auto [_leftLeft, leftRight] = segment(lc(node));
        auto [rightLeft, _rightRight] = segment(rc(node));
        if (qRight <= leftRight) {
            return query(lc(node), qLeft, qRight);
        } else if (qLeft >= rightLeft) {
            return query(rc(node), qLeft, qRight);
        } 
        T leftResult = query(lc(node), qLeft, leftRight);
        T rightResult = query(rc(node), rightLeft, qRight);
        return binOp_(leftResult, rightResult);
    }

    // Helpers
    Interval segment(int node) {
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
    int m_ = 1;  // smallest power of 2 geq n_. Number of leaves in segment tree

    std::vector<T> data_;  // copy of input data, padded to length m_

    // array of length 2 * m_ representing the segment tree
    // root is stored in index 1, and ordering is based on level-order traversal
    // first m_-1 nodes are non-leaves, last m_ are leaves. Total 2*m_-1 nodes
    std::vector<T> stree_;

    // Mapping indices in stree_ to corresponding segments of data
    // idxToSegment_[i] returns the left and right endpoints (inclusive) of the
    // segment represented by node i
    // Length is m_ as we don't explicitly store segments for leaves
    std::vector<Interval> idxToSegment_;

    // The client-specified binary reduction operation for queries
    BinOp binOp_;

};  // class SegmentTree
