# lesson_15_rate_limiter.py
"""
Phase 4, Lesson 15: Sliding Window API Rate Limiter using Redis Sorted Sets
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
import redis.asyncio as redis

redis_client: redis.Redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
        protocol=2
    )
    yield
    await redis_client.close()

app = FastAPI(title="Redis Rate Limiter API", lifespan=lifespan)

async def get_redis():
    return redis_client

# Rate Limiter Helper: Allows max 'limit' requests per 'window_seconds'
async def rate_limiter(request: Request, r: redis.Redis = Depends(get_redis)):
    client_ip = request.client.host or "127.0.0.1"
    rate_limit_key = f"rate_limit:{client_ip}"
    
    current_time = time.time()
    window_seconds = 10
    max_requests = 5
    clear_before_time = current_time - window_seconds

    # Use a Redis pipeline for atomic execution
    pipe = r.pipeline()
    # 1. Clear requests outside the current sliding window
    pipe.zremrangebyscore(rate_limit_key, 0, clear_before_time)
    # 2. Count active requests remaining in window
    pipe.zcard(rate_limit_key)
    # 3. Add current request timestamp
    pipe.zadd(rate_limit_key, {str(current_time): current_time})
    # 4. Set auto-expire on the key to prevent memory leaks
    pipe.expire(rate_limit_key, window_seconds + 1)
    
    results = await pipe.execute()
    request_count = results[1]

    if request_count >= max_requests:
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded. Maximum 5 requests per 10 seconds allowed."
        )

@app.get("/flash-sale/checkout", dependencies=[Depends(rate_limiter)])
async def checkout():
    return {"status": "success", "message": "Order successfully placed!"}