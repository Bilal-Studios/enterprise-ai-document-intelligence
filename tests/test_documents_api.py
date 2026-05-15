from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest_document_endpoint_returns_chunk_count():
    response = client.post(
        "/documents/ingest",
        json={
            "document_id": "api-resilience-policy",
            "title": "API Resilience Policy",
            "content": (
                "External API calls must use timeouts.\n\n"
                "Retries should use exponential backoff.\n\n"
                "Fallback providers should be available."
            ),
            "category": "engineering",
            "access_level": "internal",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == "api-resilience-policy"
    assert data["chunks_created"] == 3
    assert data["status"] == "indexed"


def test_ingest_document_endpoint_rejects_invalid_access_level():
    response = client.post(
        "/documents/ingest",
        json={
            "document_id": "api-resilience-policy",
            "title": "API Resilience Policy",
            "content": "External API calls must use timeouts and fallback behavior",
            "category": "engineering",
            "access_level": "secret",
        },
    )    

    assert response.status_code == 422