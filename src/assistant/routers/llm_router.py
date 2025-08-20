from fastapi import APIRouter, Depends

from src.core.llm_provider import LlmProvider
from ..schemas import LlmResponse, LlmRequest

router = APIRouter()

@router.post("/", response_model=LlmResponse)
async def llm_query(request: LlmRequest, llm_provider: LlmProvider = Depends()):
    response = await llm_provider.chat_completion(
        user_prompt=request.prompt,
    )
    return LlmResponse.model_validate({ "response" : response })