import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api_telegram.order_book import fetch_order_book, process_order_book, plot_heatmap

# Your visualization code here
def visualize_order_book(symbol):
    order_book = fetch_order_book(symbol)
    bids, asks = process_order_book(order_book)
    plot_heatmap(bids, asks, symbol)

if __name__ == "__main__":
    visualize_order_book("BTC_USDT")