import deepseek  # Pievienojam DeepSeek-V3 AI modeli
import pandas as pd
from trading.indicators import calculate_indicators


class DeepSeekSignals:
    """AI-based trading signal generator using DeepSeek-V3."""
    
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.model = deepseek.load_model("deepseek-v3")

    def generate_signals(self):
        """Generate BUY/SELL signals using DeepSeek-V3."""
        indicators = calculate_indicators(self.historical_data)
        input_data = indicators.to_dict(orient='records')

        # AI prognozes uz vēsturiskajiem datiem
        predictions = self.model.predict(input_data)
        signals = ["BUY" if pred > 0.5 else "SELL" for pred in predictions]
        return signals
