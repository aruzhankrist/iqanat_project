import { useEffect, useState } from "react";
import { getSettings } from "../api/client";

export default function SettingsPage() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSettings()
      .then(setSettings)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (!settings) return <p>No settings found</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>General Settings</h1>

      <div style={{ marginTop: 20 }}>

        <label>
          Privacy:
          <span style={{ marginLeft: 10 }}>
            {settings.privacy}
          </span>
        </label>

        <br />

        <label>
          Notifications:
          <input
            type="checkbox"
            checked={settings.notifications}
            readOnly
          />
        </label>

        <br />

        <label>
          Marketing opt-in:
          <input
            type="checkbox"
            checked={settings.marketing_opt_in}
            readOnly
          />
        </label>

        <br />

        <label>
          Role:
          <b style={{ marginLeft: 10 }}>
            {settings.role}
          </b>
        </label>

      </div>
    </div>
  );
}
