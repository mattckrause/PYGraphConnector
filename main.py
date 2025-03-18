import trio
from graph_config import create_external_connection, create_schema, write_objects
from external_service import extract_objects

#load_dotenv()
# suppress warnings when working locally with Dev Proxy
import urllib3
urllib3.disable_warnings()

id='MKObjectSearch02'
name='Random Object Search'
description='Random object search. Providing object description, a fun fact about the object, and a link to the wikipedia page for the object.'

async def main() -> None:
    await create_external_connection(id, name, description)
    await create_schema(id)
    await write_objects(id, await extract_objects())

if __name__ == "__main__":
    trio.run(main())