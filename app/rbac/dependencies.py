from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from ..core.config import settings
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user_claims(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return payload
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, claims: dict = Depends(get_current_user_claims)):
        user_roles = claims.get("roles", [])
        
        # Check if the user has at least one of the allowed roles
        has_role = any(role in self.allowed_roles for role in user_roles)
        
        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for the assigned role"
            )
        return claims
