#getting app secrets from azure keyvault
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secrets():
    keyVaultName = "mkrandomobjectGC"
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    print(f"loading secrets from from {keyVaultName}")
    appID = client.get_secret("appID")
    clientSec = client.get_secret("clientSecret")
    return appID.value, clientSec.value

if __name__ == "__main__":
    get_secrets()