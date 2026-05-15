from app.domain.models import DocumentChunk
from app.infrastructure.vector_store.in_memory_vector_store import InMemoryVectorStore


def test_vector_store_returns_matching_chunks():
    store = InMemoryVectorStore()

    chunks = [
        DocumentChunk(
            chunk_id="api-001",
            document_id="api-policy",
            title="API Policy",
            text="External API calls must use retries and fallback behavior.",
            category="engineering",
            access_level="internal",
        ),
        DocumentChunk(
            chunk_id="security-001",
            document_id="security-policy",
            title="Security Policy",
            text="Customer data must not be logged in plaintext.",
            category="security",
            access_level="restricted",
        ),
    ]

    store.add_chunks(chunks)

    results = store.search(
        query="How should external API failures be handled?",
        user_role="employee",
        max_results=3,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "api-001"


def test_vector_store_filters_restricted_chunks_for_non_admin():
    store = InMemoryVectorStore()

    restricted_chunk = DocumentChunk(
        chunk_id="security-001",
        document_id="security-policy",
        title="Security Policy",
        text="Customer data must not be logged in plaintext.",
        category="security",
        access_level="restricted",
    )

    store.add_chunks([restricted_chunk])

    results = store.search(
        query="customer data plaintext",
        user_role="employee",
        max_results=3,
    )

    assert results == []


def test_vector_store_allows_admin_to_retrieve_restricted_chunks():
    store = InMemoryVectorStore()

    restricted_chunk = DocumentChunk(
        chunk_id="security-001",
        document_id="security-policy",
        title="Security Policy",
        text="Customer data must not be logged in plaintext.",
        category="security",
        access_level="restricted",
    )

    store.add_chunks([restricted_chunk])

    results = store.search(
        query="customer data plaintext",
        user_role="admin",
        max_results=3,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "security-001"        