"""RAG query engine: retrieve relevant chunks then generate an answer."""

import _chromadb_compat  # noqa: F401 — must be before chromadb
import chromadb
from sentence_transformers import SentenceTransformer

from constants import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K
from ollama_client import query_llm


# Module-level singletons (lazy-loaded)
_model = None
_collection = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def retrieve_chunks(question: str, top_k: int = TOP_K) -> list[dict]:
    """Embed the question and retrieve the top-K matching chunks.

    Returns a list of dicts with keys: text, runbook_id, title, category,
    section_name, score.
    """
    model = _get_model()
    collection = _get_collection()

    embedding = model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        chunks.append({
            "text": results["documents"][0][i],
            "runbook_id": metadata["runbook_id"],
            "title": metadata["title"],
            "category": metadata["category"],
            "section_name": metadata["section_name"],
            "score": results["distances"][0][i],
        })
    return chunks


def generate_answer(question: str, chunks: list[dict]) -> dict:
    """Format context from chunks and call the LLM.

    Returns a dict with keys: answer, sources.
    """
    answer_text = query_llm(question, chunks)

    sources = []
    for chunk in chunks:
        sources.append({
            "runbook_id": chunk["runbook_id"],
            "title": chunk["title"],
            "section_name": chunk["section_name"],
            "score": chunk["score"],
        })

    return {"answer": answer_text, "sources": sources}


def ask(question: str, top_k: int = TOP_K) -> dict:
    """End-to-end RAG: retrieve chunks, generate answer.

    Returns a dict with keys: answer, sources, chunks.
    """
    chunks = retrieve_chunks(question, top_k=top_k)
    result = generate_answer(question, chunks)
    result["chunks"] = chunks
    return result


if __name__ == "__main__":
    sample = "A user's printer keeps jamming. What should I do?"
    print(f"Question: {sample}\n")
    result = ask(sample)
    print(f"Answer:\n{result['answer']}\n")
    print("Sources:")
    for src in result["sources"]:
        print(f"  {src['runbook_id']} - {src['title']} > {src['section_name']} (score: {src['score']:.4f})")
