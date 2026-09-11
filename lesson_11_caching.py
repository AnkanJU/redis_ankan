# lesson_11_caching.py
"""
Phase 3, Lesson 11: Redis Cache-Aside Pattern Implementation
"""
import time
import redis

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)

# Simulated slow SQL Database lookup
def get_product_from_db(product_id: int):
    print(f"  [DB DISK READ] Fetching product {product_id} from Primary Database...")
    time.sleep(1.5)  # Simulate slow disk I/O latency
    return f"Product #{product_id}: Pro Gaming Mouse"

# Cache-Aside logic wrapper
def get_product(product_id: int):
    cache_key = f"cache:product:{product_id}"
    
    # 1. Check Redis Cache
    cached_data = r.get(cache_key)
    
    if cached_data:
        print(f"  [CACHE HIT] Product {product_id} retrieved from Redis RAM!")
        return cached_data
    
    # 2. Cache Miss: Fall back to Database
    print(f"  [CACHE MISS] Product {product_id} not in Redis.")
    product_data = get_product_from_db(product_id)
    
    # 3. Write data to Redis with 10-second TTL
    r.set(cache_key, product_data, ex=10)
    print(f"  [CACHE UPDATE] Product {product_id} cached in Redis with 10s TTL.")
    
    return product_data

if __name__ == "__main__":
    print("--- Request 1 (Initial Request - Expect Cache Miss) ---")
    start_time = time.time()
    data = get_product(101)
    print(f"Result: {data} | Response Time: {time.time() - start_time:.4f}s")

    print("\n--- Request 2 (Immediate Follow-up - Expect Cache Hit) ---")
    start_time = time.time()
    data = get_product(101)
    print(f"Result: {data} | Response Time: {time.time() - start_time:.4f}s")