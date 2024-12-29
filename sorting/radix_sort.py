from functools import reduce
from typing import List 

ALPHABET_SZ = 256

def radix_sort(arr: List[str]) -> List[str]:
    return radix_sort_wrapper(arr, 0)

def radix_sort_wrapper(arr: List[str], pos: int) -> List[str]:
    # base case
    if len(arr) <= 1:
        return arr 
    
    # build buckets based on each string's char at pos
    buckets = [[] for _ in range(ALPHABET_SZ+1)]
    for s in arr:
        idx = ord(s[pos]) + 1 if pos < len(s) else 0
        buckets[idx].append(s)

    # recursively sort each bucket other than empty
    for i in range(1, ALPHABET_SZ+1):
        buckets[i] = radix_sort_wrapper(buckets[i], pos+1)

    # concat the buckets
    return reduce(lambda x, y: x+y, buckets)

def radix_sort_iterative(arr: List[str]) -> List[str]:
    if not arr:
        return arr
    max_len = max(len(s) for s in arr)
    for i in range(max_len-1, -1, -1):
        buckets = [[] for _ in range(ALPHABET_SZ+1)]
        for s in arr:
            bucket = 1 + ord(s[i]) if i < len(s) else 0
            buckets[bucket].append(s)
        arr = reduce(lambda x, y: x+y, buckets)
    return arr

def radix_sort_int32(arr: List[int]) -> List[int]:
    if not arr:
        return arr
    # in ith round, consider ith bit starting from right (lsb)
    for i in range(32):
        buckets = [[], []]
        for val in arr:
            bucket = ((val & (1 << i)) >> i)
            buckets[bucket].append(val)
        arr = buckets[0] + buckets[1]
    return arr

def test():
    strs = ["elephant", "cat", "dog", "fox", "dog", "eagle", "aardvark", "", "hen", "", "cat"]
    print(radix_sort(strs))
    print(radix_sort_iterative(strs))
    vals = [7, 2, 1, 889, 38]
    print(radix_sort_int32(vals))

if __name__=="__main__":
    test()
