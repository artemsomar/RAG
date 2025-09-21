from sqlalchemy.ext.asyncio import AsyncSession
from src.retrieval.preprocessing import chunking, embedding, tokenizing
from src.models import Chunk, Document, ChunkTokens, ChunkVector
from src.retrieval.exceptions import InvalidRagMethod
from src.retrieval.methods import bm25, semantic_search
from src.retrieval.services.chunks_service import get_chunks_from_session, create_chunks_into_session, \
    get_chunks_related, get_chunks_by_children


async def get_best_chunks(
        query: str,
        documents: list[Document],
        method: str,
        best_num: int,
        session: AsyncSession
) -> list[Chunk]:
    strategies = {
        "bm25": {
            "child_type": ChunkTokens,
            "preprocess_chunks": tokenizing.preprocess_chunks,
            "preprocess_query": tokenizing.preprocess_query,
            "search_best": bm25.search_best,
        },
        "semantic": {
            "child_type": ChunkVector,
            "preprocess_chunks": embedding.preprocess_chunks,
            "preprocess_query": embedding.preprocess_query,
            "search_best": semantic_search.search_best,
        }
    }

    if method not in strategies:
        raise InvalidRagMethod

    strat = strategies[method]
    processed_chunks: list[ChunkTokens | ChunkVector] = []

    for document in documents:
        chunks = await get_chunks_from_session(document, session)
        if not chunks:
            raw_chunks = chunking.chunk_document_by_characters(document)
            chunks = await create_chunks_into_session(raw_chunks, session)

        children = await get_chunks_related(chunks, strat["child_type"], session)
        if not children:
            children = await strat["preprocess_chunks"](document, chunks)
            children = await create_chunks_into_session(children, session)

        processed_chunks.extend(children)

    query_repr = await strat["preprocess_query"](query)
    best_children = strat["search_best"](query_repr, processed_chunks, best_num)
    best_chunks = await get_chunks_by_children(best_children, strat["child_type"], session)
    return best_chunks



