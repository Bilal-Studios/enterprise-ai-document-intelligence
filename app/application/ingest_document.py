from app.application.chunking import chunk_document
from app.domain.models import DocumentIngestRequest, DocumentIngestResponse
from app.infrastructure.vector_store.base import VectorStore


def ingest_document(
        document: DocumentIngestRequest,
        vector_store: VectorStore,
) -> DocumentIngestResponse:
    chunks = chunk_document(document)
    vector_store.add_chunks(chunks)

    return DocumentIngestResponse(
        document_id=document.document_id,
        chunks_created=len(chunks),
        status="indexed",
    )