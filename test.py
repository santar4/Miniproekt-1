import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from main import app, url

client = TestClient(app)


@pytest.mark.anyio
async def test_url_parsing():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/url_parsing/", params={"url": url})
    assert response.status_code == 200
    assert list(response.json().keys()) == ["title", "urls"]
    assert response.json()["title"] == "JSONPlaceholder - Free Fake REST API"

@pytest.mark.anyio
async def test_error_url_parsing():
    url = "hps://jsonplaceholder.typicode.com/"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/url_parsing/", params={"url": url})
    assert response.status_code == 200
