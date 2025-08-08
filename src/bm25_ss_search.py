from sklearn.preprocessing import minmax_scale
from src.bm25.bm25_search import BM25
from src.semantic_search.semantic_search import SemanticSearch


class Bm25SsSearch:
    def __init__(self, df):
        self.df = df

    def search_best(self, query):
        bm25 = BM25(self.df)
        bm25_scores = bm25.get_all_scores(query)

        ss = SemanticSearch(self.df)
        ss_scores = ss.get_all_scores(query)

        combined_scores = minmax_scale(bm25_scores) + minmax_scale(ss_scores)
        best_index = int(combined_scores.argmax())
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote

