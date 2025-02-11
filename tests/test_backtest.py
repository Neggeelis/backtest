import pandas as pd
import pytest
from backtest.backtest import Backtest  # ✅ Noņem dublikātu

@pytest.mark.parametrize("test_data", [
    pd.DataFrame({
        "close": [50000, 50500, 51000, 50000, 49500],
        "low": [49800, 50300, 50800, 49800, 49300]
    })
])
def test_backtest_run(test_data):
    """Pārbauda, vai backtest skripts darbojas pareizi."""

    backtest = Backtest(test_data)

    # ✅ Nodrošina, ka `execute_strategy` eksistē
    strategy_code = """
def execute_strategy(row):
    return 'BUY' if row['close'] > row['low'] else 'SELL'
"""

    results = backtest.run(strategy_code)
    
    assert len(results) == len(test_data), "Rezultātu skaits neatbilst ievaddatiem"
    assert all(res in ['BUY', 'SELL'] for res in results), "Rezultāti nav korekti"
