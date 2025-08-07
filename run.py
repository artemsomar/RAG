from src.dataset_loader import DatasetLoader
from src.llm_client import LLMClient

import nltk
nltk.download('punkt_tab')


def main():
    data_loader = DatasetLoader()
    df = data_loader.load()
    
    model="meta-llama/Meta-Llama-3-8B-Instruct"
    query = "How neural networks are used for text classification"

    client = LLMClient(model, df)
    answer = client.do_request(query)
    print(answer)
    

if __name__ == "__main__":
    main()