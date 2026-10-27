"""NagarSetu — FastAPI application entrypoint."""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Make `backend.*` imports resolvable regardless of launch directory.
# MUST run before any backend.* imports below.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("nagarsetu")

# §15: missing keys → warn + Demo Mode
if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    log.warning("No LLM API keys found — setting DEMO_MODE=true (§15).")
    os.environ["DEMO_MODE"] = "true"

app = FastAPI(
    title="NagarSetu API",
    version="0.4.0",
    description="Civic procedure navigation — RAG-grounded, checklist-first.",
)

# Configurable CORS origins per AGENTS.md Phase 4
env_origins = os.getenv("CORS_ORIGINS", "")
if env_origins:
    origins = [o.strip() for o in env_origins.split(",") if o.strip()]
else:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://nagar-setu-iota.vercel.app",
        "https://nagarsetu.pages.dev",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^chrome-extension://[a-z]{32}$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
    expose_headers=["X-Demo-Mode"],
)

MAX_REQUEST_BYTES = 1_048_576  # 1 MB maximum payload


@app.middleware("http")
async def security_and_limit_middleware(request: Request, call_next):
    # Guard against oversized payloads causing memory exhaustion
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_BYTES:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=413,
            content={"detail": "Payload too large. Maximum allowed size is 1MB."},
        )

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.get("/health")
@app.get("/api/health")
def health() -> dict:
    """Liveness probe."""
    return {"ok": True}


@app.get("/ready")
@app.get("/api/ready")
def readiness() -> dict:
    """Readiness probe checking critical RAG and storage subsystems."""
    checks = {}
    ready = True

    # Check index artifacts
    from backend.rag.retrieve import BM25_PATH, CHROMA_PATH
    checks["bm25_index"] = BM25_PATH.exists() and BM25_PATH.is_file()
    checks["chroma_dir"] = CHROMA_PATH.exists() and CHROMA_PATH.is_dir()
    if not (checks["bm25_index"] and checks["chroma_dir"]):
        ready = False

    # Check database connectivity
    from backend.db.progress import is_postgres, DB_PATH
    if is_postgres():
        checks["database"] = "postgres"
    else:
        checks["database"] = "sqlite"
        checks["sqlite_ready"] = DB_PATH.parent.exists()

    # Check LLM provider availability
    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    gemini_configured = bool(os.getenv("GEMINI_API_KEY"))
    demo_mode = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")

    checks["llm_providers"] = {
        "groq": groq_configured,
        "gemini": gemini_configured,
        "demo_mode": demo_mode,
    }

    if not ready:
        from fastapi import status
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"ready": False, "checks": checks},
        )

    return {"ready": True, "checks": checks}


from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Routers — imported AFTER sys.path fix.
from backend.routers.auth import router as auth_router  # noqa: E402
from backend.routers.chat import router as chat_router  # noqa: E402
from backend.routers.progress import router as progress_router  # noqa: E402

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(progress_router)

# Mount frontend static export if built (enables single-application hosting on Antideploy)
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "out"
if FRONTEND_DIST.exists() and (FRONTEND_DIST / "index.html").exists():
    # Mount Next.js static asset directories (_next, demo, etc.)
    _next_dir = FRONTEND_DIST / "_next"
    if _next_dir.exists():
        app.mount("/_next", StaticFiles(directory=str(_next_dir)), name="_next")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API requests that didn't match to 404 naturally
        if full_path.startswith("api/"):
            return {"error": "Not Found", "path": full_path}

        requested_file = FRONTEND_DIST / full_path
        if requested_file.is_file():
            return FileResponse(requested_file)

        html_file = FRONTEND_DIST / f"{full_path}.html"
        if html_file.is_file():
            return FileResponse(html_file)

        index_fallback = FRONTEND_DIST / full_path / "index.html"
        if index_fallback.is_file():
            return FileResponse(index_fallback)

        return FileResponse(FRONTEND_DIST / "index.html")
