import asyncio

from app.infrastructure.llm.base import ModelClient


class ResilientModelClient(ModelClient):
    def __init__(
        self,
        primary_client: ModelClient,
        fallback_client: ModelClient,
        max_retries: int = 3,
        retry_delay_seconds: float = 0.01,
    ) -> None:
        self.primary_client = primary_client
        self.fallback_client = fallback_client
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    async def generate_json(self, prompt: str) -> dict:
        last_error: Exception | None = None

        for _ in range(self.max_retries):
            try:
                return await self.primary_client.generate_json(prompt)
            except Exception as error:
                last_error = error
                await asyncio.sleep(self.retry_delay_seconds)

        try:
            return await self.fallback_client.generate_json(prompt)
        except Exception as fallback_error:
            raise RuntimeError(
                f"Primary and fallback model clients failed. Last primary error: {last_error}"
            ) from fallback_error