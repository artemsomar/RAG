
from rank_bm25 import BM25Okapi
from src.rag.bm25.tokenizator import Tokenizator

class BM25:
    def __init__(self, df):
        self.df = df

    def search_best(self, query):
        tokenizator = Tokenizator(self.df)
        tokenized_corpus =  tokenizator.load_tokenized_corpus()
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = tokenizator.tokenize_query(query)
        doc_scores = bm25.get_scores(tokenized_query)

        best_index = int(doc_scores.argmax())
        quote = f" [{best_index}] {self.df[best_index]['title']} "
        best_abstract = self.df[best_index]['abstract']

        return best_abstract, quote
    
    def get_all_scores(self, query):
        tokenizator = Tokenizator(self.df)
        tokenized_corpus =  tokenizator.load_tokenized_corpus()
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = tokenizator.tokenize_query(query)
        doc_scores = bm25.get_scores(tokenized_query)

        return doc_scores