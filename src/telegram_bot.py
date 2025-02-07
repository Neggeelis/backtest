from telegram import Bot
import os
import logging
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("-1002294913710")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_signal(symbol, signal, message):
    """Sūta signālu uz Telegram."""
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"🚨 **Signāls**: {symbol}\n"
                 f"📊 **Stratēģija**: {signal}\n"
                 f"📝 **Piezīmes**: {message}"
        )
        return True
    except Exception as e:
        logging.error(f"Kļūda, sūtot signālu: {e}")
        return False

async def send_profit_update(hourly_profit, daily_summary):
    """Sūta stundas peļņu un dienas apkopojumu uz Telegram."""
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"🕒 **1h Profits**: {hourly_profit}\n"
                 f"📊 **Daily Summary**: {daily_summary}"
        )
        return True
    except Exception as e:
        logging.error(f"Kļūda, sūtot peļņas atjauninājumu: {e}")
        return False