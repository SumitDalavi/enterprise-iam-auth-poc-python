import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/token", data={"username": "user", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/token", data={"username": "user", "password": "wrong"})
    assert response.status_code == 400

def test_protected_route():
    # Login
    token_resp = client.post("/token", data={"username": "user", "password": "password123"})
    token = token_resp.json()["access_token"]
    
    # Access protected
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "user"

def test_rbac_admin_route_forbidden():
    # Login as regular user
    token_resp = client.post("/token", data={"username": "user", "password": "password123"})
    token = token_resp.json()["access_token"]
    
    # Attempt to access admin route
    response = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_rbac_admin_route_success():
    # Login as admin
    token_resp = client.post("/token", data={"username": "admin", "password": "password123"})
    token = token_resp.json()["access_token"]
    
    # Attempt to access admin route
    response = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
