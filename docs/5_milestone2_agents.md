# Milestone 2: Multi-Agent Query Resolution & Response Generation

```
User Query → Query Understanding Agent → Retrieval Agent → Response Generation Agent → Final Response
```

API: `POST /api/ask` with `{"question": "...", "domain": "hr_policy"}`. The domain is optional.

## M2.1 Query Understanding Agent (`agents/query_understanding.py`)

**Steps**
1. Clean the query: remove fillers such as "um", "ok" and "please", and collapse extra spaces.
2. Classify it with rules, which gives a type and a confidence.
3. If the rule confidence is below 0.6 and a Groq key is set, classify with the LLM prompt (`prompts.CLASSIFY_SYSTEM`) instead.
4. Return the structured output with routing information.

**Classification rules** (checked in this order)

| Type | Rule | Confidence |
|---|---|---|
| ambiguous | no content words; "what about it / and that"; 1–2 words with no question mark ("leave", "warranty") | 0.8–0.95 |
| comparative | difference, compare, compared to, vs, versus, better, worse, "more/less/bigger … than", "which … A or B" | 0.9 |
| factual | starts with "how many / how much / how long / how often" | 0.85 |
| procedural | "how do/can/should I", "how to", steps, procedure, process, "what should I do", set up, install, reset, apply for, request, claim, raise, connect, submit, replace | 0.85 |
| factual | starts with what, when, where, who, which, is, does, can… | 0.8 |
| factual (unsure) | no rule matched → LLM fallback if available | 0.5 |

**Routing**

| Type | Route | What happens next |
|---|---|---|
| factual, procedural | `single_search` | one semantic search |
| comparative | `multi_search` | one search for the full question plus one per compared item (e.g. "AirPure P3", "AirPure P5") |
| ambiguous | `clarification` | pipeline stops and asks the user for more detail (clarification handling is Milestone 3) |

**Output example**

```json
{"agent": "query_understanding", "status": "ok", "error": null,
 "query": "Which purifier covers a bigger room, AirPure P3 or AirPure P5?",
 "normalized_query": "Which purifier covers a bigger room, AirPure P3 or AirPure P5?",
 "query_type": "comparative", "confidence": 0.9, "method": "rules",
 "needs_clarification": false,
 "routing": {"path": "multi_search", "sub_queries": ["AirPure P3", "AirPure P5"]}}
```

## M2.2 Retrieval Agent (`agents/retrieval_agent.py`)

1. Receives the Query Understanding output.
2. Runs semantic search through the Milestone 1 pipeline (`vector_store.search`), top-k = 5, using one or several searches depending on the route.
3. Removes duplicate chunks, keeping each one's best score.
4. Ranks the chunks by relevance score, highest first.
5. Filters out chunks scoring below `min_score` (default 0.45). This is configurable per request (`"min_score"` in `/api/ask`) or in `config.py`.
6. Keeps the metadata for each chunk: rank, `chunk_id`, `chunk_index`, filename, domain, page and score.
7. If no chunk is left, it returns `status: "no_results"`. The Response Agent then says the information was not found, without calling the LLM.

## M2.3 Response Generation Agent (`agents/response_agent.py`)

- **Grounded prompt** (`prompts.ANSWER_SYSTEM`):
  - answer **only** from the numbered context passages;
  - cite every sentence as [n];
  - reply `INSUFFICIENT_CONTEXT` if the context does not answer the question;
  - say what is missing when the answer is only partial.
- **Answer style per type:**
  - factual: 1–3 sentences;
  - procedural: numbered steps;
  - comparative: point-by-point comparison plus a one-line summary.
- **LLM:** Groq, model `openai/gpt-oss-120b` (set `GROQ_MODEL` in `.env` to change it), temperature 0.
- **Source attribution:** only the passages the answer cites, each with filename, page, chunk id and score.
- **Confidence indicator:** based on the best retrieval score and the number of cited sources.

  | Level | Best score |
  |---|---|
  | High | ≥ 0.65 |
  | Medium | ≥ 0.55 |
  | Low | ≥ 0.45 |
  | None | nothing relevant found |

  The UI shows the level as a badge and a bar.
