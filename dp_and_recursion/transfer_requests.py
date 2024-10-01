
import itertools
from typing import List

"""
Problem Source: https://leetcode.com/problems/maximum-number-of-achievable-transfer-requests/description/?envType=problem-list-v2&envId=backtracking&difficulty=HARD
Level: LC Hard
Idea: brute force all combinations.
"""
class Solution:
    def maximumRequests(self, n: int, requests: List[List[int]]) -> int:
        self.n = n 
        self.k = len(requests)
        self.reqs = requests
        return self.run()

    def run(self):
        for i in range(self.k, -1, -1):
            if self.exists_combination(i):
                return i

    def exists_combination(self, i):
        for req_tuple in itertools.combinations(self.reqs, i):
            if self.is_valid(req_tuple):
                return True
        return False
    
    def is_valid(self, req_tuple):
        buffer = [0 for _ in range(self.n)]
        for source, sink in req_tuple:
            buffer[source] -= 1
            buffer[sink] += 1
        return not any(buffer)
        