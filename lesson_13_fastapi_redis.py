# lesson_13_fastapi_redis.py
"""
Phase 4, Lesson 13: Persistent Redis Connection Pooling in FastAPI
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import redis.asyncio as redis

# Global reference for our Redis connection pool
redis_client: redis.Redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    # 1. Startup: Initialize asynchronous Redis client with protocol=2
    print("Connecting to Redis...")
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True,
        protocol=2  # Ensures compatibility with legacy Redis versions
    )
    yield
    # 2. Shutdown: Cleanly close Redis connections
    print("Closing Redis connection...")
    await redis_client.close()

app = FastAPI(title="Redis Flash Sale API", lifespan=lifespan)

# Dependency injection helper to acquire Redis instance
async def get_redis():
    return redis_client

@app.get("/")
async def root():
    return {"message": "FastAPI + Redis Service Online"}

@app.get("/ping")
async def ping_redis(r: redis.Redis = Depends(get_redis)):
    pong = await r.ping()
    return {"redis_status": pong}