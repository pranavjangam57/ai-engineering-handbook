"""
src/chunker.py — Document chunking strategies
"""

import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    index: int
    total_chunks: int
    char_start: int
    char_end: int


def chunk_by_tokens(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    """
    Split text into overlapping fixed-size chunks (by approximate token count).
    1 token ≈ 4 characters — rough but effective for chunking purposes.
    """
    chars_per_chunk = chunk_size * 4
    overlap_chars = chunk_overlap * 4

    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = min(start + chars_per_chunk, len(text))

        # Try to end at a sentence boundary for cleaner chunks
        if end < len(text):
            last_period = text.rfind(".", start, end)
            last_newline = text.rfind("\n", start, end)
            boundary = max(last_period, last_newline)
            if boundary > start + (chars_per_chunk // 2):
                end = boundary + 1

        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(
                Chunk(
                    text=chunk_text,
                    index=len(chunks),
                    total_chunks=0,  # Set after all chunks collected
                    char_start=start,
                    char_end=end,
                )
            )

        start = end - overlap_chars

    # Set total_chunks now that we know the count
    for chunk in chunks:
        chunk.total_chunks = len(chunks)

    return chunks


def chunk_by_markdown_sections(text: str) -> list[Chunk]:
    """
    Split markdown by headings (##, ###).
    Preserves section context — best for structured documentation.
    """
    sections = re.split(r"(?m)^#{1,3} ", text)
    chunks = []

    for i, section in enumerate(sections):
        section = section.strip()
        if len(section) < 50:  # Skip tiny sections
            continue
        chunks.append(
            Chunk(
                text=section,
                index=i,
                total_chunks=len(sections),
                char_start=0,
                char_end=len(section),
            )
        )

    return chunks


def chunk_documents(
    text: str,
    source: str,
    strategy: str = "token",
    chunk_size: int = 512,
    chunk_overlap: int = 50,
) -> list[dict]:
    """
    Chunk a document and return ready-to-ingest dicts.

    Args:
        text: Raw document text
        source: Source identifier (filename, URL, etc.)
        strategy: "token" or "markdown"
        chunk_size: Tokens per chunk (token strategy only)
        chunk_overlap: Overlap tokens between chunks (token strategy only)

    Returns:
        List of dicts with 'text', 'source', and 'metadata' keys
    """
    if strategy == "markdown":
        chunks = chunk_by_markdown_sections(text)
    else:
        chunks = chunk_by_tokens(text, chunk_size, chunk_overlap)

    return [
        {
            "text": chunk.text,
            "source": source,
            "metadata": {
                "chunk_index": chunk.index,
                "total_chunks": chunk.total_chunks,
                "strategy": strategy,
            },
        }
        for chunk in chunks
        if chunk.text.strip()
    ]
