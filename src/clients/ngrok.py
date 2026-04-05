import asyncio

import httpx


async def get_ngrok_public_url(ngrok_api: str = "http://ngrok:4040", retries: int = 30) -> str:
    await asyncio.sleep(3)
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ngrok_api}/api/tunnels")
                response.raise_for_status()
                tunnels = response.json()["tunnels"]
                https = next((t for t in tunnels if t["proto"] == "https"), None)
                if https:
                    return https["public_url"]
        except Exception:
            pass
        await asyncio.sleep(2)
    raise RuntimeError("ngrok tunnel not available after retries")
