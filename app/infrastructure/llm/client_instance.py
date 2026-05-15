from app.infrastructure.llm.fake_client import FakeModelClient

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