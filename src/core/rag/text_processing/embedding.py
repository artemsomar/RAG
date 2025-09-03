import cohere
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from torch import Tensor

from .utils import chunk_document_by_characters
from src.config import settings
from src.models import Document, EmbeddedChunk


class Embedding:
    
    def __init__(self, model = settings.embedding.model, batch_size = settings.embedding.batch_size):
        self._client = cohere.AsyncClientV2(settings.embedding.token)
        self._embedding_model = model
        self._model_embedding_batch = batch_size


    async def get_embedded_chunks(self, document: Document, session: AsyncSession) -> list[EmbeddedChunk]:
        loaded_document = await session.execute(
            select(Document)
            .options(selectinload(Document.embedded_chunks))
            .where(Document.id == document.id)
        )
        loaded_document = loaded_document.scalars().first()
        if not loaded_document.embedded_chunks:
            await self._document_embedding_by_chunks(loaded_document, session)
        chunks = await session.execute(
            select(EmbeddedChunk).order_by(asc(EmbeddedChunk.serial_idx))
        )

        return list(chunks.scalars().all())


    async def get_embedded_query(self, query) -> Tensor:
        embedded_query_result = await self._client.embed(
            texts=[query],
            model=self._embedding_model,
            input_type="search_query",
            embedding_types=["float"],
        )
        embedded_query = embedded_query_result.embeddings.float[0]
        return embedded_query


    async def _document_embedding_by_chunks(self, document: Document, session: AsyncSession):
        indexed_chunks = chunk_document_by_characters(
            document,
            settings.chunking.chunk_size_in_characters,
            settings.chunking.overlap_in_characters
        )
        for i in range(0, len(indexed_chunks), self._model_embedding_batch):
            batch = indexed_chunks[i:i+self._model_embedding_batch]
            batch_text = [chunk[0] for chunk in batch]
            embedded_batch_result = await self._client.embed(
                texts=batch_text,
                model=self._embedding_model,
                input_type="search_document",
                embedding_types=["float"]
            )
            embedded_batch = embedded_batch_result.embeddings.float
            for index in range(len(embedded_batch)):
                embedded_chunk = EmbeddedChunk(
                    vector=embedded_batch[index],
                    model=self._embedding_model,
                    start_index=indexed_chunks[index][1],
                    end_index=indexed_chunks[index][2],
                    serial_idx=index,
                    document=document,
                )
                session.add(embedded_chunk)

        await session.commit()
