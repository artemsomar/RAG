import os
from pathlib import Path
import pickle
import cohere
from .base_processor import BaseProcessor


class TokenizingProcessor(BaseProcessor):
    
    def __init__(self, default_path_to_file="data/tokenized_corpus.pkl"):
        super().__init__(default_path_to_file)
        self._cohere_async_v1 = cohere.AsyncClient(os.getenv("CO_TOKEN"))


    async def get_tokenized_query(self, query):
        text = query.lower()
        tokens_info = await self._cohere_async_v1.tokenize(text=text, model=self._model)
        return tokens_info.tokens


    async def get_tokenized_corpus(self, df, path_to_file=None):

        if path_to_file is None:
            path_to_file = self.path_to_file
        else:
            self.path_to_file = path_to_file

        if Path(path_to_file).is_file():
            with open(path_to_file, "rb") as f:
                print("Loading tokenized file")
                return pickle.load(f)
        else:
            corpus = await self.__tokenize_df(df, path_to_file)
            return corpus


    async def __tokenize_df(self, df, path_to_file):

        preprocessed_texts = self._preprocess_df(df)
        tokenized_corpus = []
        for text in preprocessed_texts:
            tokenized_query = await self.get_tokenized_query(text)
            tokenized_corpus.append(tokenized_query)

        super()._save_file(tokenized_corpus, path_to_file)

        return tokenized_corpus