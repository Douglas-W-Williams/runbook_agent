# IT Runbook Agent — Interview Notes

## 30-Second Pitch

    I built a RAG system that helps IT operations staff resolve incidents
    faster. It takes 25 enterprise-style runbooks, embeds them by section
    using sentence-transformers, stores them in ChromaDB, and uses cosine
    similarity to retrieve the most relevant sections for any natural
    language question. An Ollama-hosted Llama 3.1 model then generates a
    grounded answer citing specific runbook IDs. The whole pipeline is
    testable and runs in CI without needing a GPU or LLM server.

## 60-Second Pitch

    This is a retrieval-augmented generation system for IT incident
    resolution. The core challenge is that help desk teams have dozens of
    runbooks but finding the right section under time pressure is slow and
    error-prone.

    The pipeline has three stages. First, I generate 25 realistic runbooks
    across 10 IT categories — printers, networking, VPN, Active Directory,
    and so on. Each runbook is split into semantic sections: symptoms,
    resolution steps, escalation criteria. Second, every section is
    embedded with all-MiniLM-L6-v2 and stored in ChromaDB with full
    metadata. Third, when a user asks a question, it's embedded with the
    same model, the top-5 most similar chunks are retrieved, and Llama 3.1
    generates an answer constrained to cite only from those chunks.

    I built an evaluation pipeline with 53 test questions that measures
    Recall@K and MRR without needing Ollama, so retrieval quality is
    validated in CI. The Streamlit dashboard shows both the answer and
    full retrieval diagnostics.

## Component Walkthrough

    ** constants.py **
        Central definition of all paths, model names, and categories.
        Same pattern as a config module — change one file, everything
        updates.

    ** generate_runbooks.py **
        25 runbooks with realistic IT content: specific commands, error
        codes, escalation paths. Each runbook follows a consistent
        markdown structure for reliable parsing.

    ** index_runbooks.py **
        Three functions: load_runbooks reads and parses the markdown,
        chunk_by_section splits by ## headers, build_index embeds all
        chunks and stores them in ChromaDB. The index is idempotent —
        it deletes and recreates the collection every time.

    ** ollama_client.py **
        Thin wrapper around Ollama's /api/chat endpoint. System prompt
        enforces grounding: answer only from context, cite runbook IDs,
        say clearly when information is insufficient. Temperature 0.0
        for deterministic output.

    ** query_engine.py **
        Orchestrates the RAG pipeline. retrieve_chunks embeds the
        question and queries ChromaDB. generate_answer formats the
        context and calls the LLM. ask is the end-to-end entry point.

    ** evaluate_retrieval.py **
        Measures Recall@K (did the expected runbook appear in top-K?)
        and MRR (how high did it rank?). Runs without Ollama so it
        works in CI.

## Technical Decisions

    ** Why section-based chunking? **
        Each section (Symptoms, Resolution Steps) is semantically
        coherent. Fixed-size windows would split mid-step, mixing
        symptoms with resolution content and hurting retrieval precision.

    ** Why explicit embeddings instead of ChromaDB built-in? **
        Using sentence-transformers directly makes the embedding step
        visible, testable, and explainable. I can show the embedding
        dimension (384), verify it in tests, and swap models without
        changing the storage layer.

    ** Why cosine similarity? **
        Sentence-transformer models are trained with cosine similarity
        as the objective. Using a different distance metric would
        misalign with the model's training.

    ** Why Ollama instead of an API? **
        Fully local inference means no API keys, no cost, no data
        leaving the machine. For a portfolio project, this also means
        anyone can clone and run it without an API account.

    ** Why temperature 0.0? **
        IT runbook guidance should be deterministic and reproducible.
        Creative variation in troubleshooting steps would be harmful.

## RAG Explained (for non-technical interviewers)

    Imagine you're a librarian. Someone asks a question, and instead of
    writing an answer from memory, you first search the library for the
    most relevant book passages, then write your answer using only those
    passages. That's RAG — Retrieval-Augmented Generation.

    The "retrieval" part finds the right runbook sections. The
    "generation" part writes a human-readable answer from those sections.
    The model is explicitly told not to make things up — it can only use
    what was retrieved.

## Potential Follow-Up Questions

    ** How would you handle runbook updates? **
        Re-run the indexing pipeline. It's idempotent — deletes the old
        collection and rebuilds from whatever's in the runbooks folder.
        In production, you'd trigger this from a CI/CD pipeline when
        runbooks are updated in the repo.

    ** How would you improve retrieval accuracy? **
        Add a cross-encoder re-ranking step. The initial retrieval uses
        bi-encoder similarity (fast but approximate). A cross-encoder
        scores each candidate against the query jointly (slower but more
        accurate). You retrieve top-20 with the bi-encoder, then re-rank
        to top-5 with the cross-encoder.

    ** How would you handle multi-turn conversations? **
        Add conversation memory to the query engine. Append the last N
        exchanges to the context window so the model can reference
        previous answers. For retrieval, combine the current question
        with conversation context before embedding.

    ** What if the runbook corpus grows to thousands of documents? **
        ChromaDB handles moderate scale well. For tens of thousands of
        chunks, consider a dedicated vector database like Weaviate or
        Pinecone. Also add metadata filtering (by category) to narrow
        the search space before similarity search.

    ** How do you prevent hallucination? **
        Three layers: the system prompt explicitly forbids answering
        outside the provided context, temperature is set to 0.0, and
        the context chunks include specific runbook IDs so the model
        can cite sources. The evaluation pipeline measures whether
        retrieved chunks actually match expected runbooks.
