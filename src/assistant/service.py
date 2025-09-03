from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.llm_provider import LlmProvider
from src.core.rag.rag_controller import RagController
from .utils import get_chunks_info
from ..models import Prompt


class RetrievalService:

    def __init__(self):
        self._llm_provider = LlmProvider()
        self._rag_controller = RagController()


    async def generate_answer_with_rag(
            self,
            query: str,
            session: AsyncSession,
            best_num: int = 1,
            method: str = "bm25",
    ):
        chunks = await self._rag_controller.search_best(query, session, best_num, method)
        chunks_info = await get_chunks_info(chunks, session)
        information, quotes = "", ""
        for chunk in chunks_info:
            information += f"{chunk.chunk_text}\n\n"
            quotes += f"\n[{chunk.document_title}] "

        prompt_result = await session.execute(
            select(Prompt).where(Prompt.template_key == "answer_with_sources")
        )
        prompt = prompt_result.scalar_one_or_none()
        if prompt is None:
            raise ValueError("Prompt with key 'answer_with_sources' not found")

        prompt = prompt.template.format(
            information=information,
            query=query,
        )

        llm_answer = await self._llm_provider.chat_completion(prompt)
        answer = f"{llm_answer} {quotes}"
        return answer