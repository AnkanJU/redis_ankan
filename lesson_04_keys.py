# lesson_04_keys.py
"""
Phase 2, Lesson 4: Redis Keys & Naming Conventions
"""
import redis

def practice_redis_keys():
    # Connecting with protocol=2 for compatibility
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    
    # 1. Standard key naming conventions for our Flash Sale project
    user_key = "user:101:profile"
    item_key = "flashsale:item:99:stock"
    
    print("--- 1. Setting Keys ---")
    r.set(user_key, "Ankan")
    r.set(item_key, "500")
    print(f"Set '{user_key}' and '{item_key}'")

    print("\n--- 2. Checking Existence ---")
    user_exists = r.exists(user_key)
    dummy_exists = r.exists("user:999:profile")
    print(f"Does '{user_key}' exist? {bool(user_exists)}")
    print(f"Does 'user:999:profile' exist? {bool(dummy_exists)}")

    print("\n--- 3. Fetching Values ---")
    print(f"User: {r.get(user_key)}")
    print(f"Initial Stock: {r.get(item_key)}")

    print("\n--- 4. Deleting a Key ---")
    r.delete(item_key)
    print(f"Deleted '{item_key}'. Stock key now exists: {bool(r.exists(item_key))}")

if __name__ == "__main__":
    practice_redis_keys()