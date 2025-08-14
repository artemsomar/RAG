from fastapi import APIRouter, Depends
from app.rag_schemas import QueryRequest, QueryResponse
from app.services.llm import LLMService

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest, llm_service: LLMService = Depends()):
    response = await llm_service.do_request_with_rag(
        query=request.query,
        method=request.method,
    )
    return QueryResponse(response)