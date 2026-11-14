# Tests for ingestion and retrieval.  Run:  pytest
# They use a temporary data folder, so the real knowledge base is not touched.

import os
import sys
import tempfile

os.environ["RAG_DATA_DIR"] = tempfile.mkdtemp()
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

import pytest  # noqa: E402

from app import app  # noqa: E402
from ingestion import extract_text, split_into_chunks  # noqa: E402

SAMPLE_FILES = [os.path.join("sample_docs", d, f)
                for d in sorted(os.listdir("sample_docs"))
                for f in sorted(os.listdir(os.path.join("sample_docs", d)))]


@pytest.fixture(scope="module")
def client():
    return app.test_client()


def test_text_is_extracted_from_every_format():
    for path in SAMPLE_FILES:
        with open(path, "rb") as f:
            pieces = extract_text(os.path.basename(path), f.read())
        assert any(p["text"].strip() for p in pieces), path


def test_csv_rows_become_sentences():
    pieces = extract_text("products.csv", b"Model,Price\nT2,14999\n")
    assert pieces[0]["text"] == "Products: Model: T2 | Price: 14999"


def test_chunks_respect_size_and_overlap():
    text = " ".join(f"This is sentence number {i}." for i in range(100))
    chunks = split_into_chunks(text, chunk_size=200, overlap=40)
    assert all(len(c) <= 200 for c in chunks)
    last_sentence_of_first = chunks[0].split(". ")[-1]
    assert chunks[1].startswith(last_sentence_of_first.rstrip("."))   # overlap


def test_upload_all_sample_files(client):
    for path in SAMPLE_FILES:
        domain = os.path.basename(os.path.dirname(path))
        with open(path, "rb") as f:
            response = client.post("/api/upload", data={"domain": domain, "files": (f, os.path.basename(path))})
        result = response.get_json()[0]
        assert result["ok"] and result["num_chunks"] > 0
    assert len(client.get("/api/documents").get_json()) == len(SAMPLE_FILES)


def test_wrong_file_type_is_rejected(client):
    result = client.post("/api/upload", data={"files": (open(SAMPLE_FILES[0], "rb"), "virus.exe")}).get_json()[0]
    assert not result["ok"]


def test_search_finds_the_right_document(client):
    hits = client.post("/api/search", json={"question": "How do I factory reset the thermostat?"}).get_json()
    assert hits[0]["filename"] == "thermostat_t2_user_manual.pdf"


def test_domain_filter(client):
    hits = client.post("/api/search", json={"question": "warranty", "domain": "hr_policy"}).get_json()
    assert all(h["domain"] == "hr_policy" for h in hits)


def test_unknown_topic_has_low_score(client):
    hits = client.post("/api/search", json={"question": "What is the dress code on Fridays?"}).get_json()
    assert hits[0]["low_relevance"]
