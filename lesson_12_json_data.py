# lesson_12_json_data.py
"""
Phase 3, Lesson 12: Storing & Serializing Structured Data in Redis
"""
import json
import redis

def practice_json_serialization():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    
    # 1. Complex nested user payload
    user_data = {
        "id": 101,
        "name": "Ankan",
        "email": "ankan@example.com",
        "roles": ["admin", "customer"],
        "preferences": {"notifications": True, "theme": "dark"}
    }
    
    print("--- 1. Approach A: JSON String Serialization ---")
    json_key = "user:101:json"
    
    # Serialize dict to JSON string before storing
    r.set(json_key, json.dumps(user_data), ex=300)
    
    # Fetch and deserialize back to Python dict
    raw_json = r.get(json_key)
    parsed_data = json.loads(raw_json)
    print(f"Retrieved JSON Object: {parsed_data}")
    print(f"Accessing nested key 'theme': {parsed_data['preferences']['theme']}")

    print("\n--- 2. Approach B: Redis Hash for Top-Level Fields ---")
    hash_key = "user:101:hash"
    
    # Flatten top-level fields for fast field-level operations
    r.hset(hash_key, mapping={
        "id": str(user_data["id"]),
        "name": user_data["name"],
        "email": user_data["email"],
        "cart_count": "3"
    })
    
    # Atomically increment cart count directly in Hash without touching other fields
    r.hincrby(hash_key, "cart_count", 1)
    
    updated_hash = r.hgetall(hash_key)
    print(f"Retrieved Hash Object: {updated_hash}")

if __name__ == "__main__":
    practice_json_serialization()