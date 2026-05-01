from tests.conftest import client

def test_trainer_create_session():
    login = client.post("/auth/login", json={
        "email": "trainer@example.com",
        "password": "123456"
    })

    token = login.json()["access_token"]

    response = client.post(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "batch_id": 1,
            "title": "Test Session",
            "date": "2026-05-01",
            "start_time": "10:00",
            "end_time": "11:00"
        }
    )

    assert response.status_code == 200