/**
 * NagarSetu Extension — Background Service Worker (Manifest V3).
 *
 * Responsibilities:
 * - Handle side panel behavior and opening on action/command/context-menu.
 * - Manage context menus for text selection ("Explain with NagarSetu", "Check Civic Requirements").
 * - Coordinate active tab scripting to extract clean, accessible page context safely.
 */

// Enable side panel on action click behavior when supported
if (chrome.sidePanel && chrome.sidePanel.setPanelBehavior) {
  chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: false })
    .catch((err) => console.warn("SidePanel behavior note:", err));
}

// Setup context menus on installation
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "nagarsetu_explain_selection",
    title: "Explain selection with NagarSetu",
    contexts: ["selection"],
  });

  chrome.contextMenus.create({
    id: "nagarsetu_civic_check",
    title: "Check civic requirements for selection",
    contexts: ["selection"],
  });
});

// Handle Context Menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (!tab || !tab.id) return;

  const selectedText = (info.selectionText || "").trim();
  const actionType = info.menuItemId === "nagarsetu_civic_check" ? "civic_check" : "explain";

  // Store the pending selection task in chrome.storage.session or local so the side panel can pick it up
  await chrome.storage.local.set({
    pendingAction: {
      type: actionType,
      text: selectedText,
      pageUrl: tab.url || "",
      pageTitle: tab.title || "",
      timestamp: Date.now(),
    },
  });

  // Open the side panel for the active tab window
  if (chrome.sidePanel && chrome.sidePanel.open) {
    try {
      await chrome.sidePanel.open({ tabId: tab.id });
    } catch {
      try {
        await chrome.sidePanel.open({ windowId: tab.windowId });
      } catch (err) {
        console.warn("Could not open side panel directly:", err);
      }
    }
  }
});

// Handle keyboard command
chrome.commands.onCommand.addListener(async (command, tab) => {
  if (command === "open_side_panel" && tab && tab.id) {
    if (chrome.sidePanel && chrome.sidePanel.open) {
      try {
        await chrome.sidePanel.open({ tabId: tab.id });
      } catch {
        try {
          await chrome.sidePanel.open({ windowId: tab.windowId });
        } catch (e) {
          console.warn("Failed to open side panel via command:", e);
        }
      }
    }
  }
});

// Listen for message requests from popup or sidepanel
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "EXTRACT_PAGE_CONTENT") {
    handlePageExtraction(message.tabId)
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err.message }));
    return true; // Keep message channel open for async response
  }

  if (message.type === "OPEN_SIDE_PANEL") {
    const tabId = message.tabId || sender.tab?.id;
    if (chrome.sidePanel && chrome.sidePanel.open && tabId) {
      chrome.sidePanel.open({ tabId }).catch((err) => {
        console.warn("Side panel open error:", err);
      });
    }
    sendResponse({ ok: true });
    return false;
  }
});

/**
 * Extracts accessible text and metadata from the active tab.
 * Respects page boundaries, excludes scripts/styles, strips sensitive inputs.
 */
async function handlePageExtraction(targetTabId) {
  let tabId = targetTabId;
  if (!tabId) {
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!activeTab || !activeTab.id) throw new Error("No active tab found.");
    tabId = activeTab.id;
  }

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab?.url || "";

  // Guard against browser-internal or restricted URLs
  if (
    url.startsWith("chrome://") ||
    url.startsWith("chrome-extension://") ||
    url.startsWith("edge://") ||
    url.startsWith("about:") ||
    url.startsWith("view-source:")
  ) {
    throw new Error("Cannot analyze browser-internal or restricted system pages.");
  }

  const results = await chrome.scripting.executeScript({
    target: { tabId },
    func: () => {
      // Clean, sanitized text extraction inside document context
      const title = document.title || "";
      const url = window.location.href;

      // Extract main heading / meta description
      const metaDesc = document.querySelector('meta[name="description"]')?.getAttribute("content") || "";
      const h1Text = Array.from(document.querySelectorAll("h1")).map((h) => h.innerText.trim()).filter(Boolean).join(" | ");

      // Clone body to manipulate without breaking live DOM
      const clone = document.body.cloneNode(true);

      // Strip out scripts, styles, inputs, passwords, iframes, SVGs, noscripts
      const forbiddenTags = ["script", "style", "noscript", "svg", "iframe", "input", "textarea", "select", "form"];
      forbiddenTags.forEach((tag) => {
        clone.querySelectorAll(tag).forEach((el) => el.remove());
      });

      // Get readable text, truncate at 6000 characters to prevent excessive context
      let rawText = clone.innerText || clone.textContent || "";
      rawText = rawText.replace(/\s+/g, " ").trim();
      const truncatedText = rawText.slice(0, 6000);

      return {
        title,
        url,
        metaDescription: metaDesc,
        headings: h1Text,
        text: truncatedText,
        isTruncated: rawText.length > 6000,
      };
    },
  });

  if (!results || !results[0] || !results[0].result) {
    throw new Error("Failed to extract content from page.");
  }

  return results[0].result;
}
