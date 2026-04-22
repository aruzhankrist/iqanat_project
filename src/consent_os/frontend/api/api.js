const API = "http://127.0.0.1:8000";

export async function getAccount(token) {
  const res = await fetch(`${API}/account`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return res.json();
}

export async function updateSettings(token, data) {
  const res = await fetch(`${API}/account/settings`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });

  return res.json();
}

export async function deleteAccount(token) {
  const res = await fetch(`${API}/account/delete`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return res.json();
}

export async function login(email, password) {
  const res = await fetch(`${API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email,
      password
    })
  });

  return res.json();
}

export async function register(username, email, password) {
  const res = await fetch(`${API}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      email,
      password
    })
  });

  return res.json();
}

export async function getAgreements(token) {
  const res = await fetch(`${API}/agreements`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return res.json();
}

export async function getAgreement(token, agreementId) {
  const res = await fetch(`${API}/agreements/${agreementId}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  return res.json();
}

export async function uploadAgreement(token, file, title, reason, risk_level) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("title", title);
  formData.append("reason", reason);
  formData.append("risk_level", risk_level);

  const res = await fetch(`${API}/agreements/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  return res.json();
}

export async function deleteAgreement(token, agreementId) {
  const res = await fetch(
    `${API}/agreements/${agreementId}/delete`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return res.json();
}

export async function analyseAgreement(agreement, reason) {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API}/agreements/upload/analyse`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      agreement,
      reason,
    }),
  });

  return res.json();
}

export async function updateAgreement(token, agreementId, data) {
  const res = await fetch(
    `${API}/agreements/${agreementId}/update`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    }
  );

  return res.json();
}

export async function getHistory() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API}/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return res.json();
}

export async function getSettings() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API}/settings`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return res.json();
}
