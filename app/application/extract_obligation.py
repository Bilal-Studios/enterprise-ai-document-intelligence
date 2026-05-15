from app.domain.models import (
    ObligationExtractionRequest,
    ObligationExtractionResponse,
)
from app.infrastructure.llm.base import ModelClient


async def extract_obligations(
        request: ObligationExtractionRequest,
        model_client: ModelClient,
) -> ObligationExtractionResponse: 
    prompt = (
        "Extract compliance or operational obligations from the document text. "
        "Return JSON with an 'obligations' list. "
        "Each obligation must include requirement, category, and priority.\n\n"
        "Document text:\n(request.docuemnt_text)"
    )


    raw_result = await model_client.generate_json(prompt)

    return ObligationExtractionResponse.model_validate(raw_result)