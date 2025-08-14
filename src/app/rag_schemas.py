from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    method: str = "bm25"

class QueryResponse(BaseModel):
    response: str