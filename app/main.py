import asyncio
import redis

from get_logger import setup_async_logger
from db_orm import Database
from fastapi import FastAPI

app = FastAPI()
red_db = redis.Redis(host='redis', port=6379, decode_responses=True)
db = Database()
logger = setup_async_logger()


@app.get("/api/v1/courses/")
async def root(pair: str = None, source: str = None):
    source = 'binance' if not source else source
    if source not in ['binance', 'coingecko']:
        return {"message": "source not found"}
    items = red_db.hgetall(f'all_prices_{source}') if not pair else {pair: red_db.hget(f'all_prices_{source}', pair)}
    if any(items.values()):  # Если словарь не пустой
        return {
            "exchanger": source,
            "courses": [{"direction": x[0], "value": x[1], "time": red_db.get(f'{x[0]}_{source}_time')} for x in
                        items.items()]

        }
    await logger.info('PAIR NOT FOUND')
    return {'message': 'pair not found'}


@app.on_event('startup')
async def startup():
    Database().create_tables()
