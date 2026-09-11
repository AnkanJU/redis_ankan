# lesson_07_lists.py
"""
Phase 2, Lesson 7: Redis Lists for Task Queues & Activity Logs
"""
import redis

def practice_redis_lists():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    queue_key = "flashsale:queue:orders"
    
    # Clear key to start fresh for test run
    r.delete(queue_key)

    print("--- 1. Enqueuing Orders (RPUSH) ---")
    # Simulate users placing flash-sale orders in sequence
    r.rpush(queue_key, "order:1001", "order:1002", "order:1003")
    print(f"Total orders in queue: {r.llen(queue_key)}") # CLI equivalent: LLEN

    print("\n--- 2. Inspecting Queue (LRANGE) ---")
    # Fetch all items from index 0 to -1 (the end)
    all_orders = r.lrange(queue_key, 0, -1)
    print(f"Current Queue Order: {all_orders}")

    print("\n--- 3. Processing Orders (LPOP - First In, First Out) ---")
    # Kitchen worker processes the first incoming order
    processed_order = r.lpop(queue_key)
    print(f"Worker processed: {processed_order}")
    print(f"Remaining Queue: {r.lrange(queue_key, 0, -1)}")

if __name__ == "__main__":
    practice_redis_lists()