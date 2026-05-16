from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.application.ingest_document import ingest_document
from app.domain.models import (
    AccessLevel,
    DocumentClearResponse,
    DocumentIngestRequest,
    DocumentIngestResponse,
    DocumentUploadResponse,
)
from app.infrastructure.vector_store.store_instance import vector_store

router = APIRouter(prefix="/documents", tags=["documents"])


def _document_id_from_filename(filename: str) -> str:
    path = Path(filename)
    return path.stem.lower().replace(" ", "-").replace("_", "-")


@router.post("/ingest", response_model=DocumentIngestResponse)
async def ingest_document_endpoint(
    request: DocumentIngestRequest,
) -> DocumentIngestResponse:
    return ingest_document(request, vector_store)


@router.post("/clear", response_model=DocumentClearResponse)
async def clear_documents_endpoint() -> DocumentClearResponse:
    vector_store.clear()

    return DocumentClearResponse(
        status="cleared",
        chunks_remaining=0,
    )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document_endpoint(
    file: Annotated[UploadFile, File()],
    category: str = "uploaded",
    access_level: AccessLevel = "internal",
) -> DocumentUploadResponse:
    filename = file.filename or "uploaded-document.txt"
    suffix = Path(filename).suffix.lower()

    if suffix not in {".txt", ".md"}:
        raise HTTPException(
            status_code=400,
            detail="Only .txt and .md files are supported.",
        )

    raw_content = await file.read()
    content = raw_content.decode("utf-8")

    document = DocumentIngestRequest(
        document_id=_document_id_from_filename(filename),
        title=Path(filename).stem.replace("_", " ").replace("-", " ").title(),
        content=content,
        category=category,
        access_level=access_level,
    )

    response = ingest_document(document, vector_store)

    return DocumentUploadResponse(
        document_id=response.document_id,
        filename=filename,
        chunks_created=response.chunks_created,
        status=response.status,
    )