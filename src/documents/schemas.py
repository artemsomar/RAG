from typing import Optional
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    content: str
    source_url: Optional[str] = None


class DocumentSchema(DocumentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    title: str | None = None
    content: str | None = None
    source_url: Optional[str] = None