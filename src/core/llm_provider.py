import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

SYSTEM_PROMPT = "You are a research assistant. Give accurate, short answers to the question asked."

class LlmProvider:

    def __init__(self):
        self.model = os.getenv("HF_MODEL")
        self.provider = os.getenv("HF_PROVIDER")
        self.api_key = os.getenv("HF_API_KEY")
        self.client = self.__connect_to_client()


    def __connect_to_client(self) -> InferenceClient:
        client = InferenceClient(
            model=self.model,
            provider=self.provider,
            api_key=self.api_key,
        )
        return client


    def chat_completion(self, user_prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                { "role": "system", "content": SYSTEM_PROMPT },
                { "role": "user", "content": user_prompt }
            ]
        )
        return completion.choices[0].message.content
