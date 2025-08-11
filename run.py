from src.dataset_loader import DatasetLoader
from src.llm_client import LLMClient

import nltk
nltk.download('punkt_tab')


def main():
    data_loader = DatasetLoader()
    df = data_loader.load()
    
    model = "meta-llama/Llama-3.1-8B-Instruct"
    query = "How neural networks are used for text classification"

    llm = LLMClient(model)

    print(llm.do_request_with_rag(query, df, method="bm25"))
  

if __name__ == "__main__":
    main()