# Milestone 2 tests: agents and orchestration. Run:  pytest
# (runs after test_app.py, which already loads the sample documents)
# The LLM is replaced by a fake function, so these tests need no API key and no internet.

import os
import sys
import tempfile

os.environ.setdefault("RAG_DATA_DIR", tempfile.mkdtemp())
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

import pytest  # noqa: E402

import vector_store  # noqa: E402
from agents import llm, orchestrator, query_understanding, response_agent, retrieval_agent  # noqa: E402
from app import app, ingest_file  # noqa: E402


@pytest.fixture(scope="module", autouse=True)
def knowledge_base():
    if vector_store.count() == 0:
        for domain in sorted(os.listdir("sample_docs")):
            for name in sorted(os.listdir(os.path.join("sample_docs", domain))):
                with open(os.path.join("sample_docs", domain, name), "rb") as f:
                    ingest_file(name, f.read(), domain)


@pytest.fixture
def fake_llm(monkeypatch):
    """Fake LLM: answers using passage [1], or says the context is not enough."""
    replies = {"answer": "Employees get 10 days of sick leave per year [1]."}
    monkeypatch.setenv("GROQ_API_KEY", "test")
    monkeypatch.setattr(llm, "chat", lambda system, user, max_tokens=600: replies["answer"])
    return replies


# ---------------------------------------------------------------- Query Understanding Agent
@pytest.mark.parametrize("query, expected", [
    ("How many days of sick leave do I get?", "factual"),
    ("How do I factory reset the thermostat?", "procedural"),
    ("What is the difference between the T2 and the T2 Pro?", "comparative"),
    ("warranty", "ambiguous"),
])
def test_classification(query, expected):
    result = query_understanding.understand(query)
    assert result["query_type"] == expected
    assert 0 <= result["confidence"] <= 1
    assert result["needs_clarification"] == (expected == "ambiguous")


def test_comparative_routing_splits_items():
    result = query_understanding.understand("Which purifier covers a bigger room, AirPure P3 or AirPure P5?")
    assert result["routing"]["path"] == "multi_search"
    assert result["routing"]["sub_queries"] == ["AirPure P3", "AirPure P5"]


# ---------------------------------------------------------------- Retrieval Agent
def test_retrieval_ranks_and_keeps_metadata():
    result = retrieval_agent.retrieve(query_understanding.understand("How do I factory reset the thermostat?"))
    scores = [c["score"] for c in result["chunks"]]
    assert result["status"] == "ok" and scores == sorted(scores, reverse=True)
    first = result["chunks"][0]
    assert first["filename"] == "thermostat_t2_user_manual.pdf"
    assert {"chunk_id", "page", "score", "text"} <= set(first)


def test_retrieval_filters_low_confidence():
    understanding = query_understanding.understand("What is the dress code on Fridays?")
    assert retrieval_agent.retrieve(understanding)["status"] == "no_results"
    # the threshold is configurable
    assert retrieval_agent.retrieve(understanding, min_score=0.0)["status"] == "ok"


# ---------------------------------------------------------------- Response Generation Agent
def test_response_has_sources_and_confidence(fake_llm):
    understanding = query_understanding.understand("How many days of sick leave do I get?")
    result = response_agent.generate(understanding, retrieval_agent.retrieve(understanding))
    assert result["status"] == "answered"
    assert result["sources"][0]["number"] == 1 and result["sources"][0]["filename"]
    assert result["confidence"]["level"] in ("High", "Medium", "Low")


def test_response_not_found_when_llm_says_insufficient(fake_llm):
    fake_llm["answer"] = "INSUFFICIENT_CONTEXT"
    understanding = query_understanding.understand("How many days of sick leave do I get?")
    result = response_agent.generate(understanding, retrieval_agent.retrieve(understanding))
    assert result["status"] == "not_found" and result["sources"] == []


# ---------------------------------------------------------------- Orchestration
def test_pipeline_end_to_end(fake_llm):
    result = orchestrator.handle_query("How many days of sick leave do I get?")
    assert result["status"] == "answered"
    assert result["understanding"]["agent"] == "query_understanding"
    assert result["retrieval"]["agent"] == "retrieval"
    assert result["response"]["agent"] == "response_generation"


def test_pipeline_ambiguous_marked_for_clarification():
    result = orchestrator.handle_query("leave")
    assert result["status"] == "needs_clarification" and result["retrieval"] is None


def test_pipeline_no_results_skips_llm(monkeypatch):
    monkeypatch.setattr(llm, "chat", lambda *a, **k: pytest.fail("LLM should not be called"))
    assert orchestrator.handle_query("What is the dress code on Fridays?")["status"] == "not_found"


def test_pipeline_handles_llm_failure(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = orchestrator.handle_query("How many days of sick leave do I get?")
    assert result["status"] == "error" and result["errors"] and result["sources"]


def test_pipeline_handles_retrieval_failure(monkeypatch):
    monkeypatch.setattr(vector_store, "search", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("db down")))
    result = orchestrator.handle_query("How many days of sick leave do I get?")
    assert result["status"] == "error" and "Search failed" in result["errors"][0]


def test_ask_api(fake_llm):
    response = app.test_client().post("/api/ask", json={"question": "How many days of sick leave do I get?"})
    body = response.get_json()
    assert response.status_code == 200 and body["status"] == "answered" and body["sources"]
