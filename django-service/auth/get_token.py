import os
import msal

# Your Microsoft Entra ID Configuration
TENANT_ID = os.getenv("AZURE_TENANT_ID", "your-tenant-id.onmicrosoft.com")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "your-client-id-guid")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "your-client-secret-if-confidential")
# For an API scope, it's typically "api://<client-id>/.default" or your exposed scope
SCOPES = [os.getenv("AZURE_SCOPE", f"api://{CLIENT_ID}/.default")]

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

def get_access_token_client_credentials() -> str:
    """Acquires a token using Confidential Client (Client Credentials Flow)."""
    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )
    
    result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        print("Successfully acquired access token!")
        return result["access_token"]
    else:
        raise Exception(f"Could not acquire token: {result.get('error_description', result)}")

def get_access_token_device_code() -> str:
    """Acquires a token interactively using Device Code Flow (great for local CLI testing)."""
    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY
    )
    
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception(f"Failed to create device flow: {flow}")

    print(flow["message"]) # Prints instructions to log in via browser
    
    result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" in result:
        print("Successfully authenticated and acquired access token!")
        return result["access_token"]
    else:
        raise Exception(f"Device flow authentication failed: {result.get('error_description', result)}")

if __name__ == "__main__":
    # Choose the flow matching your Entra ID app registration type
    token = get_access_token_device_code()
    print("\nAccess Token:\n", token)