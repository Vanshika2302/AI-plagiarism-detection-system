"""
pgvector-backed corpus store.

Lets the service check a new submission against every document already
indexed in Postgres (not just a single pairwise comparison), which is
what makes this a real plagiarism *detector* rather than a diff tool.
"""
import os

from sqlalchemy import create_engine, text
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import declarative_base, sessionmaker, mapped_column, Mapped

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://plagiarism:plagiarism@db:5432/plagiarism"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int]
    chunk_index: Mapped[int]
    chunk_text: Mapped[str]
    embedding = mapped_column(Vector(384))


def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(engine)


def store_chunks(document_id: int, chunks: list[str], embeddings) -> None:
    session = SessionLocal()
    try:
        for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            session.add(
                DocumentEmbedding(
                    document_id=document_id,
                    chunk_index=idx,
                    chunk_text=chunk,
                    embedding=emb.tolist(),
                )
            )
        session.commit()
    finally:
        session.close()


def find_similar_chunks(embedding, top_k: int = 5, exclude_document_id: int | None = None):
    """
    Nearest-neighbor search over stored chunks using pgvector's cosine
    distance operator (<=>). Returns the closest matches across the whole
    corpus, not just one document.
    """
    session = SessionLocal()
    try:
        query = text(
            """
            SELECT document_id, chunk_text, 1 - (embedding <=> :emb) AS similarity
            FROM document_embeddings
            WHERE (:exclude_id IS NULL OR document_id != :exclude_id)
            ORDER BY embedding <=> :emb
            LIMIT :top_k
            """
        )
        rows = session.execute(
            query,
            {"emb": str(embedding.tolist()), "exclude_id": exclude_document_id, "top_k": top_k},
        ).fetchall()
        return [
            {"document_id": r.document_id, "chunk_text": r.chunk_text, "similarity": float(r.similarity)}
            for r in rows
        ]
    finally:
        session.close()
