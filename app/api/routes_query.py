from fastapi import APIRouter

from app.application.query_documents import query_documents
from app.domain.models import QueryRequest, QueryResponse
from app.infrastructure.vector_store.store_instance import vector_store

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def query_documents_endpoint(request: QueryRequest) -> QueryResponse:
    return query_documents(request, vector_store)