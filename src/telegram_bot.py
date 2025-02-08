from telegram import Bot
import os
import logging
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

def send_signal(symbol, signal, message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"🚨 **Signāls**: {symbol}\n📊 **Stratēģija**: {signal}\n📝 **Piezīmes**: {message}")
    except Exception as e:
        logging.error(f"Telegram sūtīšanas kļūda: {e}")

def send_profit_update(hourly_profit, daily_summary):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"🕒 **1h Profits**: {hourly_profit}\n📊 **Daily Summary**: {daily_summary}")
    except Exception as e:
        logging.error(f"Telegram sūtīšanas kļūda: {e}")
