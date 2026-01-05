from fastapi import UploadFile, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.documents.exceptions import UserNotFound, DocumentNotFound, DocumentUploadError
from src.documents.schemas import DocumentUpdate
from src.database.models import Document, User
from src.file_storage.client import upload_file, delete_file


async def get_user_documents(user: User, session: AsyncSession) -> list[Document]:
    user_request = await session.execute(
        select(User).options(selectinload(User.documents)).where(User.id == user.id)
    )
    user = user_request.scalar_one_or_none()
    if not user:
        raise UserNotFound()
    return user.documents


async def get_document_by_id(
    document_id: int, user: User, session: AsyncSession
) -> Document | None:
    document_req = await session.execute(
        select(Document).where(Document.id == document_id, Document.user_id == user.id)
    )
    document = document_req.scalar_one_or_none()

    if not document:
        raise DocumentNotFound()

    return document


async def create_document(
    file: UploadFile, user: User, session: AsyncSession
) -> Document:

    s3_data = await run_in_threadpool(upload_file, file)

    try:
        document = Document(
            user_id=user.id,
            title=file.filename,
            s3_object_key=s3_data["key"],
            source_url=s3_data["url"],
            media_type=s3_data["media_type"],
            content="",
        )
        session.add(document)
        await session.commit()
        await session.refresh(document)
        return document

    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        await run_in_threadpool(delete_file, s3_data["key"])
        raise DocumentUploadError() from e


async def update_document(
    document: Document,
    document_update: DocumentUpdate,
    session: AsyncSession,
) -> Document | None:
    for name, value in document_update.model_dump(exclude_unset=True).items():
        setattr(document, name, value)
    await session.commit()
    return document


async def delete_document(
    document: Document,
    session: AsyncSession,
    background_task: BackgroundTasks,
) -> None:
    file_key = document.s3_object_keys

    await session.delete(document)
    await session.commit()

    background_task.add_task(
        delete_file,
        file_key,
    )
