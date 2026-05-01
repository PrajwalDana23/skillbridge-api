from tests.conftest import client

def test_student_attendance():
    login = client.post("/auth/login", json={
        "email": "student@example.com",
        "password": "123456"
    })

    token = login.json()["access_token"]

    response = client.post(
        "/attendance/mark",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "session_id": 1,
            "status": "present"
        }
    )

    assert response.status_code in [200, 403]