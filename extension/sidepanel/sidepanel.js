/**
 * NagarSetu Extension — Side Panel Controller.
 *
 * Implements:
 * 1. Civic Procedure Chat (Official NagarSetu RAG + Groundedness Verification).
 * 2. On-demand Government Webpage Analysis (BYOK-driven, strict prompt guardrails).
 * 3. Selection Explanation (BYOK-driven).
 * 4. Persistent Checklist Synchronization (Server-side progress persistence & Demo Mode).
 * 5. Full BYOK configuration (Groq, Gemini, OpenAI) and connection testing.
 */

import { PROVIDERS, executeBYOKCompletion } from "../lib/providers.js";
import {
  checkBackendHealth,
  fetchCurrentUser,
  getBackendBaseUrl,
  setBackendBaseUrl,
  getAuthToken,
  setAuthToken,
  queryNagarSetuChat,
  fetchProcedureProgress,
  updateProcedureProgress,
} from "../lib/api.js";
import { explainSelectedText, analyzePageContent } from "../lib/router.js";

// State
let currentChecklist = null;
let currentSessionId = "ext-sess-1";
let activeUser = null;

document.addEventListener("DOMContentLoaded", async () => {
  setupNavigation();
  setupSettings();
  setupChat();
  setupPageAnalysis();
  await initializeState();
  checkPendingActions();
});

// ---------------------------------------------------------------------------
// Navigation & Views
// ---------------------------------------------------------------------------
function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".view-panel");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const targetView = tab.getAttribute("data-view");
      activateView(targetView);
    });
  });

  const btnTabNav = document.getElementById("btnTabNav");
  if (btnTabNav) {
    btnTabNav.addEventListener("click", () => activateView("settings"));
  }
}

function activateView(viewName) {
  const tabs = document.querySelectorAll(".nav-tab");
  const panels = document.querySelectorAll(".view-panel");

  tabs.forEach((t) => {
    t.classList.toggle("active", t.getAttribute("data-view") === viewName);
  });

  panels.forEach((p) => {
    p.classList.remove("active");
  });

  const targetPanel = document.getElementById(
    `view${viewName.charAt(0).toUpperCase() + viewName.slice(1)}`
  );
  if (targetPanel) {
    targetPanel.classList.add("active");
  }
}

