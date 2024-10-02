from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://practicegr17:GYBI6J3idUPaaCL2@urlshortener.i8u0d.mongodb.net/?retryWrites=true&w=majority&appName=URLShortener')
client = MongoClient(MONGO_URI)
# client = AsyncIOMotorClient(MONGO_URI)
db = client.url_shortener

async def save_url(uuid,short_code, long_url):
    db.urls.insert_one({"id": uuid,"short_code": short_code, "long_url": long_url})

async def get_url(short_code):
    url_entry = db.urls.find_one({"short_code": short_code})
    return url_entry["long_url"] if url_entry else None