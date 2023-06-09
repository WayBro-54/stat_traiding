import asyncio
import os 

from binance import AsyncClient, BinanceSocketManager
from dotenv import load_dotenv

# from .constants import BARS, TF

load_dotenv()

in_symbols = (
    # 1 символ,  второй,   ТФ,   количество баров
    ('BTCUSDT', 'ETHUSDT', '1h', 200),
    ('SOLUSDT', 'TRXUSDT', '1h', 200),
)

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')


async def async_get_historical_klines(symbols: tuple, cl: AsyncClient):
    """Получаем данные о монетах из кортежа."""
    result_1 = await cl.get_historical_klines(symbols[0], interval=symbols[2], limit=symbols[3])
    result_2 = await cl.get_historical_klines(symbols[1], interval=symbols[2], limit=symbols[3])
    print('Работу закончил')
    return result_1, result_2

async def get_price_symbol(symbols: tuple, bm: BinanceSocketManager, tf: str):
    print(symbols)
    ts_p = bm.kline_futures_socket(symbols, interval=tf)
    async with ts_p as tsbm:
        while True:
            res = await tsbm.recv()
            print(res)


async def main(cl: AsyncClient):
    """ Основаная функция проекта"""
    bm = BinanceSocketManager(cl)                             # Создали экземпляр вебсокета

    tasks_kline = [                                           # Создали список тасков
        (loop.create_task(
            async_get_historical_klines(symbols, cl),         # Перебираем кортеж in_symbols  
        )) for symbols in in_symbols if in_symbols
    ]
    kline_symbol_bars = [await task for task in tasks_kline]  # Запускаем таски

    price_symbol = [
        get_price_symbol(
            symbol, bm, symbols[2]
        ) for symbols in in_symbols 
            for symbol in symbols[:2]
                if in_symbols
    ]



if __name__ == '__main__':
    cl = AsyncClient(api_key=API_KEY, api_secret=SECRET_KEY)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(cl))
