import React, { useState } from "react";
import FileDrop from "./FileDrop.jsx";
import { documentApi } from "../api.js";

export default function AnalyzePage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await documentApi.analyze(file);
      setResult(data);
    } catch (e) {
      setError(e.response?.data?.detail || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Submit for full plagiarism check</h1>
      <p className="muted">
        This checks your document against every document previously submitted
        to the corpus (not just one file), then adds it to the corpus.
      </p>

      <div className="card">
        <FileDrop label="Document to check" file={file} onFile={setFile} />
        <div style={{ height: 16 }} />
        <button disabled={!file || loading} onClick={runAnalyze}>
          {loading ? "Analyzing..." : "Run Corpus Check"}
        </button>
        {error && <p className="error-text">{error}</p>}
      </div>

      {result && (
        <div className="card">
          <h2>Highest similarity found: {result.highestSimilarityPct}%</h2>
          <p className="muted">Word count: {result.wordCount}</p>

          <h3>Closest matches in corpus</h3>
          {(!result.topCorpusMatches || result.topCorpusMatches.length === 0) && (
            <p className="muted">No prior submissions to compare against yet.</p>
          )}
          {result.topCorpusMatches?.map((m, i) => (
            <div key={i} className="match-item">
              <strong>{(m.similarity * 100).toFixed(1)}%</strong> match with document #
              {m.documentId}
              <p style={{ margin: "6px 0 0" }}>"{m.chunkText.slice(0, 200)}..."</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
