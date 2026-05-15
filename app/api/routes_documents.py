from fastapi import APIRouter

from app.application.ingest_document import ingest_document
from app.domain.models import DocumentIngestRequest, DocumentIngestResponse
from app.infrastructure.vector_store.store_instance import vector_store

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/ingest", response_model=DocumentIngestResponse)
async def ingest_document_endpoint(
    request: DocumentIngestRequest,
) -> DocumentIngestResponse:
    return ingest_document(request, vector_store)