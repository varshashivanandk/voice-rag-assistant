# M2.1 Query Understanding Agent

import re

from agents import llm, prompts

AGENT = "query_understanding"
LLM_FALLBACK_BELOW = 0.6   # rules confidence below this -> ask the LLM

STOPWORDS = {"a", "an", "the", "is", "are", "was", "of", "to", "in", "on", "for", "and", "or", "do",
             "does", "did", "i", "me", "my", "we", "you", "what", "how", "when", "where", "which", "who",
             "can", "with", "about", "it", "this", "that", "these", "those", "there", "tell", "more",
             "please", "get", "be", "any", "some", "thing", "things", "stuff", "info", "information"}

FILLERS = r"^(um+|uh+|hey|hi|okay|ok|so|please)[,\s]+"

# Classification rules
COMPARATIVE_RULES = [
    r"\bdifferences?\b", r"\bcompare\b", r"\bcompared (to|with)\b", r"\bcomparison\b",
    r"\bvs\.?\b", r"\bversus\b", r"\bbetter\b", r"\bworse\b",
    r"\b(more|less|fewer|bigger|smaller|larger|cheaper|longer|shorter)\b.*\bthan\b",
    r"^which\b.*\bor\b",                      
]
PROCEDURAL_RULES = [
    r"^how (do|can|should|would) (i|we|you|one)\b", r"^how to\b",
    r"\bsteps?\b", r"\bprocedure\b", r"\bprocess\b", r"\bwhat should i do\b",
    r"\b(set ?up|install|configure|reset|apply for|request|claim|raise|connect|submit|replace)\b",
]
FACTUAL_RULES = [
    r"^(what|when|where|who|which|whose)\b", r"^how (many|much|long|often|old|far)\b",
    r"^(is|are|does|do|can|will|was)\b",
]
AMBIGUOUS_PRONOUN = r"^(what|how) about (it|that|this|them|those)\b|^(and|what about|how about)\b|^(tell me more|explain|more)\b"


def clean(query):
    text = re.sub(FILLERS, "", query.strip(), flags=re.I)
    text = re.sub(r"\s+", " ", text)
    return text


def content_words(text):
    return [w for w in re.findall(r"[a-z0-9\-]+", text.lower()) if w not in STOPWORDS and len(w) > 1]


def classify_with_rules(text):
    """Returns (query_type, confidence)."""
    lower = text.lower().rstrip("?.! ")
    words = content_words(lower)

    # Ambiguous: nothing to search for, a single vague word, or a reference to "it/that" with no subject
    if not words:
        return "ambiguous", 0.95
    if re.search(AMBIGUOUS_PRONOUN, lower) and len(words) <= 2:
        return "ambiguous", 0.9
    if len(lower.split()) <= 2 and not re.search(r"\?$", text):
        return "ambiguous", 0.8

    if any(re.search(r, lower) for r in COMPARATIVE_RULES):
        return "comparative", 0.9
    if re.search(r"^how (many|much|long|often|old|far)\b", lower):
        return "factual", 0.85     
    if any(re.search(r, lower) for r in PROCEDURAL_RULES):
        return "procedural", 0.85
    if any(re.search(r, lower) for r in FACTUAL_RULES):
        return "factual", 0.8
    return "factual", 0.5 


def classify_with_llm(text):
    reply = llm.chat(prompts.CLASSIFY_SYSTEM, prompts.CLASSIFY_USER.format(query=text), max_tokens=5)
    label = reply.strip().lower().strip(".")
    if label not in ("factual", "procedural", "comparative", "ambiguous"):
        raise llm.LLMError(f"Unexpected label from LLM: {reply!r}")
    return label, 0.75


def split_comparison(text):
    """'difference between A and B' / 'A or B' / 'A vs B' -> ['A', 'B'] (used for one search per item)."""
    t = text.rstrip("?.! ")
    patterns = [
        r"between (?:the )?(.+?) and (?:the )?(.+)$",
        r"compare (?:the )?(.+?) (?:and|with|to) (?:the )?(.+)$",
        r",\s*(.+?) or (.+)$",
        r"(.+?) (?:vs\.?|versus) (.+)$",
        r"(?:is|are) (?:the )?(.+?) or (?:the )?(.+?) (?:better|cheaper|bigger|longer)\b.*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, t, re.I)
        if match:
            return [match.group(1).strip(), match.group(2).strip()]
    return []


def understand(query):
    """Main function of the agent."""
    text = clean(query)
    query_type, confidence = classify_with_rules(text)
    method = "rules"

    if confidence < LLM_FALLBACK_BELOW and llm.is_available():
        try:
            query_type, confidence = classify_with_llm(text)
            method = "llm"
        except llm.LLMError:
            pass   # keep the rules result

    # Routing information for the next agent
    if query_type == "ambiguous":
        routing = {"path": "clarification", "sub_queries": []}
    elif query_type == "comparative":
        sub_queries = split_comparison(text)
        routing = {"path": "multi_search" if len(sub_queries) == 2 else "single_search",
                   "sub_queries": sub_queries}
    else:
        routing = {"path": "single_search", "sub_queries": []}

    return {
        "agent": AGENT,
        "status": "ok",
        "error": None,
        "query": query,
        "normalized_query": text,
        "query_type": query_type,
        "confidence": confidence,
        "method": method,
        "needs_clarification": query_type == "ambiguous",
        "routing": routing,
    }
