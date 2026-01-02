import numpy as np
from rank_bm25 import BM25Okapi
from src.database.models import ChunkTokens


def search_best(
    tokenized_query: list[int], processed_chunks: list[ChunkTokens], best_num: int = 1
) -> list[ChunkTokens]:

    tokenized_corpus = [chunk.tokens for chunk in processed_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    doc_scores = np.asarray(bm25.get_scores(tokenized_query)).flatten()
    top_indices = np.argsort(doc_scores)[-best_num:][::-1]
    best_chunks_tokens = [processed_chunks[i] for i in top_indices]
    return best_chunks_tokens


def get_all_scores(
    tokenized_query: list[int],
    processed_chunks: list[ChunkTokens],
) -> list[list[float]]:
    tokenized_corpus = [chunk_tokens.tokens for chunk_tokens in processed_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    return bm25.get_scores(tokenized_query)
