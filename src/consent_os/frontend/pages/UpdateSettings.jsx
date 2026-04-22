import { useState } from "react";
import { updateSettings } from "../api/client";

export default function Settings() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    notifycations: false,
    privacy: "low"
  });

  const [result, setResult] = useState(null);

  function handleChange(e) {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value
    });
  }

  async function handleSubmit() {
    const token = localStorage.getItem("token");

    const res = await updateSettings(token, form);
    setResult(res);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Settings</h1>

      <input
        name="username"
        placeholder="username"
        onChange={handleChange}
      />

      <input
        name="email"
        placeholder="email"
        onChange={handleChange}
      />

      <label>
        Notifications
        <input
          type="checkbox"
          name="notifycations"
          onChange={handleChange}
        />
      </label>

      <button onClick={handleSubmit}>Save</button>

      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
