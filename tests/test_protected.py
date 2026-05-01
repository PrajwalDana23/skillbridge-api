from tests.conftest import client

def test_no_token_access():
    response = client.get("/programme/summary")
    assert response.status_code == 401