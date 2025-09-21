import re
import nltk
from nltk.corpus import stopwords


def normalize_text(text: str) -> str:
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = [w for w in text.split() if w not in stop_words]
    processed_text = " ".join(words)

    return processed_text