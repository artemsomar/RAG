from pydantic import BaseModel


class RagAssistantRequest(BaseModel):
    query: str
    method: str = "bm25"
    best_num: int = 1

class RagAssistantResponse(BaseModel):
    response: str
