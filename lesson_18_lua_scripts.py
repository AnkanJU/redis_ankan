# lesson_18_lua_scripts.py
"""
Phase 5, Lesson 18: Atomic Flash Sale Stock Deduction using Lua Scripts
"""
import redis

def practice_lua_script():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)
    
    stock_key = "flashsale:item:501:stock"
    
    # Initialize inventory to 2 items
    r.set(stock_key, 2)
    print(f"Initial Inventory for Item 501: {r.get(stock_key)} units")

    # Atomic Lua Script for Flash Sale Inventory Purchase
    # KEYS[1] -> stock_key
    # ARGV[1] -> quantity_to_buy
    lua_buy_script = """
    local current_stock = tonumber(redis.call('GET', KEYS[1]))
    local requested_qty = tonumber(ARGV[1])

    if not current_stock or current_stock < requested_qty then
        return 0 -- Insufficient stock
    else
        redis.call('DECRBY', KEYS[1], requested_qty)
        return 1 -- Purchase successful
    end
    """

    # Register the Lua script with Redis to get a reusable script object
    buy_item = r.register_script(lua_buy_script)

    print("\n--- Attempting Purchases ---")
    
    # Buyer 1 buys 1 item
    res1 = buy_item(keys=[stock_key], args=[1])
    print(f"Buyer 1 (1 unit): {'SUCCESS' if res1 == 1 else 'FAILED'} | Remaining Stock: {r.get(stock_key)}")

    # Buyer 2 buys 1 item
    res2 = buy_item(keys=[stock_key], args=[1])
    print(f"Buyer 2 (1 unit): {'SUCCESS' if res2 == 1 else 'FAILED'} | Remaining Stock: {r.get(stock_key)}")

    # Buyer 3 tries to buy 1 item (Out of Stock)
    res3 = buy_item(keys=[stock_key], args=[1])
    print(f"Buyer 3 (1 unit): {'SUCCESS' if res3 == 1 else 'OUT OF STOCK'} | Remaining Stock: {r.get(stock_key)}")

if __name__ == "__main__":
    practice_lua_script()