# lesson_14_api_caching.py
"""
Phase 4, Lesson 14: API Caching Layer in FastAPI using Redis
"""
import json
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
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

app = FastAPI(title="Redis Flash Sale API - Caching Layer", lifespan=lifespan)

async def get_redis():
    return redis_client

# Simulated Database Call (Disk I/O Latency)
async def fetch_item_from_db(item_id: int):
    await asyncio.sleep(1.5)  # Simulates 1.5s database delay
    db_mock = {
        101: {"id": 101, "name": "Mechanical Keyboard", "price": 120.0, "stock": 45},
        102: {"id": 102, "name": "Gaming Monitor", "price": 350.0, "stock": 12}
    }
    return db_mock.get(item_id)

@app.get("/items/{item_id}")
async def get_item(item_id: int, r: redis.Redis = Depends(get_redis)):
    cache_key = f"cache:item:{item_id}"
    
    # 1. Check Redis Cache
    cached_item = await r.get(cache_key)
    if cached_item:
        print(f"[CACHE HIT] Serving item {item_id} from Redis")
        return {"source": "redis_cache", "data": json.loads(cached_item)}
    
    # 2. Cache Miss: Read from DB
    print(f"[CACHE MISS] Fetching item {item_id} from Database")
    item_data = await fetch_item_from_db(item_id)
    
    if not item_data:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # 3. Store in Redis with 60-second TTL
    await r.set(cache_key, json.dumps(item_data), ex=60)
    
    return {"source": "database", "data": item_data}