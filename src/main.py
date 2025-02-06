import tkinter as tk
from tkinter import ttk, messagebox
from src.api import get_top_20_symbols, mexc_api_request, bybit_api_request
from src.telegram_bot import test_telegram, send_signal, send_profit_update
from src.order_book import fetch_order_book, process_order_book, plot_heatmap, get_order_book_metrics
import asyncio
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bots Deepseek")
        self.root.geometry("800x600")

        # Main Frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Start/Stop Buttons
        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        # USDT Amount and Leverage Input
        self.usdt_label = ttk.Label(self.main_frame, text="USDT Daudzums:")
        self.usdt_label.grid(row=1, column=0, padx=5, pady=5)

        self.usdt_entry = ttk.Entry(self.main_frame)
        self.usdt_entry.grid(row=1, column=1, padx=5, pady=5)
        self.usdt_entry.insert(0, os.getenv("USDT_AMOUNT", "100"))  # Default USDT amount

        self.leverage_label = ttk.Label(self.main_frame, text="Leverage:")
        self.leverage_label.grid(row=2, column=0, padx=5, pady=5)

        self.leverage_entry = ttk.Entry(self.main_frame)
        self.leverage_entry.grid(row=2, column=1, padx=5, pady=5)
        self.leverage_entry.insert(0, os.getenv("LEVERAGE", "10"))  # Default leverage

        # Exchange Selection
        self.exchange_label = ttk.Label(self.main_frame, text="Izvēlieties biržu:")
        self.exchange_label.grid(row=3, column=0, padx=5, pady=5)

        self.exchange_var = tk.StringVar(value="MEXC")
        self.exchange_combobox = ttk.Combobox(
            self.main_frame, textvariable=self.exchange_var,
            values=["MEXC", "Bybit"]
        )
        self.exchange_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Task Selection
        self.task_label = ttk.Label(self.main_frame, text="Izvēlieties uzdevumu:")
        self.task_label.grid(row=4, column=0, padx=5, pady=5)

        self.task_var = tk.StringVar(value="all")
        self.task_combobox = ttk.Combobox(
            self.main_frame, textvariable=self.task_var,
            values=["signals", "live_trading", "heatmap", "all"]
        )
        self.task_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Log Output
        self.log_label = ttk.Label(self.main_frame, text="Žurnāls:")
        self.log_label.grid(row=5, column=0, padx=5, pady=5)

        self.log_text = tk.Text(self.main_frame, height=15, width=70, state=tk.DISABLED)
        self.log_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Status Bar
        self.status_var = tk.StringVar(value="Statuss: Gatavs")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_bar.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        # Bot Control Variables
        self.is_running = False
        self.profit = 0.0
        self.trades = 0
        self.wins = 0
        self.strategies = {}  # Saglabā optimizētās stratēģijas

    def start_bot(self):
        """Sāk bota darbību."""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("Statuss: Darbojas...")

            # Izvēlētais uzdevums
            task = self.task_var.get()

            # Palaist bota darbību atsevišķā pavedienā
            threading.Thread(target=self.run_bot, args=(task,), daemon=True).start()

    def stop_bot(self):
        """Aptur bota darbību."""
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_var.set("Statuss: Apturēts")
            self.log("Bots apturēts.")

    def run_bot(self, task):
        """Bota darbības loģika."""
        if task == "signals":
            self.log("Sāk signālu sūtīšanu uz Telegram...")
            asyncio.run(self.send_signals())
        elif task == "live_trading":
            self.log("Sāk tiešsaistes treidingu...")
            asyncio.run(self.start_live_trading())
        elif task == "heatmap":
            self.log("Sāk Order Book Heatmap vizualizāciju...")
            self.show_heatmap()
        elif task == "all":
            self.log("Sāk visus uzdevumus reizē...")
            threading.Thread(target=self.run_all_tasks, daemon=True).start()

    def run_all_tasks(self):
        """Palaist visus uzdevumus reizē."""
        asyncio.run(self.send_signals())
        asyncio.run(self.start_live_trading())
        self.show_heatmap()

    async def send_signals(self):
        """Sūta signālus uz Telegram."""
        while self.is_running:
            try:
                await send_signal("BTCUSDT", "Buy", "Strong buy signal detected!")
                self.log("Signāls nosūtīts uz Telegram.")
                await asyncio.sleep(10)  # Pagaida 10 sekundes
            except Exception as e:
                self.log(f"Kļūda, sūtot signālu: {e}")

    async def start_live_trading(self):
        """Sāk tiešsaistes treidingu."""
        usdt_amount = float(self.usdt_entry.get())
        leverage = int(self.leverage_entry.get())
        exchange = self.exchange_var.get()
        self.log(f"Sāk treidingu ar {usdt_amount} USDT un {leverage}x leverage uz {exchange}.")

        while self.is_running:
            try:
                # Optimizē stratēģijas
                self.optimize_strategies()

                # Veic treidinga operācijas
                self.log("Veic treidinga operācijas...")
                await asyncio.sleep(5)  # Pagaida 5 sekundes
            except Exception as e:
                self.log(f"Kļūda, veicot treidingu: {e}")

    def optimize_strategies(self):
        """Optimizē stratēģijas tiešsaistes treidinga laikā."""
        symbols = get_top_20_symbols()
        for symbol in symbols:
            # Analizē un optimizē stratēģijas
            best_strategy = self.find_best_strategy(symbol)
            if best_strategy:
                self.strategies[symbol] = best_strategy
                self.log(f"Optimizēta stratēģija {symbol}: {best_strategy}")

    def find_best_strategy(self, symbol):
        """Atrod labāko stratēģiju simbolam."""
        # Pievienojiet savu stratēģiju optimizācijas loģiku šeit
        return {"strategy": "EMA_20 + RSI", "win_rate": 0.68}

    def show_heatmap(self):
        """Parāda Order Book Heatmap."""
        order_book = fetch_order_book("BTCUSDT")
        if order_book:
            bids, asks = process_order_book(order_book)
            plot_heatmap(bids, asks, "BTCUSDT")
            self.log("Order Book Heatmap parādīts.")
        else:
            self.log("Kļūda, iegūstot Order Book.")

    def log(self, message):
        """Pievieno ziņu žurnālam."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()