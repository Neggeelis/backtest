import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

BINANCE_BASE_URL = "https://api.binance.com"

def fetch_order_book(symbol, limit=100):
    """Iegūst Order Book datus no Binance."""
    url = f"{BINANCE_BASE_URL}/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Kļūda, iegūstot Order Book: {response.status_code}")
        return None

def process_order_book(order_book):
    """Apstrādā Order Book datus."""
    bids = np.array(order_book['bids'], dtype=float)
    asks = np.array(order_book['asks'], dtype=float)
    return bids, asks

def plot_heatmap(bids, asks, symbol):
    """Vizualizē Order Book kā Heatmap."""
    plt.figure(figsize=(10, 6))
    
    # Scalējam datus
    scaler = MinMaxScaler()
    bids_scaled = scaler.fit_transform(bids[:, 1].reshape(-1, 1))
    asks_scaled = scaler.fit_transform(asks[:, 1].reshape(-1, 1))
    
    # Heatmap vizualizācija
    plt.scatter(bids[:, 0], bids_scaled, color='green', label='Bids', alpha=0.6)
    plt.scatter(asks[:, 0], asks_scaled, color='red', label='Asks', alpha=0.6)
    
    plt.title(f'Order Book Heatmap: {symbol}')
    plt.xlabel('Price')
    plt.ylabel('Quantity (Scaled)')
    plt.legend()
    plt.grid(True)
    plt.show()