import json
import asyncio

import redis
import websockets


async def get_binance_price():
    async with websockets.connect(f"wss://stream.binance.com:9443/ws/btcrub@ticker") as websocket:
        try:
            while True:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                await websocket.pong()
                data = json.loads(message)
                print(data['c'])
                await asyncio.sleep(1)
        except asyncio.exceptions.TimeoutError:
            print('TimeOut')


# asyncio.run(get_binance_price())

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Сохранение данных
r.hset('all_binance', mapping={
    "BTC": 1
})
r.hset('all_binance', mapping={
    "ETH": 5
})

# Получение данных
value = r.hget('all_binance', 'qweq')
print(value)
