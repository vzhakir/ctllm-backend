import aiohttp
import json

class OllamaAsyncClient:
    def __init__(self, host="http://localhost:11434"):
        self.host = host

    async def generate(self, prompt: str, model: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/api/generate",
                json={"prompt": prompt, "model": model}
            ) as resp:
                return await resp.json()

    async def generate_stream(self, prompt: str, model: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/api/generate",
                json={"prompt": prompt, "model": model},
                timeout=None
            ) as resp:

                async for line in resp.content:
                    try:
                        data = json.loads(line.decode())
                        if "response" in data:
                            yield data["response"]
                    except json.JSONDecodeError:
                        continue

    async def generate_json(self, payload: dict, model: str):
        payload["model"] = model
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.host}/api/generate", json=payload) as resp:
                return await resp.json()

    async def embed(self, payload: dict, model: str):
        payload["model"] = model
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.host}/api/embeddings", json=payload) as resp:
                return await resp.json()