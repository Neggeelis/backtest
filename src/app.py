from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.clock import Clock
from src.order_book import fetch_order_book, process_order_book, get_order_book_metrics
import matplotlib.pyplot as plt
import io

class TradingBotApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Order Book Scanner", font_size=20)
        self.layout.add_widget(self.label)
        
        self.scan_button = Button(text="Scan Order Book", size_hint=(1, 0.2))
        self.scan_button.bind(on_press=self.scan_order_book)
        self.layout.add_widget(self.scan_button)
        
        self.image = Image()
        self.layout.add_widget(self.image)
        
        return self.layout

    def scan_order_book(self, instance):
        """Skenē Order Book un atjaunina Heatmap."""
        symbol = "BTCUSDT"  # Varat pievienot ievades lauku
        order_book = fetch_order_book(symbol)
        if order_book:
            bids, asks = process_order_book(order_book)
            self.update_heatmap(bids, asks, symbol)
            metrics = get_order_book_metrics(bids, asks)
            self.label.text = f"Order Book Metrics for {symbol}: {metrics}"

    def update_heatmap(self, bids, asks, symbol):
        """Atjaunina Heatmap bildi."""
        plt.figure(figsize=(6, 4))
        plt.scatter(bids[:, 0], bids[:, 1], color='green', label='Bids', alpha=0.6)
        plt.scatter(asks[:, 0], asks[:, 1], color='red', label='Asks', alpha=0.6)
        plt.title(f'Order Book Heatmap: {symbol}')
        plt.xlabel('Price')
        plt.ylabel('Quantity')
        plt.legend()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        self.image.source = buf
        plt.close()

if __name__ == "__main__":
    TradingBotApp().run()
    