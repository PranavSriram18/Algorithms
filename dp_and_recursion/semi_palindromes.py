
import functools
import math

"""
Problem description: https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/description/
Level: LC Hard

Basic idea: dynamic programming.
Define f(i, j) to be optimal for s[i:] with j groups. 
Now consider breaking off first chunk till m (inclusive)
f(i, j) = min_{m} g(i, m) + f(m+1, j-1),
where:
g(i, m) is palindrome adj cost of s[i...m]
i+1 <= m <= n-1

Base cases:
f(i, 1) = g(i, n-1)
f(i, j) = inf when 2 * j > (n-i+1)  (implicitly handled)

So, the basic algorithm is:
1. precompute g via brute force
2. compute f using above recurrence, going backwards for i and forwards for j

Part (2) is O(n^3). Not fully sure about Part (1).
"""

class Solution:
    LARGE_VAL = 1000000

    def minimum_changes(self, s: str, k: int) -> int:
        self.k = k
        self.n = len(s)
        self.s = s
        self.build_g_table()
        self.build_f_table()
        return self.f_table[0][k]

    def build_g_table(self):
        """
        self.g_table[i][j] will be the cost of turning s[i:j+1] into a
        semi-palindrome. Brute force.
        """
        n = self.n
        self.g_table = [[Solution.LARGE_VAL for m in range(
            n)] for i in range(n)] # n x n
        for i in range(n):
            for j in range(i+1, n):
                self.g_table[i][j] = self.palindrome_cost(i, j)

    def build_f_table(self):
        n, k = self.n, self.k
        self.f_table = [[Solution.LARGE_VAL for _ in range(
            k+1)] for _ in range(n)]  # n x (k+1)
        # Handle base case: single chunk
        for i in range(n):
            self.f_table[i][1] = self.g_table[i][n-1]
        
        # DP. O(n^3)
        for i in range(n-1, -1, -1):
            for j in range(2, k+1):
                for m in range(i+1, n-1):
                    self.f_table[i][j] = min(
                        self.g_table[i][m] + self.f_table[m+1][j-1],
                        self.f_table[i][j]
                    )
    
    def palindrome_cost(self, i, j):
        """Adjustment cost for s[i...j] inclusive."""
        k = j-i+1
        cost = k  # initialize with a strict upper bound
        for d in self.divisors(k):
            subseqs = ["".join([self.s[pos] for pos in range(
                left, j+1, d
            )]) for left in range(i, i+d)]  # length d
            curr_cost = sum(self.indiv_cost(seq) for seq in subseqs)
            cost = min(cost, curr_cost)
        return cost

    @functools.lru_cache(maxsize=2048)
    def indiv_cost(self, seq):
        l = len(seq)
        mid = (l+1) // 2
        return sum(int(seq[i] != seq[l-1-i]) for i in range(mid))
    
    @functools.lru_cache(maxsize=256)
    def divisors(self, k):
        ret = [1]
        lim = int(math.sqrt(k))
        for i in range(2, lim+1):
            if k % i == 0:
                ret.append(i)
                if i * i != k:
                    ret.append(k // i)
        return ret
    
if __name__=="__main__":
    s = Solution()
    print(s.minimum_changes("abcac", 2))  # expect 1
        