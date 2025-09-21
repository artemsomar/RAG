from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import get_document_by_id
from src.database import session_dependency
from src.documents import service as documents_service
from src.documents.schemas import DocumentCreate, DocumentSchema, DocumentUpdate
from src.models import Document, User
from ..auth.dependencies import get_current_auth_user


router = APIRouter()


@router.get("/", response_model=list[DocumentSchema])
async def get_documents(
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(session_dependency)
):
    return await documents_service.get_user_documents(user, session)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DocumentSchema)
async def create_document(
        document_in: DocumentCreate,
        user: User = Depends(get_current_auth_user),
        session: AsyncSession = Depends(session_dependency)
):
    return await documents_service.create_document(document_in, user, session)


@router.get("/{document_id}/", response_model=DocumentSchema)
async def get_document(
        document: DocumentSchema = Depends(get_document_by_id),
):
    return document


@router.patch("/{document_id}/", response_model=DocumentSchema)
async def update_document(
        document_update: DocumentUpdate,
        document: Document = Depends(get_document_by_id),
        session: AsyncSession = Depends(session_dependency)
):
    return await documents_service.update_document(document, document_update, session)


@router.delete("/{document_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        document: Document = Depends(get_document_by_id),
        session: AsyncSession = Depends(session_dependency)
):
    await documents_service.delete_document(document, session)