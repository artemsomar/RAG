import numpy as np
from rank_bm25 import BM25Okapi
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Document, TokenizedChunk
from src.core.rag.text_processing.tokenizing import Tokenizing


class BM25:

    def __init__(self):
        self.tokenizer = Tokenizing()


    async def search_best(
            self,
            query: str,
            documents: list[Document],
            session: AsyncSession,
            best_num: int = 1
    ) -> list[TokenizedChunk]:

        best_scores: list[float] = []
        best_chunks: list[TokenizedChunk] = []

        tokenized_query = await self.tokenizer.get_tokenized_query(query)
        for document in documents:
            tokenized_chunks = await self.tokenizer.get_tokenized_chunks(document, session)
            tokenized_corpus = [chunk.tokens for chunk in tokenized_chunks]
            bm25 = BM25Okapi(tokenized_corpus)
            doc_scores = np.asarray(bm25.get_scores(tokenized_query)).flatten()
            local_top_indices = np.argsort(doc_scores)[-best_num:][::-1]
            for idx in local_top_indices:
                best_scores.append(doc_scores[idx].item())
                best_chunks.append(tokenized_chunks[idx])

        best_scores_array = np.array(best_scores)
        global_top_indices = np.argsort(best_scores_array)[-best_num:][::-1]
        best_chunks = [best_chunks[i] for i in global_top_indices]
        return best_chunks


    async def get_all_scores(
            self,
            query: str,
            documents: list[Document],
            session: AsyncSession,
    ) -> list[list[float]]:
        scores: list[list[float]] = []
        tokenized_query = await self.tokenizer.get_tokenized_query(query)
        for document in documents:
            tokenized_chunks = await self.tokenizer.get_tokenized_chunks(document, session)
            tokenized_corpus = [chunk.tokens for chunk in tokenized_chunks]
            bm25 = BM25Okapi(tokenized_corpus)
            doc_scores = bm25.get_scores(tokenized_query)
            scores.append(doc_scores)

        return scores
