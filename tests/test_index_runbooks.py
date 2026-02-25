"""Tests for runbook indexing: chunking, embeddings, and ChromaDB round-trip."""

import os
import tempfile

import pytest
from sentence_transformers import SentenceTransformer

from constants import COLLECTION_NAME, EMBEDDING_DIMENSION, EMBEDDING_MODEL
from index_runbooks import build_index, chunk_by_section, load_runbooks


class TestChunking:
    """Test section-based chunking logic."""

    def test_chunk_returns_list(self, sample_runbook_text):
        runbook = {
            "runbook_id": "RB-999",
            "title": "Test Runbook",
            "category": "Testing",
            "body": sample_runbook_text,
        }
        chunks = chunk_by_section(runbook)
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_chunk_has_required_keys(self, sample_runbook_text):
        runbook = {
            "runbook_id": "RB-999",
            "title": "Test Runbook",
            "category": "Testing",
            "body": sample_runbook_text,
        }
        chunks = chunk_by_section(runbook)
        required_keys = {"runbook_id", "title", "category", "section_name", "text"}
        for chunk in chunks:
            assert required_keys.issubset(chunk.keys())

    def test_chunk_section_names(self, sample_runbook_text):
        runbook = {
            "runbook_id": "RB-999",
            "title": "Test Runbook",
            "category": "Testing",
            "body": sample_runbook_text,
        }
        chunks = chunk_by_section(runbook)
        section_names = {c["section_name"] for c in chunks}
        assert "Symptoms" in section_names
        assert "Resolution Steps" in section_names
        assert "Escalation Criteria" in section_names

    def test_chunk_excludes_empty_sections(self):
        text = """# RB-998: Empty Sections

## Category

Testing

## Symptoms

## Resolution Steps

1. Do something.
"""
        runbook = {
            "runbook_id": "RB-998",
            "title": "Empty Sections",
            "category": "Testing",
            "body": text,
        }
        chunks = chunk_by_section(runbook)
        for chunk in chunks:
            assert chunk["text"].strip() != ""


class TestEmbeddings:
    """Test embedding model output."""

    @pytest.fixture(scope="class")
    def model(self):
        return SentenceTransformer(EMBEDDING_MODEL)

    def test_embedding_dimension(self, model):
        embedding = model.encode("test sentence")
        assert len(embedding) == EMBEDDING_DIMENSION

    def test_embedding_values_are_floats(self, model):
        embedding = model.encode("test sentence")
        assert all(isinstance(float(v), float) for v in embedding)


class TestIndexRoundTrip:
    """Test full index build and query with a temporary ChromaDB."""

    def test_round_trip(self, runbooks_dir):
        if not os.path.isdir(runbooks_dir) or not os.listdir(runbooks_dir):
            pytest.skip("No runbooks generated yet")

        with tempfile.TemporaryDirectory() as tmp_chroma:
            summary = build_index(
                runbooks_dir=runbooks_dir,
                chroma_dir=tmp_chroma,
            )
            assert summary["runbook_count"] > 0
            assert summary["chunk_count"] > 0

            # Verify we can query the collection
            import chromadb
            client = chromadb.PersistentClient(path=tmp_chroma)
            collection = client.get_collection(COLLECTION_NAME)
            assert collection.count() == summary["chunk_count"]
