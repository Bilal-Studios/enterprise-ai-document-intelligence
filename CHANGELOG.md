# Changelog


## v0.5.0

### Added

- GitHub Actions workflow for continuous integration
- Automated Ruff check on push and pull request
- Automated pytest run on push and pull request

### Notes

The CI workflow uses Python 3.12 on Ubuntu and runs the same quality checks used locally: `ruff check .` and `pytest`.


## v0.4.0

### Added

- `Dockerfile` for containerizing the FastAPI backend
- `.dockerignore` to keep images clean and avoid copying local caches or virtual environments
- Docker run instructions in the README

### Verified

- Docker image builds successfully
- Container runs the FastAPI app with Uvicorn
- `/health` endpoint works from inside the container

### Notes

The container exposes port `8000` and runs the app with `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## v0.3.0

### Added

- `FailingModelClient` for simulating provider failures
- `ResilientModelClient` for retry and fallback behavior
- Retry configuration with `max_retries` and `retry_delay_seconds`
- Tests for primary model success
- Tests for fallback model usage when the primary fails
- Tests for total provider failure
- Test-only counting client to verify retry count behavior

### Notes

This version demonstrates LLM API resilience without using paid provider calls. The same pattern can wrap real OpenAI, Anthropic, or AWS Bedrock clients in production.

## v0.2.0

### Added

- `ModelClient` interface for LLM provider abstraction
- `FakeModelClient` for deterministic tests without paid LLM APIs
- Obligation extraction Pydantic models
- Structured obligation extraction application service
- `/extract/obligations` API endpoint
- Tests for fake model client
- Tests for structured extraction service
- Tests for extraction API validation

### Notes

This version keeps all LLM behavior free and deterministic by using a fake model client. In production, the same `ModelClient` interface can be implemented by OpenAI, Anthropic, AWS Bedrock, or another provider.

## v0.1.0

### Added

- FastAPI application structure
- Health endpoint
- Document ingestion endpoint
- Query endpoint
- Pydantic request and response models
- Document chunking service
- In-memory vector store adapter
- Permission-aware retrieval
- Query response with source references
- pytest test suite
- Ruff configuration

### Notes

This version uses a free in-memory retriever instead of paid LLM or vector database services. The architecture is designed so real providers can be added through adapters later.