import pandas as pd
import numpy as np
import talib
from itertools import combinations
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import requests
from src.api import test_api

async def start_backtest():
    """Backtestēšanas funkcija."""
    print("🔄 Starting backtest...")
    indicators = ["EMA_20", "RSI", "upper_band", "lower_band", "MACD"]

    def add_indicators(df):
        """Pievieno tehniskos rādītājus."""
        df["EMA_20"] = talib.EMA(df["close"], timeperiod=20)
        df["RSI"] = talib.RSI(df["close"], timeperiod=14)
        df["upper_band"], _, df["lower_band"] = talib.BBANDS(df["close"], timeperiod=20)
        df["MACD"], _, _ = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
        return df

    async def backtest(df, symbol):
        """Backtestēšanas loģika."""
        strategies = []
        for length in range(2, len(indicators) + 1):
            for combo in combinations(indicators, length):
                X = df.dropna()[list(combo)]
                y = (df["close"].pct_change().shift(-1) > 0).astype(int)
                if y.isnull().any():
                    continue
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                acc = accuracy_score(y_test, model.predict(X_test))
                if acc > 0.62:
                    strategies.append({"indicators": combo, "accuracy": acc})
        if strategies:
            best_strategy = max(strategies, key=lambda x: x["accuracy"])
            print(f"✅ {symbol}: Best Strategy -> {best_strategy}")
        else:
            print(f"❌ {symbol}: No strategy exceeded 62%.")

    symbols = test_api()
    if not symbols:
        return
    BINANCE_BASE_URL = "https://api.binance.com"
    
    for symbol in symbols:
        print(f"Backtesting {symbol}...")
        url = f"{BINANCE_BASE_URL}/api/v3/klines"
        params = {"symbol": symbol, "interval": "5m", "limit": 500}
        response = requests.get(url, params=params)
        df = pd.DataFrame(response.json(), columns=[
            "open_time", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ]).astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        df = add_indicators(df)
        await backtest(df, symbol)