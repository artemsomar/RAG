from src.dataset_loader import DatasetLoader
from src.bm25.bm25_search import BM25
from src.semantic_search.semantic_search import SemanticSearch

import nltk
nltk.download('punkt_tab')


def main():
    data_loader = DatasetLoader()
    df = data_loader.load()
    
    # bm25 = BM25(df)
    # best_article, _ = bm25.search_best("How neural networks are used for text classification")
    # print(f"BM25:\n{best_article}\n\n")

    ss = SemanticSearch(df)
    best_article, _ = ss.search_best("How neural networks are used for text classification")
    print(f"Semantic Search:\n{best_article}")

if __name__ == "__main__":
    main()