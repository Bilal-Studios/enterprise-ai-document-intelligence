import pytest
from pydantic import ValidationError

from app.domain.models import (
    DocumentChunk,
    DocumentIngestRequest,
    QueryRequest,
    QueryResponse,
    SourceReference,
)


def test_valid_document_ingest_request_passes_validation():
    document = DocumentIngestRequest(
        document_id="api-resilience-policy",
        title="API Resilience Policy",
        content="External API calls must use retries and fallback behavior.",
        category="engineering",
        access_level="internal",
    )

    assert document.document_id == "api-resilience-policy"
    assert document.access_level == "internal"


def test_invalid_access_level_fails_validation():
    with pytest.raises(ValidationError):
        DocumentIngestRequest(
            document_id="api-resilience-policy",
            title="API Resilience Policy",
            content="External API calls must use retries and fallback behavior.",
            category="engineering",
            access_level="secret",
        )


def test_valid_document_chunk_passes_validation():
    chunk = DocumentChunk(
        chunk_id="api-resilience-policy-001",
        document_id="api-resilience-policy",
        title="API Resilience Policy",
        text="External API calls must use timeouts, retries, and fallback behavior.",
        category="engineering",
        access_level="internal",
        section="Retries and Fallbacks",
    )

    assert chunk.chunk_id == "api-resilience-policy-001"
    assert chunk.section == "Retries and Fallbacks"


def test_short_document_chunk_text_fails_validation():
    with pytest.raises(ValidationError):
        DocumentChunk(
            chunk_id="bad-001",
            document_id="bad",
            title="bad",
            text="short",
            category="engineering",
            access_level="internal",
        )


def test_valid_query_request_passes_validation():
    query = QueryRequest(
        question="How should we handle external API failures?",
        user_role="engineer",
        max_sources=3,
    )

    assert query.user_role == "engineer"
    assert query.max_sources == 3


def test_invalid_query_user_role_fails_validation():
    with pytest.raises(ValidationError):
        QueryRequest(
            question="How should we handle external API failures?",
            user_role="superuser",
            max_sources=3,
        )    


def test_query_response_accepts_sources():
    response = QueryResponse(
        answer="Use timeouts, retries, backoff, and fallbacks.",
        confidence="high",
        sources=[
            SourceReference(
                document_id="api-resilience-policy",
                title="API Resilience Policy",
                section="Retries and Fallbacks",
                category="engineering",
            )
        ],
        requires_human_review=False,
    )

    assert response.confidence == "high"
    assert response.sources[0].document_id == "api-resilience-policy"        