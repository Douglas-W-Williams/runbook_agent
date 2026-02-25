"""Embed runbook sections and store in ChromaDB."""

import os
import re

import _chromadb_compat  # noqa: F401 — must be before chromadb
import chromadb
from sentence_transformers import SentenceTransformer

from constants import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    RUNBOOKS_DIR,
)


def load_runbooks(runbooks_dir: str = RUNBOOKS_DIR) -> list[dict]:
    """Read all .md files and extract runbook_id, title, category, and body."""
    runbooks = []
    for filename in sorted(os.listdir(runbooks_dir)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(runbooks_dir, filename)
        with open(filepath) as f:
            text = f.read()

        # Extract ID and title from the first heading
        first_line = text.split("\n", 1)[0]
        match = re.match(r"^#\s+(RB-\d+):\s+(.+)$", first_line)
        if not match:
            continue
        runbook_id = match.group(1)
        title = match.group(2).strip()

        # Extract category from the Category section
        cat_match = re.search(r"## Category\s+(.+)", text)
        category = cat_match.group(1).strip() if cat_match else "Unknown"

        runbooks.append({
            "runbook_id": runbook_id,
            "title": title,
            "category": category,
            "body": text,
        })
    return runbooks


def chunk_by_section(runbook: dict) -> list[dict]:
    """Split a runbook into chunks by ## section headers."""
    chunks = []
    sections = re.split(r"(?=^## )", runbook["body"], flags=re.MULTILINE)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract section name from header
        header_match = re.match(r"^## (.+)$", section, re.MULTILINE)
        if not header_match:
            continue
        section_name = header_match.group(1).strip()

        # Get section text (everything after the header line)
        text = section.split("\n", 1)[1].strip() if "\n" in section else ""
        if not text:
            continue

        chunks.append({
            "runbook_id": runbook["runbook_id"],
            "title": runbook["title"],
            "category": runbook["category"],
            "section_name": section_name,
            "text": text,
        })
    return chunks


def build_index(
    runbooks_dir: str = RUNBOOKS_DIR,
    chroma_dir: str = CHROMA_DIR,
    model_name: str = EMBEDDING_MODEL,
) -> dict:
    """Embed all runbook chunks and store in ChromaDB.

    Returns a summary dict with runbook_count and chunk_count.
    """
    runbooks = load_runbooks(runbooks_dir)
    if not runbooks:
        raise FileNotFoundError(f"No runbooks found in {runbooks_dir}")

    # Collect all chunks
    all_chunks = []
    for rb in runbooks:
        all_chunks.extend(chunk_by_section(rb))

    # Load embedding model
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    assert embeddings.shape[1] == EMBEDDING_DIMENSION, (
        f"Expected {EMBEDDING_DIMENSION} dimensions, got {embeddings.shape[1]}"
    )

    # Store in ChromaDB
    os.makedirs(chroma_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=chroma_dir)

    # Idempotent: delete existing collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = []
    metadatas = []
    for chunk in all_chunks:
        chunk_id = f"{chunk['runbook_id']}_{chunk['section_name']}"
        chunk_id = re.sub(r"\s+", "_", chunk_id)
        ids.append(chunk_id)
        metadatas.append({
            "runbook_id": chunk["runbook_id"],
            "title": chunk["title"],
            "category": chunk["category"],
            "section_name": chunk["section_name"],
        })

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )

    summary = {"runbook_count": len(runbooks), "chunk_count": len(all_chunks)}
    print(f"Indexed {summary['chunk_count']} chunks from {summary['runbook_count']} runbooks")
    return summary


if __name__ == "__main__":
    build_index()
