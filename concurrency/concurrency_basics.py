from concurrent.futures import ProcessPoolExecutor
#import numpy as np
from functools import reduce
import itertools
from itertools import accumulate
import random
import time
from time import perf_counter
from typing import List, Tuple


class DistributedAlgs:
    def __init__(self, num_workers: int):
        self.max_workers = num_workers

    def max(self, data: List[float]) -> float:
        chunks = self.chunk(data)
        with ProcessPoolExecutor() as pool:
            partial_max = list(pool.map(DistributedAlgs.segment_max, chunks))
        return max(partial_max)
    
    def find_all_k(self, data: List[int], k: int) -> List[int]:
        """
        Find indices of positions of all occurrences of k in data.
        """
        chunks = self.chunk(data)
        chunk_lens = [len(chunk) for chunk in chunks]
        offsets = [0] + list(accumulate(chunk_lens))
        offsets = offsets[0:-1]
        args = list(zip(chunks, itertools.repeat(k), offsets))
        with ProcessPoolExecutor() as pool:
            partial_lists = list(pool.map(DistributedAlgs.segment_find, args))
        return reduce(lambda x, y: x+y, partial_lists)

    @staticmethod
    def segment_max(chunk: List[float]) -> float:
        return max(chunk)
    
    @staticmethod
    def segment_find(chunk_k_offset: Tuple[List[int], int, int]) -> List[int]:
        chunk, k, offset = chunk_k_offset
        return [i+offset for i, x in enumerate(chunk) if x == k]
    
    def chunk(self, data: List[float]) -> List[List[float]]:
        """
        Chunking algorithm. There are 3 implementation subtleties to note:
        1. workers needs to be capped at length of data
        2. loop for chunk starts has length workers+1, to include "start" of chunk
        past the last chunk
        3. loop for actual chunking is back to just range(workers)
        """
        n = len(data)
        workers = min(self.max_workers, n)
        chunk_sz = n // workers
        rem = n % workers
        cs = [i * chunk_sz + min(i, rem) for i in range(workers+1)]
        return [data[cs[i]: cs[i+1]] for i in range(workers)]

def naive_max(data: List[float]):
    if not data:
        return 0
    ret = data[0]
    for i in range(1, len(data)):
        ret = max(ret, data[i])
    return ret

def naive_find_all_k(data: List[int], k: int) -> List[int]:
    """
    Find indices of all occurrences of k in the given list.
    """
    ret = []
    for i in range(len(data)):
        if data[i] == k:
            ret.append(i)
    return ret

def generate_ints(size: int) -> List[int]:
    f = lambda n: (((n**3) % 11079) - 2*n*n + 1444*n - 6) % 331371
    data = [f(i) for i in range(size)]
    return data

def generate_floats(size: int) -> List[float]:
    return [x * 1. for x in generate_ints(size)]

def test_max(size: int, num_workers: int):
    print(f"Running test with {size=}, {num_workers=}")
    solver = DistributedAlgs(num_workers)
    data = generate_floats(size)

    # baseline
    start = perf_counter()
    base_result = naive_max(data)
    end = perf_counter()
    base_time = end - start
    
    start = perf_counter()
    result = solver.max(data)
    end = perf_counter()
    dist_time = end - start

    ratio = dist_time / base_time

    print(f"{base_result=}")
    print(f"{result=}")
    print(f"{base_time=}")
    print(f"{dist_time=}")
    print(f"{ratio=}")
    
def test_find(size: int, num_workers: int, k: int):
    print(f"Running test_find with {size=} and {num_workers=}")
    data = generate_ints(size)
    solver = DistributedAlgs(num_workers)

    # baseline
    start = perf_counter()
    base_result = naive_find_all_k(data, k)
    end = perf_counter()
    base_time = end - start 

    # distributed
    start = perf_counter()
    dist_result = solver.find_all_k(data, k)
    end = perf_counter()
    dist_time = end - start

    ratio = dist_time / base_time

    print(f"{base_result=}")
    print(f"{dist_result=}")
    print(f"{base_time=}")
    print(f"{dist_time=}")
    print(f"{ratio=}")

if __name__=="__main__":
    # test_max(100_000, 8)
    # test_max(1_000_000, 8)
    # test_max(10_000_000, 8)
    # test_max(100_000_000, 8)

    test_find(100000, 8, 17)
    test_find(1_000_000, 8, 17)
    test_find(10_000_000, 8, 17)
