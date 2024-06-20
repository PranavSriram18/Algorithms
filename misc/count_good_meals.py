from collections import Counter
from typing import List

class Solution:
    MOD = 1000000007
    MAX_EXP = 22

    def count_pairs(self, deliciousness: List[int]) -> int:
        self.counter = Counter(deliciousness)
        total = 0
        for val, count in self.counter.items():
            total += count * self.contrib(val)
        # we've counted each pair twice ((a,b) and (b, a))
        return (total // 2 % self.MOD)
    
    def contrib(self, val) -> int:
        result = 0
        for i in range(self.MAX_EXP):
            result += self.counter[2 ** i - val]
        # if val is a power of 2, remove the pair of val with itself
        if self.is_pow_2(val):
            result -= 1
        return result

    def is_pow_2(self, x: int) -> bool:
        return x > 0 and x & (x-1) == 0
    
if __name__=='__main__':
    sol = Solution()
    print(sol.count_pairs([1,1,3,3]))
