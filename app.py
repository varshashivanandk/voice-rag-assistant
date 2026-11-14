import os
import uuid

from flask import Flask, jsonify, render_template, request

import database
import vector_store
from config import ALLOWED_EXTENSIONS, UPLOAD_DIR
from ingestion import file_to_chunks

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024   # max upload size: 25 MB


@app.route("/")
def home():
    return render_template("index.html")


# Knowledge base ingestion
def ingest_file(filename, file_bytes, domain):
    """Upload pipeline: check type -> save file -> extract/clean/chunk -> embed + store."""
    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF, DOCX, TXT and CSV files are allowed")

    doc_id = uuid.uuid4().hex[:8]
    with open(os.path.join(UPLOAD_DIR, f"{doc_id}_{filename}"), "wb") as f:
        f.write(file_bytes)

    chunks = file_to_chunks(filename, file_bytes)
    if not chunks:
        raise ValueError("No text could be extracted from this file")

    vector_store.add_chunks(doc_id, filename, domain, chunks)
    database.add_document(doc_id, filename, extension, domain, len(chunks))
    return {"id": doc_id, "filename": filename, "domain": domain, "num_chunks": len(chunks)}


@app.route("/api/upload", methods=["POST"])
def upload():
    domain = request.form.get("domain", "general").strip().lower().replace(" ", "_") or "general"
    results = []
    for file in request.files.getlist("files"):
        try:
            results.append({"ok": True, **ingest_file(file.filename, file.read(), domain)})
        except ValueError as error:
            results.append({"ok": False, "filename": file.filename, "error": str(error)})
    return jsonify(results)


@app.route("/api/documents")
def documents():
    return jsonify(database.list_documents())


@app.route("/api/domains")
def domains():
    return jsonify(database.list_domains())


#RAG retrieval
@app.route("/api/search", methods=["POST"])
def search():
    """Semantic search: returns the most relevant chunks and their similarity scores."""
    data = request.get_json()
    hits = vector_store.search(data["question"], int(data.get("top_k", 5)), data.get("domain") or None)
    return jsonify(hits)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
