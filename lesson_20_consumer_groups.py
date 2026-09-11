# lesson_20_consumer_groups.py
"""
Phase 6, Lesson 20: Scalable Worker Processing with Redis Consumer Groups
"""
import redis

def practice_consumer_groups():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    stream_key = "flashsale:tasks:payment"
    group_name = "payment_processors"
    
    # Clean up key for a fresh run
    r.delete(stream_key)

    # 1. Create the Consumer Group
    try:
        r.xgroup_create(stream_key, group_name, id="0", mkstream=True)
        print(f"Created Consumer Group '{group_name}' for stream '{stream_key}'")
    except redis.exceptions.ResponseError as e:
        print(f"Group already exists: {e}")

    # 2. Producer: Publish 3 payment processing tasks
    task1 = r.xadd(stream_key, {"order_id": "ORD-501", "amount": "99.00"})
    task2 = r.xadd(stream_key, {"order_id": "ORD-502", "amount": "149.00"})
    task3 = r.xadd(stream_key, {"order_id": "ORD-503", "amount": "200.00"})
    print("\nPublished 3 payment tasks to stream.")

    # 3. Worker 1 reads 2 tasks from the group
    print("\n--- Worker-1 Fetching Tasks ---")
    worker1_tasks = r.xreadgroup(group_name, "worker-1", {stream_key: ">"}, count=2)
    
    for stream, messages in worker1_tasks:
        for msg_id, payload in messages:
            print(f"Worker-1 processing Order: {payload['order_id']} (${payload['amount']})")
            # Acknowledge task completion
            r.xack(stream_key, group_name, msg_id)
            print(f"Worker-1 ACKed task {msg_id}")

    # 4. Worker 2 reads the remaining task
    print("\n--- Worker-2 Fetching Tasks ---")
    worker2_tasks = r.xreadgroup(group_name, "worker-2", {stream_key: ">"}, count=2)
    
    for stream, messages in worker2_tasks:
        for msg_id, payload in messages:
            print(f"Worker-2 processing Order: {payload['order_id']} (${payload['amount']})")
            r.xack(stream_key, group_name, msg_id)
            print(f"Worker-2 ACKed task {msg_id}")

if __name__ == "__main__":
    practice_consumer_groups()