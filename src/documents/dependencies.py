from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Document
from src.documents import crud
from src.database import session_dependency


async def get_document_by_id(
        document_id: int,
        session: AsyncSession = Depends(session_dependency)
) -> Document:
    document = await crud.get_document(session, document_id)
    if document:
        return document

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )