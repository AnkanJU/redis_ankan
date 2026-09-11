# lesson_09_sorted_sets.py
"""
Phase 2, Lesson 9: Redis Sorted Sets for Leaderboards & Scoring
"""
import redis

def practice_sorted_sets():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    board_key = "flashsale:leaderboard"
    
    # Clear key for clean test execution
    r.delete(board_key)

    print("--- 1. Adding Players & Scores (ZADD) ---")
    # Add top buyers based on flash-sale reward points
    r.zadd(board_key, {
        "user:101": 500,
        "user:202": 800,
        "user:303": 650
    })
    print("Added players user:101 (500), user:202 (800), user:303 (650)")

    print("\n--- 2. Fetching Single Member Score (ZSCORE) ---")
    score = r.zscore(board_key, "user:202")
    print(f"Score for 'user:202': {score}")

    print("\n--- 3. Leaderboard Ranking (ZRANGE) ---")
    # Retrieve top players ordered from highest to lowest score
    top_players = r.zrange(board_key, 0, -1, desc=True, withscores=True)
    print("Leaderboard (Ranked Highest to Lowest):")
    for rank, (player, pts) in enumerate(top_players, start=1):
        print(f"  Rank #{rank}: {player} - {pts} points")

    print("\n--- 4. Updating Scores & Removal (ZADD & ZREM) ---")
    # Updating user:101's score boosts them up the board
    r.zadd(board_key, {"user:101": 950})
    
    # Remove user:303
    r.zrem(board_key, "user:303")

    updated_top = r.zrange(board_key, 0, -1, desc=True, withscores=True)
    print("Updated Top Players after score boost & removal:")
    print(updated_top)

if __name__ == "__main__":
    practice_sorted_sets()