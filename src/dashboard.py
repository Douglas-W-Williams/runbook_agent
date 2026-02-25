"""Streamlit chat interface for the Runbook Agent."""

import os

import _chromadb_compat  # noqa: F401 — must be before chromadb
import streamlit as st

from constants import CHROMA_DIR, COLLECTION_NAME, OLLAMA_MODEL, OLLAMA_URL

st.set_page_config(page_title="IT Runbook Agent", page_icon="📖", layout="wide")
st.title("IT Runbook Agent")


def check_index() -> dict | None:
    """Check if the ChromaDB index exists and return stats."""
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = client.get_collection(COLLECTION_NAME)
        count = collection.count()
        # Count unique runbooks from metadata
        sample = collection.peek(limit=min(count, 100))
        runbook_ids = set()
        if sample["metadatas"]:
            for meta in sample["metadatas"]:
                runbook_ids.add(meta.get("runbook_id", ""))
        return {"chunk_count": count, "runbook_count": len(runbook_ids)}
    except Exception:
        return None


def check_ollama() -> bool:
    """Check if Ollama is reachable."""
    try:
        import requests
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


# --- Sidebar: index and system status ---
with st.sidebar:
    st.header("System Status")

    index_stats = check_index()
    if index_stats:
        st.success(
            f"Index: {index_stats['runbook_count']} runbooks, "
            f"{index_stats['chunk_count']} chunks"
        )
    else:
        st.warning("Index not built. Run: cd src && python index_runbooks.py")

    ollama_ok = check_ollama()
    if ollama_ok:
        st.success(f"Ollama: connected ({OLLAMA_MODEL})")
    else:
        st.error(f"Ollama: unavailable at {OLLAMA_URL}")

    st.header("Retrieval Diagnostics")
    diagnostics_container = st.container()

# --- Chat interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("Sources"):
                for src in msg["sources"]:
                    st.markdown(
                        f"**{src['runbook_id']}** — {src['title']} > "
                        f"{src['section_name']} (score: {src['score']:.4f})"
                    )

# Chat input
if prompt := st.chat_input("Describe your IT issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if not index_stats:
        with st.chat_message("assistant"):
            st.error("The runbook index has not been built yet. "
                     "Run: cd src && python index_runbooks.py")
    elif not ollama_ok:
        with st.chat_message("assistant"):
            st.error(f"Ollama is not reachable at {OLLAMA_URL}. "
                     "Start Ollama and pull the model first.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Searching runbooks..."):
                from query_engine import retrieve_chunks, generate_answer
                chunks = retrieve_chunks(prompt)

            # Show diagnostics in sidebar
            with diagnostics_container:
                st.markdown("**Last query chunks:**")
                for i, chunk in enumerate(chunks, 1):
                    with st.expander(
                        f"{chunk['runbook_id']} — {chunk['section_name']} "
                        f"(score: {chunk['score']:.4f})"
                    ):
                        st.markdown(f"**Title:** {chunk['title']}")
                        st.markdown(f"**Category:** {chunk['category']}")
                        st.text(chunk["text"][:500])

            with st.spinner("Generating answer..."):
                try:
                    result = generate_answer(prompt, chunks)
                    st.markdown(result["answer"])
                    sources = result["sources"]
                    with st.expander("Sources"):
                        for src in sources:
                            st.markdown(
                                f"**{src['runbook_id']}** — {src['title']} > "
                                f"{src['section_name']} (score: {src['score']:.4f})"
                            )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": sources,
                    })
                except Exception as e:
                    st.error(f"Error generating answer: {e}")
