from app.application.ingest_document import ingest_document
from app.domain.models import DocumentIngestRequest
from app.infrastructure.vector_store.in_memory_vector_store import InMemoryVectorStore


def test_ingest_document_returns_chunk_count():
    document = DocumentIngestRequest(
        document_id="incident-response",
        title="Incident Response Procedure",
        content=(
            "First, identify the incident impact.\n\n"
            "Second, notify the responsible team.\n\n"
            "Third, document the resolution."
        ),
        category="operations",
        access_level="internal",
    )
    store = InMemoryVectorStore()

    response = ingest_document(document, store)

    assert response.document_id == "incident-response"
    assert response.chunks_created == 3
    assert response.status == "indexed"