// ---------------------------------------------------------------------------
// Initialization & Backend Check
// ---------------------------------------------------------------------------
async function initializeState() {
  const liveBadge = document.getElementById("liveBadge");
  const authStatusText = document.getElementById("authStatusText");
  const linkAuthAction = document.getElementById("linkAuthAction");

  // Check storage for session ID
  const stored = await chrome.storage.local.get(["extensionSessionId", "openView"]);
  if (stored.extensionSessionId) {
    currentSessionId = stored.extensionSessionId;
  } else {
    currentSessionId = `ext-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    await chrome.storage.local.set({ extensionSessionId: currentSessionId });
  }

  if (stored.openView) {
    activateView(stored.openView);
    await chrome.storage.local.remove(["openView"]);
  }

  // Check Backend
  try {
    const health = await checkBackendHealth();
    if (health.healthy) {
      liveBadge.textContent = "API Live";
      liveBadge.className = "badge badge-online";
    } else {
      liveBadge.textContent = "Offline/Demo";
      liveBadge.className = "badge badge-demo";
    }
  } catch {
    liveBadge.textContent = "Disconnected";
    liveBadge.className = "badge badge-error";
  }

  // Check authenticated user
  try {
    activeUser = await fetchCurrentUser();
    if (activeUser) {
      authStatusText.textContent = `Signed in as ${activeUser.email}`;
      linkAuthAction.textContent = "Sign Out";
      linkAuthAction.onclick = async (e) => {
        e.preventDefault();
        await setAuthToken(null);
        activeUser = null;
        authStatusText.textContent = "Signed in as Demo User";
        linkAuthAction.textContent = "Sync with Account";
      };
    } else {
      authStatusText.textContent = "Signed in as Demo User";
      linkAuthAction.textContent = "Sync with Account";
      linkAuthAction.onclick = (e) => {
        e.preventDefault();
        activateView("settings");
      };
    }
  } catch {
    authStatusText.textContent = "Signed in as Demo User";
  }

  // Update active tab URL & Title in Page Analysis view
  updateActiveTabInfo();
}

async function updateActiveTabInfo() {
  const titleEl = document.getElementById("activePageTitle");
  const urlEl = document.getElementById("activePageUrl");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab) {
    titleEl.textContent = tab.title || "Untitled Tab";
    urlEl.textContent = tab.url || "No URL";
  }
}

// ---------------------------------------------------------------------------
// Pending Actions from Popup or Context Menu
// ---------------------------------------------------------------------------
async function checkPendingActions() {
  const stored = await chrome.storage.local.get(["pendingAction"]);
  if (!stored.pendingAction) return;

  const action = stored.pendingAction;
  await chrome.storage.local.remove(["pendingAction"]);

  if (action.type === "explain" || action.type === "civic_check") {
    activateView("chat");
    handleIncomingSelection(action.text, action.pageTitle, action.pageUrl, action.type);
  } else if (action.type === "analyze_page") {
    activateView("page");
    runPageAnalysis();
  }
}

async function handleIncomingSelection(text, pageTitle, pageUrl, actionType) {
  const chatMessages = document.getElementById("chatMessages");

  appendUserMessage(`Explain this excerpt from "${pageTitle}":\n"${text}"`);

  const config = await getBYOKConfig();
  if (!config.apiKey) {
    appendAssistantMessage(
      `<p><strong>BYOK Configuration Required</strong></p><p>To explain selected webpage text directly, please configure your AI provider (Groq, Gemini, or OpenAI) in the <strong>Settings / BYOK</strong> tab.</p>`,
      "byok"
    );
    return;
  }

  const loadingMsg = appendLoadingMessage("Explaining selected government text...");

  try {
    const explanation = await explainSelectedText({
      text,
      pageTitle,
      pageUrl,
      providerConfig: config,
    });
    loadingMsg.remove();
    appendAssistantMessage(
      `<div class="msg-badge badge-byok">BYOK AI Explanation (${config.provider.toUpperCase()})</div>
       <p>${escapeHtml(explanation.text).replace(/\n/g, "<br>")}</p>`,
      "byok"
    );
  } catch (err) {
    loadingMsg.remove();
    appendAssistantMessage(`<p><strong>Explanation Error:</strong> ${escapeHtml(err.message)}</p>`);
  }
}

// ---------------------------------------------------------------------------
// Civic Chat & Procedure Generation (Hybrid RAG)
// ---------------------------------------------------------------------------
function setupChat() {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const charCount = document.getElementById("charCount");

  input.addEventListener("input", () => {
    charCount.textContent = `${input.value.length}/2000`;
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    charCount.textContent = "0/2000";
    appendUserMessage(message);

    const loadingMsg = appendLoadingMessage("Searching official civic sources & validating groundedness...");

    try {
      const response = await queryNagarSetuChat(message, currentSessionId);
      loadingMsg.remove();
      renderChatResponse(response);
    } catch (err) {
      loadingMsg.remove();
      appendAssistantMessage(
        `<p><strong>Service Notice:</strong> Could not retrieve procedure: ${escapeHtml(err.message)}</p>
         <p>Check if the NagarSetu backend is reachable or switch to demo mode in Settings.</p>`
      );
    }
  });
}

function renderChatResponse(response) {
  // Check if response is out-of-scope refusal
  if (response.refusal) {
    let suggestionsHtml = "";
    if (response.suggestions && response.suggestions.length) {
      suggestionsHtml = `<p><strong>Suggested supported procedures:</strong></p><ul>` +
        response.suggestions.map((s) => `<li>${escapeHtml(s)}</li>`).join("") +
        `</ul>`;
    }
    appendAssistantMessage(
      `<div class="msg-badge badge-official">Official Scope Boundary</div>
       <p>${escapeHtml(response.assistant_message || "This query is outside verified civic procedures.")}</p>
       ${suggestionsHtml}`,
      "official"
    );
    return;
  }

  // Response with verified checklist
  if (response.checklist) {
    currentChecklist = response.checklist;
    renderChecklistView(response.checklist, response.sources || []);

    const stepsCount = response.checklist.steps.length;
    appendAssistantMessage(
      `<div class="msg-badge badge-official">Official Verified Checklist (${Math.round(response.checklist.confidence * 100)}% Grounded)</div>
       <p><strong>${escapeHtml(response.checklist.procedure_name)}</strong></p>
       <p>${escapeHtml(response.checklist.summary)}</p>
       <p><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; margin-right: 4px;"><path d="M20 6 9 17l-5-5"/></svg>Generated <strong>${stepsCount} actionable steps</strong> with official citations. View the step-by-step checklist in the <strong>Saved Checklist</strong> tab.</p>
       <button id="btnViewChecklistNow" class="btn btn-secondary" style="margin-top: 8px;">Open Checklist (${stepsCount} steps)</button>`,
      "official"
    );

    document.getElementById("btnViewChecklistNow")?.addEventListener("click", () => {
      activateView("checklist");
    });
  } else if (response.assistant_message) {
    appendAssistantMessage(`<p>${escapeHtml(response.assistant_message)}</p>`);
  }
}

function appendUserMessage(text) {
  const container = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = "msg msg-user";
  div.textContent = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function appendAssistantMessage(html, type = "") {
  const container = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = `msg msg-assistant ${type ? "msg-" + type : ""}`;
  div.innerHTML = html;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function appendLoadingMessage(text) {
  const container = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = "msg msg-assistant";
  div.innerHTML = `<div class="spinner"></div><p style="font-size: 12px; color: #64748b;">${text}</p>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

// ---------------------------------------------------------------------------
// On-Demand Page Analysis
// ---------------------------------------------------------------------------
function setupPageAnalysis() {
  const btn = document.getElementById("btnTriggerAnalysis");
  btn.addEventListener("click", () => runPageAnalysis());
}

async function runPageAnalysis() {
  const loading = document.getElementById("analysisLoading");
  const resultContainer = document.getElementById("analysisResult");
  const btn = document.getElementById("btnTriggerAnalysis");

  const config = await getBYOKConfig();
  if (!config.apiKey) {
    alert("Please configure your AI Provider key in Settings / BYOK first.");
    activateView("settings");
    return;
  }

  btn.disabled = true;
  loading.classList.remove("hidden");
  resultContainer.classList.add("hidden");

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab || !tab.id) throw new Error("No active browser tab found.");

    const pageData = await new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({ type: "EXTRACT_PAGE_CONTENT", tabId: tab.id }, (res) => {
        if (chrome.runtime.lastError) reject(chrome.runtime.lastError);
        else if (!res.ok) reject(new Error(res.error));
        else resolve(res.data);
      });
    });

    const analysisRes = await analyzePageContent({
      pageContent: pageData,
      providerConfig: config,
    });

    renderAnalysisResult(analysisRes.analysis, pageData);
  } catch (err) {
    resultContainer.innerHTML = `
      <div class="analysis-card" style="border-color: #fca5a5; background: #fff5f5;">
        <h4 style="color: #dc2626;">Analysis Error</h4>
        <p>${escapeHtml(err.message)}</p>
      </div>`;
    resultContainer.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
    btn.disabled = false;
  }
}

