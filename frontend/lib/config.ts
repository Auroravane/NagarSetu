/**
 * NagarSetu Unified Frontend Configuration.
 * 
 * Centralizes API URL resolution, environment detection, and request timeouts.
 * Guarantees consistent backend destination between auth, chat, and progress.
 */

function getResolvedApiUrl(): string {
  // If explicitly configured via environment variable (build time or runtime)
  if (process.env.NEXT_PUBLIC_API_URL !== undefined && process.env.NEXT_PUBLIC_API_URL.trim() !== "") {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/+$/, "");
  }

  // In browser: if served by Next.js or same-origin proxy, default to relative origin
  // If deployed on Vercel or Cloudflare Pages without NEXT_PUBLIC_API_URL set, default to Render backend
  if (typeof window !== "undefined") {
    const host = window.location.hostname;
    if (host.includes("pages.dev") || host.includes("vercel.app")) {
      return "https://nagarsetu-jco2.onrender.com";
    }
    // Local dev browser default if unset
    if (host === "localhost" || host === "127.0.0.1") {
      return "http://localhost:8000";
    }
    return "";
  }

  // Server-side default
  return "http://localhost:8000";
}

export const API_BASE_URL = getResolvedApiUrl();

export const IS_DEMO_MODE =
  process.env.NEXT_PUBLIC_DEMO_MODE === "true" ||
  (typeof window !== "undefined" &&
    new URLSearchParams(window.location.search).get("demo") === "true");

export const REQUEST_TIMEOUT_MS = 15000;
