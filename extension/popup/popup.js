/**
 * NagarSetu Extension — Popup Controller.
 */

import { checkBackendHealth, getBackendBaseUrl } from "../lib/api.js";

document.addEventListener("DOMContentLoaded", async () => {
  const statusBadge = document.getElementById("statusBadge");
  const providerStatus = document.getElementById("providerStatus");
  const btnOpenSidepanel = document.getElementById("btnOpenSidepanel");
  const btnAnalyzePage = document.getElementById("btnAnalyzePage");
  const btnExplainSelection = document.getElementById("btnExplainSelection");
  const btnOpenWebApp = document.getElementById("btnOpenWebApp");
  const linkOpenSettings = document.getElementById("linkOpenSettings");

  // Check Backend status
  checkBackendHealth().then(({ healthy }) => {
    if (healthy) {
      statusBadge.textContent = "API Live";
      statusBadge.className = "status-pill status-online";
    } else {
      statusBadge.textContent = "Offline/Demo";
      statusBadge.className = "status-pill status-offline";
    }
  });

  // Check BYOK configuration
  const stored = await chrome.storage.local.get(["byok_provider", "byok_key"]);
  if (stored.byok_provider && stored.byok_key) {
    providerStatus.textContent = `BYOK: ${stored.byok_provider.toUpperCase()}`;
  } else {
    providerStatus.textContent = "BYOK: Not Configured";
  }

  // Open side panel
  btnOpenSidepanel.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      chrome.runtime.sendMessage({ type: "OPEN_SIDE_PANEL", tabId: tab.id });
      window.close();
    }
  });

  // Analyze page quick trigger
  btnAnalyzePage.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      await chrome.storage.local.set({
        pendingAction: {
          type: "analyze_page",
          tabId: tab.id,
          pageUrl: tab.url || "",
          pageTitle: tab.title || "",
          timestamp: Date.now(),
        },
      });
      chrome.runtime.sendMessage({ type: "OPEN_SIDE_PANEL", tabId: tab.id });
      window.close();
    }
  });

  // Explain selection quick trigger
  btnExplainSelection.addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      try {
        const [res] = await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: () => window.getSelection().toString(),
        });
        const selected = (res?.result || "").trim();
        if (!selected) {
          alert("Please select some text on the webpage first, then click Explain Selection.");
          return;
        }

        await chrome.storage.local.set({
          pendingAction: {
            type: "explain",
            text: selected,
            pageUrl: tab.url || "",
            pageTitle: tab.title || "",
            timestamp: Date.now(),
          },
        });
        chrome.runtime.sendMessage({ type: "OPEN_SIDE_PANEL", tabId: tab.id });
        window.close();
      } catch (err) {
        alert("Cannot read selection on this page: " + err.message);
      }
    }
  });

  // Open web application
  btnOpenWebApp.addEventListener("click", () => {
    chrome.tabs.create({ url: "https://nagarsetu.pages.dev" });
    window.close();
  });

  // Open settings in sidepanel
  linkOpenSettings.addEventListener("click", async (e) => {
    e.preventDefault();
    await chrome.storage.local.set({ openView: "settings" });
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.id) {
      chrome.runtime.sendMessage({ type: "OPEN_SIDE_PANEL", tabId: tab.id });
      window.close();
    }
  });
});
