from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models import Chunk, Document, ChunkTokens, ChunkVector
from src.retrieval.exceptions import DocumentInvalid, ChunkInvalid


async def get_chunks_info(chunks: list[Chunk], session: AsyncSession) -> list[tuple[str, str]]:
    chunks_info_lst = []
    for chunk_in in chunks:
        chunk_req = await session.execute(
            select(Chunk)
            .options(
                selectinload(Chunk.document)
            )
            .where(Chunk.id == chunk_in.id)
        )
        chunk = chunk_req.scalar_one_or_none()
        if not chunk:
            raise ChunkInvalid
        document = chunk.document
        chunk_text = get_chunk_text(chunk, document)
        document_title = document.title
        chunks_info_lst.append((document_title, chunk_text))

    return chunks_info_lst


def get_chunk_text(chunk: Chunk, document: Document) -> str:
    start_index, end_index = chunk.start_index, chunk.end_index
    content = document.content
    return content[start_index:end_index]


async def get_chunks_from_session(
        document: Document,
        session: AsyncSession
) -> list[Chunk]:
    document_result = await session.execute(
        select(Document)
        .options(
            selectinload(Document.chunks)
        )
        .where(Document.id == document.id)
    )
    document = document_result.scalar_one_or_none()
    if not document:
        raise DocumentInvalid

    return document.chunks


async def create_chunks_into_session(
        chunks: list[Chunk | ChunkTokens | ChunkVector],
        session: AsyncSession
) -> list[Chunk]:
    for chunk in chunks:
        session.add(chunk)

    await session.flush()
    await session.commit()

    return chunks


async def get_chunks_related(
    chunks: list[Chunk],
    related_type: type,
    session: AsyncSession
):
    chunk_ids = [c.id for c in chunks]
    result = await session.execute(
        select(related_type)
        .options(selectinload(related_type.chunk))
        .where(related_type.chunk_id.in_(chunk_ids))
    )
    return result.scalars().all()


async def get_chunks_by_children(
        children_lst: list[ChunkTokens | ChunkVector],
        children_type: type,
        session: AsyncSession
) -> list[Chunk]:
    chunks = []

    if children_type != ChunkTokens and children_type != ChunkVector:
        raise ValueError("Unknown children type")

    for child in children_lst:
        child_result = await session.execute(
            select(children_type)
            .options(
                selectinload(children_type.chunk)
            )
            .where(ChunkTokens.id == child.id)
        )
        child = child_result.scalar_one_or_none()
        if not child:
            raise ChunkInvalid
        chunks.append(child.chunk)

    return chunks
