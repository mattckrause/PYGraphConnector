import httpx
import re
from graph_client import CreateClient
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.access_type import AccessType

async def extract_objects():
    url = "https://mkobjectsapi.azurewebsites.net/api/ObjectsAPI?code=uRMW41xZWP0UMcVFflmtmVlJrzInWXWfmxPC01rcuX-3AzFubidOUw%3D%3D"
    async with httpx.AsyncClient(verify=False) as client:
        object_response = await client.get(url)
    json_content = object_response.json()

    return json_content

async def build_acl(user_ids):
    return [
        Acl(
            type=AclType.User,
            value=id,
            access_type=AccessType.Grant,
        )
        for id in user_ids
    ]

async def user_mapping(users, graph_client):
    mapped_users = []
    for user in users:
        upn = re.sub(r'^([a-zA-Z]+)\.([a-zA-Z])[a-zA-Z]*@[\w.-]+$', r'\1\2@1d65k.onmicrosoft.com', user)
        if upn:
            ID = (await graph_client.users.by_user_id(upn).get()).id
            mapped_users.append(ID)
    ctrl_list = await build_acl(mapped_users)
    return ctrl_list
