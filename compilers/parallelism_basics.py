from functools import partial
import multiprocessing as mp
from multiprocessing import Value, Array
import numpy as np
import time
from typing import List, Tuple

class MPProcessor:
    @staticmethod
    def process_chunk(chunk: np.ndarray, sq_threshold: float) -> int:
        return sum(1 for x in chunk if x > 0 and x*x > sq_threshold)
    
    def process(self, data: np.ndarray, sq_threshold: float, num_processes: int):
        # Split data into chunks
        chunks = np.array_split(data, num_processes)
        
        # Create pool and map chunks to processes
        with mp.Pool(num_processes) as pool:
            worker = partial(self.process_chunk, sq_threshold=sq_threshold)
            results = pool.map(worker, chunks)
        
        return sum(results)


class DataProcessor:
    def __init__(self, num_workers: int):
        # Shared counters for statistics
        self.total_processed = Value('i', 0)
        self.num_large_values = Value('i', 0)
        
        # Shared array for running statistics
        self.chunk_maxes = Array('d', num_workers)
        
        # Shared flag for early stopping
        self.should_stop = Value('b', False)  # boolean
    
    @staticmethod
    def process_chunk(chunk: np.ndarray, 
                     worker_id: int,
                     threshold: float,
                     total_processed: Value,
                     num_large: Value,
                     chunk_maxes: Array,
                     should_stop: Value) -> Tuple[int, float]:
        """Process a data chunk and update shared statistics"""
        
        # Check if we should stop
        if should_stop.value:
            return 0, 0.0
            
        # Process data
        chunk_max = float(np.max(chunk))
        large_values = sum(1 for x in chunk if x > threshold)
        
        # Update shared statistics atomically
        with total_processed.get_lock():
            total_processed.value += len(chunk)
            
        with num_large.get_lock():
            num_large.value += large_values
            
        # Update this worker's max value
        chunk_maxes[worker_id] = chunk_max
        
        # Check if we should trigger early stopping
        if chunk_max > threshold * 2:
            should_stop.value = True
            
        return large_values, chunk_max
    
    def process_data(self, 
                    data: np.ndarray, 
                    threshold: float,
                    chunk_size: int) -> dict:
        """Process data in parallel with multiple workers"""
        
        # Split data into chunks
        chunks = [
            data[i:i + chunk_size] 
            for i in range(0, len(data), chunk_size)
        ]
        
        start_time = time.time()
        
        # Process chunks using pool
        with mp.Pool(processes=len(self.chunk_maxes)) as pool:
            # Create worker function with shared state
            worker = partial(
                self.process_chunk,
                threshold=threshold,
                total_processed=self.total_processed,
                num_large=self.num_large_values,
                chunk_maxes=self.chunk_maxes,
                should_stop=self.should_stop
            )
            
            # Process chunks asynchronously
            async_results = []
            for i, chunk in enumerate(chunks):
                r = pool.apply_async(worker, (chunk, i))
                async_results.append(r)
            
            # Monitor and collect results
            results: List[Tuple[int, float]] = []
            max_so_far = float('-inf')
            
            for r in async_results:
                large_count, chunk_max = r.get()
                results.append((large_count, chunk_max))
                max_so_far = max(max_so_far, chunk_max)
                
                # Print progress periodically
                if len(results) % 10 == 0:
                    print(f"Processed {self.total_processed.value:,} items, "
                          f"found {self.num_large_values.value:,} large values")
        
        end_time = time.time()
        
        # Collect and return statistics
        return {
            'total_processed': self.total_processed.value,
            'num_large_values': self.num_large_values.value,
            'max_value': max(self.chunk_maxes),
            'processing_time': end_time - start_time,
            'early_stopped': self.should_stop.value
        }
    
if __name__ == "__main__":
    processor = MPProcessor()
    num_processes = 10
    num_elems = 1000000
    data = np.random.randn(num_elems)

    for sq_threshold in range(0, 11):
        print(f"\nPercentage of elems > sqrt({sq_threshold}): {100. * processor.process(
            data, 1.0 * sq_threshold, num_processes)/num_elems}")
