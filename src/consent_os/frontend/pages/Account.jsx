import { useEffect, useState } from "react";
import { getAccount } from "../api/client";

export default function Account() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    getAccount(token).then(setUser);
  }, []);

  if (!user) return <p>Loading...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Account</h1>

      <div>
        <p><b>Username:</b> {user.username}</p>
        <p><b>Email:</b> {user.email}</p>
        <p><b>Role:</b> {user.role}</p>
        <p><b>Privacy:</b> {user.privacy}</p>
        <p><b>Notifications:</b> {String(user.notifications)}</p>
        <p><b>Verified:</b> {String(user.is_verified)}</p>
        <p><b>Created:</b> {user.created}</p>
      </div>
    </div>
  );
}
