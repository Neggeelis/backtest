import os
import requests
from dotenv import load_dotenv

# Ielādē .env failu
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """Nosūta testa ziņu uz Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Telegram ziņa nosūtīta veiksmīgi!")
        print(response.json())
    else:
        print("❌ Telegram nosūtīšana neizdevās:", response.status_code, response.text)

if __name__ == "__main__":
    send_telegram_message("🚀 Testa ziņa no Trading Bot!")
