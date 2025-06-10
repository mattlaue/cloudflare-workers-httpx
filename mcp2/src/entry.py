from workers import Response

import sys

sys.path.insert(0, "/session/metadata/vendor")
sys.path.insert(0, "/session/metadata")

import httpx


async def on_fetch(request):
    async with httpx.AsyncClient() as client:
        res = await client.get("https://www.example.com")
        return Response(res.text)
