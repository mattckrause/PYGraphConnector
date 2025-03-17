import httpx

async def extract_objects():
    url = "https://mkobjectsapi.azurewebsites.net/api/ObjectsAPI?code=uRMW41xZWP0UMcVFflmtmVlJrzInWXWfmxPC01rcuX-3AzFubidOUw%3D%3D"
    async with httpx.AsyncClient(verify=False) as client:
        object_response = await client.get(url)
    json_content = object_response.json()

    return json_content
