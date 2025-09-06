from pydantic import BaseModel


class RagRequest(BaseModel):
    prompt: str
    method: str = "bm25"
    best_num: int = 1


class LlmRequest(BaseModel):
    prompt: str


class LlmResponse(BaseModel):
    response: str

class ChunkResponse(BaseModel):
    document_title: str
    chunk_text: str

class RagResponse(BaseModel):
    chunks: list[ChunkResponse]
