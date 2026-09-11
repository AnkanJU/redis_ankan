# lesson_24_memory_eviction.py
"""
Phase 8, Lesson 24: Redis Memory Inspection and Eviction Policy Management
"""
import redis

def practice_memory_management():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)

    print("--- 1. Inspecting Memory Metrics ---")
    memory_info = r.info("memory")
    used_memory_human = memory_info.get("used_memory_human")
    peak_memory_human = memory_info.get("peak_memory_human")
    mem_fragmentation_ratio = memory_info.get("mem_fragmentation_ratio")

    print(f"Used Memory: {used_memory_human}")
    print(f"Peak Memory: {peak_memory_human}")
    print(f"Fragmentation Ratio: {mem_fragmentation_ratio}")

    print("\n--- 2. Checking Current Eviction Policy & MaxMemory ---")
    max_mem = r.config_get("maxmemory")
    policy = r.config_get("maxmemory-policy")

    print(f"Current Max Memory Limit: {max_mem.get('maxmemory')} bytes")
    print(f"Current Eviction Policy: {policy.get('maxmemory-policy')}")

    print("\n--- 3. Dynamically Setting Eviction Policy for Caching ---")
    # Set eviction policy to allkeys-lru (ideal for flash-sale caching layers)
    r.config_set("maxmemory-policy", "allkeys-lru")
    
    updated_policy = r.config_get("maxmemory-policy")
    print(f"Updated Eviction Policy: {updated_policy.get('maxmemory-policy')}")

if __name__ == "__main__":
    practice_memory_management()