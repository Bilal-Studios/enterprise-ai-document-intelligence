from app.application.chunking import chunk_document
from app.domain.models import DocumentIngestRequest


def test_chunk_document_splits_content_by_paragraphs():
    document = DocumentIngestRequest(
        document_id="api-resilience-policy",
        title="API Resilience Policy",
        content=(
            "External API calls must use timeouts.\n\n"
            "Retries should use exponential backoff.\n\n"
            "Fallback providers should be available."
        ),
        category="engineering",
        access_level="internal",
    )

    chunks = chunk_document(document)

    assert len(chunks) == 3
    assert chunks[0].chunk_id == "api-resilience-policy-001"
    assert chunks[1].chunk_id == "api-resilience-policy-002"
    assert chunks[2].chunk_id == "api-resilience-policy-003"


def test_chunks_document_preserves_document_metadata():
    document = DocumentIngestRequest(
        document_id="cloud-security-policy",
        title="Cloud Security Policy",
        content=(
            "Cloud resources must use least-privilege IAM.\n\n"
            "Sensitive data must be logged in plaintext."
        ),
        category="security",
        access_level="restricted",
    )

    chunks = chunk_document(document)

    assert chunks[0].document_id == "cloud-security-policy"
    assert chunks[0].title == "Cloud Security Policy"
    assert chunks[0].category == "security"
    assert chunks[0].access_level == "restricted"
