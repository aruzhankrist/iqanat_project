import { useState } from "react";
import { uploadAgreement } from "../api/client";

export default function UploadAgreement() {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [reason, setReason] = useState("");
  const [risk, setRisk] = useState("low");

  const [message, setMessage] = useState("");

  async function handleUpload() {
    const token = localStorage.getItem("token");

    const res = await uploadAgreement(
      token,
      file,
      title,
      reason,
      risk
    );

    setMessage(res.message);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Upload Agreement</h1>

      <input
        type="text"
        placeholder="title"
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        type="text"
        placeholder="reason"
        onChange={(e) => setReason(e.target.value)}
      />

      <select onChange={(e) => setRisk(e.target.value)}>
        <option value="low">low</option>
        <option value="medium">medium</option>
        <option value="high">high</option>
      </select>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>
        Upload
      </button>

      {message && <p>{message}</p>}
    </div>
  );
}
