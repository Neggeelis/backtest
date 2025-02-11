import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from api_telegram.order_book import fetch_order_book
import pandas as pd
import matplotlib.pyplot as plt

def generate_chart(data):
    fig, ax = plt.subplots()
    ax.plot(data["time"], data["price"])
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.set_title("Trading Chart")
    return fig  # ✅ Atgriež figūru, nevis `None`


class TestVisualization(unittest.TestCase):
    def test_generate_chart(self):
        data = pd.DataFrame({'timestamp': pd.date_range(start='1/1/2022', periods=10, freq='H'),
                             'close': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        generate_chart(data)
        self.assertTrue(True)  # Just a placeholder for now

if __name__ == "__main__":
    unittest.main()


class TestVisualization(unittest.TestCase):
    def test_generate_chart(self):
        data = {"time": [1, 2, 3], "price": [100, 105, 110]}
        result = generate_chart(data)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
