from sentence_transformers import util
from src.semantic_search.embedder import Embedder


class SemanticSearch:
    def __init__(self, df):
        self.df = df

    def search_best(self, query):
        embedder = Embedder(self.df)
        embedded_query = embedder.embed_query(query)
        embedded_corpus = embedder.loaded_embedded_corpus()
        cor_scores = util.pytorch_cos_sim(embedded_query, embedded_corpus)[0]

        best_index = int(cor_scores.argmax())
        quote = f"{self.df[best_index]['title']} [{best_index}]"
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote
