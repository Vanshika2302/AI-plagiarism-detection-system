"""
Embedding generation using Sentence-Transformers.
Loaded once at process startup and reused across requests — loading the
model per-request would be far too slow.
"""
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"  # 384-dim, fast, strong semantic quality/speed tradeoff


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Return an (n, 384) array of embeddings for a list of text chunks."""
    model = get_model()
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)


def embed_single(text: str) -> np.ndarray:
    return embed_texts([text])[0]
