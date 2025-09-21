from pydantic import BaseModel


class RagRequest(BaseModel):
    query: str
    method: str = "bm25"
    best_num: int = 1

class ChunkInfo(BaseModel):
    document_title: str
    content: str

class RagResponse(BaseModel):
    chunks: list[ChunkInfo]


