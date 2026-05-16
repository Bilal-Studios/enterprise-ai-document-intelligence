from typing import Literal

from pydantic import BaseModel, Field

AccessLevel = Literal["public", "internal", "restricted"]
UserRole = Literal["guest", "employee", "engineer", "admin"]
ConfidenceLevel = Literal["low", "medium", "high"]

class DocumentIngestRequest(BaseModel):
    document_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    content: str = Field(min_length=20)
    category: str = Field(min_length=2)
    access_level: AccessLevel = "internal"


class DocumentIngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    status: Literal["indexed"]


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    text: str = Field(min_length=10)
    category: str
    access_level: AccessLevel
    section: str | None = None


class SourceReference(BaseModel):
    document_id: str
    title: str
    section: str | None = None
    category: str | None = None


class QueryRequest(BaseModel):
    question: str = Field(min_length=5)
    user_role: UserRole = "employee"
    max_sources: int = Field(default=3, ge=1, le=10) 


class QueryResponse(BaseModel):
    answer: str
    confidence: ConfidenceLevel
    sources: list[SourceReference]
    requires_human_review: bool = False       


class Obligation(BaseModel):
    requirement: str = Field(min_length=5)
    category: str = Field(min_length=2)
    priority: Literal["low", "medium", "high", "critical"]


class ObligationExtractionRequest(BaseModel):
    document_text: str = Field(min_length=20)


class ObligationExtractionResponse(BaseModel):
    obligations: list[Obligation]            


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_created: int
    status: Literal["indexed"]    


class DocumentClearResponse(BaseModel):
    status: Literal["cleared"]
    chunks_remaining: int    