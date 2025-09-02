import nltk
from nltk.corpus import stopwords
import re
from src.models import Document


def chunk_document_by_words(
        document: Document,
        chunk_size: int = 50,
        overlap: int = 20,
) -> list[tuple[str, int, int]]:
    preprocessed_content = preprocess_text(document.content)
    words = preprocessed_content.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = f"{document.title}\n{' '.join(chunk_words)}"
        chunks.append(chunk_text)
        start += chunk_size - overlap
        if start < 0:
            start = 0

    return chunks


def chunk_document_by_characters(
        document: Document,
        chunk_size: int = 1000,
        overlap: int = 200,
) -> list[tuple[str, int, int]]:
    start_index = 0
    end_index = chunk_size
    chunks_with_indexes: list[tuple[str, int, int]] = []
    while start_index < len(document.content):
        if end_index > len(document.content):
            end_index = len(document.content)
        chunk_text = document.content[start_index:end_index]
        chunks_with_indexes.append((chunk_text, start_index, end_index))
        start_index = start_index + chunk_size - overlap
        end_index = end_index + chunk_size - overlap

    preprocessed_chunks = [(preprocess_text(chunk[0]), chunk[1], chunk[2]) for chunk in chunks_with_indexes]
    preprocessed_chunks_with_title = [(f"{document.title}\t{chunk[0]}", chunk[1], chunk[2]) for chunk in preprocessed_chunks]

    return preprocessed_chunks_with_title

def preprocess_text(text: str) -> str:
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = [w for w in text.split() if w not in stop_words]
    processed_text = " ".join(words)
    return processed_text