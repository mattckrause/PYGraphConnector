import os
from AZCreds import get_secrets
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

class CreateClient:
    @staticmethod
    async def create_with_client_Secret(tenantID) -> GraphServiceClient:
        print("Creating client with client secret")
        appID, clientSec = get_secrets()

        credential = ClientSecretCredential(tenantID,
                                            appID,
                                            clientSec,
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
        return graph_client


if __name__ == "__main__":
    CreateClient.create_with_client_Secret()