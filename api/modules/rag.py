from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    method: str 

class QueryResponse(BaseModel):
    answer: str