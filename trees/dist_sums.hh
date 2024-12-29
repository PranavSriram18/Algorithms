
using namespace std;

/*
Basic idea:
We have the following recurrence relating children and parent nodes:
s(c) = s(p) + n - 2 * t(c),

where:
s() is the quantity we are trying to compute,
c and p are child and parent node respectively,
t(c) is the size of the subtree rooted at c (including c)

To evaluate this recurrence, we:
1. Identify all parents and their children in the tree
2. Recognize the base case s(root) is the sum of node levels
3. Compute t(u) for each node u recursively
4. Evaluate the recurrence by processing nodes in a topological order

The parent-child relationships, level sums, and topological ordering can all
be computed jointly - see computeLevels().
*/
class Solution {

public:
    vector<int> sumOfDistancesInTree(int n, vector<vector<int>>& edges) {
        n_ = n;
        vector<vector<int>> al = buildAdjList(edges);
        computeLevels(al);
        computeSubtreeSizes();
        return computeDistSums();
    }

private:

    void computeSubtreeSizes() {
        st_.resize(n_, 1);
        for (auto it = sorted_nodes_.rbegin(); it != sorted_nodes_.rend(); ++it) {
            for (int c : children_[*it]) {
                st_[*it] += st_[c];
            }
        }
    }

    vector<vector<int>> buildAdjList(vector<vector<int>>& edges) {
        vector<vector<int>> al = vector<vector<int>>(n_);
        for (auto& edge : edges) {
            int u = edge[0], v = edge[1];
            al[u].push_back(v);
            al[v].push_back(u);
        }
        return al;
    }

    void computeLevels(vector<vector<int>>& al) {
        children_.resize(n_);
        parent_.resize(n_, -1);
        vector<bool> seen(n_, 0);  // which nodes have been enqueued already
        deque<pair<int, int>> q;  // (node, level) pairs
        q.emplace_back(0, 0);
        seen[0] = 1;
        while (q.size()) {
            auto [node, level] = q.front();
            q.pop_front();
            sorted_nodes_.push_back(node);
            for (int nbr : al[node]) {
                if (seen[nbr]) continue;
                q.emplace_back(nbr, level+1);
                levelSum_ += (level+1);
                seen[nbr] = 1;
                children_[node].push_back(nbr);
                parent_[nbr] = node;
            }
        }
    }

    vector<int> computeDistSums() {
        vector<int> distSums(n_, 0);
        for (int node : sorted_nodes_) {
            distSums[node] = (
                node ? distSums[parent_[node]] + n_ - 2 * st_[node] : levelSum_);
        }
        return distSums;
    }

    int n_;  // number of nodes
    int levelSum_;  // sum of levels of all nodes
    vector<int> st_;  // st_[i] is size of subtree rooted at i
    vector<vector<int>> children_;  // ith entry is children of node i
    vector<int> parent_;  // ith entry is parent of node i
    vector<int> sorted_nodes_;  // topologically sorted so parents precede children
};
