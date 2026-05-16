# Enterprise AI Document Intelligence

A production-style FastAPI backend for enterprise AI document intelligence.

This project demonstrates how to build a testable, provider-independent AI backend with:

- RAG-style document ingestion and retrieval
- Pydantic request and response schemas
- permission-aware search for enterprise documents
- fake LLM clients for deterministic testing
- structured extraction from policy text
- retry and fallback behavior for LLM provider failures
- Docker support
- GitHub Actions CI
- Ruff and pytest quality checks

The project is intentionally free to run. It does not require OpenAI, Anthropic, AWS Bedrock, Pinecone, Qdrant, or any paid cloud service.

---

## Goal

The goal of this project is to demonstrate production AI engineering patterns without relying on paid APIs or cloud infrastructure.

Instead of calling a real LLM or vector database, the project uses:

- `FakeModelClient` for deterministic LLM responses
- `FailingModelClient` to simulate provider outages
- `ResilientModelClient` to test retry and fallback behavior
- `InMemoryVectorStore` to demonstrate retrieval and permission filtering

This keeps the system:

- free to run
- deterministic in tests
- CI-friendly
- easy to reason about
- ready to swap fake adapters for real providers later

---

## Architecture

The project uses a layered architecture:

```text
API Layer
  FastAPI routes, request validation, response models

Application Layer
  Use cases such as document ingestion, querying, and obligation extraction

Domain Layer
  Pydantic models, access rules, source references, query/response contracts

Infrastructure Layer
  LLM clients, vector store adapters, shared runtime instances
```

High-level request flow:

```text
HTTP request
  → FastAPI route
  → Pydantic request model
  → application service
  → infrastructure adapter
  → Pydantic response model
  → JSON response
```

The application layer depends on interfaces, not concrete providers. For example, obligation extraction depends on `ModelClient`, not directly on OpenAI, Anthropic, or AWS Bedrock.

---

## Project Structure

```text
app/
  api/
    FastAPI route modules

  application/
    Business use cases such as ingestion, querying, and extraction

  domain/
    Pydantic models and permission logic

  infrastructure/
    LLM clients, vector store adapters, and runtime instances

tests/
  pytest test suite covering API, application, domain, and infrastructure layers

.github/workflows/
  GitHub Actions CI workflow

Dockerfile
  Container definition for running the FastAPI app

pyproject.toml
  Ruff and pytest configuration
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns a simple health response to confirm the API is running.

---

### Document Ingestion

```http
POST /documents/ingest
```

Example request:

```json
{
  "document_id": "api-resilience-policy",
  "title": "API Resilience Policy",
  "content": "External API failures should use timeouts, retries, and fallback providers.",
  "category": "engineering",
  "access_level": "internal"
}
```

Example response:

```json
{
  "document_id": "api-resilience-policy",
  "chunks_created": 1,
  "status": "indexed"
}
```

---

### Query Documents

```http
POST /query
```

Example request:

```json
{
  "question": "How should external API failures be handled?",
  "user_role": "employee",
  "max_sources": 3
}
```

Example response:

```json
{
  "answer": "Based on the retrieved documents: External API failures should use timeouts, retries, and fallback providers.",
  "confidence": "high",
  "sources": [
    {
      "document_id": "api-resilience-policy",
      "title": "API Resilience Policy",
      "section": null,
      "category": "engineering"
    }
  ],
  "requires_human_review": false
}
```

---

### Extract Obligations

```http
POST /extract/obligations
```

Example request:

```json
{
  "document_text": "External APIs must use retries with exponential backoff. Customer data must not be logged in plaintext."
}
```

Example response:

```json
{
  "obligations": [
    {
      "requirement": "External APIs must use retries with exponential backoff.",
      "category": "resilience",
      "priority": "high"
    },
    {
      "requirement": "Customer data must not be logged in plaintext.",
      "category": "security",
      "priority": "critical"
    }
  ]
}
```

---

## RAG Flow

The project implements a free RAG-style flow without external vector databases.

```text
Document input
  → Pydantic validation
  → chunking
  → metadata preservation
  → in-memory vector store
  → permission-aware retrieval
  → sourced response
