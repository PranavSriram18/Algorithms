from itertools import combinations, permutations
from typing import List, Tuple

"""
The classic N-Queens problem.

Solution - brute force generate all permutations and check each one.
Note that for checking validity we only need to check pairwise diagonal attacks.
"""
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        return [self.to_strs(perm) for perm in filter(self.is_valid, permutations(range(n)))]

    def is_valid(self, perm: tuple) -> bool:
        def diag_attack(pos0: Tuple[int, int], pos1: Tuple[int, int]) -> bool:
            return abs(pos0[0] - pos1[0]) == abs(pos0[1] - pos1[1])
        return not any(diag_attack(*x) for x in combinations(enumerate(perm), 2))

    def to_strs(self, perm: tuple) -> List[str]:
        return ["." * col + "Q" + (len(perm) - 1 - col) * "." for col in perm]
    