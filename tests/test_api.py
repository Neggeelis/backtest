import unittest
from api_telegram.api_helpers import send_request

class TestAPI(unittest.TestCase):
    def test_send_request(self):
        response = send_request("/spot/candlesticks", {"currency_pair": "BTC_USDT", "interval": "1m"})
        self.assertIsInstance(response, list)

if __name__ == '__main__':
    unittest.main()
