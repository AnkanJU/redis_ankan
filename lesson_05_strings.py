# lesson_05_strings.py
"""
Phase 2, Lesson 5: Redis Strings & Atomic Operations
"""
import redis

def practice_redis_strings():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    
    print("--- 1. Multi-Set (MSET) and Multi-Get (MGET) ---")
    # Batch write to reduce network round-trips
    r.mset({
        "flashsale:item:101:name": "Gaming Laptop",
        "flashsale:item:101:price": "1200",
        "flashsale:item:101:stock": "50"
    })
    
    # Batch read
    items = r.mget(["flashsale:item:101:name", "flashsale:item:101:price", "flashsale:item:101:stock"])
    print(f"Item Details: Name={items[0]}, Price=${items[1]}, Stock={items[2]}")

    print("\n--- 2. Atomic Increments (INCR / INCRBY) ---")
    # Increment total item page views
    views_key = "flashsale:item:101:views"
    r.set(views_key, "100")
    
    new_views = r.incr(views_key) # Adds 1
    print(f"Page views after 1 view: {new_views}")
    
    new_views = r.incrby(views_key, 25) # Adds 25
    print(f"Page views after 25 bulk views: {new_views}")

    print("\n--- 3. Atomic Decrements (DECRBY for Flash Sale Orders) ---")
    # Customer buys 3 laptops in a flash sale
    stock_key = "flashsale:item:101:stock"
    remaining_stock = r.decrby(stock_key, 3)
    print(f"Purchased 3 items. Remaining Stock: {remaining_stock}")

if __name__ == "__main__":
    practice_redis_strings()