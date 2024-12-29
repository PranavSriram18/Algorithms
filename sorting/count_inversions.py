from typing import List, Tuple

def count_inversions(arr: List[int]) -> int:
    return count_inversions_wrapper(arr)[1]

def count_inversions_wrapper(arr: List[int]) -> Tuple[List[int], int]:
    """
    Returns sorted(arr), num_inversions(arr)
    """
    # base case
    n = len(arr)
    if n <= 1:
        return arr, 0
    
    mid = n // 2
    left, right = arr[0:mid], arr[mid:]
    left, left_inversions = count_inversions_wrapper(left)
    right, right_inversions = count_inversions_wrapper(right)
    arr, num_crossing = count_merge(left, right)
    return arr, left_inversions + right_inversions + num_crossing

def count_merge(left: List[int], right: List[int]) -> int:
    """
    Merge sorts the lists and counts the number of inversions
    """
    left_idx, right_idx = 0, 0
    ret = []
    inversions = 0
    while left_idx < len(left) and right_idx < len(right):
        left_val, right_val = left[left_idx], right[right_idx]
        if left_val <= right_val:
            ret.append(left_val)
            left_idx += 1
            # this val participates as the small entry in right_idx inversions
            inversions += right_idx
        else:
            ret.append(right_val)
            right_idx += 1
    
    # each remaining left val is smaller entry in len(right) inversions
    inversions += len(right) * (len(left) - left_idx)
    
    ret.extend(left[left_idx:])
    ret.extend(right[right_idx:])
    return ret, inversions 

def test():
    arr = [1, 3, 4, 2, 6, 5]
    print(count_inversions(arr))
    arr = [1]

if __name__=="__main__":
    test()


