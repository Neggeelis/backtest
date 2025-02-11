import numpy as np
import matplotlib.pyplot as plt
import time
from collections import deque
from sklearn.preprocessing import MinMaxScaler
from api_telegram.api_helpers import send_request
from tests.order_book import OrderBook

class GateAPIClient:
    def __init__(self):
        self.order_book = OrderBook()

    def connect(self):
        print("Connecting to Gate.io API...")

    def fetch_order_book(self, symbol):
        print(f"Fetching order book for {symbol}")

# Laika kadru skaits, cik daudz vēsturisko datu saglabāt
TIME_FRAME_SIZE = 10
REFRESH_INTERVAL = 3  # Sekundes starp atjauninājumiem

# Glabā aktīvos orderus (FIFO queue, saglabā pēdējos TIME_FRAME_SIZE ierakstus)
order_book_history = deque(maxlen=TIME_FRAME_SIZE)

def get_order_book(symbol):
    """Get order book data from Gate.io API"""
    endpoint = f"/spot/order_book"
    params = {"currency_pair": symbol}
    return send_request(endpoint, params=params)

def process_order_book(order_book):
    """Process order book data and update the historical order list"""
    if not order_book or "bids" not in order_book or "asks" not in order_book:
        print("❌ Order Book dati nav pieejami.")
        return None, None

    try:
        bids = np.array(order_book["bids"], dtype=float)
        asks = np.array(order_book["asks"], dtype=float)

        # Aprēķina USDT vērtību katram orderim (cena * daudzums)
        bids[:, 1] = bids[:, 0] * bids[:, 1]
        asks[:, 1] = asks[:, 0] * asks[:, 1]

        # Saglabā jauno momentāno datu kopu
        order_book_history.append((bids, asks))

        print(f"✅ Atjaunināti dati: {len(order_book_history)} laika periodi saglabāti")
        return bids, asks
    except ValueError as e:
        print(f"⚠️ Kļūda datu apstrādē: {e}")
        return None, None

def plot_heatmap(symbol):
    """Continuously update order book heatmap based on historical time frames"""
    plt.ion()  # Ieslēdz interaktīvo režīmu
    fig, ax = plt.subplots(figsize=(10, 6))
    scaler = MinMaxScaler()

    while True:
        order_book = get_order_book(symbol)
        if not order_book:
            print("❌ API neatgrieza datus, gaidu nākamo ciklu...")
            time.sleep(REFRESH_INTERVAL)
            continue

        bids, asks = process_order_book(order_book)
        if bids is None or asks is None:
            print("⚠️ Nav pietiekami daudz datu vizualizācijai, gaidu nākamo ciklu...")
            time.sleep(REFRESH_INTERVAL)
            continue
        
        # Notīra iepriekšējo grafiku
        ax.clear()

        # Zīmē datus no visiem saglabātajiem time frames
        for i, (bids_frame, asks_frame) in enumerate(order_book_history):
            alpha = (i + 1) / TIME_FRAME_SIZE  # Vecākie dati ir caurspīdīgāki
            ax.scatter(bids_frame[:, 0], bids_frame[:, 1], c='green', alpha=alpha, label='Bids' if i == TIME_FRAME_SIZE - 1 else "")
            ax.scatter(asks_frame[:, 0], asks_frame[:, 1], c='red', alpha=alpha, label='Asks' if i == TIME_FRAME_SIZE - 1 else "")

        ax.set_xlabel("Price")
        ax.set_ylabel("USDT Volume")
        ax.set_title(f"Order Book Heatmap for {symbol} (Last {TIME_FRAME_SIZE} Frames)")
        ax.legend()
        ax.grid(True)

        plt.draw()
        plt.pause(REFRESH_INTERVAL)
