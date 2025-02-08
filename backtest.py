import pandas as pd
import numpy as np

def backtest_strategy(data):
    """Veic backtest stratēģijai un analizē win rate"""
    wins = 0
    losses = 0
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            wins += 1
        else:
            losses += 1
    win_rate = (wins / (wins + losses)) * 100
    return win_rate >= 65
