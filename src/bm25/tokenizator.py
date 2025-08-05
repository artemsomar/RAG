from pathlib import Path
import pickle
from nltk.tokenize import word_tokenize

class Tokenizator:
    def __init__(self, df, path_to_file="data/bm25_tokenized_corpus.pkl"):
        self.df = df
        self.path_to_file = path_to_file

    def load_tokenized_corpus(self):
        if Path(self.path_to_file).is_file():
            with open(self.path_to_file, "rb") as f:
                print("Loaded tokenized corpus.")
                return pickle.load(f) 
        else:
            tokenized_corpus = self._tokenize_and_save()
            return tokenized_corpus

    def tokenize_query(self, query):
        return word_tokenize(query.lower())
        

    def _tokenize_and_save(self):
        texts = [f"{x['title']}\t{x['abstract']}" for x in self.df]
        tokenized_corpus = [word_tokenize(doc.lower()) for doc in texts]

        Path(self.path_to_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.path_to_file, "wb") as f:
            pickle.dump(tokenized_corpus, f)

        return tokenized_corpus
    
    
    