from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.documents.schemas import DocumentCreate, DocumentUpdate
from src.models import Document


async def get_documents(session: AsyncSession) -> list[Document]:
    stmt = select(Document).order_by(Document.id)
    result: Result = await session.execute(stmt)
    documents = result.scalars().all()
    return list(documents)


async def get_document(session: AsyncSession, document_id: int) -> Document | None:
    return await session.get(Document, document_id)


async def create_document(session: AsyncSession, document_in: DocumentCreate) -> Document:
    document = Document(**document_in.model_dump())
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document


async def update_document(session: AsyncSession, document: Document, document_update: DocumentUpdate) -> Document:
    for name, value in document_update.model_dump(exclude_unset=True).items():
        setattr(document, name, value)
    await session.commit()
    return document


async def delete_document(session: AsyncSession, document: Document) -> None:
    await session.delete(document)
    await session.commit()