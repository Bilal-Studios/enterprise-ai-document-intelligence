from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_extract_obligations_endpoint_returns_structured_response():
    response = client.post(
        "/extract/obligations",
        json={
            "document_text": (
                "External APIs must use retries with exponential backoff. "
                "Customer data must not be logged in plaintext."
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["obligations"]) == 2
    assert data["obligations"][0]["category"] == "resilience"
    assert data["obligations"][1]["priority"] == "critical"


def test_extract_obligations_endpoint_rejects_short_text():
    response = client.post(
        "/extract/obligations",
        json={"document_text": "too short"},
    )

    assert response.status_code == 422    