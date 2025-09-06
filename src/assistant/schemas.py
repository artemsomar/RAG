from pydantic import BaseModel


class RagRequest(BaseModel):
    prompt: str
    method: str = "bm25"
    best_num: int = 1


class LlmRequest(BaseModel):
    prompt: str


class LlmResponse(BaseModel):
    response: str


class RagResponse(BaseModel):
    documents_titles: list[str]
    chunks_text: list[str]
