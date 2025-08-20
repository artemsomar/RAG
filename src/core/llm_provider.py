import os
import cohere
from dotenv import load_dotenv

load_dotenv()


class LlmProvider:

    def __init__(self):
        self.model = os.getenv("CO_MODEL")
        self.api_key = os.getenv("CO_TOKEN")
        self.client = cohere.AsyncClientV2(api_key=self.api_key)


    async def chat_completion(self, user_prompt: str) -> str:
        completion = await self.client.chat(
            model=self.model,
            messages=[cohere.UserChatMessageV2(content=user_prompt)],
        )
        return completion.message.content[0].text
