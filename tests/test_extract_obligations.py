import pytest
from pydantic import ValidationError

from app.application.extract_obligation import extract_obligations
from app.domain.models import ObligationExtractionRequest
from app.infrastructure.llm.fake_client import FakeModelClient


@pytest.mark.asyncio
async def test_extract_obligation_returns_validated_response():
    request = ObligationExtractionRequest(
        document_text=(
            "External APIs must use retries with exponential backoff. "
            "Customer data must not be logged in plaintext."
        )
    )

    model_client = FakeModelClient(
        response={
            "obligations": [
                {
                    "requirement": "External APIs must use retries with exponential backoff.",
                    "category": "resilience",
                    "priority": "high",
                },
                {
                    "requirement": "Customer data must not be logged in plaintext.",
                    "category": "security",
                    "priority": "critical",
                },
            ]
        }
    )


    response= await extract_obligations(request, model_client)


    assert len(response.obligations) == 2
    assert response.obligations[0].category == "resilience"
    assert response.obligations[1].priority == "critical"



    @pytest.mark.asyncio
    async def test_extract_obligations_rejects_invalid_model_output():
        request = ObligationExtractionRequest(
            document_text="External APIs must use retries with exponential backoff."
        )

        model_client = FakeModelClient(
            response={
                "obligations": [
                    {
                        "requirement": "External APIs must use retries with exponential backoff.",
                        "category": "resilience",
                        "priority": "urgent",
                    }
                ]
            }
        )

        with pytest.raises(ValidationError):
            await extract_obligations(request, model_client)