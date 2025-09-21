from typing import Optional
from pydantic import BaseModel


class DocumentSchema(BaseModel):
    id: int
    title: str
    content: str
    source_url: Optional[str] = None


class DocumentCreate(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None


class DocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source_url: Optional[str] = None