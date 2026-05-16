# Enterprise AI Document Intelligence

A production-style Python backend demo for enterprise AI document intelligence.

This project is built for technical interview preparation and demonstrates:

- FastAPI backend structure
- Pydantic request and response schemas
- RAG-style document ingestion and retrieval
- Fake LLM clients for deterministic testing
- Provider abstraction for future OpenAI, Anthropic, or AWS Bedrock integration
- pytest-based automated testing
- Resilience patterns such as retries and fallbacks
- Docker and CI/CD readiness

## Goal

## Architecture

## Why Fake LLM Clients?

he project intentionally avoids paid LLM APIs.

Instead of calling OpenAI, Anthropic, or AWS Bedrock directly, the app uses a `ModelClient` abstraction with fake clients for testing.

This makes the code:

- free to run
- deterministic
- CI-friendly
- easy to test
- provider-independent

In production, the fake client can be replaced with a real provider adapter.

## Testing Strategy

This project uses pytest to validate the backend from the beginning.

The test suite is designed to cover:

- API route behavior
- Pydantic schema validation
- document chunking
- permission filtering
- RAG-style retrieval logic
- fake LLM responses
- fallback and retry behavior

Real LLM APIs are intentionally not required for tests. The project uses fake clients so tests remain free, deterministic, and CI-friendly.

## RAG Flow

## Resilience Patterns

## Run with Docker

Build the image:

```bash
docker build -t enterprise-ai-document-intelligence .
```

## Running Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
## Running Tests

## Production Improvements