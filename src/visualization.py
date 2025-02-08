import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import asyncio
import tkinter as tk
from tkinter import ttk
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FixedLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.api_helpers import send_request
from src.order_book import get_order_book, process_order_book

# **GPU paātrinājums**
matplotlib.use("agg")

class OrderBookVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("Gate.io Futures Order Book - Optimized")

        # **Pieejamie Futures pāri**
        self.symbols = ["BTC_USDT", "ETH_USDT", "BNB_USDT", "SOL_USDT"]
        self.selected_symbol = tk.StringVar(value=self.symbols[0])

        # **Krāsu shēmas**
        self.color_schemes = {
            "dark": ("black", "white", "limegreen", "crimson"),
            "light": ("white", "black", "green", "red"),
            "blue": ("#1a1aff", "white", "#66ff99", "#ff5050"),
            "red": ("#660000", "white", "#ff9999", "#ff4d4d"),
        }
        self.color_scheme_var = tk.StringVar(value="dark")

        # **GUI izvēlne**
        control_frame = ttk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(control_frame, text="Select Token:").pack(side=tk.LEFT, padx=5)
        self.token_menu = ttk.Combobox(control_frame, values=self.symbols, textvariable=self.selected_symbol)
        self.token_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        self.color_menu = ttk.Combobox(control_frame, values=list(self.color_schemes.keys()), textvariable=self.color_scheme_var)
        self.color_menu.pack(side=tk.LEFT, padx=5)

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # **Matplotlib logs**
        self.fig, self.ax = plt.subplots(figsize=(8, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # **Saglabā sākotnējo Market Price, lai zoom in/out saglabā fokusu**
        self.market_price = None
        self.zoom_level = 1.0
        self.ax.yaxis.set_major_locator(plt.MaxNLocator(10))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # X ass pielāgošana
        self.canvas.mpl_connect("scroll_event", self.zoom)

        # **Asinhrona API datu ielāde**
        self.loop = asyncio.get_event_loop()
        self.running = False
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100, blit=True, cache_frame_data=False)

    def zoom(self, event):
        """Zoom funkcija, kas saglabā Market Price kā fiksētu centru"""
        zoom_factor = 1.1 if event.step > 0 else 0.9
        self.zoom_level *= zoom_factor

        y_min, y_max = self.ax.get_ylim()
        center_price = self.market_price if self.market_price else (y_min + y_max) / 2

        # **Saglabā Market Price centrā**
        new_y_min = center_price - ((center_price - y_min) * zoom_factor)
        new_y_max = center_price + ((y_max - center_price) * zoom_factor)

        self.ax.set_ylim(new_y_min, new_y_max)
        self.canvas.draw_idle()

    async def fetch_order_book(self, symbol):
        """Asinhroni iegūst order book datus no Gate.io API"""
        return await self.loop.run_in_executor(None, get_order_book, symbol)

    def update_plot(self, frame):
        """Reālā laika vizualizācija ar asinhronu API datu ielādi"""
        if not self.running:
            return []

        symbol = self.selected_symbol.get()
        order_book = self.loop.run_until_complete(self.fetch_order_book(symbol))

        if not order_book or "bids" not in order_book or "asks" not in order_book:
            print(f"⚠️ API neatgrieza datus par {symbol}")
            return []

        bids, asks = process_order_book(order_book)

        if bids is not None and asks is not None:
            self.ax.clear()

            # **Krāsu shēma**
            bg_color, text_color, bid_color, ask_color = self.color_schemes[self.color_scheme_var.get()]
            self.fig.patch.set_facecolor(bg_color)
            self.ax.set_facecolor(bg_color)

            try:
                bid_prices, bid_volumes = np.array(bids[:, 0], dtype=float), np.array(bids[:, 1], dtype=float)
                ask_prices, ask_volumes = np.array(asks[:, 0], dtype=float), np.array(asks[:, 1], dtype=float)
            except Exception as e:
                print(f"❌ Kļūda datu pārveidošanā: {e}")
                return []

            self.market_price = float(asks[0, 0]) if len(asks) > 0 else None
            if self.market_price:
                self.ax.axhline(self.market_price, color="yellow", linestyle="--", linewidth=2)
                self.ax.text(self.ax.get_xlim()[1], self.market_price, f"{self.market_price:.2f} USDT",
                             verticalalignment='bottom', horizontalalignment='right', fontsize=14, color="yellow", weight='bold')

            self.ax.barh(bid_prices, bid_volumes, color=bid_color, alpha=0.8, label="Bids (USDT Volume)")
            self.ax.barh(ask_prices, ask_volumes, color=ask_color, alpha=0.8, label="Asks (USDT Volume)")
            self.ax.set_ylim(min(bid_prices) * self.zoom_level, max(ask_prices) * self.zoom_level)
            self.ax.legend()
            return []

    def start(self):
        """Sāk vizualizācijas atjaunošanu"""
        if not self.running:
            self.running = True
            self.ani.event_source.start()

    def stop(self):
        """Aptur vizualizāciju"""
        if self.running:
            self.running = False
            self.ani.event_source.stop()

    def run(self):
        """Sāk Tkinter GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderBookVisualization(root)
    app.run()
