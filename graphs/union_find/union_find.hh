#pragma once

#include <vector>

class UnionFind {
public:
    UnionFind(int n) {
        parents_.resize(n);
        sizes_.resize(n);
        for (int i = 0; i < n; ++i) {
            parents_[i] = i;
            sizes_[i] = 1;
        }
    }
    
    int repr(int u) {
        int& parent = parents_[u];
        return (parent == u) ? u : parent = repr(parent);    
    }
    
    void addEdge(int u, int v) {
        int uRep = repr(u);
        int vRep = repr(v);
        if (uRep == vRep) return;
        int& uSize = sizes_[uRep];
        int& vSize = sizes_[vRep];
        if (uSize < vSize) {
            parents_[uRep] = vRep;
            vSize += uSize; 
        } else {
            parents_[vRep] = uRep;
            uSize += vSize;
        }
    }
    
    std::vector<int> componentSizes() {
        std::vector<int> result;
        for (int node = 0; node < parents_.size(); ++node) {
            if (parents_[node] == node) {
                result.push_back(sizes_[node]);
            }
        }
        return result;
    }
    
private:
    std::vector<int> parents_;
    std::vector<int> sizes_;
};  // class UnionFind
