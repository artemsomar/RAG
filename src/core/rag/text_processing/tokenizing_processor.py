from pathlib import Path
import pickle
from .base_processor import BaseProcessor
from nltk.tokenize import word_tokenize
import nltk


class TokenizingProcessor(BaseProcessor):
    
    def __init__(self, default_path_to_file="data/tokenized_corpus.pkl"):
        super().__init__(default_path_to_file)
        

    def get_tokenized_corpus(self, df, path_to_file=None):

        if path_to_file is None:
            path_to_file = self.path_to_file
        else:
            self.path_to_file = path_to_file

        if Path(path_to_file).is_file():
            with open(path_to_file, "rb") as f:
                print("Loading tokenized file")
                return pickle.load(f)
        else:
            corpus = self.__tokenize_df(df, path_to_file)
            return corpus


    def get_tokenized_query(self, query):
        return word_tokenize(query.lower())
    

    def __tokenize_df(self, df, path_to_file):

        nltk.download('punkt_tab')

        preprocessed_texts = self._preprocess_df(df)
        tokenized_corpus = [word_tokenize(x) for x in preprocessed_texts]

        super()._save_file(tokenized_corpus, path_to_file)

        return tokenized_corpus