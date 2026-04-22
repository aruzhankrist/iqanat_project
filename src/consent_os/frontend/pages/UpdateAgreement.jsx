import { useState } from "react";
import { updateAgreement } from "../api/client";

export default function EditAgreement({ agreementId, initialData }) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [reason, setReason] = useState(initialData?.reason || "");
  const [content, setContent] = useState(initialData?.content || "");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleUpdate() {
    setLoading(true);

    const token = localStorage.getItem("token");

    const res = await updateAgreement(token, agreementId, {
      title,
      reason,
      content,
    });

    setMessage(res.message);
    setLoading(false);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Edit Agreement</h1>

      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="title"
      />

      <input
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        placeholder="reason"
      />

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={10}
      />

      <button onClick={handleUpdate} disabled={loading}>
        {loading ? "Updating..." : "Update"}
      </button>

      {message && <p>{message}</p>}
    </div>
  );
}
