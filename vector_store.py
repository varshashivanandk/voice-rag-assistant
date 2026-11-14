import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from config import CHROMA_DIR, TOP_K, MIN_SCORE

embedding_model = DefaultEmbeddingFunction()   # all-MiniLM-L6-v2

client = chromadb.PersistentClient(path=CHROMA_DIR)   # saved on disk
collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"},   # compare vectors with cosine similarity
)


def create_embeddings(texts):
    """Text -> vectors (one list of 384 numbers per text)."""
    return [list(map(float, vector)) for vector in embedding_model(texts)]


def add_chunks(doc_id, filename, domain, chunks):
    """Store chunks with their vectors and metadata in ChromaDB."""
    texts = [c["text"] for c in chunks]
    collection.add(
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))],
        embeddings=create_embeddings(texts),
        documents=texts,
        metadatas=[{
            "doc_id": doc_id,
            "filename": filename,
            "domain": domain,
            "chunk_index": i,
            "page": c["page"] or 0,   # 0 means no page number because Chroma doesn't allow None
        } for i, c in enumerate(chunks)],
    )


def search(question, top_k=TOP_K, domain=None):
    """Semantic search: return the top_k chunks most similar to the question."""
    if collection.count() == 0:
        return []
    results = collection.query(
        query_embeddings=create_embeddings([question]),
        n_results=min(top_k, collection.count()),
        where={"domain": domain} if domain else None,   
    )
    hits = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]   # Chroma gives distance (similarity = 1 - distance)
        hits.append({
            "rank": i + 1,
            "text": results["documents"][0][i],
            "filename": meta["filename"],
            "domain": meta["domain"],
            "page": meta["page"] or None,
            "score": round(score, 3),
            "low_relevance": score < MIN_SCORE,
        })
    return hits


def count():
    return collection.count()
