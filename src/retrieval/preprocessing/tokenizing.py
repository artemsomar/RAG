import cohere
from src.config import settings
from src.models import Document, ChunkTokens, Chunk
from ..services.chunks_service import get_chunk_text


CLIENT = cohere.AsyncClient(settings.tokenizing.token)
MODEL = settings.tokenizing.model


async def preprocess_chunks(
        document: Document,
        chunks: list[Chunk],
) -> list[ChunkTokens]:

    chunks_tokens: list[ChunkTokens] = []
    for chunk in chunks:
        tokens_result = await CLIENT.tokenize(
            # TODO: Normalization
            text=get_chunk_text(chunk, document).lower(),
            model=MODEL
        )
        tokens = tokens_result.tokens
        chunk_token = ChunkTokens(
            tokens=tokens,
            model=MODEL,
            chunk=chunk
        )
        chunks_tokens.append(chunk_token)

    return chunks_tokens


async def preprocess_query(query) -> list[int]:
    text = query.lower()
    tokens_info = await CLIENT.tokenize(
        text=text,
        model=MODEL
    )
    return tokens_info.tokens
