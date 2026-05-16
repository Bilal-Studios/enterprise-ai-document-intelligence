from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes_documents import router as documents_router
from app.api.routes_extract import router as extract_router
from app.api.routes_health import router as health_router
from app.api.routes_query import router as query_router

app = FastAPI(
    title="Enterprise AI Document Intelligence",
    description="A production-style AI backend demo for document ingestion, "
     "RAG-style retrieval, structured extraction, testing, and resilience",
    version="0.9.0",
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(query_router)
app.include_router(extract_router)


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.get("/app")
async def frontend_app() -> FileResponse:
    return FileResponse("app/static/index.html")

# @app.get("/health")
# async def health():
#        return {"status":"ok"}
