from pathlib import Path
import pickle
from .base_processor import BaseProcessor
from sentence_transformers import SentenceTransformer


class EmbeddingProcessor(BaseProcessor):
    
    def __init__(self, default_path_to_file="data/embedded_corpus.pkl"):
        super().__init__(default_path_to_file)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        

    def get_embedded_corpus(self, df, path_to_file=None):

        if path_to_file is None:
            path_to_file = self.path_to_file
        else:
            self.path_to_file = path_to_file

        if Path(path_to_file).is_file():
            with open(path_to_file, "rb") as f:
                print("Loading embedded file")
                return pickle.load(f)
        else:
            corpus = self.__embed_df(df, path_to_file)
            return corpus


    def get_embedded_query(self, query):
        return self.model.encode(query, convert_to_numpy=True)
    

    def __embed_df(self, df, path_to_file):
        
        preprocessed_texts = self._preprocess_df(df)
        embedded_corpus = self.model.encode(preprocessed_texts, convert_to_tensor=True)
        embedded_corpus_numpy = embedded_corpus.cpu().numpy()

        super()._save_file(embedded_corpus_numpy, path_to_file)

        return embedded_corpus_numpy
