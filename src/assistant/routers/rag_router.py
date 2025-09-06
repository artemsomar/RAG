from fastapi import APIRouter, Depends

from src.core.rag.rag_controller import RagController
from ..schemas import RagRequest, RagResponse

router = APIRouter()

@router.post("/", response_model=RagResponse)
async def rag_search(request: RagRequest, rag_controller: RagController = Depends()):
    best_abstract, quote = await rag_controller.search_best(
        query=request.prompt,
        method=request.method,
    )
    return RagResponse.model_validate( {
        "quote": quote,
        "best_abstract": best_abstract
    })