import asyncio
import datetime

import redis
import websockets
import json
import aiohttp

from db_orm import Database
from redis import Redis


async def save_price(red_db: Redis, pair: tuple, source):
    red_db.hset(f"all_prices_{source}", mapping={
        pair[0]: pair[1]
    })
    red_db.set(f'{pair[0]}_{source}_time', datetime.datetime.now().__str__())


async def get_binance_price(red_db: Redis, pair: dict):
    while True:
        async with websockets.connect(f"wss://stream.binance.com:9443/ws/{pair['binance_name']}@ticker") as websocket:
            try:
                while True:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    await websocket.pong()
                    data = json.loads(message)
                    price = data['c']
                    await save_price(red_db, (pair['name'], price), 'binance')
                    await asyncio.sleep(1)
            except asyncio.exceptions.TimeoutError:
                pass
            except asyncio.CancelledError:
                return


async def get_coingecko_price(red_db: Redis, pair: dict):
    while True:
        try:
            pair_from, pair_to = pair["coingeko_name"].split('-')
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={pair_from}&vs_currencies={pair_to}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    price = data[pair_from][pair_to]
                    await save_price(red_db, (pair['name'], price), 'coingecko')
            await asyncio.sleep(4)
        except asyncio.CancelledError:
            return
        except:
            pass


async def start_pair_tasks(red_db: Redis, pair: dict):
    await asyncio.gather(get_coingecko_price(red_db, pair), get_binance_price(red_db, pair))


async def main(red_db: Redis, db: Database):  # Update all pair prices
    pairs = db.get_pairs()
    tasks = [asyncio.create_task(start_pair_tasks(red_db, pair)) for pair in pairs]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    red_db = redis.Redis(host='redis', port=6379, decode_responses=True)
    db = Database()
    asyncio.run(main(red_db, db))
