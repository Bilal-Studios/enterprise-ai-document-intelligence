from app.domain.models import QueryRequest, QueryResponse, SourceReference
from app.infrastructure.vector_store.base import VectorStore


def query_documents(
    request: QueryRequest,
    vector_store: VectorStore,
) -> QueryResponse:
    chunks = vector_store.search(
        query=request.question,
        user_role=request.user_role,
        max_results=request.max_sources,
    )

    if not chunks:
        return QueryResponse(
            answer="I could not find enough relevant context to answer this question.",
            confidence="low",
            sources=[],
            requires_human_review=True,
        )

    sources = [
        SourceReference(
            document_id=chunk.document_id,
            title=chunk.title,
            section=chunk.section,
            category=chunk.category,
        )
        for chunk in chunks
    ]

    combined_context = " ".join(chunk.text for chunk in chunks)
    answer = f"Based on the retrieved documents: {combined_context}"

    return QueryResponse(
        answer=answer,
        confidence="high",
        sources=sources,
        requires_human_review=False,
    )