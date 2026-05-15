import pytest

from app.infrastructure.llm.failing_client import FailingModelClient


@pytest.mark.asyncio
async def test_failing_model_client_raises_runtime_error():
    client = FailingModelClient()


    with pytest.raises(RuntimeError):
        await client.generate_json("Extract obligations from this policy.")