from tests.conftest import client
def test_monitoring_post_blocked():
    response = client.post("/monitoring/attendance")
    assert response.status_code == 405