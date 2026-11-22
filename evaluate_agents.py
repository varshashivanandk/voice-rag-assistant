# Milestone 2 evaluation
#
#   python evaluate_agents.py
#
# 1. Query Understanding Agent: classification accuracy on 41 labelled queries (2 domains).
# 2. Retrieval Agent: retrieval quality on the 40 Milestone 1 test queries.
# 3. End-to-end (needs GROQ_API_KEY): answers checked for correctness, grounding/"not found",
#    source attribution and length.
# Writes evaluation/milestone2_results.md

import json
import os
import shutil
from collections import Counter

os.environ["RAG_DATA_DIR"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_eval")
shutil.rmtree(os.environ["RAG_DATA_DIR"], ignore_errors=True)

from app import ingest_file                                   # noqa: E402
from agents import llm                                        # noqa: E402
from agents.orchestrator import handle_query                  # noqa: E402
from agents.query_understanding import understand             # noqa: E402
from agents.retrieval_agent import retrieve                   # noqa: E402

TYPES = ["factual", "procedural", "comparative", "ambiguous"]

# End-to-end test set: question, expected status, words the answer must contain, expected source file
END_TO_END = [
    ("How many days of casual leave do employees get per year?", "answered", ["8"], "leave_policy.docx"),
    ("When is the Diwali holiday?", "answered", ["November|11-09"], "holiday_calendar_2026.csv"),
    ("What does error code E3 mean?", "answered", ["authentication"], "troubleshooting_guide.docx"),
    ("What is the price of the AirPure P5?", "answered", ["18999"], "product_specifications.csv"),
    ("How do I apply for earned leave?", "answered", ["PeopleHub"], "leave_policy.docx"),
    ("What should I do if my laptop is stolen?", "answered", ["4 hours"], "remote_work_it_faq.txt"),
    ("How do I factory reset the thermostat?", "answered", ["15 seconds"], "thermostat_t2_user_manual.pdf"),
    ("How do I claim warranty for a faulty device?", "answered", ["serial"], "warranty_and_returns.txt"),
    ("What is the difference between casual leave and sick leave?", "answered", ["8", "10"], "leave_policy.docx"),
    ("Which purifier covers a bigger room, AirPure P3 or AirPure P5?", "answered", ["P5"], "product_specifications.csv"),
    ("What is the dress code on Fridays?", "not_found", [], None),
    ("How much is the gym membership reimbursement?", "not_found", [], None),
    ("Does AeroHome sell solar panels?", "not_found", [], None),
    ("Can I pair the thermostat with a Zigbee hub?", "not_found", [], None),
]


def pct(a, b):
    return round(100 * a / b, 1) if b else 0


def load_documents():
    for domain in sorted(os.listdir("sample_docs")):
        for name in sorted(os.listdir(os.path.join("sample_docs", domain))):
            with open(os.path.join("sample_docs", domain, name), "rb") as f:
                ingest_file(name, f.read(), domain)


def evaluate_classification(lines):
    data = json.load(open("evaluation/classification_queries.json"))
    rows, correct = [], 0
    confusion = Counter()
    for item in data:
        result = understand(item["query"])
        ok = result["query_type"] == item["expected_type"]
        correct += ok
        confusion[(item["expected_type"], result["query_type"])] += 1
        rows.append(f"| {item['query']} | {item['expected_type']} | {result['query_type']} | "
                    f"{result['confidence']} | {result['method']} | {result['routing']['path']} | {'✔' if ok else '✘'} |")
    lines += ["## 1. Query Understanding Agent: classification", "",
              f"**Accuracy: {correct} of {len(data)} ({pct(correct, len(data))}%)**", "",
              "| Expected \\ Predicted | " + " | ".join(TYPES) + " |", "|---" * (len(TYPES) + 1) + "|"]
    for t in TYPES:
        lines.append(f"| **{t}** | " + " | ".join(str(confusion[(t, p)]) for p in TYPES) + " |")
    lines += ["", "| Query | Expected | Predicted | Confidence | Method | Route | |", "|---|---|---|---|---|---|---|"]
    lines += rows + [""]
    return pct(correct, len(data))


def evaluate_retrieval(lines):
    data = json.load(open("evaluation/test_queries.json"))
    rows = []
    stats = {t: [0, 0] for t in ["factual", "procedural", "comparative", "unavailable"]}
    for item in data:
        understanding = understand(item["question"])
        result = retrieve(understanding)
        if item["type"] == "unavailable":
            ok = result["status"] == "no_results"
            outcome = "no results (correct)" if ok else f"{len(result['chunks'])} chunk(s) kept (wrong)"
        else:
            found = [c["rank"] for c in result["chunks"]
                     if any(c["filename"] == e["file"] and e["text"].lower() in c["text"].lower()
                            for e in item["expected"])]
            ok = bool(found)
            outcome = f"relevant chunk at rank {found[0]}" if found else "MISSED"
        stats[item["type"]][0] += ok
        stats[item["type"]][1] += 1
        rows.append(f"| {item['id']} | {item['type']} | {item['question']} | {len(result['chunks'])} | "
                    f"{result['filtered_out']} | {result['top_score']} | {outcome} |")
    lines += ["## 2. Retrieval Agent: retrieval quality", "",
              "Top-5 search (more for comparative queries), ranked by score, chunks below 0.45 filtered out.", "",
              "| Query type | Correct | Meaning of correct |", "|---|---|---|"]
    for t, (ok, n) in stats.items():
        meaning = "no chunk kept (handled as 'not found')" if t == "unavailable" else "a relevant chunk is kept"
        lines.append(f"| {t} | {ok} of {n} ({pct(ok, n)}%) | {meaning} |")
    lines += ["", "| ID | Type | Query | Kept | Filtered out | Top score | Result |", "|---|---|---|---|---|---|---|"]
    lines += rows + [""]


def evaluate_end_to_end(lines):
    lines += ["## 3. End-to-end: Response Generation Agent through the orchestrator", ""]
    if not llm.is_available():
        lines += ["Skipped: GROQ_API_KEY is not set. Add it to .env and run this script again.", ""]
        print("End-to-end test skipped (no GROQ_API_KEY).")
        return
    rows, passed = [], 0
    for question, expected_status, must_contain, expected_file in END_TO_END:
        r = handle_query(question)
        status_ok = r["status"] == expected_status
        # ignore thousands commas ("18,999") and unusual spaces when checking the key fact
        plain = (r["answer"].lower().replace(",", "").replace("\u202f", " ")
                 .replace("\u00a0", " ").replace("\u2011", "-"))
        # each entry must appear; "a|b" means either a or b is accepted
        correct = all(any(option.lower() in plain for option in w.split("|")) for w in must_contain)
        attributed = expected_file is None or any(s["filename"] == expected_file for s in r["sources"])
        ok = status_ok and correct and attributed
        passed += ok
        answer = r["answer"].replace("\n", " ").replace("|", "/")
        rows.append(f"| {question} | {r['query_type']} | {r['status']} | {r['confidence']['level']} | "
                    f"{len(r['sources'])} | {len(r['answer'].split())} | {'✔' if ok else '✘'} | {answer} |")
    lines += [f"**Passed: {passed} of {len(END_TO_END)}** (status as expected, answer contains the key fact, "
              "expected document cited; unavailable questions must return 'not found')", "",
              "| Question | Type | Status | Confidence | Sources | Words | Pass | Answer |",
              "|---|---|---|---|---|---|---|---|"]
    lines += rows + [""]


if __name__ == "__main__":
    load_documents()
    lines = ["# Milestone 2 Evaluation Results", ""]
    accuracy = evaluate_classification(lines)
    evaluate_retrieval(lines)
    evaluate_end_to_end(lines)
    with open("evaluation/milestone2_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Classification accuracy: {accuracy}%")
    print("Full report: evaluation/milestone2_results.md")
