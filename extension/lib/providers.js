/**
 * NagarSetu Extension — BYOK Provider Adapters
 *
 * Supports:
 * - Groq (llama-3.3-70b-versatile, openai/gpt-oss-120b)
 * - Google Gemini (gemini-1.5-flash, gemini-2.5-flash)
 * - OpenAI (gpt-4o-mini, gpt-4o)
 *
 * Normalizes request format, error messages, and cancellation.
 */

export const PROVIDERS = {
  groq: {
    id: "groq",
    name: "Groq Cloud",
    defaultModel: "llama-3.3-70b-versatile",
    models: ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    keyPlaceholder: "gsk_...",
    docsUrl: "https://console.groq.com/keys",
  },
  gemini: {
    id: "gemini",
    name: "Google Gemini",
    defaultModel: "gemini-1.5-flash",
    models: ["gemini-1.5-flash", "gemini-1.5-pro"],
    keyPlaceholder: "AIzaSy...",
    docsUrl: "https://aistudio.google.com/app/apikey",
  },
  openai: {
    id: "openai",
    name: "OpenAI",
    defaultModel: "gpt-4o-mini",
    models: ["gpt-4o-mini", "gpt-4o"],
    keyPlaceholder: "sk-...",
    docsUrl: "https://platform.openai.com/api-keys",
  },
};

/**
 * Execute an LLM completion using the user's BYOK credentials.
 */
export async function executeBYOKCompletion({
  provider,
  apiKey,
  model,
  systemPrompt,
  userPrompt,
  jsonMode = false,
  timeoutMs = 15000,
}) {
  if (!apiKey || !apiKey.trim()) {
    throw new Error(`API key for ${provider} is not configured.`);
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    if (provider === "groq") {
      return await callGroq({
        apiKey: apiKey.trim(),
        model: model || PROVIDERS.groq.defaultModel,
        systemPrompt,
        userPrompt,
        jsonMode,
        signal: controller.signal,
      });
    } else if (provider === "gemini") {
      return await callGemini({
        apiKey: apiKey.trim(),
        model: model || PROVIDERS.gemini.defaultModel,
        systemPrompt,
        userPrompt,
        jsonMode,
        signal: controller.signal,
      });
    } else if (provider === "openai") {
      return await callOpenAI({
        apiKey: apiKey.trim(),
        model: model || PROVIDERS.openai.defaultModel,
        systemPrompt,
        userPrompt,
        jsonMode,
        signal: controller.signal,
      });
    } else {
      throw new Error(`Unsupported provider: ${provider}`);
    }
  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error(`Request timed out after ${Math.round(timeoutMs / 1000)}s.`);
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

async function callGroq({ apiKey, model, systemPrompt, userPrompt, jsonMode, signal }) {
  const url = "https://api.groq.com/openai/v1/chat/completions";
  const body = {
    model,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature: 0.2,
  };
  if (jsonMode) {
    body.response_format = { type: "json_object" };
  }

  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
    signal,
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    const msg = errorJson.error?.message || `Groq request failed (${res.status})`;
    throw new Error(msg);
  }

  const data = await res.json();
  const content = data.choices?.[0]?.message?.content || "";
  return content;
}

async function callGemini({ apiKey, model, systemPrompt, userPrompt, jsonMode, signal }) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  const generationConfig = {
    temperature: 0.2,
  };
  if (jsonMode) {
    generationConfig.responseMimeType = "application/json";
  }

  const body = {
    system_instruction: {
      parts: [{ text: systemPrompt }],
    },
    contents: [
      {
        role: "user",
        parts: [{ text: userPrompt }],
      },
    ],
    generationConfig,
  };

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    const msg = errorJson.error?.message || `Gemini request failed (${res.status})`;
    throw new Error(msg);
  }

  const data = await res.json();
  const content = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
  return content;
}

async function callOpenAI({ apiKey, model, systemPrompt, userPrompt, jsonMode, signal }) {
  const url = "https://api.openai.com/v1/chat/completions";
  const body = {
    model,
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature: 0.2,
  };
  if (jsonMode) {
    body.response_format = { type: "json_object" };
  }

  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
    signal,
  });

  if (!res.ok) {
    const errorJson = await res.json().catch(() => ({}));
    const msg = errorJson.error?.message || `OpenAI request failed (${res.status})`;
    throw new Error(msg);
  }

  const data = await res.json();
  return data.choices?.[0]?.message?.content || "";
}
