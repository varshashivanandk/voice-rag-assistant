# M2.3 Response Generation Agent
#
# 1. Builds a prompt with the retrieved chunks as numbered context [1], [2], ...
# 2. Asks the LLM (Groq) to answer using ONLY that context, with a style per query type.
# 3. Adds source attribution (document, page, chunk id, score) for each [n].
# 4. Calculates a confidence indicator from the retrieval scores.
# 5. If nothing relevant was found, or the LLM says the context is not enough,
#    it tells the user that sufficient information was not found.

import re

from agents import llm, prompts

AGENT = "response_generation"
NOT_FOUND_MESSAGE = ("Sorry, I couldn't find enough information in the knowledge base to answer this. "
                     "Try rephrasing the question or upload a document that covers it.")


def confidence_indicator(chunks, cited_numbers):
    """Application-level confidence, based on retrieval quality and supporting context."""
    if not chunks:
        return {"level": "None", "score": 0.0, "reason": "No relevant information found."}
    top = chunks[0]["score"]
    supporting = len(cited_numbers) or 1
    score = round(min(1.0, top + 0.03 * (supporting - 1)), 3)
    if top >= 0.65:
        level = "High"
    elif top >= 0.55:
        level = "Medium"
    else:
        level = "Low"
    reason = f"Best match score {top:.2f}; answer supported by {supporting} source(s)."
    return {"level": level, "score": score, "reason": reason}


def build_context(chunks):
    parts = []
    for i, c in enumerate(chunks, start=1):
        where = c["filename"] + (f", page {c['page']}" if c["page"] else "")
        parts.append(f"[{i}] ({where})\n{c['text']}")
    return "\n\n".join(parts)


def not_found(reason):
    return {"agent": AGENT, "status": "not_found", "error": None, "answer": NOT_FOUND_MESSAGE,
            "sources": [], "confidence": {"level": "None", "score": 0.0, "reason": reason}}


def generate(understanding, retrieval):
    chunks = retrieval["chunks"]
    if not chunks:
        return not_found("No chunk scored above the relevance threshold.")

    query_type = understanding["query_type"]
    user_prompt = prompts.ANSWER_USER.format(
        query_type=query_type,
        instruction=prompts.TYPE_INSTRUCTIONS.get(query_type, prompts.TYPE_INSTRUCTIONS["factual"]),
        context=build_context(chunks),
        query=understanding["normalized_query"],
    )

    try:
        answer = llm.chat(prompts.ANSWER_SYSTEM, user_prompt)
    except llm.LLMError as error:
        return {"agent": AGENT, "status": "error", "error": str(error),
                "answer": "The answer could not be generated. The most relevant sources are listed below.",
                "sources": [source(i, c) for i, c in enumerate(chunks, start=1)],
                "confidence": confidence_indicator(chunks, [])}

    # Clean up the model's formatting: 【1】 -> [1], unusual spaces -> normal spaces
    answer = re.sub(r"[【\[]\s*(\d+)\s*[】\]]", r"[\1]", answer)
    answer = answer.replace("\u202f", " ").replace("\u00a0", " ")

    if prompts.NOT_FOUND_TOKEN in answer:
        return not_found("The retrieved passages do not contain the answer.")

    # Source attribution: only the passages the answer actually cites
    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer) if 1 <= int(n) <= len(chunks)})
    sources = [source(n, chunks[n - 1]) for n in cited]

    return {"agent": AGENT, "status": "answered", "error": None, "answer": answer,
            "sources": sources, "confidence": confidence_indicator(chunks, cited)}


def source(number, chunk):
    return {"number": number, "filename": chunk["filename"], "page": chunk["page"],
            "chunk_id": chunk["chunk_id"], "score": chunk["score"]}
