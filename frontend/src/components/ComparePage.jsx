import React, { useState } from "react";
import FileDrop from "./FileDrop.jsx";
import { documentApi } from "../api.js";

function scoreClass(score) {
  if (score >= 70) return "score-high";
  if (score >= 35) return "score-mid";
  return "score-low";
}

export default function ComparePage() {
  const [fileA, setFileA] = useState(null);
  const [fileB, setFileB] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runCompare = async () => {
    if (!fileA || !fileB) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await documentApi.compare(fileA, fileB);
      setResult(data);
    } catch (e) {
      setError(e.response?.data?.detail || "Comparison failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Compare two documents</h1>
      <p className="muted">
        Upload two files to check semantic + lexical similarity between them directly.
      </p>

      <div className="card">
        <FileDrop label="Document A" file={fileA} onFile={setFileA} />
        <div style={{ height: 12 }} />
        <FileDrop label="Document B" file={fileB} onFile={setFileB} />
        <div style={{ height: 16 }} />
        <button disabled={!fileA || !fileB || loading} onClick={runCompare}>
          {loading ? "Analyzing..." : "Compare Documents"}
        </button>
        {error && <p className="error-text">{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h2>
            Overall similarity:{" "}
            <span className={`score-badge ${scoreClass(result.overallScore)}`}>
              {result.overallScore}%
            </span>
          </h2>
          <p className="muted">
            Semantic (meaning-based): {result.semanticScore}% &nbsp;|&nbsp; Lexical
            (word-overlap): {result.lexicalScore}%
          </p>

          <h3>Matched sentences ({result.matches?.length || 0})</h3>
          {result.matches?.length === 0 && (
            <p className="muted">No significant sentence-level matches found.</p>
          )}
          {result.matches?.map((m, i) => (
            <div
              key={i}
              className={`match-item ${m.similarity >= 0.9 ? "high" : "medium"}`}
            >
              <strong>{(m.similarity * 100).toFixed(1)}% match</strong> ({m.matchType})
              <p style={{ margin: "6px 0 2px" }}>"{m.sourceSentence}"</p>
              <p style={{ margin: 0, color: "#9ca3af" }}>≈ "{m.matchedSentence}"</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
