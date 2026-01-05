from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.documents.service import get_user_documents
from src.retrieval.schemas import RagResponse, RagRequest, ChunkInfo
from src.retrieval.services import retrieval_service, chunks_service
from src.auth.dependencies import get_current_auth_user
from src.database.session import session_dependency
from src.database.models import User


router = APIRouter()


@router.post("/", response_model=RagResponse)
async def rag_search(
    request: RagRequest,
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(session_dependency),
):
    user_documents = await get_user_documents(user, session)
    best_chunks = await retrieval_service.get_best_chunks(
        request.query, user_documents, request.method, request.best_num, session
    )
    chunks = await chunks_service.get_chunks_info(best_chunks, session)
    chunks_info = [
        ChunkInfo(document_title=chunk[0], content=chunk[1]) for chunk in chunks
    ]
    return RagResponse(chunks=chunks_info)
