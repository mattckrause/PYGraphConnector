import httpx
from graph_client import graph_client

async def extract_objects():
    url = "https://mkdemoapi.com/objects"
    async with httpx.AsyncClient(verify=False) as client:
        object_response = await client.get(url)
    json_content = object_response.json()

    return json_content
