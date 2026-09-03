"""
AI Microservice for the Plagiarism Detector.

Exposes:
  POST /analyze          -> extract text from an uploaded file, chunk + embed it,
                             store it in the corpus, and return similarity against
                             the existing corpus.
  POST /compare          -> direct pairwise comparison of two uploaded files.
  GET  /health           -> readiness probe for Docker/K8s.

Consumed by the Spring Boot backend, never called directly by the frontend.
"""
import logging
from contextlib import asynccontextmanager

import spacy
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from services.text_extraction import extract_text, clean_text, split_into_sentences, chunk_text
from services.embeddings import embed_texts, embed_single
from services.similarity import compare_documents
from services.vector_store import init_db, store_chunks, find_similar_chunks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("plagiarism-ai")

nlp = None  # loaded on startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    global nlp
    logger.info("Loading spaCy model + initializing DB...")
    nlp = spacy.load("en_core_web_sm")
    init_db()
    logger.info("AI microservice ready.")
    yield


app = FastAPI(title="Plagiarism Detection AI Service", lifespan=lifespan)


class SentenceMatchResponse(BaseModel):
    source_sentence: str
    matched_sentence: str
    similarity: float
    match_type: str


class CompareResponse(BaseModel):
    overall_score: float
    semantic_score: float
    lexical_score: float
    matches: list[SentenceMatchResponse]


class CorpusMatch(BaseModel):
    document_id: int
    chunk_text: str
    similarity: float


class AnalyzeResponse(BaseModel):
    document_id: int
    word_count: int
    top_corpus_matches: list[CorpusMatch]
    highest_similarity_pct: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/compare", response_model=CompareResponse)
async def compare(file_a: UploadFile = File(...), file_b: UploadFile = File(...)):
    """Direct pairwise comparison — used for A/B document checks."""
    try:
        text_a = clean_text(extract_text(file_a.filename, await file_a.read()))
        text_b = clean_text(extract_text(file_b.filename, await file_b.read()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text_a or not text_b:
        raise HTTPException(status_code=400, detail="One or both files contained no extractable text.")

    sentences_a = split_into_sentences(text_a, nlp)
    sentences_b = split_into_sentences(text_b, nlp)

    result = compare_documents(text_a, text_b, sentences_a, sentences_b)

    return CompareResponse(
        overall_score=result.overall_score,
        semantic_score=result.semantic_score,
        lexical_score=result.lexical_score,
        matches=[
            SentenceMatchResponse(
                source_sentence=m.source_sentence,
                matched_sentence=m.matched_sentence,
                similarity=m.similarity,
                match_type=m.match_type,
            )
            for m in result.matches[:25]  # cap payload size
        ],
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(document_id: int, file: UploadFile = File(...)):
    """
    Ingests a document into the corpus AND checks it against everything
    already indexed. This is what the backend calls when a user submits
    a document for a full plagiarism check (vs. a direct A/B compare).
    """
    try:
        raw_text = extract_text(file.filename, await file.read())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    cleaned = clean_text(raw_text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="No extractable text found in file.")

    chunks = chunk_text(cleaned)
    embeddings = embed_texts(chunks)

    # Check against existing corpus BEFORE inserting this doc's own chunks
    best_matches = []
    for emb in embeddings:
        best_matches.extend(find_similar_chunks(emb, top_k=3, exclude_document_id=document_id))

    best_matches.sort(key=lambda m: m["similarity"], reverse=True)
    top_matches = best_matches[:10]
    highest = top_matches[0]["similarity"] * 100 if top_matches else 0.0

    # Now index this document's chunks for future comparisons
    store_chunks(document_id, chunks, embeddings)

    return AnalyzeResponse(
        document_id=document_id,
        word_count=len(cleaned.split()),
        top_corpus_matches=[CorpusMatch(**m) for m in top_matches],
        highest_similarity_pct=round(highest, 2),
    )
