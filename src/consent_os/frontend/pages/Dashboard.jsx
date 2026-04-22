import { useEffect, useState } from "react";
import { getAgreements } from "../api/client";

export default function Dashboard() {
  const [agreements, setAgreements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    getAgreements(token)
      .then((data) => {
        setAgreements(data);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>My Agreements</h1>

      {agreements.length === 0 && (
        <p>No agreements yet</p>
      )}

      {agreements.map((a) => (
        <div
          key={a.agreement_id}
          style={{
            border: "1px solid #ccc",
            marginBottom: 10,
            padding: 10,
            borderRadius: 6
          }}
        >
          <h3>{a.title}</h3>
          <p>Status: {a.status}</p>
          <p>Risk: {a.risk_index}</p>
          <p>Created: {a.created}</p>
        </div>
      ))}
    </div>
  );
}
