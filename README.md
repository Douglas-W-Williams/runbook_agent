# IT Runbook Agent

    A Retrieval-Augmented Generation (RAG) system that helps IT operations
    staff resolve incidents by retrieving relevant runbook sections and
    generating step-by-step guidance. Demonstrates embeddings, vector
    search, and retrieval pipelines using local models.

## Problem

    IT help desk and operations teams maintain runbooks — documented
    procedures for resolving common incidents. Finding the right runbook
    section under time pressure is difficult, especially when runbooks
    span dozens of documents across multiple categories. This agent
    retrieves the most relevant sections and generates focused guidance
    from them.

## Components

    ** Runbook Generator **
        Produces 25 synthetic markdown runbooks across 10 IT categories
        (Printer, Network, Endpoint, Access, VPN, Email, Server, etc.)
        with realistic symptoms, prerequisites, resolution steps, and
        escalation criteria.

    ** Indexing Pipeline **
        Splits each runbook by section headers (Symptoms, Resolution
        Steps, etc.), embeds each section with sentence-transformers
        (all-MiniLM-L6-v2), and stores vectors + metadata in ChromaDB.

    ** RAG Query Engine **
        Embeds the user's question, retrieves the top-K most similar
        chunks from ChromaDB, formats them as context, and sends them
        to Ollama (Llama 3.1 8B) with a grounded system prompt.

    ** Streamlit Dashboard **
        Chat interface with retrieval diagnostics sidebar showing
        per-chunk scores, runbook IDs, and section names.

    ** Evaluation Pipeline **
        53 synthetic test questions with expected runbook IDs. Measures
        Recall@K and Mean Reciprocal Rank (MRR) without requiring Ollama,
        so it runs in CI.

## Tech Stack

    | Component           | Technology                      |
    |---------------------|---------------------------------|
    | Embeddings          | sentence-transformers (MiniLM)  |
    | Vector store        | ChromaDB (persistent)           |
    | LLM                 | Ollama + Llama 3.1 8B           |
    | Interface           | Streamlit                       |
    | Runbooks            | Markdown (synthetic)            |
    | Language            | Python 3.14                     |

## How to Run

    # Create and activate the virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Generate runbooks and build the index
    cd src
    python generate_runbooks.py
    python index_runbooks.py

    # Run the query engine (requires Ollama with llama3.1:8b)
    python query_engine.py

    # Launch the Streamlit dashboard
    python -m streamlit run dashboard.py

    # Run the evaluation pipeline (no Ollama needed)
    python generate_eval_questions.py
    python evaluate_retrieval.py

    # Run tests
    cd ..
    python -m pytest tests/ -v -m "not ollama"

    # Or use the Makefile
    make all        # runbooks + index + test
    make eval       # generate questions + evaluate retrieval
    make run        # launch Streamlit dashboard

## Project Structure

    runbook_agent/
        src/
            constants.py               Shared paths, model names, categories
            generate_runbooks.py       Synthetic runbook markdown generator
            index_runbooks.py          Embedding + ChromaDB indexing pipeline
            ollama_client.py           Ollama /api/chat wrapper
            query_engine.py            RAG query engine (retrieve + generate)
            dashboard.py               Streamlit chat interface
            generate_eval_questions.py Synthetic test question generator
            evaluate_retrieval.py      Retrieval accuracy evaluation
        tests/
            conftest.py                Shared fixtures
            test_index_runbooks.py     Chunking, embedding, round-trip tests
            test_query_engine.py       Retrieval and answer structure tests
        runbooks/                      Generated .md files (not checked in)
        data/                          ChromaDB + eval results (not checked in)

## RAG Pipeline

    The retrieval-augmented generation pipeline works in three stages:

    1. Indexing (offline)
        Each runbook is split into sections by ## headers. Every section
        becomes a chunk with metadata (runbook_id, title, category,
        section_name). Chunks are embedded with all-MiniLM-L6-v2 (384
        dimensions) and stored in ChromaDB with cosine similarity.

    2. Retrieval (per query)
        The user's question is embedded with the same model. ChromaDB
        returns the top-5 most similar chunks by cosine distance. Each
        result includes the original text and full metadata.

    3. Generation (per query)
        Retrieved chunks are formatted as numbered sources with runbook
        IDs and section names. The LLM receives a system prompt that
        constrains it to answer only from provided context and cite
        runbook IDs. Temperature is set to 0.0 for deterministic output.

## Key Design Decisions

    ** Section-Based Chunking **
        Each runbook section (Symptoms, Resolution Steps, Escalation
        Criteria) is semantically coherent. This produces better
        retrieval than fixed-size character windows that split mid-step.

    ** Explicit Embeddings **
        Using sentence-transformers directly rather than ChromaDB's
        built-in embedding. This makes the embedding step testable,
        visible, and demonstrable in interviews.

    ** Idempotent Index Rebuild **
        The indexing pipeline deletes and recreates the ChromaDB
        collection on every run. No stale data, no migration logic.

    ** Eval Without Ollama **
        Recall@K and MRR measure retrieval quality without needing a
        running LLM. This means evaluation runs in CI alongside unit
        tests.

## Evaluation Results

    Run the eval pipeline to see current metrics:

    cd src && python generate_eval_questions.py && python evaluate_retrieval.py

    Expected output includes Recall@5, MRR, and per-runbook breakdown
    across all 10 categories.

## Future Enhancements

    Re-ranking with cross-encoder models for improved precision.
    Hybrid search combining semantic and keyword (BM25) retrieval.
    Conversation memory for multi-turn troubleshooting sessions.
    Feedback loop to track which retrieved chunks were actually useful.
    Integration with a ticketing system (ServiceNow, Jira Service Mgmt).
