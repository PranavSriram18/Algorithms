import cProfile
import math
import pstats
import sys
import trace
from pstats import SortKey

"""
Experiments with profiling, tracing, and visualizing performance.
"""

def is_special_value(x, y, z):
    # Simulate some complex check
    eps = 1e-6
    x, y, z = 1.0 * x + eps, 1.0 * y + eps, 1.0 * z + eps
    return math.sin(x/(y+z)) * math.cos(y/(x+z)) > 0.5

def process_element(value):
    # Simulate data processing
    # testing effects of abs before sqrt vs no abs
    # return sum(math.sqrt(abs(value+i)) for i in range(100))
    return sum(math.sqrt(value+i) for i in range(100))

def update_accumulator(acc, value):
    # Simulate updating some running calculations
    return acc + math.log(abs(value) + 1.)

def inefficient_matrix_operation(size):
    result = 0
    accumulator = 0
    special_count = 0
    
    for i in range(size):
        for j in range(size):
            for k in range(size):
                # Check if this is a special value
                if is_special_value(i, j, k):
                    special_count += 1
                    value = (i + 1) * (j + 2) * (k + 3) % 7
                    
                    # Process the value
                    processed = process_element(value)
                    
                    # Update running calculations
                    accumulator = update_accumulator(accumulator, processed)
                    
                    result += processed
                    
    return result, accumulator, special_count

# 1. Basic trace
def run_with_trace():
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=1
    )
    tracer.run('inefficient_matrix_operation(4)')
    # Save counts to a file
    r = tracer.results()
    r.write_results(show_missing=True, summary=True)

# 2. Profile with cProfile
def run_with_profile():
    profiler = cProfile.Profile()
    profiler.enable()
    res, acc, sc = inefficient_matrix_operation(20)  # Larger size for more obvious results
    profiler.disable()
    print(f"Result: {res}, Accumulator: {acc}, Special Count: {sc}")

    # Save stats to file
    profiler.dump_stats('profile_output.stats')
    
    # Print sorted stats
    stats = pstats.Stats(profiler).sort_stats(SortKey.CUMULATIVE)
    stats.print_stats()

if __name__ == "__main__":
    #print("Running with basic trace (size=5):")
    #run_with_trace()
    
    print("\nRunning with profiler (size=20):")
    run_with_profile()
