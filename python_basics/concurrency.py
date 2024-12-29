from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import multiprocessing as mp
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
from queue import Queue
from threading import Thread, Lock, Event
import threading
import time
import numpy as np
from typing import List, Dict, Any
import logging
import requests

#######################
# Threading Patterns  #
#######################

def threading_patterns():
    """
    Threading is best for IO-bound tasks:
    - Network operations
    - File operations
    - User interface
    Does not help with CPU-bound tasks due to GIL
    """
    
    # Basic thread creation
    def worker(name: str):
        print(f"Thread {name} starting")
        time.sleep(1)
        print(f"Thread {name} finished")
    
    thread = Thread(target=worker, args=("Worker 1",))
    thread.start()
    thread.join()
    
    # Thread pool for multiple tasks
    def fetch_url(url: str) -> str:
        return requests.get(url).text
    
    urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net"
    ]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Map pattern
        results = executor.map(fetch_url, urls)
        
        # Submit pattern with as_completed
        future_to_url = {executor.submit(fetch_url, url): url 
                        for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                print(f"{url}: {len(data)} bytes")
            except Exception as e:
                print(f"{url}: {str(e)}")
    
    # Thread synchronization
    lock = Lock()
    shared_resource = []
    
    def synchronized_worker():
        with lock:
            shared_resource.append(1)
            time.sleep(0.1)
    
    threads = [Thread(target=synchronized_worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Event for signaling between threads
    event = Event()
    
    def waiter():
        print("Waiter: Waiting for event")
        event.wait()
        print("Waiter: Event received")
    
    def signaler():
        time.sleep(1)
        print("Signaler: Sending event")
        event.set()
    
    Thread(target=waiter).start()
    Thread(target=signaler).start()

#########################
# Multiprocessing       #
#########################

def multiprocessing_patterns():
    """
    Multiprocessing is best for CPU-bound tasks:
    - Data processing
    - Number crunching
    - Parallel algorithms
    Bypasses GIL but has higher overhead
    """
    
    # Basic process creation
    def worker(name: str):
        print(f"Process {name} starting")
        time.sleep(1)
        print(f"Process {name} finished")
    
    process = mp.Process(target=worker, args=("Worker 1",))
    process.start()
    process.join()
    
    # Process pool
    def cpu_bound(x: int) -> int:
        return sum(i * i for i in range(x))
    
    numbers = [5000000 + x for x in range(20)]
    
    # Using map
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_bound, numbers))
    
    # Using apply_async
    pool = mp.Pool(processes=4)
    results = [pool.apply_async(cpu_bound, (x,)) for x in numbers]
    output = [p.get() for p in results]
    pool.close()
    pool.join()

#########################
# Shared Memory         #
#########################

def shared_memory_patterns():
    """
    Shared memory patterns for efficient data sharing between processes.
    """
    
    # Using SharedMemoryManager
    def worker_shared(shm_name: str):
        # Attach to existing shared memory
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        # Create numpy array using shared memory buffer
        array = np.ndarray((10,), dtype=np.int64, buffer=existing_shm.buf)
        # Modify the array
        array += 1
        existing_shm.close()
    
    with SharedMemoryManager() as smm:
        # Create shared memory array
        shm = smm.SharedMemory(size=10 * 8)  # 10 int64s
        array = np.ndarray((10,), dtype=np.int64, buffer=shm.buf)
        array[:] = range(10)
        
        # Start processes that share memory
        processes = []
        for _ in range(3):
            p = mp.Process(target=worker_shared, args=(shm.name,))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
    
    # Direct shared memory usage
    shm = shared_memory.SharedMemory(create=True, size=10 * 8)
    array = np.ndarray((10,), dtype=np.int64, buffer=shm.buf)
    array[:] = range(10)
    
    try:
        # Use the shared memory
        processes = []
        for _ in range(3):
            p = mp.Process(target=worker_shared, args=(shm.name,))
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
    finally:
        # Cleanup
        shm.close()
        shm.unlink()

#########################
# Queue Patterns        #
#########################

def queue_patterns():
    """
    Queue patterns for thread and process communication.
    """
    
    # Threading Queue
    def producer(queue: Queue):
        for i in range(5):
            time.sleep(0.1)
            queue.put(f"item {i}")
    
    def consumer(queue: Queue):
        while True:
            item = queue.get()
            if item is None:
                break
            print(f"Consumed {item}")
            queue.task_done()
    
    # Thread queue example
    queue = Queue()
    prod_thread = Thread(target=producer, args=(queue,))
    cons_thread = Thread(target=consumer, args=(queue,))
    
    prod_thread.start()
    cons_thread.start()
    
    prod_thread.join()
    queue.put(None)  # Signal to stop consumer
    cons_thread.join()
    
    # Multiprocessing Queue
    def mp_producer(queue: mp.Queue):
        for i in range(5):
            time.sleep(0.1)
            queue.put(f"item {i}")
    
    def mp_consumer(queue: mp.Queue):
        while True:
            item = queue.get()
            if item is None:
                break
            print(f"Consumed {item}")
    
    # Process queue example
    mp_queue = mp.Queue()
    prod_process = mp.Process(target=mp_producer, args=(mp_queue,))
    cons_process = mp.Process(target=mp_consumer, args=(mp_queue,))
    
    prod_process.start()
    cons_process.start()
    
    prod_process.join()
    mp_queue.put(None)  # Signal to stop consumer
    cons_process.join()

#########################
# Best Practices        #
#########################

def choose_concurrency_method(task_type: str) -> str:
    """
    Guide for choosing the right concurrency method.
    """
    if task_type == "cpu_bound":
        return """
        Use multiprocessing:
        - Heavy computations
        - Data processing
        - Image/video processing
        - Machine learning
        """
    elif task_type == "io_bound":
        return """
        Use threading or asyncio:
        - Network requests
        - File operations
        - Database operations
        Choose asyncio if the libraries you use support it
        """
    elif task_type == "mixed":
        return """
        Use combination:
        - ProcessPoolExecutor for CPU tasks
        - ThreadPoolExecutor for IO tasks
        - Consider using task queues
        """

def concurrency_best_practices():
    """Common best practices for concurrent programming."""
    
    # 1. Use context managers
    with ThreadPoolExecutor() as executor:
        pass
    
    # 2. Set appropriate timeouts
    with ThreadPoolExecutor() as executor:
        future = executor.submit(some_task)
        try:
            result = future.result(timeout=10)
        except TimeoutError:
            print("Task timed out")
    
    # 3. Proper cleanup
    try:
        # Do work
        pass
    finally:
        # Cleanup resources
        pass
    
    # 4. Handle exceptions
    def worker():
        try:
            # Do work
            pass
        except Exception as e:
            logger.exception("Worker failed")
    
    # 5. Use appropriate pool sizes
    n_cores = mp.cpu_count()
    pool_size = n_cores  # For CPU-bound tasks
    pool_size = min(32, n_cores * 4)  # For IO-bound tasks

def main():
    # Threading examples
    threading_patterns()
    
    # Multiprocessing examples
    multiprocessing_patterns()
    
    # Shared memory examples
    shared_memory_patterns()
    
    # Queue examples
    queue_patterns()

if __name__ == "__main__":
    main()