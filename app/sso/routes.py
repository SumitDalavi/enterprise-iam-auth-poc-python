from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import uuid
from ..core import security

router = APIRouter()

# In a real enterprise system, this simulates the OIDC/SAML redirection logic
@router.get("/login/oauth2/{provider}")
def sso_login(provider: str):
    """
    Simulates redirecting the user to an external identity provider (IdP).
    """
    if provider not in ["google", "okta", "azure"]:
        raise HTTPException(status_code=400, detail="Unsupported SSO provider")
    
    # Simulate a callback URL logic
    callback_url = f"/api/v1/sso/callback?provider={provider}&code={uuid.uuid4().hex}"
    return RedirectResponse(url=callback_url)

@router.get("/callback")
def sso_callback(provider: str, code: str):
    """
    Simulates the IdP returning the user to our system with an authorization code.
    We "exchange" the code for a JWT.
    """
    # Mocking user data retrieved from provider
    mock_email = f"sso_user_{provider}@enterprise.local"
    mock_roles = ["user", "sso_federated"]
    
    # Generate our internal JWT for this federated user
    access_token = security.create_access_token(subject=mock_email, roles=mock_roles)
    return {
        "message": f"Successfully authenticated via {provider}",
        "access_token": access_token, 
        "token_type": "bearer",
        "roles": mock_roles
    }
