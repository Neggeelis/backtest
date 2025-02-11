from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer
from trading.strategies import trading_strategy
import pandas as pd

class Backtest:
    def __init__(self, historical_data):
        self.historical_data = historical_data

    def run(self, strategy_code):
        """
        Izpilda backtest AI ģenerētajai stratēģijai.
        """
        results = []
        
        # ✅ Definē funkciju izpildei no koda
        exec_locals = {}
        exec(strategy_code, {}, exec_locals)
        
        if "execute_strategy" not in exec_locals:
            raise ValueError("❌ Stratēģijas kods nesatur 'execute_strategy' funkciju!")

        execute_strategy = exec_locals["execute_strategy"]  # Iegūst stratēģijas funkciju

        for _, row in self.historical_data.iterrows():
            decision = execute_strategy(row["close"], row["low"])  # ✅ Pareizi izsauc stratēģiju
            results.append(decision)
        
        return results
