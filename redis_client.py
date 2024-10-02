import aioredis

redis = None  # Global Redis connection object

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url("redis://url_shortener_redis:6379", encoding="utf-8", decode_responses=True)
    return redis

async def close_redis():
    global redis
    if redis is not None:
        await redis.close()
        redis = None
