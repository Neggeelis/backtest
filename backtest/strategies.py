import numpy as np
from trading.indicators import calculate_rsi, calculate_macd

class StrategyManager:
    def __init__(self):
        self.strategies = [self.rsi_strategy]

    def select_best_strategy(self, df):
        return self.strategies[0]  # Šeit var pievienot AI izvēli

    def rsi_strategy(self, df):
        df["rsi"] = calculate_rsi(df["close"].values)
        df["signal"] = np.where(df["rsi"] < 30, 1, np.where(df["rsi"] > 70, -1, 0))
        return df
