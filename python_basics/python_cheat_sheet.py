import bisect
import heapq

def some_function(x):
    return x * x - 6 * x + 1


## LISTS (TODO)

## MAPS (TODO)

## TOP-K

# Top k elements
def top_k(nums, k):
    return heapq.nlargest(k, nums)

# Bottom k elements
def bottom_k(nums, k):
    return heapq.nsmallest(k, nums)

# With custom key function
def top_k_custom(nums, k):
    return heapq.nlargest(k, nums, key=lambda x: some_function(x))

# For dictionaries
def top_k(my_dict, k):
    return heapq.nlargest(k, my_dict.items(), key=lambda x: x[1])

# kth smallest
def kth_smallest(nums, k):
    return heapq.nsmallest(k, nums)[-1]

# kth largest
def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]

# With custom key function
def kth_smallest_custom(nums, k):
    return heapq.nsmallest(k, nums, key=lambda x: some_function(x))[-1]

## BISECTION

# bisect_left(arr, x): if i is returned then: 
# * arr[0]...arr[i-1] are strictly less than arr[i]
# * arr[i]...arr[-1] are strictly greater than arr[i]

def find_closest(sorted_list, x):
    pos = bisect.bisect_left(sorted_list, x)
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    if after - x < x - before:
        return after
    else:
        return before
    

## BIT OPS
def greatest_power_of_2_le(n):
    return 1 << (n.bit_length() - 1)

def smallest_power_of_2_geq(n):
    return 1 << (n-1).bit_length()

def floor_log2(n):
    return n.bit_length() - 1

