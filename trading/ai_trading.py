import asyncio
import pandas as pd
try:
    from deepseek_analysis.deepseek_signals import DeepSeekSignals
    from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer

except ImportError:
    print("Module deepseek_signals not found. Please ensure it is installed and accessible.")
from deepseek_analysis.deepseek_signals import DeepSeekSignals

from trading.order_book import OrderBook
from trading.exchange import TradingExchange  # API biržas savienojums

class AITradingBot:
    def __init__(self):
        self.exchange = TradingExchange()  # API savienojums ar biržu
        self.optimizer = DeepSeekOptimizer()
        self.symbols = ["BTC/USDT", "ETH/USDT"]
        self.timeframes = ["1m", "5m", "15m", "1h"]

    async def analyze_market(self, symbol, timeframe):
        """Iegūst reāllaika tirgus datus un izmanto AI optimizētu stratēģiju."""
        df = self.exchange.get_latest_data(symbol, timeframe)

        # ✅ 1. Pirmais AI optimizācijas solis
        optimized_strategy = self.optimizer.optimize_strategy(df)

        # ✅ 2. Pārbauda reāllaika win rate
        win_rate = self.calculate_win_rate()

        if win_rate < 65:
            print("🔹 AI stratēģija nepārsniedz 65% win rate, uzlabojam...")
            
            # ✅ 3. DeepSeek-Coder refaktorē AI ģenerēto stratēģiju
            improved_strategy_code = self.optimizer.optimize_strategy(df)["comment"]

            # ✅ 4. Izpilda AI refaktorēto stratēģiju
            exec(improved_strategy_code, globals())

        # ✅ 5. Veic tirdzniecības darījumu, balstoties uz AI signāliem
        if optimized_strategy["signal"] == 1:
            self.place_order(symbol, "buy")
        elif optimized_strategy["signal"] == -1:
            self.place_order(symbol, "sell")

    async def run(self):
        """Palaiž Trading Botu reāllaikā"""
        while True:
            for symbol in self.symbols:
                for timeframe in self.timeframes:
                    await self.analyze_market(symbol, timeframe)
            await asyncio.sleep(60)

if __name__ == "__main__":
    bot = AITradingBot()
    asyncio.run(bot.run())
