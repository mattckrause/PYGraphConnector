import asyncio
from external_service import extract_objects

objects = asyncio.run(extract_objects())
print(objects)