# M2.4 Multi-Agent Orchestration Layer

from agents import query_understanding, response_agent, retrieval_agent
from config import MIN_SCORE, TOP_K

CLARIFICATION_MESSAGE = ("Your question is a bit unclear. Could you add more detail, "
                         "for example which policy, product or topic you mean?")


def handle_query(query, domain=None, top_k=TOP_K, min_score=MIN_SCORE):
    errors = []
    final = {"query": query, "status": "error", "answer": "", "query_type": "",
             "sources": [], "confidence": {"level": "None", "score": 0.0, "reason": ""},
             "understanding": None, "retrieval": None, "response": None, "errors": errors}

    if not query or not query.strip():
        errors.append("Empty query.")
        final["answer"] = "Please type a question."
        return final

    # 1. Query Understanding
    try:
        understanding = query_understanding.understand(query)
    except Exception as error:
        # classification failure: continue as a factual query so the user still gets an answer
        errors.append(f"Classification failed: {error}")
        understanding = {"agent": "query_understanding", "status": "error", "error": str(error),
                         "query": query, "normalized_query": query.strip(), "query_type": "factual",
                         "confidence": 0.0, "method": "fallback", "needs_clarification": False,
                         "routing": {"path": "single_search", "sub_queries": []}}
    final["understanding"] = understanding
    final["query_type"] = understanding["query_type"]

    # Ambiguous queries are marked for clarification (handled in Milestone 3)
    if understanding["needs_clarification"]:
        final["status"] = "needs_clarification"
        final["answer"] = CLARIFICATION_MESSAGE
        return final

    # 2. Retrieval
    retrieval = retrieval_agent.retrieve(understanding, domain, top_k, min_score)
    final["retrieval"] = retrieval
    if retrieval["status"] == "error":
        errors.append(retrieval["error"])
        final["answer"] = "Searching the knowledge base failed. Please try again."
        return final

    # 3. Response Generation
    try:
        response = response_agent.generate(understanding, retrieval)
    except Exception as error:
        errors.append(f"Response generation failed: {error}")
        final["answer"] = "The answer could not be generated. Please try again."
        return final
    final["response"] = response
    if response["error"]:
        errors.append(response["error"])

    # 4. Final response
    final["status"] = response["status"]
    final["answer"] = response["answer"]
    final["sources"] = response["sources"]
    final["confidence"] = response["confidence"]
    return final
