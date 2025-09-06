import os
from pathlib import Path
import pickle
import cohere
from .base_processor import BaseProcessor


class EmbeddingProcessor(BaseProcessor):
    
    def __init__(self, default_path_to_file="data/embedded_corpus.pkl"):
        super().__init__(default_path_to_file)
        self._cohere_async_v2 = cohere.AsyncClientV2(os.getenv("CO_TOKEN"))
        self._embedding_model = os.getenv("CO_EMBEDDING_MODEL")

    async def get_embedded_corpus(self, df, path_to_file=None):

        if path_to_file is None:
            path_to_file = self.path_to_file
        else:
            self.path_to_file = path_to_file

        if Path(path_to_file).is_file():
            with open(path_to_file, "rb") as f:
                print("Loading embedded file")
                return pickle.load(f)
        else:
            corpus = await self.__embed_df(df, path_to_file)
            return corpus


    async def get_embedded_query(self, query):
        embedded_quary_reult = await self._cohere_async_v2.embed(
            texts=[query],
            model=self._embedding_model,
            input_type="search_query",
            embedding_types=["float"],
        )
        embedded_quary = embedded_quary_reult.embeddings.float[0]
        return embedded_quary
    

    async def __embed_df(self, df, path_to_file):

        embedded_corpus = []
        chunk_size = 96

        for i in range(0, len(df), chunk_size):
            chunk = df[i:i+chunk_size]
            texts = [f"{t}\n{a}" for t, a in zip(chunk["title"], chunk["abstract"])]
            embedded_batch_result = await self._cohere_async_v2.embed(
                texts=texts,
                model=self._embedding_model,
                input_type="search_document",
                embedding_types=["float"]
            )
            embedded_batch = embedded_batch_result.embeddings.float
            embedded_corpus.extend(embedded_batch)

        super()._save_file(embedded_corpus, path_to_file)

        return embedded_corpus
