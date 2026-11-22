import { useState } from "react";
import { uploadFiles } from "../api";

// Knowledge base management: upload documents and show the document list.
export default function UploadPanel({ documents, onUploaded }) {
  const [domain, setDomain] = useState("general");
  const [files, setFiles] = useState([]);
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);

  async function handleUpload() {
    if (files.length === 0) return alert("Choose at least one file");
    setBusy(true);
    setMessages([]);
    const results = await uploadFiles(files, domain);
    setMessages(results);
    setBusy(false);
    setFiles([]);
    onUploaded();
  }

  return (
    <section className="panel">
      <h2>Upload documents</h2>
      <label>
        Domain (knowledge base name)
        <input value={domain} onChange={(e) => setDomain(e.target.value)} />
      </label>
      <div className="row">
        <input
          type="file"
          multiple
          accept=".pdf,.docx,.txt,.csv"
          key={messages.length}
          onChange={(e) => setFiles([...e.target.files])}
        />
        <button onClick={handleUpload} disabled={busy}>
          {busy ? "Uploading…" : "Upload"}
        </button>
      </div>

      {messages.map((m, i) => (
        <p key={i} className={m.ok ? "ok" : "error"}>
          {m.ok ? `✔ ${m.filename}: ${m.num_chunks} chunks indexed` : `✘ ${m.filename}: ${m.error}`}
        </p>
      ))}

      <table>
        <thead>
          <tr>
            <th>File</th>
            <th>Domain</th>
            <th>Chunks</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((d) => (
            <tr key={d.id}>
              <td>{d.filename}</td>
              <td>{d.domain}</td>
              <td>{d.num_chunks}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
