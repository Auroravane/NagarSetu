/**
 * NagarSetu Extension — Client for NagarSetu Backend API.
 *
 * Integrates with:
 * - GET /health & GET /ready
 * - POST /api/chat (RAG retrieval & structured checklist generation)
 * - POST /api/progress & GET /api/progress (authenticated/demo checklist persistence)
 * - GET /api/auth/me (current user verification)
 */

export const DEFAULT_BACKEND_URL = "https://nagarsetu-jco2.onrender.com";
export const LOCAL_BACKEND_URL = "http://localhost:8000";

export async function getBackendBaseUrl() {
  const data = await chrome.storage.local.get(["backendUrl"]);
  return data.backendUrl || DEFAULT_BACKEND_URL;
}

export async function setBackendBaseUrl(url) {
  const clean = (url || "").trim().replace(/\/+$/, "");
  await chrome.storage.local.set({ backendUrl: clean });
}

export async function getAuthToken() {
  const data = await chrome.storage.local.get(["authToken"]);
  return data.authToken || null;
}

export async function setAuthToken(token) {
  if (token) {
    await chrome.storage.local.set({ authToken: token });
  } else {
    await chrome.storage.local.remove(["authToken"]);
  }
}

/**
 * Check backend liveness and readiness
 */
export async function checkBackendHealth() {
  const baseUrl = await getBackendBaseUrl();
  try {
    const res = await fetch(`${baseUrl}/health`, { method: "GET" });
    if (!res.ok) return { healthy: false, status: res.status };
    const json = await res.json().catch(() => ({}));
    return { healthy: json.ok === true, data: json };
  } catch (err) {
    return { healthy: false, error: err.message };
  }
}

/**
 * Retrieve verified user profile from backend
 */
export async function fetchCurrentUser() {
  const baseUrl = await getBackendBaseUrl();
  const token = await getAuthToken();

  const headers = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${baseUrl}/api/auth/me`, {
    method: "GET",
    headers,
    credentials: "include",
  });

  if (!res.ok) {
    return null;
  }

  const data = await res.json();
  return data.user || null;
}

/**
 * Ask NagarSetu backend for civic procedure guidance (Hybrid RAG & Groundedness)
 */
export async function queryNagarSetuChat(message, sessionId = "ext-sess-1", language = "en") {
  const baseUrl = await getBackendBaseUrl();
  const token = await getAuthToken();

  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${baseUrl}/api/chat`, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({
      session_id: sessionId,
      message,
      language,
    }),
  });

  if (!res.ok) {
    let detail = `Server responded with ${res.status}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) detail = errJson.detail;
    } catch {}
    throw new Error(detail);
  }

  return await res.json();
}

/**
 * Update checklist step completion state on backend
 */
export async function updateProcedureProgress({ sessionId, procedureId, stepNumber, completed }) {
  const baseUrl = await getBackendBaseUrl();
  const token = await getAuthToken();

  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${baseUrl}/api/progress`, {
    method: "POST",
    headers,
    credentials: "include",
    body: JSON.stringify({
      session_id: sessionId,
      procedure_id: procedureId,
      step_number: stepNumber,
      completed,
    }),
  });

  if (!res.ok) {
    throw new Error(`Failed to update step progress (${res.status})`);
  }

  return await res.json();
}

/**
 * Fetch persisted checklist progress from backend
 */
export async function fetchProcedureProgress(procedureId, sessionId = "ext-sess-1") {
  const baseUrl = await getBackendBaseUrl();
  const token = await getAuthToken();

  const headers = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const params = new URLSearchParams({
    procedure_id: procedureId,
    session_id: sessionId,
  });

  const res = await fetch(`${baseUrl}/api/progress?${params.toString()}`, {
    method: "GET",
    headers,
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch progress (${res.status})`);
  }

  return await res.json();
}
