""" 
TODO - fix this
Scratch:
If we fix left endpoint, right endpoint walks until not a mountain
Record best possible, then left jumps to right-1
"""
class Solution:
    def longestMountain(self, arr: List[int]) -> int:
        n = len(arr)
        left, right, best, ascent = 0, 0, 0, True
        while right+1 < n:
            if ascent:
                if arr[right+1] > arr[right]:
                    right += 1
                elif arr[right+1] < arr[right] and right and arr[right] > arr[right-1]:
                    right += 1
                    ascent = False
                else:
                    left, right = right+1, right+2
            else:
                if arr[right+1] < arr[right]:
                    right += 1
                elif arr[right+1] > arr[right]:
                    best = max(best, (right-left+1)) if right-left >= 2 else best
                    left, right, ascent = right, right+1, True
                else:
                    best = max(best, (right-left+1)) if right-left >= 2 else best
                    left, right, ascent = right+1, right+2, True
        best = max(best, (right-left+1)) if right-left >= 2 and not ascent else best
        return best
