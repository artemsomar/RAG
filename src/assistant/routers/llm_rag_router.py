from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from ..schemas import RagRequest, LlmResponse
from ..service import RetrievalService

router = APIRouter()


@router.post("/", response_model=LlmResponse)
async def rag_llm_query(
        request: RagRequest,
        retrieval_service: RetrievalService = Depends(),
        session: AsyncSession = Depends(session_dependency)
):
    response = await retrieval_service.generate_answer_with_rag(
        query=request.query,
        session=session,
        best_num=request.best_num,
        method=request.method,
    )
    return LlmResponse.model_validate({ "response" : response })