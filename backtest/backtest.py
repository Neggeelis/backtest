import pandas as pd
import numpy as np
from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer
from deepseek_analysis.deepseek_code_optimizer import DeepSeekCodeOptimizer
import backtest.indicators as ind  

class Backtest:
    def __init__(self):
        self.optimizer = DeepSeekOptimizer()
        self.code_optimizer = DeepSeekCodeOptimizer()

    def run_backtest(self, df: pd.DataFrame):
        """AI optimizē stratēģiju un pielāgo indikatorus, ja win rate < 65%"""
        
        # ✅ 1. Aprēķina indikatorus
        df["rsi"] = ind.calculate_rsi(df["close"])
        df["macd"], df["macd_signal"] = ind.calculate_macd(df["close"])

        # ✅ 2. AI ģenerē stratēģiju
        optimized_strategy = self.optimizer.optimize_strategy(df)

        # ✅ 3. Integrē AI signālus
        df["ai_signal"] = optimized_strategy["signal"]
        df["final_signal"] = np.where(df["ai_signal"] != 0, df["ai_signal"], df["rsi"] < 30)

        df["pnl"] = df["final_signal"].shift(1) * df["close"].pct_change()
        total_pnl = df["pnl"].sum()
        win_rate = (df["pnl"] > 0).mean() * 100

        # ✅ 4. Ja win rate < 65%, AI refaktorē stratēģiju
        if win_rate < 65:
            optimized_strategy_code = self.code_optimizer.refactor_strategy(str(optimized_strategy))
            exec(optimized_strategy_code, globals())

        return {"total_pnl": total_pnl, "win_rate": win_rate}
