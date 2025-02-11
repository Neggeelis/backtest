import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from order_book import fetch_order_book, process_order_book, plot_heatmap

# Your application code here
def main():
    symbol = "BTC_USDT"
    order_book = fetch_order_book(symbol)
    bids, asks = process_order_book(order_book)
    plot_heatmap(bids, asks, symbol)

if __name__ == "__main__":
    main()