from abc import ABC, abstractmethod

from app.domain.models import DocumentChunk, UserRole


class VectorStore(ABC):
    @abstractmethod
    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def search(
        self,
        query: str,
        user_role: UserRole,
        max_results: int,
    ) -> list[DocumentChunk]:
        raise NotImplementedError