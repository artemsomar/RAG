import torch
from sentence_transformers import util
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Document, EmbeddedChunk
from src.core.rag.text_processing.embedding import Embedding

class SemanticSearch:

    def __init__(self):
        self.embedder = Embedding()


    async def search_best(
            self,
            query: str,
            documents: list[Document],
            session: AsyncSession,
            best_num: int = 1
    ) -> list[EmbeddedChunk]:

        best_scores: list[float] = []
        best_chunks: list[EmbeddedChunk] = []

        embedded_query = await self.embedder.get_embedded_query(query)
        for document in documents:
            embedded_chunks = await self.embedder.get_embedded_chunks(document, session)
            chunks_vectors = [chunk.vector for chunk in embedded_chunks]
            embedded_chunks_tensor = torch.tensor(chunks_vectors, dtype=torch.float32)
            cor_scores = util.pytorch_cos_sim(embedded_query, embedded_chunks_tensor)[0]
            local_top_indices = cor_scores.topk(best_num).indices.tolist()
            for idx in local_top_indices:
                best_scores.append(cor_scores[idx].item())
                best_chunks.append(embedded_chunks[idx])

        best_scores_tensor = torch.tensor(best_scores)
        global_top_indices = best_scores_tensor.topk(best_num).indices.tolist()
        best_chunks = [best_chunks[i] for i in global_top_indices]
        return best_chunks


    async def get_all_scores(
            self,
            query: str,
            documents: list[Document],
            session: AsyncSession
    ) -> list[list[float]]:
        scores: list[list[float]] = []
        embedded_query = await self.embedder.get_embedded_query(query)
        for document in documents:
            embedded_chunks = await self.embedder.get_embedded_chunks(document, session)
            chunks_vectors = [chunk.vector for chunk in embedded_chunks]
            embedded_chunks_tensor = torch.tensor(chunks_vectors, dtype=torch.float32)
            cor_scores = util.pytorch_cos_sim(embedded_query, embedded_chunks_tensor)[0]

            scores.append(cor_scores.tolist())

        return scores