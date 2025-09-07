from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from src.core.rag.rag_controller import RagController
from ..schemas import RagRequest, RagResponse
from ..utils import get_chunks_info

router = APIRouter()

@router.post("/", response_model=RagResponse)
async def rag_search(
        request: RagRequest,
        rag_controller: RagController = Depends(),
        session: AsyncSession = Depends(session_dependency)
):
    best_chunks = await rag_controller.search_best(
        query=request.query,
        session=session,
        method=request.method,
        best_num=request.best_num,
    )
    chunks = get_chunks_info(best_chunks, session)
    return RagResponse.model_validate({ "chunks" : chunks })