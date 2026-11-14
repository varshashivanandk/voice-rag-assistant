# M1.4 Retrieval Pipeline and Validation

Run it yourself with `python evaluate.py`. The full table of every question is in [`evaluation/results.md`](../evaluation/results.md).

## Setup

| | |
|---|---|
| Domain 1: `hr_policy` | Employee handbook (PDF), leave policy (DOCX), remote work & IT FAQ (TXT), holiday calendar (CSV) |
| Domain 2: `smart_home_support` | Thermostat user manual (PDF), troubleshooting guide (DOCX), warranty & returns (TXT), product specifications (CSV) |
| Index | 8 documents → 69 chunks |
| Test questions | 40 = 16 factual, 8 procedural, 8 comparative, 8 unavailable (20 per domain) |
| Correct chunk | Comes from the expected file and contains the expected text |
| Settings | all-MiniLM-L6-v2, top 5, chunks of 800 characters with 120 overlap, threshold 0.45 |

Example questions:

- **Factual:** "How long is paternity leave?"
- **Procedural:** "How do I factory reset the thermostat?"
- **Comparative:** "What is the difference between casual leave and sick leave?"
- **Unavailable:** "What is the dress code on Fridays?" (not in any document)

Two questions are written the way speech recognition outputs them ("um what's the minimum password length").

## Results

| Question type | Questions | Top-1 | Top-3 | Top-5 | MRR |
|---|---|---|---|---|---|
| Factual | 16 | 93.8 % | 100 % | 100 % | 0.969 |
| Procedural | 8 | 100 % | 100 % | 100 % | 1.000 |
| Comparative | 8 | 100 % | 100 % | 100 % | 1.000 |
| **All answerable** | **32** | **96.9 %** | **100 %** | **100 %** | **0.984** |
| HR policy domain | 16 | 93.8 % | 100 % | 100 % | 0.969 |
| Smart home domain | 16 | 100 % | 100 % | 100 % | 1.000 |

**Unavailable information:** 7 of 8 questions were correctly rejected (best score below 0.45). 3 of 32 answerable questions were wrongly rejected.

| Threshold | Unavailable rejected | Answerable kept |
|---|---|---|
| 0.40 | 5 of 8 | 30 of 32 |
| **0.45 (chosen)** | **7 of 8** | **29 of 32** |
| 0.50 | 8 of 8 | 28 of 32 |

**Chunk size test**

| Chunk size / overlap | Chunks | Top-1 | Top-3 | Top-5 |
|---|---|---|---|---|
| 300 / 50 | 106 | 93.8 % | 96.9 % | 96.9 % |
| **800 / 120 (chosen)** | 69 | **96.9 %** | **100 %** | **100 %** |
| 1500 / 200 | 69 | 96.9 % | 100 % | 100 % |

Small chunks separate facts from their headings. 800 and 1500 give the same chunks here, because every section of these documents is shorter than 800 characters.

## Low-relevance results and failures

| Question | What happened | Why |
|---|---|---|
| "How much internet reimbursement do remote employees get?" | Correct chunk at rank 2. Rank 1 was the home-office allowance. | Two similar "money for remote employees" facts |
| "What does error code E3 mean?" | Correct chunk at rank 1, but score 0.35, so it was rejected as low relevance | A code like "E3" carries little meaning for an embedding model; keyword search would find it |
| "How often should I replace the HEPA filter?" | Correct, but score 0.39, so rejected | The answer sits in a section about several purifier lights |
| "How does the per diem for metro cities compare…" | Correct, but score 0.41, so rejected | The document says "daily allowance", the question says "per diem" |
| "Can I pair the thermostat with a Zigbee hub?" (not in the documents) | **Not rejected**: score 0.49 from the Wi-Fi pairing section | The topic "pairing the thermostat" matches, even though Zigbee is never mentioned |

## Limitations

1. The test set is small (69 chunks, 40 questions), so real collections will be harder.
2. Vector search alone is weak for codes and exact terms (E3, model numbers).
3. One fixed threshold cannot separate every "not available" question from real ones.
4. Only retrieval is built; answer generation comes in Milestone 2.
5. Scanned PDFs (images) are not supported, because there is no OCR.

## Planned improvements for Milestone 2

1. **Hybrid search:** combine keyword search (BM25) with vector search, which fixes "E3" and "per diem".
2. **Re-ranking:** a cross-encoder model re-orders the top 20 results for better Top-1.
3. **LLM answer generation:** the LLM writes the answer only from the chunks and says "not found" when the chunks do not contain it, which fixes the Zigbee case.
4. LLM-based query understanding and clarification.
5. More test questions, and answer-quality checks.
