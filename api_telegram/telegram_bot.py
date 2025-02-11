import asyncio
import aiohttp
import json

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send_message(self, message):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    response_text = await response.text()
                    print(f"📌 Telegram RAW response: {response_text}")  # 🔹 **Pievienots diagnostikai**
                    return json.loads(response_text)
            except Exception as e:
                print(f"❌ Telegram API kļūda: {e}")
                return None

    async def send_trade_update(self, symbol, win_rate, total_pnl):
        message = f"📊 Trade Update:\nSymbol: {symbol}\nWin Rate: {win_rate:.2f}%\nTotal PnL: {total_pnl:.2%}"
        return await self.send_message(message)
