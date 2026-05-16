# Changelog

## v1.0.0

### Added

- Final interview-ready release checkpoint
- Stable project version for technical review
- Final verification of tests, linting, evals, Docker build, and CI workflow

### Included

- FastAPI backend
- Pydantic request and response schemas
- Document ingestion and chunking
- In-memory RAG-style retrieval
- Permission-aware document access
- Structured obligation extraction
- Fake LLM clients for deterministic tests
- Resilient model client with retry and fallback behavior
- Lightweight HTML demo UI
- `.txt` and `.md` document upload
- In-memory store clearing for demos
- Retrieval evals with golden questions
- Docker support
- GitHub Actions CI
- Ruff and pytest quality checks
- README documentation and production upgrade path

### Notes

This release marks the project as interview-ready. The system is intentionally free to run and uses fake or in-memory adapters instead of paid LLM APIs, external vector databases, or cloud infrastructure.

The architecture is designed so fake adapters can later be replaced with real providers such as OpenAI, Anthropic, AWS Bedrock, pgvector, Qdrant, Pinecone, Weaviate, or OpenSearch.


## v0.9.0

### Added

- `.env.example` for documented local configuration
- `Makefile` with common developer commands
- README quick demo flow
- README known limitations section

### Improved

- FastAPI OpenAPI version updated to `0.9.0`
- Developer experience for running lint, tests, evals, and Docker commands

### Notes

This version focuses on final developer polish before the `v1.0.0` interview-ready release. No major product features were added.


## v0.8.0

### Added

- Sample enterprise documents for local demos and evals
- `golden_questions.json` with expected retrieval scenarios
- `run_evals.py` evaluation runner
- Eval checks for expected confidence
- Eval checks for expected source document
- Eval checks for human-review behavior
- Eval coverage for permission-aware retrieval

### Improved

- In-memory retriever tokenization
- Stop-word filtering for keyword scoring
- Retrieval threshold to reduce weak/noisy matches
- Title-aware chunk scoring

### Notes

This version separates deterministic software tests from retrieval evals. `pytest` validates code behavior, while `python evals/run_evals.py` checks whether the RAG-style system retrieves expected sources and handles permission/no-context scenarios correctly.


## v0.7.0

### Added

- Lightweight HTML demo interface at `/app`
- Document upload endpoint at `/documents/upload`
- Support for uploading `.txt` and `.md` documents
- Clear in-memory document store endpoint at `/documents/clear`
- Clear store button in the HTML demo interface
- `DocumentUploadResponse` response model
- `DocumentClearResponse` response model
- Tests for document upload and clear behavior

### Notes

This version makes the backend easier to demo without using Swagger directly. The core API remains JSON-first, but `/app` provides a simple human-friendly interface for uploading documents, asking questions, and clearing the in-memory store.

The document store is still in-memory. Restarting the server or calling `/documents/clear` resets uploaded chunks. In production, this would be replaced with persistent storage, document versioning, and upsert/delete behavior.

## v0.6.0

### Added

- Polished README documentation
- Architecture explanation
- Project structure overview
- RAG flow explanation
- Permission-aware retrieval explanation
- LLM provider abstraction explanation
- Resilience strategy documentation
- Testing strategy documentation
- Docker usage instructions
- CI/CD explanation
- Production upgrade path
- Version roadmap

### Notes

This version improves the repository’s readability for technical review. It explains the engineering decisions behind the project, including why the app uses fake LLM clients, in-memory retrieval, Pydantic validation, and provider abstractions.


## v0.5.0

### Added

- GitHub Actions workflow for continuous integration
- Automated Ruff check on push and pull request
- Automated pytest run on push and pull request
- Node 24 opt-in for GitHub Actions runtime migration

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