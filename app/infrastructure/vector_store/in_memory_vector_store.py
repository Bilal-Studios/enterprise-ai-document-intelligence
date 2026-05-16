from app.domain.models import DocumentChunk, UserRole
from app.domain.permissions import can_access
from app.infrastructure.vector_store.base import VectorStore


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._chunks: list[DocumentChunk] = []

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        self._chunks.extend(chunks)   


    def clear(self) -> None:
        self._chunks.clear()     


    def _score_chunk(self, query: str, chunk: DocumentChunk) -> int:
        query_words = set(query.lower().split())
        chunk_words = set(chunk.text.lower().split())

        return len(query_words.intersection(chunk_words))


    def search(
            self,
            query: str,
            user_role: UserRole,
            max_results: int,
    ) -> list[DocumentChunk]:
        accessible_chunks = [
            chunk
            for chunk in self._chunks
            if can_access(user_role, chunk.access_level)
        ]

        scored_chunks = [
            (self._score_chunk(query, chunk), chunk)
            for chunk in accessible_chunks
        ]

        positive_matches = [
            (score, chunk)
            for score, chunk in scored_chunks
            if score > 0
        ]

        positive_matches.sort(key=lambda item: item[0], reverse=True)

        return [chunk for _, chunk in positive_matches[:max_results]]
        