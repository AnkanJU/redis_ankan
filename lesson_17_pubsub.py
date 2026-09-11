# lesson_17_pubsub.py
"""
Phase 5, Lesson 17: Redis Pub/Sub Real-Time Messaging System
"""
import time
import threading
import redis

# Redis connection with protocol=2 for legacy compatibility
def get_client():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)

def start_subscriber(channel_name: str):
    r = get_client()
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)
    
    print(f"  [SUBSCRIBER] Subscribed to '{channel_name}'. Waiting for events...")
    
    # Listen for published messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"  [SUBSCRIBER] Received notification: {message['data']}")
            if message['data'] == "STOP":
                print("  [SUBSCRIBER] Stopping listener...")
                break

def practice_pubsub():
    channel_name = "flash_sale_notifications"
    
    # 1. Start subscriber in a background thread
    subscriber_thread = threading.Thread(target=start_subscriber, args=(channel_name,), daemon=True)
    subscriber_thread.start()
    
    time.sleep(1)  # Give subscriber thread time to establish connection

    print("\n--- 2. Publishing Messages ---")
    publisher = get_client()
    
    publisher.publish(channel_name, "Flash Sale starts in 5 minutes!")
    time.sleep(0.5)
    
    publisher.publish(channel_name, "PRICE DROP: PS5 Console is now $299!")
    time.sleep(0.5)
    
    publisher.publish(channel_name, "STOP")
    subscriber_thread.join()

if __name__ == "__main__":
    practice_pubsub()