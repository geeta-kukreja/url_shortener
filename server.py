from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from uuid import uuid4
from database import save_url, get_url
from utils import generate_short_url , uuid_to_binary


app = FastAPI()
BASE_URL: str = "http://locahost:5001"

class ShortenRequest(BaseModel):
    url: str

@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.
    """
    collision = True
    attempts = 0
    max_attempts = 5
    while collision and attempts < max_attempts:
        uuid_str = str(uuid4())
        # binary_url = uuid_to_binary(uuid_str)
        short_url = generate_short_url(uuid_str, 6)
        existing_url = await get_url(short_url)
        if not existing_url:
            collision = False
        attempts += 1
    if collision:
        return {"error": "Failed to generate a unique short URL after multiple attempts."}
    await save_url(uuid_str,short_url,request.url)
    # await db.url_generator.insert_one({
    #     "_id": binary_url,
    #     "original_url": request.url,
    #     "short_url": short_url
    # })
    return {"short_url": f"{BASE_URL}/r/{short_url}"}



class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    print(short_url)
    url_entry = await get_url(short_url)
    original_url =  url_entry["long_url"]
    if url_entry:
        return RedirectResponse(original_url)
    raise HTTPException(status_code=404, detail="URL not found")


@app.get("/")
async def index():
    return "Your URL Shortener is running!"


# from flask import Flask, request, redirect, jsonify
# from database import save_url, get_url
# from utils import generate_short_code, is_valid_url

# app = Flask(__name__)

# @app.route('/shorten', methods=['POST'])
# def shorten_url():
#     data = request.get_json()
#     long_url = data.get("long_url")

#     if not long_url or not is_valid_url(long_url):
#         return jsonify({"error": "Invalid URL"}), 400

#     short_code = generate_short_code()
#     save_url(short_code, long_url)

#     return jsonify({"short_code": short_code, "shortened_url": f"http://localhost:5000/{short_code}"}), 201

# @app.route('/<short_code>', methods=['GET'])
# def redirect_url(short_code):
#     long_url = get_url(short_code)

#     if long_url:
#         return redirect(long_url)
#     else:
#         return jsonify({"error": "Short code not found"}), 404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
