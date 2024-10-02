from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from uuid import uuid4
from database import save_url, get_url, setup_indexes
from utils import generate_short_url
import validators
from redis_client import get_redis, close_redis


app = FastAPI()
BASE_URL: str = "http://localhost:8000"

@app.on_event("startup")
async def startup_event():
    await get_redis()
    await setup_indexes()

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()

class ShortenRequest(BaseModel):
    url: str

@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
 Given a URL, generate a short version of the URL that can be later resolved to the originally
 specified URL.
 """
    if not validators.url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    collision = True
    attempts = 0
    max_attempts = 5
    short_url = None
    while collision and attempts < max_attempts:
        uuid_str = str(uuid4())
        short_url = generate_short_url(uuid_str, 6)
        redis = await get_redis()
        existing_url = await redis.get(short_url)
        if not existing_url:
            collision = False
        attempts += 1
    if collision:
        return {"error": "Failed to generate a unique short URL after multiple attempts."}

    # Save to Redis and MongoDB
    await redis.setex(short_url, 3600, request.url) # Cache for 1 hour
    await save_url(uuid_str,short_url, request.url)

    return {"short_url": f"{BASE_URL}/r/{short_url}"}

# async def modify_and_check_url(original_short_url, attempt):
#     redis = await get_redis()
#     modified_short_url = f"{original_short_url}{attempt}"
#     existing_url = await redis.get(modified_short_url)
#     if existing_url is None:
#         return modified_short_url
#     return None


class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    redis = await get_redis()
    url = await redis.get(short_url)

    if not url:
        url = await get_url(short_url)
        if url:
            await redis.setex(short_url, 3600, url)  # Re-cache for another hour

    if url:
        return RedirectResponse(url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
