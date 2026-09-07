import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.security import create_access_token, decode_access_token, get_password_hash, verify_password

client = TestClient(app)

def test_password_hashing():
    pw = "SecretPass123!"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_flow():
    token = create_access_token(data={"sub": "admin", "role": "Administrator"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "admin"
    assert payload["role"] == "Administrator"

def test_auth_login_api():
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "adminpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "Administrator"
