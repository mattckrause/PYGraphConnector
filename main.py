import asyncio
import os
from dotenv import load_dotenv, set_key
from graph_config import create_external_connection, create_schema, write_objects
from external_service import extract_objects

load_dotenv()
# suppress warnings when working locally.
import urllib3
urllib3.disable_warnings()

id='MKRandomObjectSearch03'
name='Random Object Search'
description='Random object search. Providing object description, a fun fact about the object, and a link to the wikipedia page for the object.'

async def main() -> None:
    if os.environ.get("_firstrun") == "true":
        await create_external_connection(id, name, description)
        await create_schema(id)
        set_key('.env', '_firstrun', 'false')
        await write_objects(id, await extract_objects())
        
    else:
        print("writing objects")
        await write_objects(id, await extract_objects())

if __name__ == "__main__":
    asyncio.run(main())
