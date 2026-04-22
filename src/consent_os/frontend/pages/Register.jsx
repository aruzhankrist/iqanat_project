import { useState } from "react";
import { register } from "../api/client";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");

  async function handleRegister() {
    const res = await register(username, email, password);

    if (res.success) {
      setMessage("Регистрация успешна");

      // можно сразу перекинуть на login
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } else {
      setMessage(res.detail || "Ошибка");
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Register</h1>

      <input
        placeholder="username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        placeholder="email"
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleRegister}>
        Register
      </button>

      {message && <p>{message}</p>}
    </div>
  );
}
