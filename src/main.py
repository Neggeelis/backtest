### main.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gate_api_client import get_order_book, place_trailing_stop_order
from src.order_book import process_order_book, plot_heatmap

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot GUI")
        self.root.geometry("800x600")
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop_bot)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.order_book_button = ttk.Button(self.main_frame, text="Show Order Book", command=self.show_order_book)
        self.order_book_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        self.trailing_stop_button = ttk.Button(self.main_frame, text="Set Trailing Stop", command=self.set_trailing_stop)
        self.trailing_stop_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Status: Not Running", foreground="red")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.bot_running = False

    def start_bot(self):
        if not self.bot_running:
            self.bot_running = True
            self.status_label.config(text="Status: Running", foreground="green")
            messagebox.showinfo("Bot Status", "Trading bot started!")

    def stop_bot(self):
        if self.bot_running:
            self.bot_running = False
            self.status_label.config(text="Status: Not Running", foreground="red")
            messagebox.showinfo("Bot Status", "Trading bot stopped!")

    def show_order_book(self):
        symbol = "BTC_USDT"
        order_book = get_order_book(symbol)
        bids, asks = process_order_book(order_book)
        plot_heatmap(bids, asks, symbol)
    
    def set_trailing_stop(self):
        symbol = "BTC_USDT"
        trigger_price = float(input("Enter trigger price: "))
        trail_percent = float(input("Enter trailing stop percentage: "))
        response = place_trailing_stop_order(symbol, trigger_price, trail_percent)
        messagebox.showinfo("Trailing Stop", f"Trailing stop set: {response}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()
