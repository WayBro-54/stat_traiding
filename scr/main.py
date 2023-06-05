import asyncio
import os 

from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

async def get_exchange_info_async(cl: AsyncClient = None):
    result = await cl.get_exchange_info()
    print(result)

async def main(cl: AsyncClient):
    task = loop.create_task(get_exchange_info_async(cl))
    await asyncio.wait([task])


if __name__ == '__main__':
    cl = AsyncClient(api_key=API_KEY, api_secret=SECRET_KEY)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(cl))
