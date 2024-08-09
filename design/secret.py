from collections import Counter
from typing import List

"""
Source: https://leetcode.com/problems/number-of-people-aware-of-a-secret/
Level: LC Medium

Basic idea:
Counter of days since learned -> num people
Buckets - learned but can't share, can share, forgotten
Each time step: learned but can't share -> progress a level
can share -> progress a level, update counter[0]
forget -> drop out
"""
MOD = 1000000007
class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        self.counts = Counter()
        self.delay = delay
        self.forget = forget
        return self.run(n)

    def run(self, n: int) -> int:
        # day 1
        self.counts[0] = 1
        for i in range(2, n+1):
            self.next_day()
        vals = [v for k, v in self.counts.items()]
        return reduce(lambda x, y: (x + y) % MOD, vals)

    def next_day(self):
        c = Counter()
        for time, num_people in self.counts.items():
            if time+1 < self.delay:
                c[time+1] = num_people
            elif time+1 < self.forget:
                c[time+1] = num_people
                c[0] += num_people
        self.counts = c