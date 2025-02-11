import os
import time
import json
from dotenv import load_dotenv
from api_telegram.api_helpers import send_request
from tests.order_book import get_order_book, process_order_book
from src.visualization import plot_heatmap  # ✅ Importē vizualizāciju
from api_telegram.order_book import OrderBook

class GateAPIClient:
    def __init__(self):
        self.order_book = OrderBook()

    def connect(self):
        print("Connecting to Gate.io API...")

    def fetch_order_book(self, symbol):
        print(f"Fetching order book for {symbol}")


# Ielādē .env failu
load_dotenv()

if __name__ == "__main__":
    symbol = "BTC_USDT"
    print(f"📡 Sāku Order Book vizualizāciju {symbol} ar 3 sekunžu atjaunošanu...")
    plot_heatmap(symbol, refresh_interval=3)
