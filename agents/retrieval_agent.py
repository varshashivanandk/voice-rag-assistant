# M2.2 Retrieval Agent

import vector_store
from config import MIN_SCORE, TOP_K

AGENT = "retrieval"


def retrieve(understanding, domain=None, top_k=TOP_K, min_score=MIN_SCORE):
    query = understanding["normalized_query"]
    sub_queries = understanding["routing"]["sub_queries"]

    try:
        if understanding["routing"]["path"] == "multi_search":
            # comparative: search the full question AND each item, so both sides are found
            hits = []
            for q in [query] + sub_queries:
                hits += vector_store.search(q, top_k, domain)
        else:
            hits = vector_store.search(query, top_k, domain)
    except Exception as error:
        return {"agent": AGENT, "status": "error", "error": f"Search failed: {error}",
                "chunks": [], "filtered_out": 0, "top_score": 0.0, "min_score": min_score}

    # Remove duplicates (same chunk found by several searches): keep its best score
    best = {}
    for hit in hits:
        if hit["chunk_id"] not in best or hit["score"] > best[hit["chunk_id"]]["score"]:
            best[hit["chunk_id"]] = hit

    # Rank by relevance score
    ranked = sorted(best.values(), key=lambda h: h["score"], reverse=True)
    if understanding["routing"]["path"] == "multi_search":
        ranked = ranked[:top_k + 2]   # a few extra so both compared items fit

    # Low-confidence filtering
    kept = [h for h in ranked if h["score"] >= min_score]
    chunks = [{
        "rank": i + 1,
        "chunk_id": h["chunk_id"],
        "chunk_index": h["chunk_index"],
        "filename": h["filename"],
        "domain": h["domain"],
        "page": h["page"],
        "score": h["score"],
        "text": h["text"],
    } for i, h in enumerate(kept)]

    return {
        "agent": AGENT,
        "status": "ok" if chunks else "no_results",
        "error": None,
        "chunks": chunks,
        "filtered_out": len(ranked) - len(kept),
        "top_score": ranked[0]["score"] if ranked else 0.0,
        "min_score": min_score,
    }
