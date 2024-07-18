import asyncio
import os
from dotenv import load_dotenv, set_key
from graph_config import create_external_connection, create_schema, write_objects
from external_service import extract_objects

#load_dotenv()
# suppress warnings when working locally with Dev Proxy
import urllib3
urllib3.disable_warnings()

id='MKObjectSearch5'
name='Random Object Search'
description='Random object search. Providing object description, a fun fact about the object, and a link to the wikipedia page for the object.'


if __name__ == '__main__':
    #asyncio.run(create_external_connection(id, name, description))
    asyncio.run(create_schema(id))
    #asyncio.run(write_objects(id, extract_objects()))
