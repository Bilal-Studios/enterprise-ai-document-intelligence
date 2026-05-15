from fastapi.testclient import TestClient

from app.infrastructure.vector_store.store_instance import vector_store
from app.main import app

client = TestClient(app)


def clear_vector_store():
    vector_store._chunks.clear()


def test_query_endpoint_returns_answer_after_document_ingestion():
    clear_vector_store()

    ingest_response = client.post(
        "/documents/ingest",
        json={
            "document_id": "api-resilience-policy",
            "title": "API Resilience Policy",
            "content": (
                "External API failures should use timeouts, retries, "
                "and fallback providers.\n\n"
                "Customer data must not be logged in plaintext."
            ),
            "category": "engineering",
            "access_level": "internal",
        },
    )

    assert ingest_response.status_code == 200

    query_response = client.post(
        "/query",
        json={
            "question": "How should external API failures be handled?",
            "user_role": "employee",
            "max_sources": 3,
        },
    )

    assert query_response.status_code == 200

    data = query_response.json()

    assert data["confidence"] == "high"
    assert data["requires_human_review"] is False
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["document_id"] == "api-resilience-policy"
    assert "timeouts" in data["answer"]    


def test_query_endpoint_returns_human_review_when_no_context_exists():
    clear_vector_store()

    response = client.post(
        "/query",
        json={
            "question": "What is the vacation policy?",
            "user_role": "employee",
            "max_sources": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["confidence"] == "low"
    assert data["sources"] == []
    assert data["requires_human_review"] is True


def test_query_endpoint_does_not_expose_restricted_context_to_employee():
    clear_vector_store()

    ingest_response = client.post(
        "/documents/ingest",
        json={
            "document_id": "security-policy",
            "title": "Security Policy",
            "content": "Customer data must not be logged in plaintext.",
            "category": "security",
            "access_level": "restricted",
        },
    )

    assert ingest_response.status_code == 200

    query_response = client.post(
        "/query",
        json={
            "question": "Can customer data be logged in plaintext?",
            "user_role": "employee",
            "max_sources": 3,
        },
    )

    assert query_response.status_code == 200

    data = query_response.json()

    assert data["confidence"] == "low"
    assert data["sources"] == []
    assert data["requires_human_review"] is True


