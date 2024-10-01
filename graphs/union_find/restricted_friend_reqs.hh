#pragma once

#include <numeric>
#include <unordered_set>
#include <vector>

/*
Problem Source: https://leetcode.com/problems/process-restricted-friend-requests/description/?envType=problem-list-v2&envId=graph&difficulty=HARD
Level: LC Hard

Basic idea: consider processing a request (u, v). Essentially, we care about
whether F(cc(u)) has a nonempty intersection with cc(v), where cc(u) is the 
set of nodes in the connected component of u, and F(S) is the set of forbidden
neighbors for a set of nodes S. We can dynamically maintain F for each connected
component by augmenting a UnionFind structure.
*/

class AugmentedUnionFind {
public:
    AugmentedUnionFind() = default;

    AugmentedUnionFind(int n, std::vector<std::vector<int>>& restrictions) {
        n_ = n;
        parent_.resize(n_);
        std::iota(parent_.begin(), parent_.end(), 0);
        ccs_.resize(n_);
        for (int i = 0; i < n; ++i) {
            ccs_[i].insert(i);
        }
        sizes_ = std::vector<int>(n_, 1);
        buildForbidden(restrictions);
    }

    void buildForbidden(std::vector<std::vector<int>>& restrictions) {
        forbidden_.resize(n_);
        for (auto& r : restrictions) {
            int r0 = r[0];
            int r1 = r[1];
            forbidden_[r0].insert(r1);
            forbidden_[r1].insert(r0);
        }
    }

    int repr(int u) {
        int& p = parent_[u];
        return (p == u) ? p : p = repr(p);
    }

    bool addEdge(int u, int v) {
        int u_rep = repr(u);
        int v_rep = repr(v);
        if (u_rep == v_rep) return true;

        auto& u_forbidden = forbidden_[u_rep];
        auto& v_forbidden = forbidden_[v_rep];
        if (intersects(u_forbidden, ccs_[v_rep])) {
            return false;
        }

        int u_sz = sizes_[u_rep];
        int v_sz = sizes_[v_rep];
        int smaller_rep = (u_sz < v_sz) ? u_rep : v_rep;
        int larger_rep = (u_sz < v_sz) ? v_rep : u_rep;

        parent_[smaller_rep] = larger_rep;
        sizes_[larger_rep] += sizes_[smaller_rep];
        forbidden_[larger_rep] = set_union(u_forbidden, v_forbidden);
        ccs_[larger_rep] = set_union(ccs_[larger_rep], ccs_[smaller_rep]);
        return true;
    }

    bool intersects(std::unordered_set<int>& s0, std::unordered_set<int>& s1) {
        std::unordered_set<int>& smaller = (s0.size() < s1.size() ? s0 : s1);
        std::unordered_set<int>& larger = (s0.size() < s1.size() ? s1 : s0);
        for (int x : smaller) {
            if (larger.count(x)) return true;
        }
        return false;
    }

    std::unordered_set<int> set_union(std::unordered_set<int>& s0, std::unordered_set<int>& s1) {
        std::unordered_set<int> result = s0;
        for (int x : s1) {
            result.insert(x);
        }
        return result;
    }

private:
    int n_;
    std::vector<int> parent_;
    std::vector<int> sizes_;
    // ith entry is forbidden set for component of ith node
    std::vector<std::unordered_set<int>> forbidden_;
    // ccs_[u] is set of nodes in component that u is repr of, IF u is a repr
    std::vector<std::unordered_set<int>> ccs_;
};

class Solution {
public:
    std::vector<bool> friendRequests(int n, std::vector<std::vector<int>>& restrictions, std::vector<std::vector<int>>& requests) {
        auf_ = AugmentedUnionFind(n, restrictions);
        int q = requests.size();
        std::vector<bool> result(q);
        for (int i = 0; i < q; ++i) {
            result[i] = auf_.addEdge(requests[i][0], requests[i][1]);
        }
        return result;
    }

private:
    AugmentedUnionFind auf_;
};
