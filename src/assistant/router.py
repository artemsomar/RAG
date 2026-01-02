from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.assistant.schemas import RagAssistantRequest, RagAssistantResponse
from src.auth.dependencies import get_current_auth_user
from src.database.database import session_dependency
from src.database.models import User
from src.documents import service as documents_service
from src.assistant import service as assistant_service


router = APIRouter()


@router.post("/", response_model=RagAssistantResponse)
async def assistant_with_rag(
    request: RagAssistantRequest,
    user: User = Depends(get_current_auth_user),
    session: AsyncSession = Depends(session_dependency),
):
    documents = await documents_service.get_user_documents(user, session)
    response = await assistant_service.generate_rag_answer(
        request.query, documents, request.method, request.best_num, session
    )
    return RagAssistantResponse(response=response)
