import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deepseek_analysis')))

from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer


def trading_strategy(data):
    """Trading strategy optimized with DeepSeek AI."""
    
    strategy_code = """
    def execute_strategy(data):
        buy_signal = data['rsi'] < 30
        sell_signal = data['rsi'] > 70
        
        return 'BUY' if buy_signal else 'SELL' if sell_signal else 'HOLD'
    """
    
    optimized_strategy = DeepSeekOptimizer().optimize_strategy(data)
    exec(optimized_strategy)  # Pielieto AI uzlaboto stratēģiju
    return execute_strategy(data)

def execute_strategy(data):
    buy_signal = data.get('rsi', 50) < 30
    sell_signal = data.get('rsi', 50) > 70

    if buy_signal:
        return "BUY"
    elif sell_signal:
        return "SELL"
    return "HOLD"
# Izmanto AI uzlaboto stratēģiju