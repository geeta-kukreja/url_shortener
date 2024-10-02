from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://practicegr17:GYBI6J3idUPaaCL2@urlshortener.i8u0d.mongodb.net/?retryWrites=true&w=majority&appName=URLShortener')
# client = MongoClient(MONGO_URI)
client = AsyncIOMotorClient(MONGO_URI)
db = client.url_shortener

async def setup_indexes():
    await db.urls.create_index("short_code", unique=True)

async def save_url(uuid,short_code, long_url):
    await db.urls.update_one(
        {"id": uuid},  
        {"$setOnInsert": {"short_code": short_code, "long_url": long_url}},
        upsert=True
    )

async def get_url(short_code):
    url_entry = db.urls.find_one({"short_code": short_code})
    return url_entry["long_url"] if url_entry else None