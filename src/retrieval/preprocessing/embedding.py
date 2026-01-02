import cohere
from src.config import settings
from src.database.models import Document, Chunk, ChunkVector
from src.retrieval.services.chunks_service import get_chunk_text


CLIENT = cohere.AsyncClientV2(settings.embedding.token)
MODEL = settings.embedding.model
BATCH_SIZE = settings.embedding.batch_size


async def preprocess_chunks(
    document: Document,
    chunks: list[Chunk],
) -> list[ChunkVector]:

    vectors: list[ChunkVector] = []

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        batch_text = [get_chunk_text(chunk, document) for chunk in batch]
        # TODO: Normalization
        embedded_batch_result = await CLIENT.embed(
            texts=batch_text,
            model=MODEL,
            input_type="search_document",
            embedding_types=["float"],
        )
        embedded_batch = embedded_batch_result.embeddings.float
        for index, embedding in enumerate(embedded_batch):
            chunk_vector = ChunkVector(
                vector=embedding, model=MODEL, chunk=chunks[i + index]
            )
            vectors.append(chunk_vector)

    return vectors


async def preprocess_query(query) -> list[float]:
    embedded_query_result = await CLIENT.embed(
        texts=[query],
        model=MODEL,
        input_type="search_query",
        embedding_types=["float"],
    )
    embedded_query = embedded_query_result.embeddings.float[0]
    return embedded_query
