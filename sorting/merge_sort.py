from typing import List 

def merge_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    # base case
    if n <= 1:
        return arr
    
    # recursively sort subarrays
    mid = n // 2
    left, right = arr[:mid], arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)

    # merge sorted subarrays
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    left_idx, right_idx = 0, 0
    result = []

    while left_idx < len(left) and right_idx < len(right):
        left_val, right_val = left[left_idx], right[right_idx]
        if left_val <= right_val:
            result.append(left_val)
            left_idx += 1
        else:
            result.append(right_val)
            right_idx += 1
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    return result

def test():
    vals = [3, 5, 1, 2, 7]
    print(merge_sort(vals))
    print(merge_sort([3]))
    print(merge_sort([i * i % 17 for i in range(10)]))

if __name__=="__main__":
    test()
