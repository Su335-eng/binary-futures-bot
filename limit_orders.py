#!/usr/bin/env python3
"""
limit_orders.py
CLI script to place a Limit Order (simulated) for Binance USDT-M Futures.

Usage:
    python src/limit_orders.py BTCUSDT SELL 0.02 65000
"""
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
import random

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

def validate_price(p_str: str) -> float:
    try:
        p = float(p_str)
        if p <= 0:
            raise ValueError("Price must be > 0")
        return p
    except Exception as e:
        raise argparse.ArgumentTypeError(str(e))

def simulate_place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    order_id = random.randint(10_000_000, 99_999_999)
    result = {
        "orderId": order_id,
        "symbol": symbol,
        "side": side,
        "status": "NEW",
        "origQty": quantity,
        "price": price,
        "transactTime": int(datetime.utcnow().timestamp() * 1000)
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Place a simulated Limit Order (Binance Futures).")
    parser.add_argument("symbol", help="Trading pair symbol, e.g., BTCUSDT")
    parser.add_argument("side", help="BUY or SELL")
    parser.add_argument("quantity", help="Quantity (e.g., 0.01)")
    parser.add_argument("price", help="Limit price (e.g., 65000)")
    args = parser.parse_args()

    symbol = args.symbol.strip().upper()
    side = args.side.strip().upper()
    try:
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)
    except Exception as e:
        logging.error(f"Invalid input: {e}")
        parser.error(f"Invalid input: {e}")

    if side not in VALID_SIDES:
        logging.error(f"Invalid side: {side}")
        parser.error("side must be BUY or SELL")

    if not validate_symbol(symbol):
        logging.error(f"Invalid symbol: {symbol}")
        parser.error("symbol must end with 'USDT' (e.g., BTCUSDT)")

    logging.info(f"Placing limit order | {symbol} | {side} | qty={quantity} | price={price}")
    try:
        order = simulate_place_limit_order(symbol, side, quantity, price)
        logging.info(f"Limit order placed | orderId={order['orderId']} | status={order['status']}")
        print({
            "orderId": order["orderId"],
            "symbol": order["symbol"],
            "side": order["side"],
            "status": order["status"],
            "origQty": order["origQty"],
            "price": order["price"]
        })
    except Exception as e:
        logging.exception("Failed to place limit order")
        sys.exit(1)

if __name__ == "__main__":
    main()
