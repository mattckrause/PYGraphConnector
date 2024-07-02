import asyncio
import json
from graph_config import get_user
from external_service import extract_objects

#load data
data = extract_objects()
print(data)
asyncio.run(get_user())