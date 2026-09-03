import React, { useEffect, useState } from "react";
import { documentApi } from "../api.js";

export default function HistoryPage() {
  const [docs, setDocs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    documentApi
      .history()
      .then(setDocs)
      .catch(() => setError("Could not load history."));
  }, []);

  return (
    <div>
      <h1>Your submission history</h1>
      {error && <p className="error-text">{error}</p>}
      {docs.length === 0 && !error && (
        <p className="muted">No documents submitted yet.</p>
      )}
      {docs.map((d) => (
        <div key={d.id} className="card">
          <strong>{d.filename}</strong>
          <p className="muted">
            {d.wordCount ?? "—"} words · highest similarity:{" "}
            {d.highestSimilarityPct != null ? `${d.highestSimilarityPct}%` : "—"}
          </p>
          <p className="muted">
            {new Date(d.uploadedAt).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}
