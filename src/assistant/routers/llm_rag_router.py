from fastapi import APIRouter, Depends

from ..schemas import RagRequest, LlmResponse
from ..service import RetrievalService

router = APIRouter()


@router.post("/", response_model=LlmResponse)
def rag_llm_query(request: RagRequest, retrieval_service: RetrievalService = Depends()):
    response = retrieval_service.generate_answer_with_rag(
        prompt=request.prompt,
        method=request.method,
    )
    return LlmResponse.model_validate({ "response" : response })