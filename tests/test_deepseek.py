import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'deepseek_analysis')))

import pytest
import pandas as pd
from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer

@pytest.mark.asyncio
async def test_deepseek_optimization():
    """
    Pārbauda, vai DeepSeek AI optimizācijas algoritms darbojas pareizi.
    """
    optimizer = DeepSeekOptimizer()
    
    df = pd.DataFrame({
        "close": [50000, 50500, 51000, 50000, 49500, 49000, 48500, 48000, 47500, 47000],
        "high": [50200, 50700, 51200, 50200, 49700, 49200, 48700, 48200, 47700, 47200],
        "low": [49800, 50300, 50800, 49800, 49300, 48800, 48300, 47800, 47300, 46800],
        "volume": [1200, 1500, 1700, 1400, 1300, 1600, 1550, 1420, 1380, 1250]
    })

    optimized_strategy = optimizer.optimize_strategy(df)

    assert isinstance(optimized_strategy, dict), "❌ `optimize_strategy` jāatgriež vārdnīca!"
    assert "BUY" in optimized_strategy or "SELL" in optimized_strategy or "HOLD" in optimized_strategy, "❌ Stratēģijas rezultāts nav derīgs!"
    
    print(f"✅ DeepSeek optimizācija veiksmīga! Stratēģija: {optimized_strategy}")