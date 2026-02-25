"""Tests for the RAG query engine."""

import os
import tempfile

import pytest

from constants import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL
from index_runbooks import build_index


@pytest.fixture(scope="module")
def indexed_chroma(tmp_path_factory):
    """Build a temporary index for query engine tests."""
    runbooks_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "runbooks",
    )
    if not os.path.isdir(runbooks_dir) or not os.listdir(runbooks_dir):
        pytest.skip("No runbooks generated yet")

    tmp_chroma = str(tmp_path_factory.mktemp("chroma"))
    build_index(runbooks_dir=runbooks_dir, chroma_dir=tmp_chroma)
    return tmp_chroma


class TestRetrieveChunks:
    """Test retrieval without Ollama."""

    def test_returns_list_of_dicts(self, indexed_chroma, monkeypatch):
        # Point query_engine at our temp ChromaDB
        import query_engine
        monkeypatch.setattr(query_engine, "_collection", None)
        import chromadb
        client = chromadb.PersistentClient(path=indexed_chroma)
        collection = client.get_collection(COLLECTION_NAME)
        monkeypatch.setattr(query_engine, "_collection", collection)

        chunks = query_engine.retrieve_chunks("printer paper jam")
        assert isinstance(chunks, list)
        assert len(chunks) > 0
        assert isinstance(chunks[0], dict)

    def test_chunks_have_metadata_keys(self, indexed_chroma, monkeypatch):
        import query_engine
        monkeypatch.setattr(query_engine, "_collection", None)
        import chromadb
        client = chromadb.PersistentClient(path=indexed_chroma)
        collection = client.get_collection(COLLECTION_NAME)
        monkeypatch.setattr(query_engine, "_collection", collection)

        chunks = query_engine.retrieve_chunks("account lockout")
        required_keys = {"text", "runbook_id", "title", "category", "section_name", "score"}
        for chunk in chunks:
            assert required_keys.issubset(chunk.keys())

    def test_respects_top_k(self, indexed_chroma, monkeypatch):
        import query_engine
        monkeypatch.setattr(query_engine, "_collection", None)
        import chromadb
        client = chromadb.PersistentClient(path=indexed_chroma)
        collection = client.get_collection(COLLECTION_NAME)
        monkeypatch.setattr(query_engine, "_collection", collection)

        chunks = query_engine.retrieve_chunks("VPN connection", top_k=3)
        assert len(chunks) <= 3


class TestGenerateAnswer:
    """Test answer generation — requires Ollama."""

    @pytest.mark.ollama
    def test_answer_structure(self, indexed_chroma, monkeypatch):
        import query_engine
        monkeypatch.setattr(query_engine, "_collection", None)
        import chromadb
        client = chromadb.PersistentClient(path=indexed_chroma)
        collection = client.get_collection(COLLECTION_NAME)
        monkeypatch.setattr(query_engine, "_collection", collection)

        chunks = query_engine.retrieve_chunks("printer jam")
        result = query_engine.generate_answer("How do I fix a printer jam?", chunks)
        assert "answer" in result
        assert "sources" in result
        assert isinstance(result["answer"], str)
        assert len(result["answer"]) > 0
        assert isinstance(result["sources"], list)
