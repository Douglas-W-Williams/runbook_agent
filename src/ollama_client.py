"""Shared Ollama /api/chat wrapper with prompt injection defense."""

import requests

from constants import OLLAMA_MODEL, OLLAMA_URL

SYSTEM_PROMPT = (
    "You are an IT support assistant. Answer questions ONLY using the "
    "provided runbook context below. Cite runbook IDs (e.g., RB-001) in "
    "your answers. If the provided context is insufficient to answer the "
    "question, say clearly that you don't have enough information and "
    "suggest the user check with the relevant team. Do NOT make up "
    "information or steps that are not in the provided context."
)


def query_llm(
    user_question: str,
    context_chunks: list[dict],
    model: str = OLLAMA_MODEL,
    base_url: str = OLLAMA_URL,
) -> str:
    """Send a question with context chunks to Ollama and return the response.

    Args:
        user_question: The user's natural language question.
        context_chunks: List of dicts with at least 'text', 'runbook_id',
                       'title', and 'section_name' keys.
        model: Ollama model name.
        base_url: Ollama server URL.

    Returns:
        The model's response text.
    """
    # Format context for the user message
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        runbook_id = chunk.get("runbook_id", "Unknown")
        title = chunk.get("title", "Unknown")
        section = chunk.get("section_name", "Unknown")
        text = chunk.get("text", "")
        context_parts.append(
            f"[Source {i}: {runbook_id} - {title} > {section}]\n{text}"
        )

    context_text = "\n\n---\n\n".join(context_parts)

    user_message = (
        f"CONTEXT:\n{context_text}\n\n"
        f"QUESTION:\n{user_question}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
        "options": {"temperature": 0.0},
    }

    response = requests.post(
        f"{base_url}/api/chat",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()["message"]["content"]


if __name__ == "__main__":
    # Quick test — requires Ollama running with the configured model
    test_chunks = [
        {
            "runbook_id": "RB-001",
            "title": "Printer Paper Jam Resolution",
            "section_name": "Resolution Steps",
            "text": "1. Power off the printer.\n2. Remove jammed paper.\n3. Restart.",
        }
    ]
    answer = query_llm("How do I fix a paper jam?", test_chunks)
    print(answer)
