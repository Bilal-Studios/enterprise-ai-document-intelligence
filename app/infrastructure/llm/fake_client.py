from app.infrastructure.llm.base import ModelClient


class FakeModelClient(ModelClient):

    def __init__(self, response: dict) -> None:
        self.response = response


    async def generate_json(self, prompt: str) -> dict:
        return self.response