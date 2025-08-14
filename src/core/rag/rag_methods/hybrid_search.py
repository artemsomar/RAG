from sklearn.preprocessing import minmax_scale
from src.core.rag.rag_methods.bm25_search import BM25
from src.core.rag.rag_methods.semantic_search import SemanticSearch


class HybridSearch:

    def __init__(self, df):
        self.df = df
        self.bm25 = BM25(df)
        self.ss = SemanticSearch(df)


    def search_best(self, query):
        bm25_scores = self.bm25.get_all_scores(query)
        ss_scores = self.ss.get_all_scores(query)

        combined_scores = minmax_scale(bm25_scores) + minmax_scale(ss_scores)
        best_index = int(combined_scores.argmax())
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote
