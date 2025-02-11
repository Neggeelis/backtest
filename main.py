import asyncio
import sys
import os

# ✅ Pievieno nepieciešamās mapes Python ceļam
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

deepseek_analysis_path = os.path.join(BASE_DIR, "deepseek_analysis")
if deepseek_analysis_path not in sys.path:
    sys.path.append(deepseek_analysis_path)

api_telegram_path = os.path.join(BASE_DIR, "api_telegram")
if api_telegram_path not in sys.path:
    sys.path.append(api_telegram_path)

# ✅ Importē nepieciešamos moduļus
from trading.ai_trading import AITradingBot
from deepseek_analysis.deepseek_optimizer import DeepSeekOptimizer
from api_telegram.telegram_bot import TelegramBot
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def main():
    """ Galvenā funkcija, kas palaiž Trading Botu un Telegram ziņojumus """
    print("🚀 Trading bot tiek palaists...")
    
    trading_bot = AITradingBot()
    optimizer = DeepSeekOptimizer()
    telegram = TelegramBot(token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

    await trading_bot.run()
    await telegram.send_message("✅ Trading bot started!")

if __name__ == "__main__":
    asyncio.run(main())
