"""Shared constants for the Runbook Agent RAG system."""

import os

# --- Paths ---
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
RUNBOOKS_DIR = os.path.join(PROJECT_DIR, "runbooks")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
CHROMA_DIR = os.path.join(DATA_DIR, "chromadb")
EVAL_QUESTIONS_PATH = os.path.join(DATA_DIR, "eval_questions.json")
EVAL_RESULTS_PATH = os.path.join(DATA_DIR, "eval_results.json")

# --- Embedding model ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# --- ChromaDB ---
COLLECTION_NAME = "runbooks"

# --- Ollama ---
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

# --- Retrieval ---
TOP_K = 5

# --- Runbook categories ---
RUNBOOK_CATEGORIES = [
    "Printer",
    "VTC",
    "Network",
    "Endpoint",
    "Access",
    "VPN",
    "Email",
    "Server",
    "Storage",
    "Telephony",
]
