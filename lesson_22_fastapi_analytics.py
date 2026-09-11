# lesson_22_fastapi_analytics.py
"""
Phase 7, Lesson 22: Live Real-Time Analytics API Integration in FastAPI
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request
from pydantic import BaseModel
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

app = FastAPI(title="Redis Analytics & Flash Sale API", lifespan=lifespan)

async def get_redis():
    return redis_client

class CheckoutRequest(BaseModel):
    user_id: str
    item_id: str
    quantity: int
    price_per_unit: float

@app.post("/flash-sale/buy")
async def process_purchase(order: CheckoutRequest, r: redis.Redis = Depends(get_redis)):
    today_str = time.strftime("%Y-%m-%d")
    unique_buyers_key = f"analytics:unique_buyers:{today_str}"
    leaderboard_key = "analytics:top_products"
    revenue_key = f"analytics:total_revenue:{today_str}"
    
    total_price = order.quantity * order.price_per_unit

    # Atomic pipeline write for zero latency impact
    pipe = r.pipeline()
    # 1. HyperLogLog unique buyer tracking
    pipe.pfadd(unique_buyers_key, order.user_id)
    # 2. Leaderboard Sorted Set
    pipe.zincrby(leaderboard_key, order.quantity, order.item_id)
    # 3. Revenue counter
    pipe.incrbyfloat(revenue_key, total_price)
    
    await pipe.execute()

    return {
        "status": "success",
        "message": f"Order processed for {order.item_id}",
        "total_charged": total_price
    }

@app.get("/analytics/dashboard")
async def get_dashboard(r: redis.Redis = Depends(get_redis)):
    today_str = time.strftime("%Y-%m-%d")
    unique_buyers_key = f"analytics:unique_buyers:{today_str}"
    leaderboard_key = "analytics:top_products"
    revenue_key = f"analytics:total_revenue:{today_str}"

    pipe = r.pipeline()
    pipe.pfcount(unique_buyers_key)
    pipe.zrevrange(leaderboard_key, 0, 4, withscores=True)
    pipe.get(revenue_key)
    
    results = await pipe.execute()
    
    unique_buyers = results[0]
    top_products_raw = results[1]
    total_revenue = float(results[2]) if results[2] else 0.0

    top_products = [
        {"item_id": item_id, "units_sold": int(qty)} 
        for item_id, qty in top_products_raw
    ]

    return {
        "date": today_str,
        "unique_buyers": unique_buyers,
        "total_revenue": round(total_revenue, 2),
        "top_selling_products": top_products
    }