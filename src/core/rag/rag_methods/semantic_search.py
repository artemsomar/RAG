from sentence_transformers import util
from src.core.rag.text_processing.embedding_processor import EmbeddingProcessor


class SemanticSearch:

    def __init__(self, df):
        self.df = df
        self.embedder = EmbeddingProcessor()
        self.embedded_corpus = self.embedder.get_embedded_corpus(df)


    def search_best(self, query) -> tuple[str, str]:
        embedded_query = self.embedder.get_embedded_query(query)
        cor_scores = util.pytorch_cos_sim(embedded_query, self.embedded_corpus)[0]
        best_index = int(cor_scores.argmax()) 
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote


    def get_all_scores(self, query):
        embedded_query = self.embedder.get_embedded_query(query)
        cor_scores = util.pytorch_cos_sim(embedded_query, self.embedded_corpus)[0].cpu().numpy()

        return cor_scores