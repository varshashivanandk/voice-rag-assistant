# M1.1 Research and Technical Understanding

## 1. RAG (Retrieval-Augmented Generation)

RAG answers questions from your own documents in two phases:

| Phase | Steps |
|---|---|
| **Indexing** (once per document) | extract text → clean → split into chunks → turn each chunk into an embedding → store in a vector database |
| **Querying** (every question) | turn the question into an embedding → find the most similar chunks → build the answer from those chunks → show the sources |

Why RAG instead of only asking an LLM:

- The LLM does not know our private documents. RAG gives it the right pieces.
- Answers can **cite their sources**.
- The system can say **"not found"** instead of inventing an answer, which reduces hallucination.
- Updating knowledge means uploading a new file. No retraining is needed.

Typical weak points, and what this project does about them:

| Weak point | What this project does |
|---|---|
| Bad text extraction | A separate extractor per format, keeping page numbers |
| Chunks that mix topics | Documents are split at headings before chunking |
| Answer not in the documents | Results below score 0.45 are marked low relevance |
| Vague questions | Clarification Agent asks back (designed; built later) |
| Different words for the same thing | Embeddings match by meaning, not exact words |

## 2. Multi-agent query resolution

Instead of one big function, the work is split between specialised agents, each with one job.

| Pattern | Idea | Planned use |
|---|---|---|
| Sequential pipeline | Agents run one after another and pass the result on | Proposed orchestrator: Memory → Query Understanding → Clarification → Retrieval → Response Generation |
| Router | Decide which agent or path runs next | Proposed: a clarification check that can stop the pipeline; a different search for comparisons |
| Planner + workers | An LLM plans the steps, and worker agents do them | Later milestones |
| Critic / verifier | A second agent checks the answer is supported | Later milestones |

The five agents are proposed architectural components: Conversation Memory, Query Understanding, Clarification, Retrieval and Response Generation (their designed roles are in `2_system_architecture.md`).



## 3. Embeddings, semantic similarity, chunking, vector search

**Embedding:** a model turns text into a list of numbers (a vector). all-MiniLM-L6-v2 produces 384 numbers. Texts with similar meaning get vectors pointing in a similar direction, so "How many sick days do I get?" is close to "Employees receive 10 days of sick leave".

**Cosine similarity:** cos(a, b) = (a · b) / (|a| × |b|). A value of 1 means the same meaning and 0 means unrelated. ChromaDB returns cosine *distance* = 1 − similarity.

| Embedding model | Size | Numbers per text | Notes |
|---|---|---|---|
| **all-MiniLM-L6-v2** (chosen) | 80 MB | 384 | Fast on CPU, free, good quality, ChromaDB's default |
| bge-small-en-v1.5 | 130 MB | 384 | Often slightly better; option for M2 |
| all-mpnet-base-v2 | 420 MB | 768 | Better but much slower |
| OpenAI text-embedding-3-small | API | 1536 | Paid, sends data to the internet |

**Chunking strategies**

| Strategy | Good | Bad |
|---|---|---|
| Fixed number of characters | Simple | Cuts sentences in half |
| Sentence grouping | Keeps sentences whole | Can still mix topics |
| **Split at headings, then group sentences** (chosen) | One topic per chunk; whole sentences | Needs heading detection |
| Semantic chunking | Topic-aware | Slower, more complex |
| One CSV row per chunk (chosen for CSV) | Each row is a complete fact | Very small chunks, so the column names are repeated in each row |

**Chunk size:** the model reads at most 256 tokens, and 800 characters is about 200 tokens. A **120-character overlap** repeats the last sentence of a chunk at the start of the next one. Tested: 300 characters gave 93.8% Top-1, against 96.9% for 800.

**Vector search:** comparing a question with every chunk is slow for large collections. ChromaDB uses an **HNSW** index (a graph of neighbours) to find the closest vectors quickly. ChromaDB also stores the text and metadata and can filter by domain.

## 4. Web Speech API

A browser API with two parts. It is free and needs no API key.

**Speech-to-text: `SpeechRecognition`** (Chrome, Edge, Safari; **not Firefox**)

```js
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-IN";
recognition.onresult = (event) => { const text = event.results[0][0].transcript; };
recognition.start();
```

- Needs microphone permission and must run on `localhost` or HTTPS.
- Chrome sends the audio to Google's servers, so it needs internet.
- Spoken questions have no punctuation and may contain "um". The proposed Query Understanding Agent will remove such fillers.

**Text-to-speech: `speechSynthesis`** (all modern browsers)

```js
speechSynthesis.speak(new SpeechSynthesisUtterance("Employees receive 10 days of sick leave"));
```

- `speechSynthesis.cancel()` stops reading.
- citation markers like [1] will be removed before speaking.

## 5. Decisions

| Area | Decision | Reason |
|---|---|---|
| Backend | Python + Flask | Required: Python; Flask is simple and familiar |
| Frontend | HTML + CSS + JavaScript (replaced by React in Milestone 2) | Simple; no build tools; Web Speech API is plain JavaScript |
| Embeddings | all-MiniLM-L6-v2 | Free, fast, runs locally |
| Vector database | ChromaDB | Required; stores vectors + text + metadata |
| Document list | SQLite | Built into Python |
| Chunking | Split at headings, then sentences, 800 chars / 120 overlap | Best result in tests |
| Agents | Plain Python functions | Easy to explain|