```

The current retriever uses simple keyword scoring to stay free and understandable.

In production, the `VectorStore` interface could be implemented with:

- pgvector
- Qdrant
- Pinecone
- Weaviate
- Elasticsearch/OpenSearch hybrid search
- AWS, Azure, or GCP managed search services

The important design point is that the application depends on the `VectorStore` interface, not a specific vendor.

---

## Permission-Aware Retrieval

Enterprise RAG must not expose documents the user is not allowed to access.

This project models document access levels:

- `public`
- `internal`
- `restricted`

And user roles:

- `guest`
- `employee`
- `engineer`
- `admin`

Before returning chunks to the answer layer, the retriever filters chunks through `can_access`.

This prevents restricted context from being sent to the response layer for unauthorized users.

---

## Why Fake LLM Clients?

The project intentionally avoids paid LLM APIs.

Instead of calling OpenAI, Anthropic, or AWS Bedrock directly, the app uses a `ModelClient` abstraction with fake clients for testing.

This makes the code:

- free to run
- deterministic
- CI-friendly
- easy to test
- provider-independent

In production, the fake client can be replaced with a real provider adapter.

Example future adapters:

```text
OpenAIModelClient
AnthropicModelClient
BedrockModelClient
AzureOpenAIModelClient
```

---

## Resilience Patterns

The project includes a resilient LLM wrapper:

```text
ResilientModelClient
  → tries primary model client
  → retries if primary fails
  → falls back to fallback model client
  → raises controlled error if both fail
```

Test clients include:

- `FakeModelClient` for successful deterministic output
- `FailingModelClient` for simulated provider outage
- a test-only counting client to verify retry counts

This demonstrates how LLM provider failure can be tested without real provider calls.

In production, retry logic should be limited to retryable failures such as:

- network timeouts
- rate limits
- temporary provider errors
- HTTP 5xx errors

Non-retryable failures such as invalid request payloads or authentication errors should fail fast.

---

## Testing Strategy

This project uses pytest to validate the backend from the beginning.

The test suite covers:

- API route behavior
- Pydantic schema validation
- document chunking
- document ingestion
- permission filtering
- RAG-style retrieval logic
- fake LLM responses
- structured extraction
- fallback and retry behavior
- API validation errors

Real LLM APIs are intentionally not required for tests. The project uses fake clients so tests remain free, deterministic, and CI-friendly.

Run tests:

```bash
pytest
```

Run Ruff:

```bash
ruff check .
```

---

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

Build the image:

```bash
docker build -t enterprise-ai-document-intelligence .
```

Run the container:

```bash
docker run --rm -p 8000:8000 enterprise-ai-document-intelligence
```

Health check:

```text
http://127.0.0.1:8000/health
```

API docs:

```text
http://127.0.0.1:8000/docs
```

If port `8000` is already in use, map another host port:

```bash
docker run --rm -p 8001:8000 enterprise-ai-document-intelligence
```

Then open:

```text
http://127.0.0.1:8001/health
```

---

## CI/CD

The project uses GitHub Actions to run quality checks automatically on push and pull request.

The CI workflow runs:

```bash
ruff check .
pytest
```

This ensures the test suite runs in a clean environment, not only on the local machine.

---

## Production Upgrade Path

This project is intentionally small and free, but the architecture is designed to be replaceable.

Possible production upgrades:

- Replace `FakeModelClient` with OpenAI, Anthropic, AWS Bedrock, or Azure OpenAI adapters
- Replace `InMemoryVectorStore` with pgvector, Qdrant, Pinecone, Weaviate, or OpenSearch
- Add persistent document storage with PostgreSQL or object storage
- Add authentication and tenant-aware access control
- Add request tracing, structured logs, metrics, and token usage tracking
- Add rate limiting and provider-specific retry policies
- Add real embedding generation
- Add hybrid search and re-ranking
- Add evaluation datasets for answer quality and retrieval quality
- Add Kubernetes deployment manifests or cloud deployment configuration

---

## Version Roadmap

### v0.1.0

Backend foundation:

- FastAPI application
- Pydantic schemas
- document ingestion
- chunking
- in-memory retrieval
- permission-aware search
- query endpoint
- pytest
- Ruff

### v0.2.0

Structured extraction:

- `ModelClient` interface
- `FakeModelClient`
- obligation extraction models
- extraction application service
- `/extract/obligations` endpoint
- tests for structured model output

### v0.3.0

LLM resilience:

- `FailingModelClient`
- `ResilientModelClient`
- retry behavior
- fallback behavior
- failure tests
- retry count tests

### v0.4.0

Docker:

- `Dockerfile`
- `.dockerignore`
- containerized FastAPI app
- Docker run instructions

### v0.5.0

CI/CD:

- GitHub Actions workflow
- automated Ruff checks
- automated pytest run

### v0.6.0

Documentation polish:

- architecture explanation
- API examples
- testing strategy
- resilience strategy
- production upgrade path

---

## Interview Notes

This project demonstrates practical production AI engineering patterns:

- LLM output should be treated as untrusted and validated with Pydantic.
- Normal tests should not depend on paid or non-deterministic LLM APIs.
- Application logic should depend on interfaces, not provider SDKs.
- RAG retrieval should be permission-aware in enterprise systems.
- Fallbacks and retries should be tested with fake clients before real providers are added.
- Docker makes local and deployment environments more consistent.
- CI gives the team a shared quality gate independent of one developer’s machine.