import { useEffect, useState } from "react";
import { getAgreement, deleteAgreement } from "../api/client";
import { useNavigate } from "react-router-dom";

export default function AgreementPage({ agreementId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    getAgreement(token, agreementId)
      .then(setData)
      .finally(() => setLoading(false));
  }, [agreementId]);

  async function handleDelete() {
    const token = localStorage.getItem("token");

    const ok = window.confirm("Delete this agreement?");
    if (!ok) return;

    await deleteAgreement(token, agreementId);

    navigate("/dashboard");
  }

  if (loading) return <p>Loading...</p>;
  if (!data) return <p>Not found</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>{data.title}</h1>

      <p><b>Status:</b> {data.status}</p>
      <p><b>Risk:</b> {data.risk_index}</p>
      <p><b>Reason:</b> {data.reason}</p>

      <hr />

      <div>
        <h3>Content</h3>
        <pre style={{ whiteSpace: "pre-wrap" }}>
          {data.content}
        </pre>
      </div>

      <hr />

      <div>
        <h3>Permissions</h3>
        <pre>{JSON.stringify(data.permissions, null, 2)}</pre>
      </div>

      {data.metadata && (
        <>
          <h3>Metadata</h3>
          <pre>{JSON.stringify(data.metadata, null, 2)}</pre>
        </>
      )}

      <small>Created: {data.created}</small>

      <hr />

      <button
        onClick={handleDelete}
        style={{ color: "red" }}
      >
        Delete agreement
      </button>
    </div>
  );
}
