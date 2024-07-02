import asyncio
import os
from dotenv import load_dotenv
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

load_dotenv()

credential = ClientSecretCredential(os.environ.get("_TENANTID"),
									os.environ.get("_APPID"),
									os.environ.get("_CLIENTKEY"))
scopes = ['https://graph.microsoft.com/.default']

graph_client = GraphServiceClient(credentials=credential, scopes=scopes)
