import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from backtest import Backtest

@pytest.mark.parametrize("test_data", [
    pd.DataFrame({
        "close": [50000, 50500, 51000, 50000, 49500, 49000, 48500, 48000, 47500, 47000],
        "high": [50200, 50700, 51200, 50200, 49700, 49200, 48700, 48200, 47700, 47200],
        "low": [49800, 50300, 50800, 49800, 49300, 48800, 48300, 47800, 47300, 46800],
        "volume": [1200, 1500, 1700, 1400, 1300, 1600, 1550, 1420, 1380, 1250]
    })
])
def test_backtest_run(test_data):
    """
    Pārbauda, vai backtest skripts darbojas bez kļūdām un ģenerē rezultātus.
    """
    backtest = Backtest()
    result = backtest.run_backtest(test_data)

    assert isinstance(result, dict), "❌ Rezultātam jābūt vārdnīcai"
    assert "total_pnl" in result, "❌ `total_pnl` trūkst rezultātos!"
    assert "win_rate" in result, "❌ `win_rate` trūkst rezultātos!"
    assert "optimized_strategy" in result, "❌ `optimized_strategy` trūkst rezultātos!"

    # ✅ Pārbaude, vai indikatori tika aprēķināti