import bisect
from collections import Counter, defaultdict, deque
import copy
from functools import reduce
import heapq
import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple


def some_function(x):
    return x * x - 6 * x + 1


## LISTS

def count(li, x):
    """Return the number of times x appears in the list."""
    return li.count(x)

def find_all_indices(items: List[Any], target: Any) -> List[int]:
    """Find all indices of a target element in a list."""
    return [i for i, item in enumerate(items) if item == target]

def group_by_condition(items: List[Any], condition: Callable[[Any], bool]) -> tuple:
    """Group items by a condition."""
    return ([item for item in items if condition(item)],
            [item for item in items if not condition(item)])

def zip_lists(*lists: List[Any]) -> List[tuple]:
    """
    Zip multiple lists together to produce a list of tuples. 
    Stops at end of shortest.
    """
    return list(zip(*lists))

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into chunks of a specified size."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def list_to_dict(keys: List[Any], values: List[Any]) -> dict:
    """Convert two lists into a dictionary."""
    return dict(zip(keys, values))

## MAPS (TODO)
def key_to_list():
    d = defaultdict(list)
    d['key'].append(1)  # No KeyError, creates empty list if 'key' doesn't exist

def merge_dicts():
    d1, d2, d3 = {'a': 1}, {'b': 2}, {'c': 3}

    # Python 3.9+
    merged = d1 | d2 | d3

    # Earlier versions
    # merged = {**d1, **d2, **d3}
    return merged

def merge_all(dict_list: List[dict]) -> dict:
    return reduce(lambda d0, d1: d0 | d1, dict_list)

## TOP-K & Heaps


"""
Heap documentation: 

heapq.heapify(list)
Build a heap out of a list

heapq.heappush(heap, item)
Push the value item onto the heap, maintaining the heap invariant.

heapq.heappop(heap)
Pop and return the smallest item from the heap, maintaining the heap invariant. 
If the heap is empty, IndexError is raised. To access the smallest item without 
popping it, use heap[0].

heapq.heappushpop(heap, item)
Push item on the heap, then pop and return the smallest item from the heap. The combined action runs more efficiently than heappush() followed by a separate call to heappop().

heapq.heapify(x)
Transform list x into a heap, in-place, in linear time.

heapq.heapreplace(heap, item)
"""

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
"""
bisect_left(arr, x): if i is returned then: 
* arr[0]...arr[i-1] are strictly less than x
* arr[i]...arr[-1] are geq than arr[i]
bisect_left is thus the first possible insertion point
meanwhile, for bisect_right, if i is returned, then arr[i] > x (or, i == len(arr))
i is the first entry for which the value exceeds x
it represents the last possible insertion point for x
"""

def find_closest(sorted_list, x):
    pos = bisect.bisect_left(sorted_list, x)
    if pos == 0:
        return sorted_list[0]
    if pos == len(sorted_list):
        return sorted_list[-1]
    before = sorted_list[pos - 1]
    after = sorted_list[pos]
    return after if after - x < x - before else before
    

## BIT OPS
def greatest_power_of_2_le(n):
    return 1 << (n.bit_length() - 1)

def smallest_power_of_2_geq(n):
    return 1 << (n-1).bit_length()

def floor_log2(n):
    return n.bit_length() - 1

## GENERATOR EXPRESSIONS

def has_any_even(numbers):
    """Check if any element is even."""
    return any(num % 2 == 0 for num in numbers)

def are_all_positive(numbers):
    """Check if all elements are positive."""
    return all(num > 0 for num in numbers)

def sum_of_evens(numbers):
    """Sum all even numbers."""
    return sum(num for num in numbers if num % 2 == 0)

def find_longest_word(words):
    """Find the longest word."""
    return max(words, key=lambda w: len(w))

def find_shortest_word(words):
    """Find the shortest word."""
    return min(words, key=len)

def create_squared_numbers(numbers):
    """Create a list of squared numbers."""
    return list(num ** 2 for num in numbers)

def get_unique_word_lengths(words):
    """Get a set of unique word lengths."""
    return set(len(word) for word in words)

def create_word_length_dict(words):
    """Create a dictionary of words and their lengths."""
    return dict((word, len(word)) for word in words)

def count_even_numbers(numbers):
    """Count the number of even numbers."""
    return sum(1 for num in numbers if num % 2 == 0)

def get_odd_squares(numbers):
    """Get squares of odd numbers."""
    return [num ** 2 for num in numbers if num % 2 != 0]

def flatten_nested_lists(nested_lists):
    """Flatten a list of lists."""
    return [item for sublist in nested_lists for item in sublist]

def count_vowels_in_words(words):
    """Count vowels in each word."""
    return [(word, sum(1 for char in word if char.lower() in 'aeiou')) 
            for word in words]


## SEARCH
def find_first_comprehension(items: List[Any], criterion: Callable[[Any], bool]) -> Optional[Any]:
    """
    Find the first element using list comprehension and next().
    """
    return next((item for item in items if criterion(item)), None)

def find_first_filter(items: List[Any], criterion: Callable[[Any], bool]) -> Optional[Any]:
    """
    Find the first element using filter().
    """
    return next(filter(criterion, items), None)


## GROUP BY
def use_groupby(items: List[Any], key_func: Callable[[Any], Any]) -> List[Tuple[Any, List[Any]]]:
    """
    Group items using itertools.groupby.
    
    Args:
    items: List of items to group
    key_func: Function to determine the grouping key
    
    Returns:
    A list of (key, group) pairs

    Example: Grouping numbers by their remainder when divided by 3
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    grouped_numbers = use_groupby(numbers, key_func=lambda x: x % 3)
    print("Grouped numbers:", grouped_numbers)
    """
    # Sort the items first (important!)
    sorted_items = sorted(items, key=key_func)
    # Group the sorted items
    return [(key, list(group)) for key, group in itertools.groupby(sorted_items, key=key_func)]
