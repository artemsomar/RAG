from src.config import settings
from src.database.models import Document, Chunk


def chunk_document_by_characters(
    document: Document,
    chunk_size: int = settings.chunking.size_in_characters,
    overlap: int = settings.chunking.overlap_in_characters,
) -> list[Chunk]:

    chunks: list[Chunk] = []

    start_index = 0
    serial_idx = 0
    end_index = chunk_size

    while start_index < len(document.content):
        if end_index > len(document.content):
            end_index = len(document.content)

        chunk = Chunk(
            start_index=start_index,
            end_index=end_index,
            serial_idx=serial_idx,
            document=document,
        )
        chunks.append(chunk)
        start_index = start_index + chunk_size - overlap
        end_index = end_index + chunk_size - overlap

    return chunks
