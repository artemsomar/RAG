from dotenv import load_dotenv
from src.rag import RagController
import os
from huggingface_hub import InferenceClient

load_dotenv()

class LLMClient:

    def __init__(self, model):
        self.model = model 
        self.client = self.__connect_to_client()

    def do_request_with_rag(self, query: str, df, method: str):

        rag_controller = RagController(df)
        abstract, source = rag_controller.search_best(query, method)

        prompt = f"""
        Considering the following information from scientific abstract:
        {abstract}
    
        Give answer for this question:
        {query}
        """

        result = self.do_request(prompt) + source
        return result

    def do_request(self, prompt):
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
        result = completion.choices[0].message.content
        return result

    def __connect_to_client(self):
        client = InferenceClient(
            model = self.model,
            provider = "novita",
            api_key = os.getenv("HF_TOKEN"),
        )
        return client
