import asyncio
import json
from graph_config import get_user
from external_service import extract_objects

# suppress warnings when working locally with Dev Proxy
import urllib3
urllib3.disable_warnings()

#load data
data = extract_objects()
print(data)
asyncio.run(get_user())