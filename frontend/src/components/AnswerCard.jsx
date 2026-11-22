import { useState } from "react";

// Shows one answer: query type, confidence indicator, answer text, sources and retrieved chunks.
export default function AnswerCard({ result }) {
  const [showChunks, setShowChunks] = useState(false);
  const { understanding, retrieval, confidence } = result;
  const chunks = retrieval ? retrieval.chunks : [];

  return (
    <div className={`answer ${result.status}`}>
      <p className="question">{result.query}</p>

      <div className="badges">
        {understanding && (
          <span className="badge">
            Type: {understanding.query_type} ({Math.round(understanding.confidence * 100)}%)
          </span>
        )}
        <span className={`badge confidence ${confidence.level.toLowerCase()}`}>
          Confidence: {confidence.level}
        </span>
      </div>

      {/* Confidence indicator bar */}
      <div className="bar" title={confidence.reason}>
        <div style={{ width: `${Math.round(confidence.score * 100)}%` }} />
      </div>

      <p className="text">{result.answer}</p>

      {result.sources.length > 0 && (
        <div className="sources">
          <strong>Sources</strong>
          <ul>
            {result.sources.map((s) => (
              <li key={s.chunk_id}>
                [{s.number}] {s.filename}
                {s.page ? `, page ${s.page}` : ""} · chunk {s.chunk_id} · score {s.score}
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.errors.length > 0 && <p className="error">{result.errors.join(" ")}</p>}

      {chunks.length > 0 && (
        <button className="link" onClick={() => setShowChunks(!showChunks)}>
          {showChunks ? "Hide" : "Show"} retrieved chunks ({chunks.length})
        </button>
      )}
      {showChunks &&
        chunks.map((c) => (
          <div key={c.chunk_id} className="chunk">
            <p className="meta">
              #{c.rank} · {c.filename}
              {c.page ? `, page ${c.page}` : ""} · score {c.score}
            </p>
            <p>{c.text}</p>
          </div>
        ))}
    </div>
  );
}
