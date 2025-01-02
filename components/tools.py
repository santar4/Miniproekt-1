import httpx
from fastapi.exceptions import HTTPException


async def get_html(url) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(404, detail=f"incorrect url: {url}: status code={response.status_code}")

        elif 'text/html' not in response.headers['content-type']:
            raise HTTPException(404, detail=f"incorrect content-type: {url}: {response.headers['content-type']}")
        return response.text



