from rank_bm25 import BM25Okapi
from src.core.rag.text_processing.tokenizing_processor import TokenizingProcessor

class BM25:

    def __init__(self, df):
        self.df = df
        self.tokenizer = TokenizingProcessor()


    async def search_best(self, query) -> tuple[str, str]:

        tokenized_corpus = await self.tokenizer.get_tokenized_corpus(self.df)
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = await self.tokenizer.get_tokenized_query(query)
        doc_scores = bm25.get_scores(tokenized_query)

        best_index = int(doc_scores.argmax())
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote


    async def get_all_scores(self, query):

        tokenized_corpus = await self.tokenizer.get_tokenized_corpus(self.df)
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = await self.tokenizer.get_tokenized_query(query)
        doc_scores = bm25.get_scores(tokenized_query)

        return doc_scores