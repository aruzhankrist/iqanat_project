import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function UploadAgreement() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);

  async function analyse() {
    const token = localStorage.getItem("token");

    const text = await file.text(); // читаем файл в браузере

    const res = await fetch(`${API}/agreements/upload/analyse`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        agreement: text,
        reason: "manual analysis",
      }),
    });

    const data = await res.json();
    setAnalysis(data.analysis);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Upload + Analyse</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={analyse} disabled={!file}>
        Analyse
      </button>

      {analysis && (
        <div style={{ marginTop: 20 }}>
          <h3>Analysis result</h3>

          <pre>{JSON.stringify(analysis, null, 2)}</pre>

          <p><b>Risk:</b> {analysis.risk_index}</p>
          <p><b>Summary:</b> {analysis.summary}</p>
        </div>
      )}
    </div>
  );
}
