# Standard request/response format for communication between the agents.

from typing import List, Optional, TypedDict

QUERY_TYPES = ["factual", "procedural", "comparative", "ambiguous"]


class Routing(TypedDict):
    path: str                 # "single_search" | "multi_search" | "clarification"
    sub_queries: List[str]


class UnderstandingResult(TypedDict):          # Query Understanding Agent -> Retrieval Agent
    agent: str                # "query_understanding"
    status: str               # "ok"
    error: Optional[str]
    query: str                # original query
    normalized_query: str     # cleaned query used for search
    query_type: str           # one of QUERY_TYPES
    confidence: float         # classification confidence, 0..1
    method: str               # "rules" or "llm"
    needs_clarification: bool # True for ambiguous queries
    routing: Routing


class Chunk(TypedDict):
    rank: int
    chunk_id: str             # "<doc_id>_<chunk number>"
    chunk_index: int
    filename: str             # document name
    domain: str
    page: Optional[int]       # page number (PDF only)
    score: float              # relevance score = cosine similarity
    text: str


class RetrievalResult(TypedDict):              # Retrieval Agent -> Response Generation Agent
    agent: str                # "retrieval"
    status: str               # "ok" | "no_results" | "error"
    error: Optional[str]
    chunks: List[Chunk]       # kept chunks, ranked by score (highest first)
    filtered_out: int         # chunks dropped because score < min_score
    top_score: float
    min_score: float


class Source(TypedDict):
    number: int               # the [n] used in the answer
    filename: str
    page: Optional[int]
    chunk_id: str
    score: float


class ConfidenceIndicator(TypedDict):
    level: str                # "High" | "Medium" | "Low" | "None"
    score: float              # 0..1
    reason: str


class ResponseResult(TypedDict):               # Response Generation Agent -> Final Response
    agent: str                # "response_generation"
    status: str               # "answered" | "not_found" | "error"
    error: Optional[str]
    answer: str
    sources: List[Source]
    confidence: ConfidenceIndicator


class FinalResponse(TypedDict):                # Orchestrator -> API -> frontend
    query: str
    status: str               # "answered" | "not_found" | "needs_clarification" | "error"
    answer: str
    query_type: str
    sources: List[Source]
    confidence: ConfidenceIndicator
    understanding: UnderstandingResult
    retrieval: Optional[RetrievalResult]
    response: Optional[ResponseResult]
    errors: List[str]
