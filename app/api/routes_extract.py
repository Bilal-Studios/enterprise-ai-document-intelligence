from fastapi import APIRouter

from app.application.extract_obligation import extract_obligations
from app.domain.models import (
    ObligationExtractionRequest,
    ObligationExtractionResponse,
)
from app.infrastructure.llm.client_instance import model_client

router = APIRouter(prefix="/extract", tags=["extract"])


@router.post("/obligations", response_model=ObligationExtractionResponse)
async def extract_obligations_endpoint(
    request: ObligationExtractionRequest,
) -> ObligationExtractionResponse:
    return await extract_obligations(request, model_client)