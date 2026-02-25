# Runbook Agent — CLAUDE.md

## Tech Stack
    Python 3.14, sentence-transformers (all-MiniLM-L6-v2), ChromaDB,
    Ollama (Llama 3.1 8B), Streamlit, pytest.

## Structure
    src/            All source modules (run from here with relative paths)
    tests/          pytest tests (conftest.py adds src/ to sys.path)
    runbooks/       Generated .md files (gitignored)
    data/           ChromaDB store + eval JSON (gitignored)

## How to Run
    cd src && python generate_runbooks.py      # Generate 25 runbooks
    cd src && python index_runbooks.py         # Embed + index into ChromaDB
    cd src && python query_engine.py           # Test RAG query (needs Ollama)
    cd src && python -m streamlit run dashboard.py  # Launch UI
    python -m pytest tests/ -v -m "not ollama" # Run tests (no Ollama needed)
    make all                                    # runbooks + index + test

## Key Conventions
    All scripts run from src/ with relative paths (../runbooks/, ../data/).
    constants.py defines all paths, model names, and categories.
    Ollama tests are marked @pytest.mark.ollama and skipped in CI.
    Index is idempotent — deletes and recreates the collection each run.
    _chromadb_compat.py must be imported before chromadb in any module.
    It patches a Pydantic v1 type inference bug that breaks on Python 3.14.
    Any new file that imports chromadb needs: import _chromadb_compat first.
