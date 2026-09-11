# lesson_16_pipelines.py
"""
Phase 5, Lesson 16: Redis Pipelines for High-Performance Batch Processing
"""
import time
import redis

def benchmark_pipeline():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    total_items = 5000

    print(f"--- 1. Executing {total_items} Writes WITHOUT Pipeline ---")
    start_time = time.time()
    for i in range(total_items):
        r.set(f"nopipe:item:{i}", f"value_{i}")
    time_no_pipe = time.time() - start_time
    print(f"Time taken without pipeline: {time_no_pipe:.4f} seconds")

    print(f"\n--- 2. Executing {total_items} Writes WITH Pipeline ---")
    start_time = time.time()
    
    # Initialize pipeline
    pipe = r.pipeline()
    for i in range(total_items):
        pipe.set(f"pipe:item:{i}", f"value_{i}")
    
    # Execute all commands in a single network round-trip
    pipe.execute()
    
    time_with_pipe = time.time() - start_time
    print(f"Time taken with pipeline: {time_with_pipe:.4f} seconds")

    # Performance summary
    speedup = time_no_pipe / time_with_pipe if time_with_pipe > 0 else 0
    print(f"\nPipeline is approximately {speedup:.1f}x faster!")

if __name__ == "__main__":
    benchmark_pipeline()