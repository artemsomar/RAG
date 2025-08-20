from sentence_transformers import util
from src.core.rag.text_processing.embedding_processor import EmbeddingProcessor


class SemanticSearch:

    def __init__(self, df):
        self.df = df
        self.embedder = EmbeddingProcessor()


    async def search_best(self, query) -> tuple[str, str]:
        embedded_query = await self.embedder.get_embedded_query(query)
        embedded_corpus = await self.embedder.get_embedded_corpus(self.df)
        cor_scores = util.pytorch_cos_sim(embedded_query, embedded_corpus)[0]
        best_index = int(cor_scores.argmax()) 
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote


    async def get_all_scores(self, query):
        embedded_query = await self.embedder.get_embedded_query(query)
        embedded_corpus = await self.embedder.get_embedded_corpus(self.df)
        cor_scores = util.pytorch_cos_sim(embedded_query, embedded_corpus)[0]

        return cor_scores