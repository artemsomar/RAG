from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.documents.exceptions import InvalidUserId
from src.documents.schemas import DocumentCreate, DocumentUpdate
from src.database.models import Document, User


async def get_user_documents(user: User, session: AsyncSession) -> list[Document]:
    user_request = await session.execute(
        select(User).options(selectinload(User.documents)).where(User.id == user.id)
    )
    user = user_request.scalar_one_or_none()
    if not user:
        raise InvalidUserId
    return user.documents


async def get_document_by_id(
    document_id: int, user: User, session: AsyncSession
) -> Document | None:
    document_req = await session.execute(
        select(Document).where(Document.id == document_id, Document.user_id == user.id)
    )
    return document_req.scalar_one_or_none()


async def create_document(
    document_in: DocumentCreate, user: User, session: AsyncSession
) -> Document:
    document = Document(user_id=user.id, **document_in.model_dump())
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return document


async def update_document(
    document: Document,
    document_update: DocumentUpdate,
    session: AsyncSession,
) -> Document | None:
    for name, value in document_update.model_dump(exclude_unset=True).items():
        setattr(document, name, value)
    await session.commit()
    return document


async def delete_document(document: Document, session: AsyncSession) -> None:
    await session.delete(document)
    await session.commit()
