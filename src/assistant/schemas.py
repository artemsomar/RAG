from pydantic import BaseModel


class RagRequest(BaseModel):
    query: str
    method: str = "bm25"
    best_num: int = 1

class LlmRequest(BaseModel):
    query: str

class LlmResponse(BaseModel):
    response: str

class ChunkInfo(BaseModel):
    document_title: str
    chunk_text: str

class RagResponse(BaseModel):
    chunks: list[ChunkInfo]
