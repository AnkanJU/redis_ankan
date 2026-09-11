# lesson_21_analytics.py
"""
Phase 7, Lesson 21: Real-Time Sales Analytics & Leaderboards in Redis
"""
import redis

def practice_realtime_analytics():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    
    unique_buyers_key = "analytics:unique_buyers:2026-09-11"
    leaderboard_key = "analytics:top_products"
    
    # Cleanup keys for a fresh run
    r.delete(unique_buyers_key, leaderboard_key)

    print("--- 1. Processing Simulated Orders ---")
    simulated_orders = [
        {"user_id": "usr_1001", "item_id": "item_101", "qty": 1},
        {"user_id": "usr_1002", "item_id": "item_102", "qty": 3},
        {"user_id": "usr_1001", "item_id": "item_101", "qty": 2}, # Duplicate buyer, item_101 bought again
        {"user_id": "usr_1003", "item_id": "item_103", "qty": 5},
        {"user_id": "usr_1002", "item_id": "item_101", "qty": 1}, # usr_1002 buys item_101
    ]

    pipe = r.pipeline()
    for order in simulated_orders:
        # Track unique buyer via HyperLogLog
        pipe.pfadd(unique_buyers_key, order["user_id"])
        # Increment product sales count on live Leaderboard
        pipe.zincrby(leaderboard_key, order["qty"], order["item_id"])
    pipe.execute()

    print("Successfully processed live stream batch!")

    print("\n--- 2. Unique Daily Buyers (HyperLogLog) ---")
    unique_count = r.pfcount(unique_buyers_key)
    print(f"Total Unique Buyers Today: {unique_count}")

    print("\n--- 3. Top Selling Products Leaderboard (Sorted Set) ---")
    # Fetch top 3 items sorted by highest quantity sold
    top_products = r.zrevrange(leaderboard_key, 0, 2, withscores=True)
    
    for rank, (item_id, sales_qty) in enumerate(top_products, start=1):
        print(f"Rank {rank}: Product {item_id} - {int(sales_qty)} units sold")

if __name__ == "__main__":
    practice_realtime_analytics()