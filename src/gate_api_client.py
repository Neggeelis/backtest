import os
import time
import json
from dotenv import load_dotenv
from src.api_helpers import send_request
from src.order_book import get_order_book, process_order_book
from src.visualization import plot_heatmap  # ✅ Importē vizualizāciju

# Ielādē .env failu
load_dotenv()

if __name__ == "__main__":
    symbol = "BTC_USDT"
    print(f"📡 Sāku Order Book vizualizāciju {symbol} ar 3 sekunžu atjaunošanu...")
    plot_heatmap(symbol, refresh_interval=3)
