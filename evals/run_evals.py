import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# The eval runner is a standalone script, so I add the project root to sys.
# path before importing the app modules.
#I mark those imports with noqa: E402 
#           because the import order exception is deliberate for script execution.

from app.application.ingest_document import ingest_document  # noqa: E402
from app.application.query_documents import query_documents  # noqa: E402
from app.domain.models import AccessLevel, DocumentIngestRequest, QueryRequest  # noqa: E402
from app.infrastructure.vector_store.store_instance import vector_store  # noqa: E402

SAMPLE_DOCS_DIR = ROOT_DIR / "data" / "sample_docs"
GOLDEN_QUESTIONS_PATH = ROOT_DIR / "evals" / "golden_questions.json"


def clear_store() -> None:
    vector_store.clear()


def ingest_sample_document(
        filename: str,
        document_id: str,
        title: str,
        category: str,
        access_level: AccessLevel,
) -> None:
    content = (SAMPLE_DOCS_DIR / filename).read_text(encoding="utf-8")

    document = DocumentIngestRequest(
        document_id=document_id,
        title=title,
        content=content,
        category=category,
        access_level=access_level,
    )   

    ingest_document(document, vector_store)


def load_sample_documents() -> None:
    ingest_sample_document(
        filename="api_resilience_policy.md",
        document_id="api-resilience-policy",
        title="API Resilience Policy",
        category="engineering",
        access_level="internal",
    )

    ingest_sample_document(
        filename="cloud_security_policy.md",
        document_id="cloud-security-policy",
        title="Cloud Security Policy",
        category="security",
        access_level="restricted",
    )

    ingest_sample_document(
        filename="gdpr_data_handling.md",
        document_id="gdpr-data-handling",
        title="GDPR Data Handling Policy",
        category="compliance",
        access_level="internal",
    )

    ingest_sample_document(
        filename="incident_response.md",
        document_id="incident-response",
        title="Incident Response Procedure",
        category="operations",
        access_level="internal",
    )


def load_golden_questions() -> list[dict]:
    return json.loads(GOLDEN_QUESTIONS_PATH.read_text(encoding="utf-8"))


def evaluate_case(case: dict) -> bool:
    request = QueryRequest(
        question=case["question"],
        user_role=case["user_role"],
        max_sources=case["max_sources"],
    )

    response = query_documents(request, vector_store)

    source_document_ids = {source.document_id for source in response.sources}

    confidence_matches = response.confidence == case["expected_confidence"]
    human_review_matches = (
        response.requires_human_review == case["expected_requires_human_review"]
    )

    expected_source = case["expected_source_document_id"]

    if expected_source is None:
        source_matches = len(response.sources) == 0
    else:
        source_matches = expected_source in source_document_ids

    passed = confidence_matches and human_review_matches and source_matches

    status = "PASS" if passed else "FAIL"

    print(f"[{status}] {case['name']}")
    print(f"  Question: {case['question']}")
    print(f"  Confidence: {response.confidence}")
    print(f"  Sources: {sorted(source_document_ids)}")
    print(f"  Requires human review: {response.requires_human_review}")

    return passed


def main() -> None:
    clear_store()
    load_sample_documents()

    cases = load_golden_questions()

    results = [evaluate_case(case) for case in cases]

    passed_count = sum(results)
    total_count = len(results)

    print()
    print(f"Eval result: {passed_count}/{total_count} passed")

    if passed_count != total_count:
        raise SystemExit(1)
    

if __name__ == "__main__":
    main()
    