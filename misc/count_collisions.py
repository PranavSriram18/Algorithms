from collections import deque 

"""
Problem Description: https://leetcode.com/problems/count-collisions-on-a-road/
Level: LC Medium 

Basic idea:
Maintain a queue of positions to process. Apply the following conversions to the
sequence of directions in place:

RL -> SS (score +2)
RS -> SS (score +1)
SL -> SS (score +1)
"""
class Solution:
    def countCollisions(self, directions: str) -> int:
        dirs = [ch for ch in directions]
        n = len(dirs)
        
        is_collision = lambda j: directions[j:j+2] in ("RL", "RS", "SL")
        q = deque(filter(is_collision, range(n-1)))
        score = 0
        while q:
            idx = q.popleft()
            d0, d1 = dirs[idx], dirs[idx+1]
            score += (1 if (d0 == "S" or d1 == "S") else 2)
            
            if idx and dirs[idx-1] == "R" and dirs[idx] != "S":
                q.append(idx-1)  # created an RS

            if idx+2 <= n-1 and dirs[idx+1] != "S" and dirs[idx+2] == "L":
                q.append(idx+1)  # created an SL

            dirs[idx] = "S"
            dirs[idx+1] = "S"
        return score
            