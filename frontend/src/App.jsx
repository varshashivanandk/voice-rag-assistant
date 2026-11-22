import { useEffect, useState } from "react";
import { getDocuments, getDomains } from "./api";
import UploadPanel from "./components/UploadPanel";
import AskPanel from "./components/AskPanel";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [domains, setDomains] = useState([]);

  // Load the document list and domain names from the backend
  async function refresh() {
    setDocuments(await getDocuments());
    setDomains(await getDomains());
  }

  useEffect(() => {
    refresh();
  }, []);

  const totalChunks = documents.reduce((sum, d) => sum + d.num_chunks, 0);

  return (
    <>
      <header>
        <h1>RAG Knowledge Assistant</h1>
        <span className="status">
          {documents.length} documents · {totalChunks} chunks
        </span>
      </header>
      <main>
        <UploadPanel documents={documents} onUploaded={refresh} />
        <AskPanel domains={domains} />
      </main>
    </>
  );
}
