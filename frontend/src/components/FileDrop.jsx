import React, { useRef } from "react";

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

export default function FileDrop({ label, file, onFile }) {
  const inputRef = useRef();

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    if (selectedFile.size > MAX_FILE_SIZE) {
      alert("This file is too large. Please upload a file smaller than 10 MB.");
      return;
    }

    onFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    selectFile(e.dataTransfer.files?.[0]);
  };

  return (
    <div
      className="dropzone"
      onClick={() => inputRef.current?.click()}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        hidden
        onChange={(e) => selectFile(e.target.files?.[0])}
      />

      {file ? (
        <p>📄 {file.name}</p>
      ) : (
        <p className="muted">
          {label} — PDF, DOCX, or TXT only; maximum 10 MB
        </p>
      )}
    </div>
  );
}