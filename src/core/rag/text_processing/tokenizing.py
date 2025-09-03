import cohere
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.config import settings
from src.models import Document, TokenizedChunk
from .utils import chunk_document_by_characters


class Tokenizing:
    
    def __init__(self, model: str = settings.tokenizing.model):
        self._client = cohere.AsyncClient(settings.tokenizing.token)
        self._model = model


    async def get_tokenized_chunks(self, document: Document, session: AsyncSession) -> list[TokenizedChunk]:
        loaded_document = await session.execute(
            select(Document)
            .options(selectinload(Document.tokenized_chunks))
            .where(Document.id == document.id)
        )
        loaded_document = loaded_document.scalars().first()
        if not loaded_document.tokenized_chunks:
            await self._document_tokenizing_by_chunks(loaded_document, session)
        chunks = await session.execute(
            select(TokenizedChunk).order_by(asc(TokenizedChunk.serial_idx))
        )

        return list(chunks.scalars().all())


    async def get_tokenized_query(self, query):
        text = query.lower()
        tokens_info = await self._client.tokenize(
            text=text,
            model=self._model
        )
        return tokens_info.tokens


    async def _document_tokenizing_by_chunks(self, document: Document, session: AsyncSession):
        indexed_chunks = chunk_document_by_characters(document)
        for index, indexed_chunk in enumerate(indexed_chunks):
            tokens_info = await self._client.tokenize(
                text=indexed_chunk[0].lower(),
                model=self._model
            )
            tokenized_chunk = TokenizedChunk(
                tokens = tokens_info.tokens,
                model=self._model,
                start_index=indexed_chunks[index][1],
                end_index=indexed_chunks[index][2],
                serial_idx=index,
                document=document,
            )
            session.add(tokenized_chunk)

        await session.commit()
