import requests
from graph_client import graph_client

def extract_objects():
    url = "https://mkdemoapi.com/objects"

    object_response = requests.get(url, verify=False)
    json_content = object_response.json()

    return json_content
