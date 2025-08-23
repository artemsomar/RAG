from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import get_document_by_id
from src.database import session_dependency
from src.documents import crud
from src.documents.schemas import DocumentCreate, Document, DocumentUpdate

router = APIRouter()


@router.get("/", response_model=list[Document])
async def get_documents(
        session: AsyncSession = Depends(session_dependency)
):
    return await crud.get_documents(session)


@router.post("/", response_model=Document)
async def create_document(
        document_in: DocumentCreate,
        session: AsyncSession = Depends(session_dependency)
):
    return await crud.create_document(session, document_in)


@router.get("/{document_id}/", response_model=Document)
async def get_document(
        document: Document = Depends(get_document_by_id),
):
    return document


@router.patch("/{document_id}/", response_model=Document)
async def update_document(
        document_update: DocumentUpdate,
        document: Document = Depends(get_document_by_id),
        session: AsyncSession = Depends(session_dependency)
):
    return await crud.update_document(session, document, document_update)


@router.delete("/{document_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        document: Document = Depends(get_document_by_id),
        session: AsyncSession = Depends(session_dependency)
):
    await crud.delete_document(session, document)