#!/usr/bin/env python3
"""
market_orders.py
CLI script to place a Market Order (simulated) for Binance USDT-M Futures.

Usage:
    python src/market_orders.py BTCUSDT BUY 0.01
"""
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
import random

# Configure logging to project root bot.log
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
LOG_PATH = PROJECT_ROOT / "bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout)
    ],
)

VALID_SIDES = {"BUY", "SELL"}

def validate_symbol(symbol: str) -> bool:
    return isinstance(symbol, str) and symbol.isalnum() and symbol.endswith("USDT")

def validate_quantity(q_str: str) -> float:
    try:
        q = float(q_str)
        if q <= 0:
            raise ValueError("Quantity must be > 0")
        return q
    except Exception as e:
        raise argparse.ArgumentTypeError(str(e))

def simulate_place_market_order(symbol: str, side: str, quantity: float) -> dict:
    exec_price = round(1000 + random.random() * 1000, 2)
    order_id = random.randint(10_000_000, 99_999_999)
    result = {
        "orderId": order_id,
        "symbol": symbol,
        "side": side,
        "status": "FILLED",
        "executedQty": quantity,
        "avgPrice": exec_price,
        "transactTime": int(datetime.utcnow().timestamp() * 1000)
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Place a simulated Market Order (Binance Futures).")
    parser.add_argument("symbol", help="Trading pair symbol, e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity (e.g., 0.01)")
    args = parser.parse_args()

    symbol = args.symbol.strip().upper()
    side = args.side.strip().upper()
    try:
        quantity = validate_quantity(args.quantity)
    except Exception as e:
        logging.error(f"Invalid quantity: {e}")
        parser.error(f"Invalid quantity: {e}")

    if side not in VALID_SIDES:
        logging.error(f"Invalid side: {side}")
        parser.error("side must be BUY or SELL")

    if not validate_symbol(symbol):
        logging.error(f"Invalid symbol: {symbol}")
        parser.error("symbol must end with 'USDT' (e.g., BTCUSDT)")

    logging.info(f"Placing market order | {symbol} | {side} | qty={quantity}")
    try:
        order = simulate_place_market_order(symbol, side, quantity)
        logging.info(f"Market order placed | orderId={order['orderId']} | avgPrice={order['avgPrice']}")
        print({
            "orderId": order["orderId"],
            "symbol": order["symbol"],
            "side": order["side"],
            "status": order["status"],
            "executedQty": order["executedQty"],
            "avgPrice": order["avgPrice"]
        })
    except Exception as e:
        logging.exception("Failed to place market order")
        sys.exit(1)

if __name__ == "__main__":
    main()
