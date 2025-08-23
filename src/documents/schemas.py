from typing import Optional
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None


class Document(DocumentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    title: str | None = None
    content: str | None = None
    source_url: Optional[str] = None