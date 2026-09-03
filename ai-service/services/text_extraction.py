"""
Text extraction utilities.
Pulls raw text out of PDF, DOCX, and TXT uploads so the rest of the
pipeline never has to care what format the document arrived in.
"""
import io
import re

import fitz 
import docx
from PIL import Image
import pytesseract


def extract_text(filename: str, file_bytes: bytes) -> str:
    """Route to the right extractor based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return _extract_pdf(file_bytes)
    if lower.endswith(".docx"):
        return _extract_docx(file_bytes)
    if lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {filename}")

def _extract_pdf(file_bytes: bytes) -> str:
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text().strip()

            # Use OCR only when the page has no selectable PDF text.
            if not page_text:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image = Image.open(io.BytesIO(pixmap.tobytes("png")))
                page_text = pytesseract.image_to_string(image).strip()

            text_parts.append(page_text)

    return "\n".join(text_parts)


def _extract_docx(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def clean_text(text: str) -> str:
    """Normalize whitespace, strip control characters."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_sentences(text: str, nlp) -> list[str]:
    """Use spaCy to split into sentences (used for sentence-level matching)."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 15]


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """
    Split long text into overlapping word chunks for embedding.
    Overlap avoids losing context at chunk boundaries.
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks
