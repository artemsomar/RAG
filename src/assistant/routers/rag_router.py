from src.models import Document
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_dependency
from src.core.rag.rag_controller import RagController
from ..schemas import RagRequest, RagResponse

router = APIRouter()

@router.post("/", response_model=RagResponse)
async def rag_search(request: RagRequest, rag_controller: RagController = Depends(), session: AsyncSession = Depends(session_dependency)):

    chunks = await rag_controller.search_best(
        query=request.prompt,
        session=session,
        method=request.method,
        best_num=request.best_num,
    )
    documents_titles = []
    chunks_text = []

    for chunk in chunks:
        document = await session.get(Document, chunk.document_id)
        # TODO: Add validation

        documents_titles.append(document.title)
        text = document.content[chunk.start_index:chunk.end_index]
        chunks_text.append(text)

    return RagResponse.model_validate( {
        "documents_titles": documents_titles,
        "chunks_text": chunks_text
    })