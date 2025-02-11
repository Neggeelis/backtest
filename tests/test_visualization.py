import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.visualization import generate_chart
import pandas as pd

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
