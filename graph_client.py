from AZCreds import get_secrets
from azure.identity import ClientSecretCredential, ManagedIdentityCredential, ClientAssertionCredential
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
    # Create a GraphServiceClient using client secret authentication
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

    @staticmethod
    # Create a GraphServiceClient using managed identity authentication
    async def create_with_managed_identity(miID, tID, appID) -> GraphServiceClient:
        print("Creating client with managed identity")
        print(f"miID: {miID}, tID: {tID}, appID: {appID}")

        def get_managed_identity_token(credential, audience):
            return credential.get_token(audience).token

        credential = ManagedIdentityCredential(client_id=miID)
        client_assertion_credential = ClientAssertionCredential(tID, appID, lambda: get_managed_identity_token(credential,"api://AzureADTokenExchange/.default"))


        scopes = ['https://graph.microsoft.com/.default']

        graph_client = GraphServiceClient(
            client_assertion_credential,
            scopes=scopes)
        return graph_client


if __name__ == "__main__":
    #CreateClient.create_with_client_Secret()
    CreateClient.create_with_managed_identity()