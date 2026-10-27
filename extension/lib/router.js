/**
 * NagarSetu Extension — Intelligent Request Router.
 *
 * Categorizes and routes requests:
 * 1. General Browser Assistance (Explain selection, Simplify, Translate)
 *    -> User's configured BYOK provider (Groq / Gemini / OpenAI).
 *
 * 2. On-Demand Page Analysis
 *    -> Extracts structured summary, requirements, deadlines, and official links
 *       using BYOK provider with prompt guardrails.
 *
 * 3. Evidence-Grounded Civic Guidance (Procedures, Requirements, Checklists)
 *    -> NagarSetu Civic Platform API (Hybrid RAG + Source Provenance + Step Bounds).
 */

import { executeBYOKCompletion } from "./providers.js";
import { queryNagarSetuChat } from "./api.js";

export const TASK_TYPES = {
  EXPLAIN_SELECTION: "explain_selection",
  ANALYZE_PAGE: "analyze_page",
  CIVIC_PROCEDURE: "civic_procedure",
};

/**
 * Explains selected text in plain language using the user's BYOK provider.
 */
export async function explainSelectedText({ text, pageTitle, pageUrl, providerConfig }) {
  if (!text || !text.trim()) {
    throw new Error("No text provided to explain.");
  }

  const systemPrompt = `You are NagarSetu Civic Assistant. Your task is to explain complex government, civic, or legal text in simple, clear, citizen-friendly language.
Guidelines:
1. Explain what this text means for an ordinary citizen.
2. Highlight any actionable requirements or key definitions.
3. State clearly: "Note: This is an AI-generated explanation of the selected text, not official legal counsel."
4. Do not invent procedures or deadlines not mentioned in the text.`;

  const userPrompt = `Page: "${pageTitle}" (${pageUrl})
Selected Text:
"${text.slice(0, 3000)}"

Please explain this in plain language.`;

  const explanation = await executeBYOKCompletion({
    provider: providerConfig.provider,
    apiKey: providerConfig.apiKey,
    model: providerConfig.model,
    systemPrompt,
    userPrompt,
  });

  return {
    type: TASK_TYPES.EXPLAIN_SELECTION,
    mode: "byok",
    provider: providerConfig.provider,
    text: explanation,
    originalText: text,
    pageTitle,
    pageUrl,
  };
}

/**
 * Analyzes accessible page text on-demand to identify summary, requirements, deadlines, and ambiguities.
 */
export async function analyzePageContent({ pageContent, providerConfig }) {
  if (!pageContent || !pageContent.text || !pageContent.text.trim()) {
    throw new Error("No page text found to analyze.");
  }

  const systemPrompt = `You are NagarSetu Civic Assistant. You analyze government webpages to extract factual civic requirements without hallucination.
You MUST output valid JSON matching this schema:
{
  "summary": "2-3 sentence overview of what this page is for",
  "department": "Government body or department named on page, or 'Unknown'",
  "keyRequirements": ["list of eligibility or document requirements found on page"],
  "deadlines": ["explicit dates or filing windows stated on page"],
  "officialLinks": ["official action or portal links mentioned"],
  "ambiguities": ["missing details or unclear conditions"],
  "nextSteps": ["recommended next steps for citizen"]
}
Strict Rule: Only include requirements and deadlines explicitly stated on the page. Do not invent any facts.`;

  const userPrompt = `Page Title: ${pageContent.title}
Page URL: ${pageContent.url}
Page Headings: ${pageContent.headings}
Meta Description: ${pageContent.metaDescription}

Page Content:
${pageContent.text.slice(0, 5000)}

Analyze this page and output JSON:`;

  const rawJson = await executeBYOKCompletion({
    provider: providerConfig.provider,
    apiKey: providerConfig.apiKey,
    model: providerConfig.model,
    systemPrompt,
    userPrompt,
    jsonMode: true,
  });

  let parsed = null;
  try {
    parsed = JSON.parse(rawJson);
  } catch {
    const jsonMatch = rawJson.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      parsed = JSON.parse(jsonMatch[0]);
    } else {
      throw new Error("AI provider returned an unstructured response. Please retry.");
    }
  }

  return {
    type: TASK_TYPES.ANALYZE_PAGE,
    mode: "byok",
    provider: providerConfig.provider,
    analysis: parsed,
    pageTitle: pageContent.title,
    pageUrl: pageContent.url,
  };
}

/**
 * Routes evidence-grounded civic queries directly to the NagarSetu platform API.
 */
export async function consultCivicPlatform({ query, sessionId, language = "en" }) {
  const result = await queryNagarSetuChat(query, sessionId, language);
  return {
    type: TASK_TYPES.CIVIC_PROCEDURE,
    mode: "nagarsetu_platform",
    result,
  };
}
