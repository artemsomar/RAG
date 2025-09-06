from pydantic import BaseModel


class RagRequest(BaseModel):
    prompt: str
    method: str = "bm25"


class LlmRequest(BaseModel):
    prompt: str


class LlmResponse(BaseModel):
    response: str


class RagResponse(BaseModel):
    quote: str
    best_abstract: str