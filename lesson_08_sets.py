# lesson_08_sets.py
"""
Phase 2, Lesson 8: Redis Sets for Unique Collections & Duplicate Prevention
"""
import redis

def practice_redis_sets():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    claimed_set = "flashsale:claimed_users"
    
    # Reset key for clean run
    r.delete(claimed_set)

    print("--- 1. Adding Members (SADD) ---")
    # Simulate users claiming a flash-sale deal
    r.sadd(claimed_set, "user:101", "user:202", "user:303")
    
    # Try adding user:101 again (Duplicate test)
    added = r.sadd(claimed_set, "user:101")
    print(f"Attempted to re-add 'user:101'. Items actually added: {added}") # Returns 0 because it's duplicate

    print("\n--- 2. Checking Existence (SISMEMBER) & Size (SCARD) ---")
    print(f"Has 'user:101' already claimed? {bool(r.sismember(claimed_set, 'user:101'))}")
    print(f"Has 'user:999' claimed? {bool(r.sismember(claimed_set, 'user:999'))}")
    print(f"Total unique users who claimed deal: {r.scard(claimed_set)}")

    print("\n--- 3. Listing All Members (SMEMBERS) & Removal (SREM) ---")
    print(f"All VIP Users: {r.smembers(claimed_set)}")
    
    # Revoke claim for user:202
    r.srem(claimed_set, "user:202")
    print(f"After removing 'user:202': {r.smembers(claimed_set)}")

if __name__ == "__main__":
    practice_redis_sets()