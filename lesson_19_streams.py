# lesson_19_streams.py
"""
Phase 6, Lesson 19: Event Streaming with Redis Streams
"""
import redis

def practice_redis_streams():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    stream_key = "flashsale:events:orders"
    
    # Cleanup stream key for fresh run
    r.delete(stream_key)

    print("--- 1. Appending Events to Stream (XADD) ---")
    # Add order events (* auto-generates a unique timestamp-based ID)
    event_id1 = r.xadd(stream_key, {"order_id": "ORD-1001", "user_id": "101", "amount": "120.0"})
    event_id2 = r.xadd(stream_key, {"order_id": "ORD-1002", "user_id": "205", "amount": "350.0"})
    
    print(f"Logged Event 1 ID: {event_id1}")
    print(f"Logged Event 2 ID: {event_id2}")

    print("\n--- 2. Reading Stream History (XRANGE) ---")
    # Read all events from start (-) to end (+)
    events = r.xrange(stream_key, min="-", max="+")
    for event_id, payload in events:
        print(f"Event [{event_id}] -> Order: {payload['order_id']}, User: {payload['user_id']}, Amount: ${payload['amount']}")

    print("\n--- 3. Listening for New Events (XREAD) ---")
    # Read up to 1 new event after event_id1
    new_events = r.xread({stream_key: event_id1}, count=1)
    print(f"Events occurring after {event_id1}:")
    print(new_events)

if __name__ == "__main__":
    practice_redis_streams()