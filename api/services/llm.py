from dotenv import load_dotenv
from src.rag import RagController  # Імпорт RagController із src
from huggingface_hub import InferenceClient
import os
from pandas import DataFrame

load_dotenv()

class LLMService:

    def __init__(self, model: str):
        self.model = model
        self.client = self._connect_to_client()
        self.rag_controller = RagController() 


    async def do_request_with_rag(self, query: str, method: str) -> str:

        abstract, source = self.rag_controller.search_best(query, method)

        prompt = f"""
        Considering the following information from scientific abstract:
        {abstract}
    
        Give answer for this question:
        {query}
        """
        result = self.do_request(prompt)
        return result + source


    def do_request(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Give accurate, short answers to the question asked."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content


    def _connect_to_client(self) -> InferenceClient:
        client = InferenceClient(
            model=self.model,
            provider="novita",
            api_key=os.getenv("HF_TOKEN"),
        )
        return client