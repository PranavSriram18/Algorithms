#pragma once

#include <queue>
#include <utility>
#include <vector>

/**
 * Given an integer array nums. 
 * `nums[i]` indicates the maximum distance you can jump from the ith position.
 * Determine the minimum number of jumps needed to reach the end. 

 * Full Problem Description: https://leetcode.com/problems/jump-game-ii/

 * Basic idea: BFS.
*/
class JumpGame2 {
public:
    int solve(const std::vector<int>& nums) {
        int n = nums.size();
        std::vector<int> visited(n, false);
        std::queue<std::pair<int, int>> q;
        q.push({0, 0});
        visited[0] = true;
        while (q.size()) {
            auto [u, level] = q.front();
            if (u == n - 1) return level;
            q.pop();
            for (int i = u+1; i <= std::min(u+nums[u], n-1); ++i) {
                if (!visited[i]) {
                    q.push({i, level+1});
                    visited[i] = true;
                }
            }
        }
        return -1;
    }
};  // class JumpGame
