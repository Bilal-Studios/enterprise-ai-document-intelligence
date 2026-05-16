from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_clear_documents_endpoint_returns_cleared_status():
    response = client.post("/documents/clear")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "cleared"
    assert data["chunks_remaining"] == 0