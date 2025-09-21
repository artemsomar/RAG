import cohere
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import settings
from src.retrieval.services import retrieval_service, chunks_service
from src.models import Document, Prompt


MODEL = settings.llm.model
CLIENT = cohere.AsyncClientV2(settings.llm.token)


async def generate_rag_answer(
        query: str,
        documents: list[Document],
        method: str,
        best_num: int,
        session: AsyncSession,
) -> str:
    chunks = await retrieval_service.get_best_chunks(
        query,
        documents,
        method,
        best_num,
        session
    )
    chunks_info = await chunks_service.get_chunks_info(chunks, session)
    information, quotes = "", ""
    for document_title, content in chunks_info:
        information += f"{content}\n\n"
        quotes += f"\n[{document_title}] "

    prompt_template = await _get_prompt_template("answer_with_sources", session)

    prompt = prompt_template.template.format(
        information=information,
        query=query,
    )

    llm_answer = await chat_completion(prompt)
    answer = f"{llm_answer} {quotes}"
    return answer


async def chat_completion(user_prompt: str) -> str:
    completion = await CLIENT.chat(
        model=MODEL,
        messages=[cohere.UserChatMessageV2(content=user_prompt)],
    )
    return completion.message.content[0].text


async def _get_prompt_template(
        template_key: str,
        session: AsyncSession
):
    prompt_result = await session.execute(
        select(Prompt).where(Prompt.template_key == template_key)
    )
    prompt = prompt_result.scalar_one_or_none()
    if prompt is None:
        raise ValueError("Prompt with key 'answer_with_sources' not found")
    return prompt