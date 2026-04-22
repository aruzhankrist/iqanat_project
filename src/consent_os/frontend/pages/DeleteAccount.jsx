import { deleteAccount } from "../api/client";

export default function Account() {
  async function handleDelete() {
    const token = localStorage.getItem("token");

    const res = await deleteAccount(token);

    console.log(res);

    // после удаления — выкидываем пользователя
    localStorage.removeItem("token");

    window.location.href = "/login";
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Account</h1>

      <button
        onClick={handleDelete}
        style={{
          background: "red",
          color: "white",
          padding: 10,
          border: "none",
          cursor: "pointer"
        }}
      >
        Delete account
      </button>
    </div>
  );
}
