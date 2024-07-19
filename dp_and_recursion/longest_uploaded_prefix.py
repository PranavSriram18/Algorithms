""" 
Problem source: https://leetcode.com/problems/longest-uploaded-prefix/
Basic idea: the longest uploaded prefix only changes when (lup+1) is uploaded
Trigger lazy update (scan) of lup on this event
O(n) overall time complexity because lup monotonically increases from 0 to n
Note the padding at the beginning of self.uploaded to cleanly handle 1-indexing,
and the padding at the end so that we don't access out of bounds in the while 
loop conditional
"""
class LUPrefix:
    def __init__(self, n: int):
        self.uploaded = [True] + [False for _ in range(n+1)]
        self.lup = 0

    def upload(self, video: int) -> None:
        self.uploaded[video] = True
        if video == self.lup + 1:
            while self.uploaded[self.lup+1]:
                self.lup += 1
        
    def longest(self) -> int:
        return self.lup
        

# Your LUPrefix object will be instantiated and called as such:
# obj = LUPrefix(n)
# obj.upload(video)
# param_2 = obj.longest()