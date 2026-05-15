import pytest

from app.infrastructure.llm.fake_client import FakeModelClient


@pytest.mark.asyncio
async def test_fake_model_client_return_configured_response():
    client =  FakeModelClient(
        response={
            "obligations": [
                {
                    "requirement": "External APIs must use retries.",
                    "category": "resilience",
                    "priority": "high",
                }
            ]
        }
    )

    result = await client.generate_json("Extract obligation from this policy.")


    assert result["obligations"][0]["priority"] == "high"