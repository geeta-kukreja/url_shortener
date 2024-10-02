from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from uuid import uuid4
from database import save_url, get_url, setup_indexes, delete_url,custom_url_exists
from utils import generate_short_url, validate_custom_short_code
import validators
from redis_client import get_redis, close_redis, set_redis, get_redis_value, delete_redis_key, redis_key_exists


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
        existing_url = await get_redis_value(short_url)
        if not existing_url:
            collision = False
        attempts += 1
    if collision:
        return {"error": "Failed to generate a unique short URL after multiple attempts."}

    await set_redis(short_url, request.url)  # Cache for 1 hour
    await save_url(uuid_str,short_url, request.url)

    return {"short_url": f"{BASE_URL}/r/{short_url}"}


class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    url = await get_redis_value(short_url)

    if not url:
        url = await get_url(short_url)
        if url:
            await set_redis(short_url, url)   # Re-cache for another hour

    if url:
        return RedirectResponse(url)
    else:
        raise HTTPException(status_code=404, detail="URL not found")

@app.delete("/url/{short_code}")
async def delete_url_endpoint(short_code: str):
    result = await delete_url(short_code)
    if result == False:
        raise HTTPException(status_code=404, detail="URL not found")
    await delete_redis_key(short_code)
    return {"status": "success", "message": "URL deleted successfully"}

@app.get("/")
async def index():
    return "Your URL Shortener is running!"

class CustomShortenRequest(BaseModel):
    url: str
    custom_short_code: str

@app.post("/url/custom-shorten")
async def custom_shorten(request: CustomShortenRequest):
    if not validators.url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    if not validate_custom_short_code(request.custom_short_code):
        raise HTTPException(status_code=400, detail="Short code must be 6-10 characters long and only contain alphanumeric characters")

    in_redis = await redis_key_exists(request.custom_short_code)
    in_db = await custom_url_exists(request.custom_short_code) if not in_redis else True

    if in_redis or in_db:
        raise HTTPException(status_code=409, detail="Custom short code already in use")

    try:
        uuid_str = str(uuid4())
        await save_url(uuid_str, request.custom_short_code, request.url)
        await set_redis(request.custom_short_code, request.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"short_url": f"{BASE_URL}/r/{request.custom_short_code}"}
