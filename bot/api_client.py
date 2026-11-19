"""How the bot talks to the API. Every feature uses the shared `api` object:

    resp = await api.get("/leaderboard", limit=10, period="week")
    resp = await api.post("/spots", json={...})

    resp.status_code   # 200, 201, 400, 404, 409, ...
    resp.json()        # the body as Python lists/dicts

This file only *sends* requests. Receiving Discord messages is discord.py's job,
in bot/features/. Deciding things is the API's job, in api/routers/.

It uses httpx's async client (not `requests`) so waiting for the API doesn't
freeze the whole bot.
"""

import httpx

from bot import config


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10)

    async def get(self, path: str, **params) -> httpx.Response:
        return await self._client.get(path, params=params)

    async def post(self, path: str, json: dict) -> httpx.Response:
        return await self._client.post(path, json=json)

    async def close(self) -> None:
        await self._client.aclose()


api = ApiClient(config.API_BASE_URL)
