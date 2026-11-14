# Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | Simple; no build tools needed |
| Voice input | Web Speech API: `SpeechRecognition` | Free speech-to-text built into Chrome and Edge |
| Voice output| Web Speech API: `speechSynthesis` | Free text-to-speech built into all modern browsers |
| Backend | Python + Flask | Simple web framework for the API routes and the page |
| PDF reading | pypdf | Extracts text page by page |
| DOCX reading | python-docx | Reads paragraphs, headings and tables |
| TXT / CSV reading | Python built-ins (`csv` module) | No extra library needed |
| Embedding model | all-MiniLM-L6-v2 (sentence-transformers model, run by ChromaDB) | Small (80 MB), fast on a laptop CPU, good quality; 384 numbers per text |
| Vector database | ChromaDB | Stores vectors + text + metadata, similarity search, saves to disk, domain filter |
| Metadata database | SQLite (Python built-in `sqlite3`) | List of uploaded documents; no setup |
| Agents| Plain Python functions | Easy to read and explain |
| LLM| Groq API | To write the final answer from the retrieved chunks |
| Testing | pytest + Flask test client | 8 automated tests |
| Sample data | reportlab (PDF), python-docx (DOCX) | Creates the test documents |
