# NagarSetu Chrome Extension — Browser Companion

The **NagarSetu Civic Companion** is a Manifest V3 Chrome Extension that brings evidence-grounded civic procedure navigation, on-demand webpage analysis, and Bring Your Own Key (BYOK) AI assistance directly into the citizen's browser while navigating government portals.

---

## 1. Architecture & Capabilities

```
┌─────────────────────────────────────────────────────────────┐
│                   Browser User Interface                    │
│   ┌───────────────────────────┐ ┌───────────────────────┐   │
│   │ Quick Popup (popup.html)  │ │ Side Panel (HTML/CSS) │   │
│   └─────────────┬─────────────┘ └───────────┬───────────┘   │
└─────────────────┼───────────────────────────┼───────────────┘
                  │                           │
                  ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│        Intelligent Request Router (lib/router.js)           │
│                                                             │
│   [General Page / Selection Task]    [Civic Procedure Task] │
│                  │                               │          │
│                  ▼                               ▼          │
│       BYOK Adapters (lib/providers.js)   NagarSetu API      │
│       • Groq (llama-3.3-70b)             (lib/api.js)       │
│       • Google Gemini (1.5-flash)        • Hybrid RAG       │
│       • OpenAI (gpt-4o-mini)             • BM25 + ChromaDB  │
│                                          • Groundedness     │
│                                          • Step Persistence │
└─────────────────────────────────────────────────────────────┘
```

### Core Features
1. **Side Panel Primary Interface:** Persistent multi-tab panel (`Civic Chat`, `Page Analysis`, `Saved Checklist`, `Settings / BYOK`).
2. **Explain Selected Text:** Right-click context menu or popup button to explain complex government notices in citizen-friendly language.
3. **On-Demand Page Analysis:** Safely parses DOM text from the active tab, extracts stated requirements, deadlines, and official links while ignoring forms and passwords.
4. **Official Civic Procedure Navigation:** Queries the NagarSetu backend (`/api/chat`) for verified municipal procedures (e.g. Trade License, Water Connection, Property Tax).
5. **Persistent Checklist Synchronization:** Supports ticking and resuming steps with real-time progress saved to the NagarSetu platform via cookie or Bearer session token.
6. **Bring Your Own Key (BYOK):** Keys are stored strictly in `chrome.storage.local` within the user's browser, never sent to NagarSetu servers.

---

## 2. Installation & Loading in Chrome

1. Open Google Chrome.
2. Navigate to `chrome://extensions/` in the address bar.
3. Enable **Developer mode** toggle in the top-right corner.
4. Click **Load unpacked**.
5. Select the `extension/` directory from this repository:
   ```
   c:\Users\Code66\.antigravity-ide\Persona\NagarSetu\NagarSetu\extension
   ```
6. The **NagarSetu Civic Companion** icon will appear in your Chrome toolbar.
7. Click the icon to open the Quick Popup or press `Ctrl+Shift+U` (`Command+Shift+U` on Mac) to open the Side Panel.

---

## 3. Configuration

### A. AI Provider (BYOK)
- Navigate to the **Settings / BYOK** tab in the side panel.
- Select your preferred provider (**Groq Cloud**, **Google Gemini**, or **OpenAI**).
- Paste your personal API key.
- Click **Test Connection** to verify your key.
- Click **Save Settings**.

### B. Backend API URL
- By default, requests connect to `https://nagarsetu-jco2.onrender.com`.
- For local development, change the URL to `http://localhost:8000`.

### C. Account Synchronization (Optional)
- Paste your session token in Settings or sign in to synchronize progress across devices.

---

## 4. Privacy & Security Safeguards

- **Least Privilege:** Manifest permissions are scoped strictly to `sidePanel`, `storage`, `activeTab`, `contextMenus`, and `scripting`.
- **Zero Background Scraping:** Scripts only execute when explicitly initiated by user actions (clicking Analyze or selecting text).
- **Prompt Injection Defense:** Page context is sanitized and bounded to 6,000 characters; system prompts strictly enforce zero-hallucination and require citation of facts explicitly present on page.
- **Credential Safety:** BYOK API keys remain local to the extension and are never logged or forwarded to external third parties.
