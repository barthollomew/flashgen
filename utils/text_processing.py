import logging
from typing import List, Optional

import PyPDF2
from PyPDF2.errors import PdfReadError

try:
    import tiktoken
except ImportError:  # pragma: no cover - handled at runtime if missing
    tiktoken = None  # type: ignore


def pdf_to_formatted_text(pdf_file_path: str) -> Optional[str]:
    """Extract text from a PDF and format it."""
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            formatted_text = " ".join(text.split())
            return formatted_text.strip()
    except PdfReadError:
        logging.error(
            "Error: Could not read the PDF file: %s. It might be encrypted or corrupted.",
            pdf_file_path,
        )
        return None


def _tokenizer(encoding_name: str = "o200k_base"):
    if tiktoken is None:
        return None
    try:
        return tiktoken.get_encoding(encoding_name)
    except Exception:
        return None


def _token_len(text: str, encoding_name: str = "o200k_base") -> int:
    tokenizer = _tokenizer(encoding_name)
    if tokenizer is None:
        return max(1, len(text) // 4)  # fallback estimate
    return len(tokenizer.encode(text))


def split_into_chunks(
    text: str, max_tokens: int = 1400, overlap_tokens: int = 150, encoding_name: str = "o200k_base"
) -> List[str]:
    """
    Token-aware chunking to keep prompts within model limits.

    Falls back to rough character-based sizing when tiktoken is unavailable.
    """
    tokenizer = _tokenizer(encoding_name)
    if tokenizer is None:
        approx_chars = max_tokens * 4
        overlap_chars = overlap_tokens * 4
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + approx_chars)
            chunks.append(text[start:end])
            start = max(end - overlap_chars, start + 1)
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    tokens = tokenizer.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(len(tokens), start + max_tokens)
        chunk_tokens = tokens[start:end]
        chunks.append(tokenizer.decode(chunk_tokens))
        next_start = end - overlap_tokens
        if next_start <= start:
            next_start = end
        start = next_start

    return [chunk.strip() for chunk in chunks if chunk.strip()]
