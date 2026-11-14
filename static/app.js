// Frontend logic: talks to the Flask API with fetch().

// ------------------------------------------------------------ Upload
async function loadDocuments() {
  const docs = await (await fetch("/api/documents")).json();
  document.getElementById("documents").innerHTML = docs.map((doc) => `
      <tr><td>${doc.filename}</td><td>${doc.domain}</td><td>${doc.num_chunks}</td></tr>`).join("");

  const totalChunks = docs.reduce((sum, doc) => sum + doc.num_chunks, 0);
  document.getElementById("status").textContent = `${docs.length} documents · ${totalChunks} chunks`;

  // fill the domain filter drop-down
  const domains = await (await fetch("/api/domains")).json();
  document.getElementById("domain-filter").innerHTML = '<option value="">All domains</option>' +
    domains.map((d) => `<option value="${d}">${d}</option>`).join("");
}

async function uploadFiles() {
  const files = document.getElementById("files").files;
  if (files.length === 0) return alert("Choose at least one file");

  const form = new FormData();
  for (const file of files) form.append("files", file);
  form.append("domain", document.getElementById("domain").value);

  const messages = document.getElementById("upload-messages");
  messages.textContent = "Uploading and indexing…";
  const results = await (await fetch("/api/upload", { method: "POST", body: form })).json();
  messages.innerHTML = results.map((r) => r.ok
      ? `<p class="ok">✔ ${r.filename}: ${r.num_chunks} chunks indexed</p>`
      : `<p class="error">✘ ${r.filename}: ${r.error}</p>`).join("");
  document.getElementById("files").value = "";
  loadDocuments();
}

// ------------------------------------------------------------ Search
async function search() {
  const question = document.getElementById("question").value.trim();
  if (!question) return;

  const response = await fetch("/api/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question, top_k: 5,
                           domain: document.getElementById("domain-filter").value }),
  });
  const hits = await response.json();

  const items = hits.map((h) => `
      <div class="chunk ${h.low_relevance ? "low" : ""}">
        <p class="meta">#${h.rank} · ${h.filename}${h.page ? ", page " + h.page : ""} · ${h.domain}
          · score ${h.score} ${h.low_relevance ? "· LOW RELEVANCE" : ""}</p>
        <p>${h.text}</p>
      </div>`).join("");
  document.getElementById("results").innerHTML =
    `<p class="question">${question}</p>${items || "<p>No documents uploaded yet.</p>"}`;
}

// ------------------------------------------------------------ Start
document.getElementById("upload-btn").onclick = uploadFiles;
document.getElementById("search-btn").onclick = search;
document.getElementById("question").addEventListener("keydown", (e) => { if (e.key === "Enter") search(); });
loadDocuments();
