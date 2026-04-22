import { useState } from "react";
import { login } from "../api/client";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {
    setError("");

    const res = await login(email, password);

    if (res.token) {
      localStorage.setItem("token", res.token);
      localStorage.setItem("user_id", res.user_id);

      window.location.href = "/account";
      return;
    }

    setError(res.detail || "Login failed");
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Login</h1>

      <input
        placeholder="email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>
        Login
      </button>

      {error && (
        <p style={{ color: "red" }}>{error}</p>
      )}
    </div>
  );
}
