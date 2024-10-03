import redis.asyncio as redis
from dotenv import load_dotenv
import os

load_dotenv()

# Global Redis connection object
redis_client = None
REDIS_URL = os.getenv('REDIS_URL')

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis_client

async def close_redis():
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None

async def set_redis(key, value, ttl=3600):
    redis = await get_redis()
    await redis.setex(key, ttl, value)

async def get_redis_value(key):
    redis = await get_redis()
    return await redis.get(key)

async def delete_redis_key(key):
    redis = await get_redis()
    await redis.delete(key)

async def redis_key_exists(key):
    redis = await get_redis()
    return await redis.exists(key)
