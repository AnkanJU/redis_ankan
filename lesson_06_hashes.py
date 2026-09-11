# lesson_06_hashes.py
"""
Phase 2, Lesson 6: Redis Hashes for Object Representation
"""
import redis

def practice_redis_hashes():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    item_key = "flashsale:item:201"
    
    print("--- 1. Creating/Updating Hash (HSET) ---")
    # Store multiple fields for an item
    r.hset(item_key, mapping={
        "title": "Wireless Headphones",
        "price": "99",
        "category": "Electronics",
        "stock": "150"
    })
    print(f"Hash object created at key '{item_key}'")

    print("\n--- 2. Fetching Specific Fields (HGET & HMGET) ---")
    title = r.hget(item_key, "title")
    price, stock = r.hmget(item_key, ["price", "stock"])
    print(f"Item: {title} | Price: ${price} | Stock: {stock}")

    print("\n--- 3. Field Existence & Hash Operations ---")
    has_discount = r.hexists(item_key, "discount")
    print(f"Does field 'discount' exist? {bool(has_discount)}")

    # Incrementing integer values directly inside a hash field
    r.hincrby(item_key, "stock", -5)
    print(f"Updated Stock (after purchasing 5 items): {r.hget(item_key, 'stock')}")

    print("\n--- 4. Fetching Entire Object (HGETALL) ---")
    full_item_data = r.hgetall(item_key)
    print("Full Hash Data from Redis:")
    print(full_item_data)

if __name__ == "__main__":
    practice_redis_hashes()