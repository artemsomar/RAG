from src.dataset_loader import DatasetLoader
from src.llm_client import LLMClient
from src.bm25_ss_search import Bm25SsSearch

import nltk
nltk.download('punkt_tab')


def main():
    data_loader = DatasetLoader()
    df = data_loader.load()
    
    model = "meta-llama/Llama-3.1-8B-Instruct"
    query = "How neural networks are used for text classification"

    rag = Bm25SsSearch(df)
    answer, quote = rag.search_best(query)
    print(answer + quote)
    

if __name__ == "__main__":
    main()