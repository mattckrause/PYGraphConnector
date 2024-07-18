import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

load_dotenv()

credential = ClientSecretCredential(os.environ.get("_TENANTID"),
                                    os.environ.get("_APPID"),
                                    os.environ.get("_CLIENTKEY"),
                                    connection_verify=False)
scopes = ['https://graph.microsoft.com/.default']

graph_client = GraphServiceClient(credentials=credential, scopes=scopes)