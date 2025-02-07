import os
import requests
import hmac
import hashlib
import time
import json
from dotenv import load_dotenv

load_dotenv()

# Binance API
BINANCE_BASE_URL = "https://api.binance.com"

# MEXC API
MEXC_BASE_URL = "https://api.mexc.com"

# Bybit API
BYBIT_BASE_URL = "https://api.bybit.com"

def get_top_20_symbols():
    """Iegūst top 20 kripto valūtas pēc apjoma no Binance."""
    url = f"{BINANCE_BASE_URL}/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    symbols = [item["symbol"] for item in data if item["symbol"].endswith("USDT")]
    return symbols[:20]

def mexc_api_request(endpoint, params=None, method="GET"):
    """Veic pieprasījumu uz MEXC API."""
    api_key = os.getenv("MEXC_API_KEY")
    api_secret = os.getenv("MEXC_API_SECRET")
    timestamp = str(int(time.time() * 1000))
    
    if params is None:
        params = {}
    params["timestamp"] = timestamp
    
    query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    
    headers = {
        "X-MEXC-APIKEY": api_key,
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        response = requests.get(f"{MEXC_BASE_URL}{endpoint}", headers=headers, params=params)
    else:
        response = requests.post(f"{MEXC_BASE_URL}{endpoint}", headers=headers, json=params)
    
    return response.json()

def bybit_api_request(endpoint, params=None, method="GET"):
    """Veic pieprasījumu uz Bybit API."""
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")
    timestamp = str(int(time.time() * 1000))
    
    if params is None:
        params = {}
    params["api_key"] = api_key
    params["timestamp"] = timestamp
    
    query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["sign"] = signature
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        response = requests.get(f"{BYBIT_BASE_URL}{endpoint}", headers=headers, params=params)
    else:
        response = requests.post(f"{BYBIT_BASE_URL}{endpoint}", headers=headers, json=params)
    
    return response.json()