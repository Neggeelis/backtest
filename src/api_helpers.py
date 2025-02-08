import os
import time
import hmac
import hashlib
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.gateio.ws/api/v4"

def generate_signature(method, endpoint, params, json_body):
    """Generate signature for Gate.io API private requests"""
    api_key = os.getenv("GATE_API_KEY")
    api_secret = os.getenv("GATE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError("API key and secret must be set in environment variables")

    query_string = ""
    if params:
        query_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
    
    body_string = json.dumps(json_body) if json_body else ""
    payload = f"{method}\n{endpoint}\n{query_string}\n{body_string}"
    
    signature = hmac.new(api_secret.encode(), payload.encode(), hashlib.sha512).hexdigest()
    
    return {
        "KEY": api_key,
        "SIGN": signature,
        "Timestamp": str(int(time.time()))
    }

def send_request(endpoint, params=None, json_body=None, method="GET", private=False):
    """Send request to Gate.io API"""
    headers = {"Content-Type": "application/json"}
    
    if private:
        headers.update(generate_signature(method, endpoint, params, json_body))
    
    url = f"{BASE_URL}{endpoint}"
    print(f"📡 Sending request: {method} {url} with params: {params} and body: {json_body}")

    try:
        response = requests.request(method, url, params=params, json=json_body, headers=headers)
        print(f"🔍 Raw API Response: {response.text}")  # Izdrukājam API atbildi
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Gate.io API error: {e}")
        return None

