# lesson_02_architecture.py
import redis

def test_redis_connection():
    # Adding protocol=2 ensures compatibility with older Redis server versions
    client = redis.Redis(
        host='localhost', 
        port=6379, 
        db=0, 
        decode_responses=True,
        protocol=2  # <-- FIX: Forces RESP2 protocol (skips 'HELLO 3' command)
    )
    
    try:
        response = client.ping()
        print(f"Redis Server Response: {response}")
        print("Client-Server TCP Connection Established Successfully!")
    except redis.ConnectionError as e:
        print(f"Connection Failed: Ensure Redis is running locally. Error: {e}")

if __name__ == "__main__":
    test_redis_connection()