from app.application.query_documents import query_documents
from app.domain.models import DocumentChunk, QueryRequest
from app.infrastructure.vector_store.in_memory_vector_store import InMemoryVectorStore


def test_query_documents_returns_answer_with_sources():
    store = InMemoryVectorStore()

    store.add_chunks(
        [
            DocumentChunk(
                chunk_id="api-001",
                document_id="api-resilience-policy",
                title="API Resilience Policy",
                text="External API failures should use timeouts, retries, and fallback providers.",
                category="engineering",
                access_level="internal",
                section="External Provider failure",
            )
        ]
    )


    request = QueryRequest(
        question="How should external API failures be handled?",
        user_role="employee",
        max_sources=3,
    )

    response = query_documents(request, store)

    
    assert response.confidence == "high"
    assert response.requires_human_review is False
    assert len(response.sources) == 1
    assert response.sources[0].document_id == "api-resilience-policy"
    assert "timeouts" in response.answer


def test_query_documents_returns_human_review_when_no_context_found():
    store = InMemoryVectorStore()

    request = QueryRequest(
        question="What is the company vacation Policy?",
        user_role="employee",
        max_sources=3,
    )


    response = query_documents(request, store)


    assert response.confidence == "low"
    assert response.sources == []
    assert response.requires_human_review is True



def test_query_documents_does_not_use_restricted_context_for_employee():
    store = InMemoryVectorStore()

    store.add_chunks(
        [
            DocumentChunk(
                chunk_id="security-001",
                document_id="security-policy",
                title="Security Policy",
                text="Customer data must not be logged in plaintext.",
                category="security",
                access_level="restricted",
                section="Logging Rules",
            )
        ]
    )    

    request = QueryRequest(
        question="Can customer data be logged in plaintext?",
        user_role="employee",
        max_sources=3,
    )

    response = query_documents(request, store)


    assert response.confidence== "low"
    assert response.requires_human_review is True
    assert response.sources == []