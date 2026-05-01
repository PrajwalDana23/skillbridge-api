from tests.conftest import client
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_signup_login():
    response = client.post("/auth/signup", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "123456",
        "role": "student"
    })

    assert response.status_code == 200

    login = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "123456"
    })

    assert login.status_code == 200
    assert "access_token" in login.json()