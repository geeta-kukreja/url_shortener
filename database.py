from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from fastapi import HTTPException

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = AsyncIOMotorClient(MONGO_URI)
db = client.url_shortener

async def setup_indexes():
    try:
        await db.urls.create_index("short_code", unique=True)
    except PyMongoError as e:
        print(f"Failed to create indexes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to setup database indexes")

async def save_url(uuid, short_code, long_url):
    try:
        await db.urls.update_one(
            {"id": uuid},  
            {"$setOnInsert": {"short_code": short_code, "long_url": long_url}},
            upsert=True
        )
    except PyMongoError as e:
        print(f"Failed to save URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save URL")

async def get_url(short_code):
    try:
        url_entry = await db.urls.find_one({"short_code": short_code})
        return url_entry["long_url"] if url_entry else None
    except PyMongoError as e:
        print(f"Failed to retrieve URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve URL")

async def delete_url(short_code):
    try:
        result = await db.urls.delete_one({"short_code": short_code})
        if result.deleted_count == 0:
            return False
        return True
    except PyMongoError as e:
        print(f"Failed to delete URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete URL")

async def custom_url_exists(short_code):
    try:
        existing_url = await db.urls.find_one({"short_code": short_code})
        return existing_url is not None
    except PyMongoError as e:
        print(f"Failed to check if URL exists: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check if URL exists")
