from dotenv import load_dotenv
from src.bm25.bm25_search import BM25
from src.semantic_search.semantic_search import SemanticSearch
import os
from huggingface_hub import InferenceClient

load_dotenv()

class LLMClient:

    def __init__(self, model, df):
        self.model = model 
        self.client = self._connect_to_client()
        self.df = df

    def do_request(self, query, use_bm25: bool = True, use_ss: bool = False):
        prompt, source = self._create_prompt(query, use_bm25, use_ss)
    
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
        result = completion.choices[0].message.content + source
        return result

    def _create_prompt(self, query, use_bm25, use_ss):
        
        quote = ""
        if use_bm25:
            abstract, quote = self._get_bm25_result(query)  
        if use_ss:
            abstract, quote = self._get_ss_result(query)
        
        if use_bm25 or use_ss:
            prompt = f"""
            Considering the following information from scientific abstracts:
            {abstract}
        
            Give answer for this question:
            {query}
            """
        else:
            prompt = f"""
            Answer the following question without additional context:
            {query}
            """
            
        return prompt, quote

    def _get_bm25_result(self, query):
        bm25 = BM25(self.df)
        abstract, quote = bm25.search_best(query)
        return abstract, quote
    
    def _get_ss_result(self, query):
        ss = SemanticSearch(self.df)
        abstract, quote = ss.search_best(query)
        return abstract, quote

    def _connect_to_client(self):
        client = InferenceClient(
            model = self.model,
            provider = "novita",
            api_key = os.getenv("HF_TOKEN"),
        )
        return client
