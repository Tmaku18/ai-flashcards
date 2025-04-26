from fastapi.testclient import TestClient

def test_health_endpoint(client: TestClient):
    """Test that the health endpoint returns a 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint(client: TestClient):
    """Test that the root endpoint returns a 200 status code."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
