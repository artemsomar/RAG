from pathlib import Path
import pickle
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, df, path_to_file="data/embedded_corpus.pkl"):
        self.df = df
        self.path_to_file = path_to_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def loaded_embedded_corpus(self):
        if Path(self.path_to_file).is_file():
            with open(self.path_to_file, "rb") as f:
                print("Loading embedded file")
                return pickle.load(f)
        else:
            corpus = self._embed_and_save()
            return corpus

    def embed_query(self, query):
        return self.model.encode(query, convert_to_tensor=True)

    def _embed_and_save(self):
        texts = [f"{x['title']}\t{x['abstract']}" for x in self.df]
        print("Embedding text...")
        embedded_corpus = self.model.encode(texts, convert_to_tensor=True)

        Path(self.path_to_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.path_to_file, "wb") as f:
            pickle.dump(embedded_corpus, f)
        print("Embedded corputs was saved")
        
        return embedded_corpus
