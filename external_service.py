import json
import requests

def extract_objects():
	# url = "http://localhost:3000/objects"
	url = "https://mkdemoapi.com/objects"

	object_response = requests.get(url, verify=False)
	json_content = object_response.json()

	return json_content

#def write_objects(json_data):
#	for i in json_data:
#		#write to schem in Graph