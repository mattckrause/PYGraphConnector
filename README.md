
# PYGraphConnector

An example Python-based Microsoft Graph Connector.

## Overview
This connector creates an external connection to Microsoft Graph that indexes object data (names, descriptions, and Wikipedia links) from a mocked REST API. The indexed content becomes searchable across Microsoft 365 applications like Copilot, SharePoint, Teams, and Outlook. The connector uses mocked APIs for development and testing, either through Microsoft Dev Proxy, Mockoon, or othe equivelant solutions.

## Prerequisites
- Python 3.8 or higher
- Microsoft 365 tenant with appropriate permissions
- Azure App Registration with Microsoft Graph permissions
- Azure Key Vault for storing credentials
- Microsoft Dev Proxy OR Mockoon for API mocking

## Azure Setup

### 1. Create Azure App Registration
1. Navigate to [Azure Portal](https://portal.azure.com)
2. Go to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: PYGraphConnector (or your preferred name)
   - **Supported account types**: Single tenant
   - **Redirect URI**: Not required for this application
5. Note the **Application (client) ID** and **Directory (tenant) ID**

### 2. Configure App Permissions
1. In your app registration, go to **API permissions**
2. Add the following Microsoft Graph **Application permissions**:
   - `ExternalConnection.ReadWrite.OwnedBy`
   - `ExternalItem.ReadWrite.OwnedBy`
   - `User.Read.All` (for user mapping functionality)
3. Click **Grant admin consent** for your organization

### 3. Create Client Secret
1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add description and set expiration
4. Copy the secret **Value** (you won't be able to see it again)

### 4. Setup Azure Key Vault
1. Create a new Key Vault in Azure Portal
2. Update the `keyVaultName` variable in [AZCreds.py](AZCreds.py) to match your Key Vault name
3. Add the following secrets to your Key Vault:
   - `appID`: Your Application (client) ID
   - `clientSecret`: Your client secret value
4. Ensure your identity has **Key Vault Secrets User** role on the Key Vault

## Local Development Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd PYGraphConnector
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Authentication
Ensure you're authenticated to Azure using one of these methods:
- Azure CLI: `az login`
- Visual Studio: Sign in with your Azure account
- Environment variables: Set `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
- Managed Identity (when running on Azure resources)

### 4. Update Configuration
1. Open [main.py](main.py)
2. Update the `tenantID` variable with your Microsoft 365 tenant ID
3. Optionally modify the connector `id`, `name`, and `description` variables

### 5. Setup Mocked API

Choose one of the following options to set up a mocked API:

#### Option A: Microsoft Dev Proxy

1. **Install Dev Proxy**
   ```bash
   # Install globally
   npm install -g @microsoft/dev-proxy
   
   # Or using winget (Windows)
   winget install Microsoft.DevProxy
   ```

2. **Start Dev Proxy**
   ```bash
   # Navigate to project directory
   cd PYGraphConnector
   
   # Start Dev Proxy (uses devproxyrc.json configuration)
   devproxy
   ```

3. **Update API URL**
   In [external_service.py](external_service.py), update the URL to:
   ```python
   url = "https://mkdemoapi.com/objects"
   ```

#### Option B: Mockoon

1. **Install Mockoon**
   - Download from [mockoon.com](https://mockoon.com/)
   - Or install CLI: `npm install -g @mockoon/cli`

2. **Import Mock Configuration**
   - Open Mockoon
   - Import [.apimock/mockAPI.json](.apimock/mockAPI.json)
   - Start the mock server (default port 3000)

3. **Update API URL**
   In [external_service.py](external_service.py), update the URL to:
   ```python
   url = "http://localhost:3000/objects"
   ```

#### Expected JSON Response Structure

Both mock configurations return data in this format:
```json
[
  {
    "ID": 1,
    "Name": "Object Name",
    "Description": "Object description",
    "FunFact": "Interesting fact about the object",
    "WikipediaLink": "https://en.wikipedia.org/wiki/..."
  }
]
```

## Running the Connector

### Create/Update External Connection

1. In [main.py](main.py), set `process = "create"` (or comment out the remove section)
2. Run the application:
   ```bash
   python main.py
   ```

### Remove External Connection

1. In [main.py](main.py), set `process = "remove"`
2. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

- **main.py**: Entry point and orchestration logic
- **AZCreds.py**: Azure Key Vault integration for credential management
- **graph_client.py**: Microsoft Graph client initialization
- **graph_config.py**: External connection and schema configuration
- **external_service.py**: External API data extraction and user mapping
- **graph_middleware.py**: Custom middleware for Graph requests
- **devproxyrc.json**: Configuration for Dev Proxy
- **requirements.txt**: Python dependencies
- **.apimock/mockAPI.json**: Mockoon configuration file with sample data
- **.apimock/objects-api.json**: Alternative mock configuration

## Schema Definition

The connector creates the following searchable properties:
- **Name**: Object name (queryable, searchable, retrievable)
- **Description**: Object description (queryable, searchable, retrievable)
- **URL**: Wikipedia link (retrievable)

## Deployment Options

### Azure Container Instances

1. Create a Dockerfile:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. Build and push to Azure Container Registry
3. Deploy to Azure Container Instances with Managed Identity

### Azure Functions

1. Convert main logic to Azure Function triggers
2. Use Timer Trigger for periodic indexing
3. Configure Application Settings for tenant ID and Key Vault access

### Azure App Service

1. Deploy as a web job or background service
2. Configure Managed Identity for Key Vault access
3. Set up application settings for configuration

## Monitoring and Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify Key Vault access and app permissions
2. **Connection Creation Failed**: Check Microsoft Graph permissions and tenant ID
3. **Mock API Connection Issues**: 
   - Ensure Dev Proxy or Mockoon is running
   - Verify the correct URL in [external_service.py](external_service.py)
   - Check port availability (default: 3000 for Mockoon)
4. **Dev Proxy Issues**: Ensure devproxyrc.json configuration is correct
5. **SSL Certificate Issues**: Use `verify=False` in httpx client for local development

### Logging
The application provides console output for:
- External connection creation/removal status
- Schema deployment progress
- Object indexing results
- Error messages with stack traces

### Mock API Development

#### Dev Proxy Configuration
The project includes [devproxyrc.json](devproxyrc.json) configured to:
- Mock API calls to `https://mkdemoapi.com/*`
- Use CrudApiPlugin for RESTful operations
- Serve data from [.apimock/objects-api.json](.apimock/objects-api.json)

#### Mockoon Configuration
The [.apimock/mockAPI.json](.apimock/mockAPI.json) file contains:
- Sample object data with 10 predefined items
- Proper response structure for the Graph Connector
- HTTP GET endpoint at `/objects`

#### Switching Between Mock Tools
To switch between Dev Proxy and Mockoon:
1. Update the URL in [external_service.py](external_service.py)
2. Start your preferred mock tool
3. Restart the Graph Connector application

## Security Considerations
- Store all secrets in Azure Key Vault
- Use Managed Identity when possible
- Regularly rotate client secrets
- Apply principle of least privilege for Graph permissions
- Validate and sanitize external API data

## Contributing
1. Fork the repository
2. Create a feature branch
3. Test your changes locally
4. Submit a pull request with detailed description

## License

[Add your license information here]
