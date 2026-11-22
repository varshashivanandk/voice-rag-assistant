import os

from dotenv import load_dotenv

load_dotenv()   # reads GROQ_API_KEY (and optional GROQ_MODEL) from a .env file if present

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Where data is saved
DATA_DIR = os.environ.get("RAG_DATA_DIR", os.path.join(BASE_DIR, "data"))
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")    # original uploaded files
CHROMA_DIR = os.path.join(DATA_DIR, "chroma")     # ChromaDB vector database
DB_PATH = os.path.join(DATA_DIR, "metadata.db")   # SQLite database with document info

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "csv"}

# Chunking: each chunk is at most 800 characters i.e. around 200 tokens and neighbouring chunks share about 120 characters (overlap).
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# Retrieval: how many chunks to return & the minimum similarity score.

TOP_K = 5
MIN_SCORE = 0.45

# Milestone 2: LLM used by the Response Generation Agent (Groq).
# The API key is read from the GROQ_API_KEY environment variable or the .env file.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
