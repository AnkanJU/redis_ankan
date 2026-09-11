# lesson_03_cli_test.py
"""
Phase 1, Lesson 3: Interacting with Redis via CLI concepts
"""
import redis

def run_cli_basics():
    # Added protocol=2 to maintain legacy RESP2 protocol compatibility
    r = redis.Redis(
        host='localhost', 
        port=6379, 
        db=0, 
        decode_responses=True,
        protocol=2  # <-- FIX: Forces RESP2 protocol
    )
    
    # Executing basic commands programmatically
    print("1. Sending PING command...")
    print(f"Server replied: {r.ping()}") # CLI equivalent: PING
    
    print("\n2. Setting key 'server:status' to 'online'...")
    r.set("server:status", "online") # CLI equivalent: SET server:status online
    
    print("\n3. Fetching key 'server:status'...")
    status = r.get("server:status") # CLI equivalent: GET server:status
    print(f"Retrieved value: {status}")
    
    print("\n4. Checking database size...")
    print(f"Total keys in DB: {r.dbsize()}") # CLI equivalent: DBSIZE

if __name__ == "__main__":
    run_cli_basics()