function renderAnalysisResult(analysis, pageData) {
  const container = document.getElementById("analysisResult");
  container.innerHTML = "";

  const summaryCard = document.createElement("div");
  summaryCard.className = "analysis-card";
  summaryCard.innerHTML = `
    <h4>🏛️ Civic Purpose & Department</h4>
    <p><strong>Department:</strong> ${escapeHtml(analysis.department || "Not specified")}</p>
    <p style="margin-top: 6px;">${escapeHtml(analysis.summary || "No summary available.")}</p>
  `;
  container.appendChild(summaryCard);

  if (analysis.keyRequirements && analysis.keyRequirements.length) {
    const reqCard = document.createElement("div");
    reqCard.className = "analysis-card";
    reqCard.innerHTML = `
      <h4><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; margin-right: 5px;"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M15 2H9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1Z"/><path d="m9 14 2 2 4-4"/></svg>Key Requirements Extracted</h4>
      <ul>${analysis.keyRequirements.map((r) => `<li>${escapeHtml(r)}</li>`).join("")}</ul>
    `;
    container.appendChild(reqCard);
  }

  if (analysis.deadlines && analysis.deadlines.length) {
    const dCard = document.createElement("div");
    dCard.className = "analysis-card";
    dCard.innerHTML = `
      <h4><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; margin-right: 5px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>Deadlines & Timeframes</h4>
      <ul>${analysis.deadlines.map((d) => `<li>${escapeHtml(d)}</li>`).join("")}</ul>
    `;
    container.appendChild(dCard);
  }

  if (analysis.ambiguities && analysis.ambiguities.length) {
    const ambCard = document.createElement("div");
    ambCard.className = "analysis-card";
    ambCard.innerHTML = `
      <h4><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; margin-right: 5px;"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>Ambiguities / Unclear Points</h4>
      <ul>${analysis.ambiguities.map((a) => `<li>${escapeHtml(a)}</li>`).join("")}</ul>
    `;
    container.appendChild(ambCard);
  }

  container.classList.remove("hidden");
}

