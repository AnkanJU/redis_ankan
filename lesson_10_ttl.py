# lesson_10_ttl.py
"""
Phase 3, Lesson 10: Key Expiration & TTL Management
"""
import time
import redis

def practice_ttl():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    otp_key = "flashsale:otp:user101"
    session_key = "flashsale:session:user101"

    print("--- 1. Setting Key with Atomic TTL (SET EX) ---")
    # Store OTP valid for only 3 seconds
    r.set(otp_key, "82914", ex=3)
    print(f"OTP set successfully. Value: {r.get(otp_key)}")
    print(f"Initial TTL: {r.ttl(otp_key)} seconds remaining")

    print("\n--- 2. Watching TTL Countdown ---")
    time.sleep(2)
    print(f"TTL after 2 seconds: {r.ttl(otp_key)} seconds remaining")

    time.sleep(1.5)
    print(f"TTL after expiry: {r.ttl(otp_key)} (Returns -2 because key died)")
    print(f"Fetching expired OTP: {r.get(otp_key)}")

    print("\n--- 3. Using EXPIRE and PERSIST ---")
    r.set(session_key, "active_token_xyz")
    r.expire(session_key, 10)  # Set 10s TTL
    print(f"Session TTL: {r.ttl(session_key)} seconds")

    # Cancel expiration timer
    r.persist(session_key)
    print(f"TTL after PERSIST command: {r.ttl(session_key)} (-1 means permanent)")

if __name__ == "__main__":
    practice_ttl()