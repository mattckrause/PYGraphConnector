import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient, GraphServiceClient, GraphRequestAdapter
from msgraph_core import GraphClientFactory
from graph_middleware import GraphMiddleware
from httpx import AsyncClient, Timeout
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider,)
from kiota_http.kiota_client_factory import (
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_REQUEST_TIMEOUT,
)



load_dotenv()

credential = ClientSecretCredential(os.environ.get("_TENANTID"),
                                    os.environ.get("_APPID"),
                                    os.environ.get("_CLIENTKEY"),
                                    connection_verify=False)
scopes = ['https://graph.microsoft.com/.default']
auth_provider = AzureIdentityAuthenticationProvider(credential)
timeout = Timeout(DEFAULT_REQUEST_TIMEOUT, connect=DEFAULT_CONNECTION_TIMEOUT)
http_client = AsyncClient(timeout=timeout, http2=True)

middleware = GraphClientFactory.get_default_middleware(None)

middleware.insert(0, GraphMiddleware(60000))

http_client = GraphClientFactory.create_with_custom_middleware(
    middleware, client=http_client
)
adapter = GraphRequestAdapter(auth_provider, http_client)

graph_client = GraphServiceClient(
    credential,
    scopes=scopes,
    request_adapter=adapter,
)
