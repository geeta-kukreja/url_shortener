# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
# client = MongoClient(MONGO_URI)
client = AsyncIOMotorClient(MONGO_URI)
db = client.url_shortener

async def save_url(uuid,short_code, long_url):
    db.urls.insert_one({"id": uuid,"short_code": short_code, "long_url": long_url})

async def get_url(short_code):
    url_entry = await db.urls.find_one({"short_code": short_code})
    print(f"MongoDB returned: {url_entry}") 
    if url_entry:
        return url_entry["long_url"]
    return None