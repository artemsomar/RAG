import torch
from sentence_transformers import util
from src.database.models import ChunkVector


def search_best(
    embedded_query: list[float], processed_chunks: list[ChunkVector], best_num: int = 1
) -> list[ChunkVector]:

    embedded_query_tensor = torch.tensor(embedded_query, dtype=torch.float32)
    chunks_vectors = [chunk_vector.vector for chunk_vector in processed_chunks]
    embedded_chunks_tensor = torch.tensor(chunks_vectors, dtype=torch.float32)
    cor_scores = util.pytorch_cos_sim(embedded_query_tensor, embedded_chunks_tensor)[0]
    top_indices = cor_scores.topk(best_num).indices.tolist()
    top_chunks = [processed_chunks[i] for i in top_indices]
    return top_chunks


def get_all_scores(
    embedded_query: list[float],
    processed_chunks: list[ChunkVector],
) -> list[list[float]]:

    embedded_query_query_tensor = torch.tensor(embedded_query, dtype=torch.float32)
    chunks_vectors = [chunk_vector.vector for chunk_vector in processed_chunks]
    embedded_chunks_tensor = torch.tensor(chunks_vectors, dtype=torch.float32)
    cor_scores = util.pytorch_cos_sim(
        embedded_query_query_tensor, embedded_chunks_tensor
    )[0]
    return cor_scores.tolist()
