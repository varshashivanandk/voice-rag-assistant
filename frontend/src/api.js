// All calls to the Flask backend.

export async function getDocuments() {
  const response = await fetch("/api/documents");
  return response.json();
}

export async function getDomains() {
  const response = await fetch("/api/domains");
  return response.json();
}

export async function uploadFiles(files, domain) {
  const form = new FormData();
  for (const file of files) form.append("files", file);
  form.append("domain", domain);
  const response = await fetch("/api/upload", { method: "POST", body: form });
  return response.json();
}

export async function askQuestion(question, domain) {
  const response = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, domain }),
  });
  return response.json();
}
