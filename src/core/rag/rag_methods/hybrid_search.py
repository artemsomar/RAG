import numpy as np
from sklearn.preprocessing import minmax_scale
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.rag.text_processing.tokenizing import Tokenizing
from src.models import Document, TokenizedChunk
from src.core.rag.rag_methods.bm25_search import BM25
from src.core.rag.rag_methods.semantic_search import SemanticSearch


class HybridSearch:

    def __init__(self):
        self.bm25 = BM25()
        self.ss = SemanticSearch()
        self.tokenizer = Tokenizing()


    async def search_best(
            self,
            query: str,
            documents: list[Document],
            session: AsyncSession,
            best_num: int
    ) -> list[TokenizedChunk]:

        bm25_scores = await self.bm25.get_all_scores(query, documents, session)
        ss_scores = await self.ss.get_all_scores(query, documents, session)

        np_bm25_scores, np_ss_scores = np.array(bm25_scores), np.array(ss_scores)
        bm25_scores_flat, ss_scores_flat = np_bm25_scores.flatten(), np_ss_scores.flatten()

        if len(bm25_scores_flat) != len(ss_scores_flat):
            raise Exception("Existing tokenized and embedded chunks have different chunk sizes.")

        combined_scores = minmax_scale(bm25_scores_flat) + minmax_scale(ss_scores_flat)

        top_indices = np.argpartition(combined_scores, -best_num)[-best_num:]
        top_indices = top_indices[np.argsort(-combined_scores[top_indices])]
        coords = [np.unravel_index(idx, np_bm25_scores.shape) for idx in top_indices]

        top_chunks: list[TokenizedChunk] = []
        for coord in coords:
            document = documents[coord[0]]
            tokenized_chunks = await self.tokenizer.get_tokenized_chunks(document, session)
            top_chunks.append(tokenized_chunks[coord[1]])

        return top_chunks
