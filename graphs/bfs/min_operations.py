from typing import List
import collections 

class Solution:
    def minimumOperations(self, nums: List[int], start: int, goal: int) -> int:
        self.nums = nums
        self.start = start
        
        q = collections.deque()
        q.append((goal, 0))
        seen_set = {goal}
        while (len(q)):
            val, level = q.popleft()
            for succ in self.successors(val):
                if succ == start:
                    return level+1
                if succ in seen_set:
                    continue
                seen_set.add(succ)
                q.append((succ, level+1))
        return -1

    def successors(self, val):
        result = []
        for num in self.nums:
            curr = [val + num, val - num, val ^ num]
            for x in curr:
                if (0 <= x and x <= 1000) or x == self.start:
                    result.append(x)
        return result
