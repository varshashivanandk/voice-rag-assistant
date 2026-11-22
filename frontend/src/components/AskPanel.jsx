import { useState } from "react";
import { askQuestion } from "../api";
import AnswerCard from "./AnswerCard";

// Ask a question: sends it to /api/ask (the multi-agent pipeline) and shows the answers.
export default function AskPanel({ domains }) {
  const [question, setQuestion] = useState("");
  const [domain, setDomain] = useState("");
  const [answers, setAnswers] = useState([]);
  const [busy, setBusy] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;
    setBusy(true);
    try {
      const result = await askQuestion(question, domain);
      setAnswers([result, ...answers]);   // newest answer on top
      setQuestion("");
    } catch {
      alert("Could not reach the backend. Is python app.py running?");
    }
    setBusy(false);
  }

  return (
    <section className="panel wide">
      <h2>Ask a question</h2>
      <div className="row">
        <select value={domain} onChange={(e) => setDomain(e.target.value)}>
          <option value="">All domains</option>
          {domains.map((d) => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>
        <input
          className="question"
          placeholder="Type a question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button onClick={handleAsk} disabled={busy}>
          {busy ? "Thinking…" : "Ask"}
        </button>
      </div>

      {answers.map((a, i) => (
        <AnswerCard key={answers.length - i} result={a} />
      ))}
    </section>
  );
}
