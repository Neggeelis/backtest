import pytest
import asyncio
from api_telegram.telegram_bot import TelegramBot
from dotenv import load_dotenv
import os

# Piespiedu kārtā izmantojam SelectorEventLoop uz Windows
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Ielādējam .env failu un iestatām mainīgos
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", ".env"))
load_dotenv(env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@pytest.mark.asyncio
async def test_send_telegram_message():
    """
    Pārbauda, vai Telegram bots veiksmīgi nosūta ziņu.
    """
    assert TELEGRAM_BOT_TOKEN, "❌ TELEGRAM_BOT_TOKEN nav iestatīts .env failā vai nav pareizi ielādēts."
    assert TELEGRAM_CHAT_ID, "❌ TELEGRAM_CHAT_ID nav iestatīts .env failā vai nav pareizi ielādēts."

    telegram_bot = TelegramBot(token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

    message = "✅ Telegram bot tests veiksmīgi uzsākts!"

    try:
        response = await telegram_bot.send_message(message)

        # 🔹 **Izdrukājam `response` saturu, lai saprastu kļūdu**
        print(f"📌 Telegram API atbilde: {response}")

        assert response is not None, "❌ Telegram API neatgrieza atbildi"
        assert isinstance(response, dict), f"❌ Sagaidīts dict, bet saņemts {type(response)}"
        assert "ok" in response, f"❌ Telegram API neatgrieza `ok` lauku: {response}"
        assert response["ok"] is True, f"❌ Telegram API kļūda: {response}"

        print("✅ Telegram tests izdevies! Ziņa tika veiksmīgi nosūtīta.")
    except Exception as e:
        pytest.fail(f"❌ Kļūda ziņas sūtīšanā: {e}")
