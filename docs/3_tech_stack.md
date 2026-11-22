# Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React + Vite | Components for upload, questions and answer cards; Vite dev server forwards /api to Flask |
| Voice input | Web Speech API: `SpeechRecognition` | Free speech-to-text built into Chrome and Edge |
| Voice output| Web Speech API: `speechSynthesis` | Free text-to-speech built into all modern browsers |
| Backend | Python + Flask | Simple web framework for the API routes |
| PDF reading | pypdf | Extracts text page by page |
| DOCX reading | python-docx | Reads paragraphs, headings and tables |
| TXT / CSV reading | Python built-ins (`csv` module) | No extra library needed |
| Embedding model | all-MiniLM-L6-v2 (sentence-transformers model, run by ChromaDB) | Small (80 MB), fast on a laptop CPU, good quality; 384 numbers per text |
| Vector database | ChromaDB | Stores vectors + text + metadata, similarity search, saves to disk, domain filter |
| Metadata database | SQLite (Python built-in `sqlite3`) | List of uploaded documents; no setup |
| Agents | Plain Python modules (`agents/`) | Query Understanding, Retrieval, Response Generation + orchestrator; easy to read and explain |
| LLM | Groq API (`openai/gpt-oss-120b`), python-dotenv for the key | Writes grounded answers from the retrieved chunks; fallback for unclear query classification |
| Testing | pytest + Flask test client | 23 automated tests (LLM replaced by a fake in tests) |
| Sample data | reportlab (PDF), python-docx (DOCX) | Creates the test documents |
