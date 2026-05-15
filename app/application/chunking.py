from app.domain.models import DocumentChunk, DocumentIngestRequest


def chunk_document(document: DocumentIngestRequest) -> list[DocumentChunk]:
    paragraphs = [
        paragraph.strip()
        for paragraph in document.content.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[DocumentChunk] = []

    for index, paragraph in enumerate(paragraphs, start=1):
        chunk_id = f"{document.document_id}-{index:03d}"

        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                title=document.title,
                text=paragraph,
                category=document.category,
                access_level=document.access_level,
                section=None,
            )
        )
    return chunks
