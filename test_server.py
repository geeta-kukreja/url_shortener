import pytest
from httpx import AsyncClient
from server import app  

# Test cases for URL Shortening
@pytest.mark.asyncio
async def test_create_short_url_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/url/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        assert "short_url" in response.json()

@pytest.mark.asyncio
async def test_create_short_url_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/url/shorten", json={"url": "ftp://example.com"})
        assert response.status_code == 400
        assert "detail" in response.json()

# Testing URL Resolution 

@pytest.mark.asyncio
async def test_resolve_existing_short_url():
    # Assuming 'abc123' is a known short URL stored in the database and cache
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/r/abc123")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_resolve_non_existing_short_url():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/r/nonexist123")
        assert response.status_code == 404

# Testing Deletion
@pytest.mark.asyncio
async def test_delete_existing_short_code():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/url/abc123")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_non_existing_short_code():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/url/nonexist123")
        assert response.status_code == 404

# Testing Custom Shorten URL api
@pytest.mark.asyncio
async def test_custom_shorten_valid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/url/custom-shorten", json={"url": "https://example.com", "custom_short_code": "cust123"})
        assert response.status_code == 200
        assert "short_url" in response.json()

@pytest.mark.asyncio
async def test_custom_shorten_already_used():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/url/custom-shorten", json={"url": "https://example.com", "custom_short_code": "cust123"})
        assert response.status_code == 409

@pytest.mark.asyncio
async def test_custom_shorten_invalid_format():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/url/custom-shorten", json={"url": "https://example.com", "custom_short_code": "!nv@lid123"})
        assert response.status_code == 400

