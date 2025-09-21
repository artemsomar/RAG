from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dependencies import get_current_auth_user
from src.models import Document, User
from src.documents import service as documents_service
from src.database import session_dependency


async def get_document_by_id(
        document_id: int,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(session_dependency)
) -> Document:

    document = await documents_service.get_document_by_id(document_id, user, session)
    if document:
        return document

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )