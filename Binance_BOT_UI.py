import streamlit as st
from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
import os
from dotenv import load_dotenv
import random
import time

# Load API keys from .env file
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Flag to toggle simulation mode (set True to simulate orders)
SIMULATION_MODE = True

# Get current market price
def get_market_price(symbol):
    try:
        ticker = client.futures_mark_price(symbol=symbol)
        return float(ticker['markPrice'])
    except Exception as e:
        logging.error(f"Error fetching market price: {e}")
        return None

# Simulate placing order (fake response)
def simulate_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    simulated_order = {
        "symbol": symbol,
        "orderId": random.randint(10000000, 99999999),
        "clientOrderId": f"simulated_{int(time.time())}",
        "transactTime": int(time.time() * 1000),
        "price": str(price) if price else "0",
        "origQty": str(quantity),
        "executedQty": "0",
        "status": "NEW",
        "timeInForce": "GTC" if order_type in ["LIMIT", "STOP_MARKET"] else None,
        "type": order_type,
        "side": side,
        "stopPrice": str(stop_price) if stop_price else None,
        "simulated": True,
        "message": "This is a simulated order. No real order was placed."
    }
    logging.info(f"Simulated order: {simulated_order}")
    return simulated_order

# Place order or simulate
def place_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    if SIMULATION_MODE:
        # Just simulate the order without calling API
        return simulate_order(symbol, side, order_type, quantity, price, stop_price)

    try:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        elif order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price
            params["timeInForce"] = "GTC"

        order = client.futures_create_order(**params)
        logging.info(f"Order placed: {order}")
        return order
    except BinanceAPIException as e:
        logging.error(f"Binance error: {e.message}")
        return {"error": e.message}
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": str(e)}

# UI Layout
st.title("💹 Binance Futures Trading Bot")

symbol = st.text_input("Symbol", "BTCUSDT")
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_MARKET"])
side = st.selectbox("Side", ["BUY", "SELL"])
quantity = st.number_input("Quantity", min_value=0.001, value=0.01, step=0.001, format="%f")

price = None
stop_price = None

if order_type == "LIMIT":
    price = st.number_input("Limit Price", min_value=0.01, value=30000.0, step=0.01)
elif order_type == "STOP_MARKET":
    stop_price = st.number_input("Stop Price", min_value=0.01, value=29000.0, step=0.01)

# Live Market Price
if symbol:
    current_price = get_market_price(symbol)
    if current_price:
        st.markdown(f"**📈 Live Market Price for {symbol}:** `${current_price:,.2f}`")
    else:
        st.warning("Failed to fetch market price.")

# Place Order Button
if st.button("🚀 Place Order"):
    result = place_order(symbol, side, order_type, quantity, price, stop_price)
    st.json(result)

# Auto-refresh every 5 seconds (if needed)
params = st.query_params
if "refresh" not in params:
    st.query_params["refresh"] = "1"
    st.rerun()

