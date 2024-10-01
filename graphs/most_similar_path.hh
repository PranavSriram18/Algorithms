

/*
Problem Source: 
https://leetcode.com/problems/the-most-similar-path-in-a-graph/description/?envType=problem-list-v2&envId=graph&difficulty=HARD

Level: LC Hard

Basic idea: dynamic programming. 
Let f(i, node) denote best score starting at node in step i.
Core recurrence is:
f(i, u) = (u in target[i]) + max_{v in N(u)} f(i+1, v)
*/
class Solution {
public:
    vector<int> mostSimilar(
        int n, vector<vector<int>>& roads, vector<string>& names, vector<string>& targetPath) {
            n_ = n;
            l_ = targetPath.size();
            buildNameToId(names);
            buildGraph(roads);
            buildTarget(targetPath);
            buildCache();
            return bestPath();
    }

    void buildNameToId(vector<string>& names) {
        for (int i = 0; i < names.size(); ++i) {
            nameToId_[names[i]].push_back(i);
        }
    }

    void buildGraph(vector<vector<int>>& roads) {
        graph_.resize(n_);
        for (auto& edge : roads) {
            int u = edge[0];
            int v = edge[1];
            graph_[u].push_back(v);
            graph_[v].push_back(u);
        }
    }

    void buildTarget(vector<string>& targetPath) {
        target_.resize(l_);
        for (int i = 0; i < l_; ++i) {
            string& name = targetPath[i];
            if (nameToId_.count(name)) {
                target_[i] = {nameToId_[name].begin(), nameToId_[name].end()};
            }
        }
    }

    void buildCache() {
        cache_ = vector<vector<pair<int, int>>>(
            l_, vector<pair<int, int>>(n_)
        );

        // handle last row of table separately
        for (int u = 0; u < n_; ++u) {
            cache_[l_-1][u] = {(target_[l_-1].count(u)), -1};
        }

        for (int i = l_-2; i >= 0; --i) {
            for (int u = 0; u < n_; ++u) {
                int best = 0, succ = -1;
                for (int v : graph_[u]) {
                    if (cache_[i+1][v].first >= best) {
                        best = cache_[i+1][v].first;
                        succ = v;
                    }
                }
                cache_[i][u] = {target_[i].count(u) + best, succ};
            }
        }
    }

    vector<int> bestPath() {
        // walk through first row of cache
        int best = 0, node = 0;
        for (int u = 0; u < n_; ++u) {
            if (cache_[0][u].first >= best) {
                best = cache_[0][u].first;
                node = u;
            }
        }

        vector<int> result;
        while (result.size() < l_) {
            result.push_back(node);
            node = cache_[result.size() - 1][node].second;
        }
        return result;
    }

private:
    int n_;  // number of nodes
    int l_;  // length of target path

    unordered_map<string, vector<int>> nameToId_;

    // ith entry is list of neighbors of ith node
    vector<vector<int>> graph_;

    // length l_; ith entry is set of possible nodes for ith step in target path
    vector<unordered_set<int>> target_;

    // i, j entry is:
    // best score starting from node j in step i, and successor node
    // cache is l_ x n_
    vector<vector<pair<int, int>>> cache_;
};
