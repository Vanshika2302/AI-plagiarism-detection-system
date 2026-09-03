"""
Core plagiarism-scoring logic.

Combines two signals, since either one alone misses cases the other catches:
  1. Semantic similarity (sentence-transformer embeddings + cosine similarity)
     -> catches paraphrased / reworded plagiarism.
  2. Lexical similarity (TF-IDF n-gram overlap)
     -> catches near-verbatim copying, even across otherwise different documents.

Final score is a weighted blend, and we also return sentence-level matches
so the frontend can highlight exactly which sentences were flagged.
"""
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .embeddings import embed_texts

SEMANTIC_WEIGHT = 0.65
LEXICAL_WEIGHT = 0.35
SENTENCE_MATCH_THRESHOLD = 0.80  # cosine sim above which two sentences are "flagged"


@dataclass
class SentenceMatch:
    source_sentence: str
    matched_sentence: str
    similarity: float
    match_type: str  # "semantic" | "lexical" | "both"


@dataclass
class ComparisonResult:
    overall_score: float
    semantic_score: float
    lexical_score: float
    matches: list[SentenceMatch]


def lexical_similarity(text_a: str, text_b: str) -> float:
    """TF-IDF cosine similarity over word n-grams (1-3 grams)."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words="english")
    try:
        tfidf = vectorizer.fit_transform([text_a, text_b])
    except ValueError:
        # Happens if both texts are empty / all stopwords after cleaning
        return 0.0
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(sim)


def semantic_similarity(text_a: str, text_b: str) -> float:
    """Whole-document semantic similarity via sentence embeddings."""
    embeddings = embed_texts([text_a, text_b])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)


def find_sentence_matches(
    sentences_a: list[str], sentences_b: list[str]
) -> list[SentenceMatch]:
    """
    Compare every sentence in document A against every sentence in document B
    and return pairs above the similarity threshold, using both embeddings
    and lexical overlap so we catch paraphrase and copy-paste alike.
    """
    if not sentences_a or not sentences_b:
        return []

    emb_a = embed_texts(sentences_a)
    emb_b = embed_texts(sentences_b)
    sim_matrix = cosine_similarity(emb_a, emb_b)

    matches: list[SentenceMatch] = []
    for i, row in enumerate(sim_matrix):
        best_j = int(np.argmax(row))
        best_score = float(row[best_j])
        if best_score >= SENTENCE_MATCH_THRESHOLD:
            lex_score = lexical_similarity(sentences_a[i], sentences_b[best_j])
            match_type = "both" if lex_score >= 0.5 else "semantic"
            matches.append(
                SentenceMatch(
                    source_sentence=sentences_a[i],
                    matched_sentence=sentences_b[best_j],
                    similarity=round(best_score, 4),
                    match_type=match_type,
                )
            )
    return sorted(matches, key=lambda m: m.similarity, reverse=True)


def compare_documents(
    text_a: str, text_b: str, sentences_a: list[str], sentences_b: list[str]
) -> ComparisonResult:
    sem_score = semantic_similarity(text_a, text_b)
    lex_score = lexical_similarity(text_a, text_b)
    overall = SEMANTIC_WEIGHT * sem_score + LEXICAL_WEIGHT * lex_score
    matches = find_sentence_matches(sentences_a, sentences_b)

    return ComparisonResult(
        overall_score=round(overall * 100, 2),
        semantic_score=round(sem_score * 100, 2),
        lexical_score=round(lex_score * 100, 2),
        matches=matches,
    )
