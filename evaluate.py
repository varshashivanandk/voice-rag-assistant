import json
import os
import shutil

os.environ["RAG_DATA_DIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_eval")
shutil.rmtree(os.environ["RAG_DATA_DIR"], ignore_errors=True)

from app import ingest_file       
import vector_store                  
from config import MIN_SCORE       


def load_sample_documents():
    for domain in sorted(os.listdir("sample_docs")):
        for filename in sorted(os.listdir(os.path.join("sample_docs", domain))):
            with open(os.path.join("sample_docs", domain, filename), "rb") as f:
                ingest_file(filename, f.read(), domain)
    print(f"Indexed {vector_store.count()} chunks")


def is_relevant(hit, expected):
    """A chunk is correct if it comes from the expected file and contains the expected text."""
    return any(hit["filename"] == e["file"] and e["text"].lower() in hit["text"].lower()
               for e in expected)


def evaluate():
    queries = json.load(open("evaluation/test_queries.json"))
    rows = []
    for q in queries:
        hits = vector_store.search(q["question"], top_k=5)
        top_score = hits[0]["score"] if hits else 0
        first_correct_rank = None
        if q["expected"]:
            for hit in hits:
                if is_relevant(hit, q["expected"]):
                    first_correct_rank = hit["rank"]
                    break
        rows.append({**q, "top_file": hits[0]["filename"], "top_score": top_score,
                     "rank": first_correct_rank})
    return rows


def percent(part, total):
    return round(100 * part / total, 1) if total else 0


def make_report(rows):
    answerable = [r for r in rows if r["type"] != "unavailable"]
    unavailable = [r for r in rows if r["type"] == "unavailable"]

    def top_k(group, k):
        return percent(sum(1 for r in group if r["rank"] and r["rank"] <= k), len(group))

    def mrr(group):
        return round(sum(1 / r["rank"] for r in group if r["rank"]) / len(group), 3)

    lines = ["# Retrieval Evaluation Results", "",
             f"Model: all-MiniLM-L6-v2 · {vector_store.count()} chunks · {len(rows)} questions · "
             f"threshold {MIN_SCORE}", "",
             "## Accuracy by question type", "",
             "| Type | Questions | Top-1 % | Top-3 % | Top-5 % | MRR |", "|---|---|---|---|---|---|"]
    for qtype in ["factual", "procedural", "comparative"]:
        group = [r for r in answerable if r["type"] == qtype]
        lines.append(f"| {qtype} | {len(group)} | {top_k(group, 1)} | {top_k(group, 3)} | "
                     f"{top_k(group, 5)} | {mrr(group)} |")
    lines.append(f"| **all answerable** | {len(answerable)} | **{top_k(answerable, 1)}** | "
                 f"**{top_k(answerable, 3)}** | **{top_k(answerable, 5)}** | **{mrr(answerable)}** |")

    for domain in ["hr_policy", "smart_home_support"]:
        group = [r for r in answerable if r["domain"] == domain]
        lines.append(f"| domain: {domain} | {len(group)} | {top_k(group, 1)} | {top_k(group, 3)} | "
                     f"{top_k(group, 5)} | {mrr(group)} |")

    rejected = sum(1 for r in unavailable if r["top_score"] < MIN_SCORE)
    wrongly_rejected = sum(1 for r in answerable if r["top_score"] < MIN_SCORE)
    lines += ["", "## Unavailable-information questions", "",
              f"- Correctly rejected (top score below {MIN_SCORE}): {rejected} of {len(unavailable)}",
              f"- Answerable questions wrongly rejected: {wrongly_rejected} of {len(answerable)}", "",
              "## Threshold comparison", "",
              "| Threshold | Unavailable rejected | Answerable kept |", "|---|---|---|"]
    for t in [0.35, 0.40, 0.45, 0.50, 0.55]:
        rej = sum(1 for r in unavailable if r["top_score"] < t)
        kept = sum(1 for r in answerable if r["top_score"] >= t)
        lines.append(f"| {t} | {rej} of {len(unavailable)} | {kept} of {len(answerable)} |")

    lines += ["", "## Every question", "",
              "| ID | Type | Question | Top-1 file | Top score | Result |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r["type"] == "unavailable":
            result = "rejected (correct)" if r["top_score"] < MIN_SCORE else "NOT rejected (wrong)"
        else:
            result = f"correct at rank {r['rank']}" if r["rank"] else "MISSED"
            if r["top_score"] < MIN_SCORE:
                result += ", low relevance"
        lines.append(f"| {r['id']} | {r['type']} | {r['question']} | {r['top_file']} | "
                     f"{r['top_score']} | {result} |")
    return "\n".join(lines) + "\n", top_k(answerable, 1), top_k(answerable, 3), top_k(answerable, 5)


if __name__ == "__main__":
    load_sample_documents()
    report, top1, top3, top5 = make_report(evaluate())
    with open("evaluation/results.md", "w") as f:
        f.write(report)
    print(f"Top-1: {top1}%  Top-3: {top3}%  Top-5: {top5}%")
    print("Full report: evaluation/results.md")
