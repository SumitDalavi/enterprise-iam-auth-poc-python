import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app as src_app, create_access_token as src_create_token
from app.main import app as app_app, Base
import app.db as db_module
from app.core import security
from app.models import schemas, user as user_models

# --- src.main tests ---
src_client = TestClient(src_app)

def test_src_login():
    res = src_client.post("/token", data={"username": "admin", "password": "password123"})
    assert res.status_code == 200
    assert "access_token" in res.json()

    res = src_client.post("/token", data={"username": "admin", "password": "wrong"})
    assert res.status_code == 400

    res = src_client.post("/token", data={"username": "unknown", "password": "wrong"})
    assert res.status_code == 400

def test_src_users_me():
    token = src_create_token({"sub": "admin", "role": "admin"})
    res = src_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "admin"

    res = src_client.get("/users/me", headers={"Authorization": "Bearer invalid"})
    assert res.status_code == 401

    token2 = src_create_token({"role": "admin"})
    res = src_client.get("/users/me", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 401

def test_src_admin_dashboard():
    token = src_create_token({"sub": "admin", "role": "admin"})
    res = src_client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

    token2 = src_create_token({"sub": "user", "role": "user"})
    res = src_client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 403


# --- app tests ---

from sqlalchemy.pool import StaticPool
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app_app.dependency_overrides[db_module.get_db] = override_get_db

app_client = TestClient(app_app)

def test_app_db():
    gen = db_module.get_db()
    db = next(gen)
    assert db is not None
    try:
        next(gen)
    except StopIteration:
        pass

def test_app_auth_routes():
    # Register
    res = app_client.post("/api/v1/auth/register", json={"email": "test@test.com", "password": "test"})
    assert res.status_code == 201
    
    # Duplicate register
    res = app_client.post("/api/v1/auth/register", json={"email": "test@test.com", "password": "test"})
    assert res.status_code == 400

    # Login
    res = app_client.post("/api/v1/auth/login", data={"username": "test@test.com", "password": "test"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    
    # Bad login
    res = app_client.post("/api/v1/auth/login", data={"username": "test@test.com", "password": "bad"})
    assert res.status_code == 401

    res = app_client.post("/api/v1/auth/login", data={"username": "bad@test.com", "password": "bad"})
    assert res.status_code == 401

def test_app_security():
    hash = security.get_password_hash("hello")
    assert security.verify_password("hello", hash)
    assert not security.verify_password("world", hash)

    # create token with expiry
    token = security.create_access_token("sub1", ["admin"], expires_delta=timedelta(seconds=1))
    assert token is not None

def test_app_sso_routes():
    res = app_client.get("/api/v1/sso/login/oauth2/google", follow_redirects=False)
    assert res.status_code == 307
    
    res = app_client.get("/api/v1/sso/login/oauth2/invalid", follow_redirects=False)
    assert res.status_code == 400

    res = app_client.get("/api/v1/sso/callback?provider=google&code=123")
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_app_endpoints():
    # users me - invalid token
    res = app_client.get("/api/v1/users/me", headers={"Authorization": "Bearer bad_token"})
    assert res.status_code == 401

    # users me - good token
    token = security.create_access_token("test@test.com", ["user"])
    res = app_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["user"] == "test@test.com"
    
    # missing sub in token
    import jwt
    from app.core.config import settings
    bad_token = jwt.encode({"roles": ["user"]}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    res = app_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {bad_token}"})
    assert res.status_code == 401

    # admin dashboard - good token (no admin role)
    res = app_client.get("/api/v1/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403

    # admin dashboard - good token (admin role)
    token2 = security.create_access_token("test@test.com", ["admin"])
    res = app_client.get("/api/v1/admin/dashboard", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 200
