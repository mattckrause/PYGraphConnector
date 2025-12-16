import trio
from graph_client import CreateClient
from graph_config import create_external_connection, create_schema, write_objects, remove_external_connection
from external_service import extract_objects

#load_dotenv()
# suppress warnings when working locally with Dev Proxy
import urllib3
urllib3.disable_warnings()

id='RandomObjectSearch'
name='Random Object Search'
description='Random object search. Providing object description, a fun fact about the object, and a link to the wikipedia page for the object.'
#tenantID='7b2828b9-89a3-4507-9e1a-05ff46d1192d' #<-- my tenant
#tenantID = '5174ceb7-3102-4916-9c26-eb94f327f56d' #<-- testtest tenant
tenantID = 'd0457b46-1341-4bad-87d7-a888c2742683' #<- My CDX


async def main() -> None:
    process = "remove"
    if process == "remove":
        graph_client = await CreateClient.create_with_client_Secret(tenantID)
        await remove_external_connection(id, graph_client)
        print("External connection removed successfully")
        return
    else:
        graph_client = await CreateClient.create_with_client_Secret(tenantID)
        await create_external_connection(id, name, description,tenantID, graph_client)
        await create_schema(id, graph_client)
        await write_objects(id, await extract_objects(), graph_client)

if __name__ == "__main__":
    trio.run(main) 