// ---------------------------------------------------------------------------
// Saved Checklist View & Step Toggling
// ---------------------------------------------------------------------------
async function renderChecklistView(checklist, sources = []) {
  const title = document.getElementById("checklistTitle");
  const sub = document.getElementById("checklistSubtitle");
  const progressBadge = document.getElementById("checklistProgressBadge");
  const listContainer = document.getElementById("checklistItemsList");

  title.textContent = checklist.procedure_name;
  sub.textContent = `${checklist.estimated_total_time || "Standard processing"} • ${checklist.estimated_total_cost || "₹0 fee"}`;
  listContainer.innerHTML = "";

  // Fetch initial progress from backend
  let completedSteps = [];
  try {
    const progressData = await fetchProcedureProgress(checklist.procedure_id, currentSessionId);
    completedSteps = progressData.completed_steps || [];
  } catch (err) {
    console.warn("Could not fetch remote progress:", err);
  }

  const total = checklist.steps.length;
  updateProgressBadge(completedSteps.length, total);

  checklist.steps.forEach((step) => {
    const isCompleted = completedSteps.includes(step.step_number);
    const card = document.createElement("div");
    card.className = `step-card ${isCompleted ? "completed" : ""}`;
    card.id = `step-card-${step.step_number}`;

    const stepSource = sources.find((s) => step.source_chunk_ids && step.source_chunk_ids.includes(s.chunk_id));

    card.innerHTML = `
      <div class="step-header">
        <input
          type="checkbox"
          class="step-checkbox"
          id="cb-step-${step.step_number}"
          ${isCompleted ? "checked" : ""}
        />
        <label for="cb-step-${step.step_number}" class="step-title">
          ${step.step_number}. ${escapeHtml(step.title)}
        </label>
      </div>
      <p class="step-desc">${escapeHtml(step.description)}</p>
      <div class="step-meta">
        <span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 3px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>${escapeHtml(step.processing_time || "N/A")}</span>
        <span><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 3px;"><path d="M6 3h12"/><path d="M6 8h12"/><path d="m6 13 8.5 8"/><path d="M6 13h3a4 4 0 0 0 0-8"/></svg>${escapeHtml(step.fee || "₹0")}</span>
        ${stepSource ? `<span title="Official verified source"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 3px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>Verified Source</span>` : ""}
      </div>
    `;

    const checkbox = card.querySelector(".step-checkbox");
    checkbox.addEventListener("change", async () => {
      const checked = checkbox.checked;
      card.classList.toggle("completed", checked);

      if (checked) {
        if (!completedSteps.includes(step.step_number)) completedSteps.push(step.step_number);
      } else {
        completedSteps = completedSteps.filter((n) => n !== step.step_number);
      }

      updateProgressBadge(completedSteps.length, total);

      // Persist to backend
      try {
        await updateProcedureProgress({
          sessionId: currentSessionId,
          procedureId: checklist.procedure_id,
          stepNumber: step.step_number,
          completed: checked,
        });
      } catch (err) {
        console.error("Progress save error:", err);
      }
    });

    listContainer.appendChild(card);
  });
}

