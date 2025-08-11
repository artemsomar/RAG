from pathlib import Path
import pickle
from nltk.corpus import stopwords
import re


class BaseProcessor:

    def __init__(self, default_path_to_file):
        self.path_to_file = default_path_to_file


    def _preprocess_df(self, df):
        stop_words = set(stopwords.words("english"))

        texts = [f"{x['title']}\t{x['abstract']}" for x in df]
        processed_texts = []
        for text in texts:
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', ' ', text) 
            text = re.sub(r'\s+', ' ', text).strip()
            words = [w for w in text.split() if w not in stop_words]
            processed_texts.append(" ".join(words))
        return processed_texts
    

    def _load_file(self, path_to_file: str):
        if Path(path_to_file).is_file():
            with open(path_to_file, "rb") as f:
                return pickle.load(f) 
        else:
            raise Exception(f"There is no saved file in {path_to_file}")
        

    def _save_file(self, corpus, path_to_file: str):
        Path(path_to_file).parent.mkdir(parents=True, exist_ok=True)
        with open(path_to_file, "wb") as f:
            pickle.dump(corpus, f)

