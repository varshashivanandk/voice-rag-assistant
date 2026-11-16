# Development of AI-Based Knowledge Retrieval Platform with Query Resolution System

Milestone 1 builds the **knowledge base ingestion module** and a **basic RAG retrieval pipeline**:

- **Upload:** PDF, DOCX, TXT or CSV files.
- **Index:** the text is extracted, cleaned, split into chunks, turned into embeddings and stored in ChromaDB.
- **Search:** finds the most relevant chunks for a question by meaning (semantic search).

**Built with:** Python + Flask, ChromaDB, SQLite, and HTML/CSS/JavaScript.

The agents, the voice features (Web Speech API) and answer generation were **studied and designed** in Milestone 1 (see `docs/`). They will be built in the next milestones.

![Architecture](docs/system_architecture.jpeg)

## How to run

```bash
pip install -r requirements.txt
python app.py              # open http://localhost:5000
```

The first run downloads the embedding model (about 80 MB). Upload the files in `sample_docs/hr_policy` with the domain `hr_policy`, and the files in `sample_docs/smart_home_support` with the domain `smart_home_support`. Then search.

```bash
pytest                     # 8 tests
python evaluate.py         # retrieval evaluation in evaluation/results.md
```

## Files

```
app.py               Flask app: web page + API routes
config.py            settings (chunk size, overlap, top-k, low-relevance score)
ingestion.py         text extraction, cleaning, chunking
vector_store.py      embeddings + ChromaDB (store and search)
database.py          SQLite list of uploaded documents (metadata)
templates/index.html web page
static/app.js        upload + search in the browser
static/style.css     styling
evaluate.py          Top-1 / Top-3 / Top-5 evaluation
make_sample_docs.py  creates the sample documents (2 domains)
sample_docs/         test documents: 2 domains x 4 file types
evaluation/          test questions + results
tests/               automated tests
docs/                research, architecture, tech stack, evaluation
```

## API

| Method | Route | What it does |
|---|---|---|
| GET | `/` | Web page |
| POST | `/api/upload` | Upload files (form fields `files`, `domain`) |
| GET | `/api/documents` | List uploaded documents |
| GET | `/api/domains` | List domains |
| POST | `/api/search` | `{"question", "top_k", "domain"}` → most relevant chunks with scores |

## Results (40 test questions, 2 domains)

| Top-1 | Top-3 | Top-5 | MRR |
|---|---|---|---|
| 96.9 % | 100 % | 100 % | 0.984 |

Detailed results are in [`evaluation/results.md`](evaluation/results.md).