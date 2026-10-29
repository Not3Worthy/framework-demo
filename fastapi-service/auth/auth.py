import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Your Entra ID Tenant and Client details
AZURE_TENANT_ID = "your-tenant-id.onmicrosoft.com"
AZURE_CLIENT_ID = "your-client-id-guid"
ISSUER = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
AUDIENCE = AZURE_CLIENT_ID

async def verify_msal_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        # Decode and validate claims (for local testing, signature verification can be optional or checked against JWKS)
        payload = jwt.decode(
            token,
            options={"verify_signature": False},  # Flip to True and validate with Microsoft JWKS public keys in production
            audience=AUDIENCE,
            issuer=ISSUER
        )
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )