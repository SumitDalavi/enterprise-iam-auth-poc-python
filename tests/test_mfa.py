"""Tests for TOTP MFA implementation."""
import pytest
from app.mfa.totp import generate_totp_secret, totp, verify_totp, hotp


def test_secret_generation():
    secret = generate_totp_secret()
    assert len(secret) == 32  # 20 bytes base32 = 32 chars
    assert secret.isalnum()


def test_hotp_deterministic():
    secret = "JBSWY3DPEHPK3PXP"
    code1 = hotp(secret, 0)
    code2 = hotp(secret, 0)
    assert code1 == code2
    assert len(code1) == 6


def test_totp_length():
    secret = generate_totp_secret()
    code = totp(secret)
    assert len(code) == 6
    assert code.isdigit()


def test_verify_totp_current():
    secret = generate_totp_secret()
    code = totp(secret)
    assert verify_totp(secret, code)


def test_verify_totp_wrong_code():
    secret = generate_totp_secret()
    assert not verify_totp(secret, "000000")


def test_verify_totp_tolerance():
    """Test that tolerance window accepts slightly old codes."""
    import time
    secret = generate_totp_secret()
    # Generate code for the current step
    step = 30
    counter = int(time.time() // step)
    code = hotp(secret, counter - 1)  # previous step
    assert verify_totp(secret, code, tolerance=1)


def test_provisioning_uri_format():
    from app.mfa.totp import totp_provisioning_uri
    uri = totp_provisioning_uri("JBSWY3DPEHPK3PXP", "user@example.com")
    assert uri.startswith("otpauth://totp/")
    assert "user%40example.com" in uri


def test_scim_create_and_get():
    from fastapi.testclient import TestClient
    from app.scim.routes import router, _users
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    _users.clear()
    resp = client.post("/scim/v2/Users", json={"userName": "test@example.com", "active": True})
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    get_resp = client.get(f"/scim/v2/Users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["userName"] == "test@example.com"


def test_session_create_and_get():
    from app.auth.session import create_session, get_session, delete_session
    token = create_session("user-123", {"role": "admin"})
    assert token is not None
    session = get_session(token)
    assert session["user_id"] == "user-123"
    assert session["role"] == "admin"
    delete_session(token)
    assert get_session(token) is None