- **No answer:**
  - no chunks above the threshold, or the LLM replies `INSUFFICIENT_CONTEXT` → "Sorry, I couldn't find enough information in the knowledge base…";
  - LLM error → the message says the answer could not be generated, and the relevant sources are still listed.

## M2.4 Orchestration Layer (`agents/orchestrator.py`)

`handle_query()` runs the agents in order and passes each agent's structured output to the next. The standard format for every message is defined in `agents/schemas.py`. Each agent returns `agent`, `status` and `error` plus its own fields.

**Error handling**

| Failure | What happens |
|---|---|
| Empty query | "Please type a question." |
| Classification failure | Continues as a factual query (`method: "fallback"`) |
| Ambiguous query | `status: "needs_clarification"`, the user is asked for more detail |
| Retrieval failure | `status: "error"`, "Searching the knowledge base failed" |
| No relevant chunks | `status: "not_found"`, the LLM is not called |
| LLM / generation failure | `status: "error"`, message plus the relevant sources |

**Final response format**

```json
{"query": "...", "status": "answered | not_found | needs_clarification | error",
 "answer": "...", "query_type": "factual",
 "sources": [{"number": 1, "filename": "leave_policy.docx", "page": null, "chunk_id": "84cec4b1_3", "score": 0.822}],
 "confidence": {"level": "High", "score": 0.822, "reason": "Best match score 0.82; answer supported by 1 source(s)."},
 "understanding": {...}, "retrieval": {...}, "response": {...}, "errors": []}
```

## Testing

- `pytest` runs 23 tests. The 15 Milestone 2 tests in `tests/test_pipeline.py` replace the LLM with a fake function, so they need no API key. They cover:
  - classification of all 4 types and comparative routing;
  - ranking, metadata and configurable filtering;
  - sources and confidence, and "not found";
  - the full pipeline, including clarification, skipping the LLM when there are no results, LLM failure and retrieval failure;
  - the `/api/ask` route.
- `python evaluate_agents.py` writes `evaluation/milestone2_results.md` with three parts:
  1. **Classification accuracy:** 41 labelled queries from both domains, with a confusion table.
  2. **Retrieval quality:** the 40 Milestone 1 questions through the Retrieval Agent, covering factual, procedural, comparative and unavailable questions.
  3. **End-to-end:** 14 questions across both domains, checking the status, the key fact in the answer (correctness), that the expected document is cited (source attribution), and that unavailable questions return "not found" (groundedness). This part needs `GROQ_API_KEY`.

**Results** (from `evaluation/milestone2_results.md`)

- **Classification:** 41 of 41 (100%). The rules were written and tested on the same queries, so expect lower accuracy on new wording. Two-word queries such as "Holiday list" are marked ambiguous.
- **Retrieval:** factual 14/16, procedural 8/8, comparative 7/8, unavailable 7/8 correctly returned no results.
- **End-to-end (Groq `openai/gpt-oss-120b`):** 12 of 14 passed.
  - Correct, cited answers for every factual, procedural and comparative question except "E3".
  - 3 of the 4 unavailable questions correctly returned "not found".
  - The first run reported 9 of 14. Three answers were correct but marked as failed because the checker did not handle "₹18,999" (comma) or the model's narrow spaces in "4 hours" and "15 seconds". The checker and the answer formatting were fixed.

**Failures**

| Question | What happened | Why |
|---|---|---|
| What does error code E3 mean? | "Not found" | The correct chunk scored 0.346, below 0.45, so it was filtered out before generation. Codes carry little meaning for vector search. |
| Can I pair the thermostat with a Zigbee hub? (not in the documents) | Answered: "does not support Zigbee" | A near-miss chunk (Wi-Fi pairing, score 0.49) passed the threshold, and the LLM inferred an answer that the document does not state. |

**Planned improvements**
- Hybrid search (keyword + vector) so exact codes such as "E3" are found.
- A stricter prompt rule: if the specific item asked about is not named in the context, reply INSUFFICIENT_CONTEXT.
