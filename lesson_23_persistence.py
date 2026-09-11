# lesson_23_persistence.py
"""
Phase 8, Lesson 23: Inspecting and Triggering Redis Persistence (RDB & AOF)
"""
import time
import redis

def test_persistence():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)

    print("--- 1. Fetching Current Persistence Settings ---")
    config = r.config_get("save")
    aof_enabled = r.config_get("appendonly")
    aof_sync = r.config_get("appendfsync")

    print(f"RDB Save Policy: {config.get('save')}")
    print(f"AOF Enabled: {aof_enabled.get('appendonly')}")
    print(f"AOF Sync Strategy: {aof_sync.get('appendfsync')}")

    print("\n--- 2. Triggering Manual On-Demand RDB Snapshot ---")
    # BGSAVE forks a background process to create an RDB snapshot without blocking clients
    try:
        r.bgsave()
        print("BGSAVE command triggered successfully! Redis is snapshotting RAM to disk in the background.")
    except redis.exceptions.ResponseError as e:
        print(f"BGSAVE state: {e}")

    # Check last save timestamp
    # Check last save timestamp
    last_save_time = r.lastsave()
    # Format the datetime object directly
    formatted_time = last_save_time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Last successful snapshot timestamp: {formatted_time}")
    print(f"Last successful snapshot timestamp: {formatted_time}")

    print("\n--- 3. Triggering Manual AOF Rewrite ---")
    # BGREWRITEAOF optimizes and shrink-wraps the AOF file size in the background
    try:
        r.bgrewriteaof()
        print("BGREWRITEAOF triggered! Redis is compacting write logs in the background.")
    except redis.exceptions.ResponseError as e:
        print(f"BGREWRITEAOF state: {e}")

if __name__ == "__main__":
    test_persistence()