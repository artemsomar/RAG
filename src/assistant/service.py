from src.core.llm_provider import LlmProvider
from src.core.rag.rag_controller import RagController


class RetrievalService:

    def __init__(self):
        self._llm_provider = LlmProvider()
        self._rag_controller = RagController()


    async def generate_answer_with_rag(
            self,
            prompt: str,
            method: str = "bm25",
    ):
        best_abstract, quote = await self._rag_controller.search_best(prompt, method)
        prompt += f"\nAnswer this question referring to this information: {best_abstract}"
        llm_answer = await self._llm_provider.chat_completion(prompt)
        answer = f"{llm_answer} {quote}"
        return answer