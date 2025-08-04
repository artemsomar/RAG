
from src.bm25.tokenizator import Tokenizator
from src.dataset_loader import DatasetLoader
import nltk
nltk.download('punkt_tab')

def main():
    data_loader = DatasetLoader()
    df = data_loader.load()
    tokenizator = Tokenizator(df)
    tokenized_corpus = tokenizator.load_tokenized_corpus()
    return tokenized_corpus

if __name__ == "__main__":
    main()