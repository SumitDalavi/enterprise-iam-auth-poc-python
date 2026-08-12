from fastapi import FastAPI, Depends
from .auth import routes as auth_routes
from .sso import routes as sso_routes
from .rbac.dependencies import RoleChecker, get_current_user_claims
from .db import engine, Base
from .core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Identity and Access Management (IAM) Proof of Concept.",
    version="1.0.0"
)

# Register Domain Routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(sso_routes.router, prefix="/api/v1/sso", tags=["Single Sign-On (Mock)"])

# Secure Endpoint Example
allow_admin_only = RoleChecker(["admin"])

@app.get("/api/v1/admin/dashboard", dependencies=[Depends(allow_admin_only)], tags=["Admin"])
def get_admin_dashboard():
    """
    This endpoint is protected by RBAC. Only users with the 'admin' role can access it.
    """
    return {"message": "Welcome to the highly secure admin dashboard."}

@app.get("/api/v1/users/me", tags=["Users"])
def get_current_user_info(claims: dict = Depends(get_current_user_claims)):
    """
    This endpoint requires a valid JWT but any role is allowed.
    """
    return {"user": claims.get("sub"), "roles": claims.get("roles")}
