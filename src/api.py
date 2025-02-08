import os
import requests
from dotenv import load_dotenv

def load_api_keys():
    """Ielādē API un Telegram atslēgas no .env faila."""
    load_dotenv()
    keys = {
        "MEXC_API_KEY": os.getenv("MEXC_API_KEY"),
        "MEXC_API_SECRET": os.getenv("MEXC_API_SECRET"),
        "BYBIT_API_KEY": os.getenv("BYBIT_API_KEY"),
        "BYBIT_API_SECRET": os.getenv("BYBIT_API_SECRET"),
        "BINANCE_API_URL": os.getenv("BINANCE_API_URL"),  # Tikai publiskai piekļuvei
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    }
    
    # Pārbauda, vai MEXC API ir pieejams (Binance nav nepieciešams)
    if not keys["MEXC_API_KEY"] or not keys["MEXC_API_SECRET"]:
        raise ValueError("❌ MEXC_API_KEY vai MEXC_API_SECRET nav iestatīti! Pārbaudi .env failu.")

    return keys

def get_binance_data(endpoint):
    """Iegūst publiskos datus no Binance API."""
    keys = load_api_keys()
    url = f"{keys['BINANCE_API_URL']}{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Binance API kļūda: {e}")
        return None

# Piemērs: iegūt Binance BTC/USDT cenu
if __name__ == "__main__":
    print("✅ API atslēgas ielādētas veiksmīgi!")
    btc_price = get_binance_data("/api/v3/ticker/price?symbol=BTCUSDT")
    print("BTC cena no Binance:", btc_price)
