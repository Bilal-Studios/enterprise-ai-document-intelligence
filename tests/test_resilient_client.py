import pytest

from app.infrastructure.llm.base import ModelClient
from app.infrastructure.llm.failing_client import FailingModelClient
from app.infrastructure.llm.fake_client import FakeModelClient
from app.infrastructure.llm.resilient_client import ResilientModelClient


class CountingFailingModelClient(ModelClient):
    def __init__(self) -> None:
        self.call_count = 0

    async def generate_json(self, prompt: str) -> dict:
        self.call_count += 1
        raise RuntimeError("Model provider unavailable")


@pytest.mark.asyncio
async def test_resilient_client_returns_primary_response_when_primary_succeeds():
    primary_client = FakeModelClient(
        response={
            "provider": "primary",
            "obligations": [],
        }
    )

    fallback_client = FakeModelClient(
        response={
            "provider": "fallback",
            "obligations": [],
        }
    )

    resilient_client = ResilientModelClient(
        primary_client=primary_client,
        fallback_client=fallback_client,
        max_retries=3,
        retry_delay_seconds=0,
    )

    result = await resilient_client.generate_json("test prompt")

    assert result["provider"] == "primary"


@pytest.mark.asyncio
async def test_resilient_client_uses_fallback_when_primary_fails():
    primary_client = FailingModelClient()

    fallback_client = FakeModelClient(
        response={
            "provider": "fallback",
            "obligations": [],
        }
    )

    resilient_client = ResilientModelClient(
        primary_client=primary_client,
        fallback_client=fallback_client,
        max_retries=2,
        retry_delay_seconds=0,
    )

    result = await resilient_client.generate_json("test prompt")

    assert result["provider"] == "fallback"


@pytest.mark.asyncio
async def test_resilient_client_raises_when_primary_and_fallback_fail():
    primary_client = FailingModelClient()
    fallback_client = FailingModelClient()

    resilient_client = ResilientModelClient(
        primary_client=primary_client,
        fallback_client=fallback_client,
        max_retries=2,
        retry_delay_seconds=0,
    )

    with pytest.raises(RuntimeError, match="Primary and fallback model clients failed"):
        await resilient_client.generate_json("test prompt")


@pytest.mark.asyncio
async def test_resilient_client_retries_primary_configured_number_of_times():
    primary_client = CountingFailingModelClient()

    fallback_client = FakeModelClient(
        response={
            "provider": "fallback",
            "obligations": [],
        }
    )

    resilient_client = ResilientModelClient(
        primary_client=primary_client,
        fallback_client=fallback_client,
        max_retries=3,
        retry_delay_seconds=0,
    )

    result = await resilient_client.generate_json("test prompt")

    assert result["provider"] == "fallback"
    assert primary_client.call_count == 3