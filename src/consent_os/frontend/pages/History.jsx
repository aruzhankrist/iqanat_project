import { useEffect, useState } from "react";
import { getHistory } from "../api/client";

export default function HistoryPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then(setEvents)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (!events.length) return <p>No activity yet</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>History</h1>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {events.map((e, i) => (
          <li
            key={i}
            style={{
              padding: 10,
              marginBottom: 10,
              border: "1px solid #ddd",
            }}
          >
            <p><b>Action:</b> {e.action}</p>

            {e.contract_id && (
              <p><b>Contract:</b> {e.contract_id}</p>
            )}

            <p>
              <small>
                {new Date(e.timestamp).toLocaleString()}
              </small>
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
