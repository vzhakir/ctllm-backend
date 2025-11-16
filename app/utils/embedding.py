async def embed_text(client, text: str, model: str):
    payload = {"prompt": text}
    result = await client.embed(payload, model=model)
    return result.get("embedding", [])