from app.infrastructure.llm.base import ModelClient


class FailingModelClient(ModelClient):
    async def generate_json(self, prompt: str) -> dict:
        raise RuntimeError("Model provider unavailable")