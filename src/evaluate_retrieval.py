"""Evaluate retrieval accuracy: Recall@K, MRR, category accuracy.

Does NOT require Ollama — retrieval-only evaluation.
"""

import json
import os

from constants import DATA_DIR, EVAL_QUESTIONS_PATH, EVAL_RESULTS_PATH, TOP_K
from query_engine import retrieve_chunks


def recall_at_k(retrieved_ids: list[str], expected_ids: list[str], k: int) -> float:
    """Fraction of expected IDs found in the top-K retrieved chunks."""
    retrieved_set = set(retrieved_ids[:k])
    if not expected_ids:
        return 0.0
    hits = sum(1 for eid in expected_ids if any(eid in rid for rid in retrieved_set))
    return hits / len(expected_ids)


def reciprocal_rank(retrieved_ids: list[str], expected_ids: list[str]) -> float:
    """1 / rank of the first relevant result."""
    for rank, rid in enumerate(retrieved_ids, 1):
        for eid in expected_ids:
            if eid in rid:
                return 1.0 / rank
    return 0.0


def evaluate(eval_path: str = EVAL_QUESTIONS_PATH, top_k: int = TOP_K) -> dict:
    """Run retrieval evaluation over all questions.

    Returns a summary dict with overall and per-category metrics.
    """
    with open(eval_path) as f:
        questions = json.load(f)

    results = []
    category_hits = {}

    for q in questions:
        question_text = q["question"]
        expected_ids = q["expected_runbook_ids"]

        chunks = retrieve_chunks(question_text, top_k=top_k)
        retrieved_ids = [c["runbook_id"] for c in chunks]
        retrieved_chunk_ids = [f"{c['runbook_id']}_{c['section_name']}" for c in chunks]

        r_at_k = recall_at_k(retrieved_ids, expected_ids, top_k)
        mrr = reciprocal_rank(retrieved_ids, expected_ids)

        # Track category of first expected runbook
        top_category = chunks[0]["category"] if chunks else "Unknown"

        result = {
            "question": question_text,
            "expected_ids": expected_ids,
            "retrieved_ids": retrieved_ids[:top_k],
            "recall_at_k": r_at_k,
            "mrr": mrr,
            "top_category": top_category,
        }
        results.append(result)

        # Aggregate by expected category
        for eid in expected_ids:
            if eid not in category_hits:
                category_hits[eid] = {"recall_sum": 0.0, "mrr_sum": 0.0, "count": 0}
            category_hits[eid]["recall_sum"] += r_at_k
            category_hits[eid]["mrr_sum"] += mrr
            category_hits[eid]["count"] += 1

    # Compute overall metrics
    avg_recall = sum(r["recall_at_k"] for r in results) / len(results) if results else 0
    avg_mrr = sum(r["mrr"] for r in results) / len(results) if results else 0

    # Per-runbook metrics
    per_runbook = {}
    for rid, stats in sorted(category_hits.items()):
        per_runbook[rid] = {
            "avg_recall_at_k": stats["recall_sum"] / stats["count"],
            "avg_mrr": stats["mrr_sum"] / stats["count"],
            "question_count": stats["count"],
        }

    summary = {
        "overall": {
            "recall_at_k": round(avg_recall, 4),
            "mrr": round(avg_mrr, 4),
            "total_questions": len(results),
            "top_k": top_k,
        },
        "per_runbook": per_runbook,
        "details": results,
    }
    return summary


def main():
    """Run evaluation and save results."""
    summary = evaluate()
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(EVAL_RESULTS_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Evaluation Results (top_k={summary['overall']['top_k']})")
    print(f"  Questions:    {summary['overall']['total_questions']}")
    print(f"  Recall@K:     {summary['overall']['recall_at_k']:.4f}")
    print(f"  MRR:          {summary['overall']['mrr']:.4f}")
    print()
    print("Per-runbook:")
    for rid, stats in summary["per_runbook"].items():
        print(f"  {rid}: Recall={stats['avg_recall_at_k']:.2f}  MRR={stats['avg_mrr']:.2f}  (n={stats['question_count']})")

    print(f"\nResults saved to {EVAL_RESULTS_PATH}")


if __name__ == "__main__":
    main()
