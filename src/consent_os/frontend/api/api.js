const API = "http://127.0.0.1:8000";

export async function request(path, options = {}) {
  const token = localStorage.getItem("token");

  const isFormData = options.body instanceof FormData;

  const headers = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(!isFormData ? { "Content-Type": "application/json" } : {}),
    ...options.headers,
  };

  const res = await fetch(`http://127.0.0.1:8000${path}`, {
    ...options,
    headers,
  });

  const text = await res.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    console.error("❌ Server returned non-JSON:", text);
    return { error: "Invalid server response" };
  }

  if (!res.ok) {
    console.error("API error:", data);
  }

  return data;
}

/* AUTH */
export function login(email, password) {
  return request("/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function register(username, email, password) {
  return request("/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
}

/* ACCOUNT */
export function getAccount() {
  return request("/account");
}

export function updateSettings(data) {
  return request("/account/settings", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteAccount() {
  return request("/account/delete", {
    method: "DELETE",
  });
}

/* AGREEMENTS */
export function getAgreements() {
  return request("/agreements");
}

export function getAgreement(agreementId) {
  return request(`/agreements/${agreementId}`);
}

export function uploadAgreement(file, title, reason, riskLevel) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("title", title);
  formData.append("reason", reason);
  formData.append("risk_level", riskLevel);

  return request("/agreements/upload", {
    method: "POST",
    body: formData,
  });
}

export function deleteAgreement(agreementId) {
  return request(`/agreements/${agreementId}/delete`, {
    method: "DELETE",
  });
}

export function analyseAgreement(agreement, reason) {
  return request("/agreements/upload/analyse", {
    method: "POST",
    body: JSON.stringify({ agreement, reason }),
  });
}

export function updateAgreement(agreementId, data) {
  return request(`/agreements/${agreementId}/update`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

/* SETTINGS */
export function getSettings() {
  return request("/settings");
}
