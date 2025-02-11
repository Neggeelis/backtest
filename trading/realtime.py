import asyncio
from api_telegram.api_helpers import send_request

async def get_realtime_price(symbol):
    """
    Iegūst reāllaika tirgus datus no Gate.io API
    """
    params = {"currency_pair": symbol}
    return await asyncio.to_thread(send_request, "/spot/ticker", params)