function updateProgressBadge(completed, total) {
  const badge = document.getElementById("checklistProgressBadge");
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  badge.textContent = `${pct}%`;
}

// ---------------------------------------------------------------------------
// Settings & BYOK
// ---------------------------------------------------------------------------
function setupSettings() {
  const selectProvider = document.getElementById("selectProvider");
  const inputApiKey = document.getElementById("inputApiKey");
  const selectModel = document.getElementById("selectModel");
  const inputBackendUrl = document.getElementById("inputBackendUrl");
  const inputAuthToken = document.getElementById("inputAuthToken");
  const form = document.getElementById("settingsForm");
  const btnTest = document.getElementById("btnTestBYOK");
  const btnClear = document.getElementById("btnClearCredentials");
  const feedback = document.getElementById("settingsFeedback");
  const docsLink = document.getElementById("providerDocsLink");

  // Load existing settings
  chrome.storage.local.get(
    ["byok_provider", "byok_key", "byok_model", "backendUrl", "authToken"],
    (data) => {
      if (data.byok_provider) selectProvider.value = data.byok_provider;
      if (data.byok_key) inputApiKey.value = data.byok_key;
      if (data.backendUrl) inputBackendUrl.value = data.backendUrl;
      if (data.authToken) inputAuthToken.value = data.authToken;
      populateModels(selectProvider.value, data.byok_model);
      updateDocsLink();
    }
  );

  selectProvider.addEventListener("change", () => {
    populateModels(selectProvider.value);
    updateDocsLink();
  });

  function updateDocsLink() {
    const p = PROVIDERS[selectProvider.value];
    if (p && docsLink) {
      docsLink.href = p.docsUrl;
      docsLink.textContent = `Get a ${p.name} API key →`;
    }
  }

  function populateModels(providerId, selectedModel) {
    selectModel.innerHTML = "";
    const p = PROVIDERS[providerId] || PROVIDERS.groq;
    p.models.forEach((m) => {
      const opt = document.createElement("option");
      opt.value = m;
      opt.textContent = m;
      if (m === selectedModel || m === p.defaultModel) opt.selected = true;
      selectModel.appendChild(opt);
    });
  }

  // Save Settings
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await chrome.storage.local.set({
      byok_provider: selectProvider.value,
      byok_key: inputApiKey.value.trim(),
      byok_model: selectModel.value,
      backendUrl: inputBackendUrl.value.trim(),
      authToken: inputAuthToken.value.trim(),
    });
    showFeedback("Settings saved successfully!", "success");
    initializeState();
  });

  // Test BYOK Connection
  btnTest.addEventListener("click", async () => {
    const key = inputApiKey.value.trim();
    if (!key) {
      showFeedback("Please enter an API key first.", "error");
      return;
    }

    showFeedback("Testing connection with provider...", "neutral");
    try {
      const testRes = await executeBYOKCompletion({
        provider: selectProvider.value,
        apiKey: key,
        model: selectModel.value,
        systemPrompt: "You are a test assistant.",
        userPrompt: "Respond with the word 'READY' only.",
      });

      if (testRes.includes("READY")) {
        showFeedback("✅ Connection successful! Provider responded.", "success");
      } else {
        showFeedback(`✅ Connected, received: ${testRes.slice(0, 50)}`, "success");
      }
    } catch (err) {
      showFeedback(`❌ Connection failed: ${err.message}`, "error");
    }
  });

  // Clear credentials
  btnClear.addEventListener("click", async () => {
    inputApiKey.value = "";
    inputAuthToken.value = "";
    await chrome.storage.local.remove(["byok_key", "authToken"]);
    showFeedback("Credentials removed from browser storage.", "success");
  });

  function showFeedback(msg, type) {
    feedback.textContent = msg;
    feedback.className = `feedback-banner feedback-${type}`;
    feedback.classList.remove("hidden");
    setTimeout(() => feedback.classList.add("hidden"), 5000);
  }
}

async function getBYOKConfig() {
  const data = await chrome.storage.local.get(["byok_provider", "byok_key", "byok_model"]);
  return {
    provider: data.byok_provider || "groq",
    apiKey: data.byok_key || "",
    model: data.byok_model || "",
  };
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
