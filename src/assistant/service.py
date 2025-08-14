from src.core.llm_provider import LlmProvider
from src.core.rag.rag_controller import RagController


class RetrievalService:

    def __init__(self):
        self._llm_provider = LlmProvider()
        self._rag_controller = RagController()


    def generate_answer_with_rag(
            self,
            prompt: str,
            method: str = "bm25",
    ):
        best_abstract, quote = self._rag_controller.search_best(prompt, method)
        prompt += f"\nAnswer this question referring to this information: {best_abstract}"
        answer = f"{self._llm_provider.chat_completion(prompt)} {quote}"
        return answer