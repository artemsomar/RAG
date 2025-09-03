from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ChunkInfo
from src.models import TokenizedChunk, EmbeddedChunk, Document


async def get_chunks_info(
        chunks: list[TokenizedChunk | EmbeddedChunk],
        session: AsyncSession
) -> list[ChunkInfo]:

    documents_titles = []
    chunks_text = []

    for chunk in chunks:
        document = await session.get(Document, chunk.document_id)
        # TODO: Add validation

        documents_titles.append(document.title)
        text = document.content[chunk.start_index:chunk.end_index]
        chunks_text.append(text)


    chunks_info = [
        ChunkInfo(document_title=title, chunk_text=text)
        for title, text in zip(documents_titles, chunks_text)
    ]
    return chunks_info
