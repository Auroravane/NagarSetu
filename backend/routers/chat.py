"""
NagarSetu — POST /api/chat router per AGENTS.md §7.

Flow: validate → retrieve (hybrid RRF) → prompt → LLM (fallback chain)
→ verify groundedness → Pydantic-validate §6.2 → respond.
On LLM failure: 503 + Demo Mode cached response with X-Demo-Mode: true.
"""

import json
import logging
from pathlib import Path
from backend.rag.scope import evaluate_scope

from fastapi import APIRouter, HTTPException, Request, Response

from backend.llm.client import generate
from backend.llm.prompts import build_system_prompt, build_user_prompt
from backend.models.schemas import (
    ChatRequest,
    ChatResponse,
    Checklist,
    SourceRef,
)
from backend.rag.retrieve import retrieve
from backend.rag.verify import verify

log = logging.getLogger("nagarsetu.chat")

router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEMO_DIR = REPO_ROOT / "frontend" / "public" / "demo"


def _demo_response(procedure_id: str) -> dict:
    """Load a cached demo checklist per §11. Raises 503 if none exists."""
    demo_path = DEMO_DIR / f"{procedure_id}.json"
    if not demo_path.exists():
        raise HTTPException(
            status_code=503,
            detail="LLM unavailable and no demo cache for this procedure.",
        )
    return json.loads(demo_path.read_text(encoding="utf-8"))


# Load procedure index mapping keywords to procedure IDs
_PROCEDURE_KEYWORD_MAP: dict[str, str] = {}
try:
    _meta_file = REPO_ROOT / "data" / "index" / "chunks_meta.json"
    if _meta_file.exists():
        with open(_meta_file, encoding="utf-8") as _f:
            _meta = json.load(_f)
            for _c in _meta.values():
                _pid = _c.get("procedure_id")
                _pname = (_c.get("procedure_name") or "").lower()
                if _pid and _pname:
                    # Map slug words and title words
                    _PROCEDURE_KEYWORD_MAP[_pid.replace("_", " ")] = _pid
                    for _word in _pname.split():
                        if len(_word) > 4:
                            _PROCEDURE_KEYWORD_MAP[_word] = _pid
except Exception:
    pass

def _detect_procedure(message: str) -> str | None:
    """Keyword routing to a procedure_id for retrieval filtering."""
    m = message.lower()
    
    # Priority matches for primary services
    if "fssai" in m or "food license" in m or "food registration" in m:
        return "fssai_food_license"
    if "birth" in m and "certificate" in m:
        return "birth_certificate_registration"
    if "death" in m and "certificate" in m:
        return "death_certificate_issuance"
    if "marriage" in m:
        return "marriage_registration_certificate"
    if "caste" in m:
        return "caste_category_certificate_sc_st_obc"
    if "income certificate" in m:
        return "income_certificate_annual"
    if "domicile" in m or "residence certificate" in m:
        return "residence_domicile_certificate"
    if "learner" in m or ("license" in m and "driving" in m) or "dl" in m:
        return "learners_driving_license_sarathi"
    if "hsrp" in m or "number plate" in m:
        return "high_security_registration_plate_hsrp"
    if "shop" in m or "trade" in m:
        return "chandigarh_trade_license"
    if "water connection" in m or "new water" in m or ("water" in m and "meter" not in m):
        return "water_connection"
    if "property tax" in m or "house tax" in m:
        return "property_tax"
    if "senior citizen" in m:
        return "senior_citizen_identity_card"
    if "disability" in m or "udid" in m:
        return "unique_disability_id_udid"
    if "ration" in m and "card" in m:
        return "ration_card_new_application"
    if "solar" in m:
        return "rooftop_solar_net_metering"
    if "aadhaar" in m:
        return "e_aadhaar_demographic_biometric_update"
    if "pension" in m and "old" in m:
        return "old_age_pension_scheme"
    if "pension" in m and "widow" in m:
        return "widow_destitute_women_pension"
    if "ayushman" in m or "pmjay" in m:
        return "ayushman_bharat_pmjay_health_card"
        
    # Check dynamic mapping
    for phrase, pid in _PROCEDURE_KEYWORD_MAP.items():
        if phrase in m:
            return pid

    return None


from backend.routers.rate_limit import chat_limiter


@router.post("/api/chat", response_model=None)
def chat(req: ChatRequest, request: Request, response: Response):
    # Enforce request rate limiting
    chat_limiter.check(request)

    # 1. Retrieve (hybrid per §8.4)
    procedure_id = _detect_procedure(req.message)
    try:
        chunks = retrieve(req.message, procedure_id=procedure_id, k=8)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    # 1.5 Scope gate (Task 2): refuse out-of-scope queries BEFORE
    # generation. Supersedes the old 503-on-empty-chunks behavior —
    # refusals are 200 OK with a structured body, never errors.
    scope_result = evaluate_scope(req.message, procedure_id, chunks)
    if scope_result:
        return scope_result

    # 2. Generate (Groq → Gemini → demo per §9.4)
    valid_ids = list(dict.fromkeys(c.procedure_id for c in chunks))  # order-preserving unique
    system = build_system_prompt(req.language, valid_procedure_ids=valid_ids)
    user_prompt = build_user_prompt(req.message, chunks)
    try:
        checklist_dict = generate(user_prompt, system)
    except RuntimeError as e:
        # All providers failed → Demo Mode per §7 / §11
        demo_pid = procedure_id or "chandigarh_trade_license"
        checklist_dict = _demo_response(demo_pid)
        response.headers["X-Demo-Mode"] = "true"

    # 3. Verify groundedness (§8.5)
    checklist_dict = verify(checklist_dict, chunks)

    # 4. Strict §6.2 validation — reject malformed LLM output
    try:
        checklist = Checklist.model_validate(checklist_dict)
    except Exception as e:
        log.error("LLM output failed §6.2 validation: %s", e)
        raise HTTPException(
            status_code=503,
            detail="LLM returned an invalid checklist. Retry or use Demo Mode.",
        )

    # 5. Assemble response per §7 with Phase Three evidence metadata
    # Ensure all step citation chunk IDs are in sources for rich popovers
    chunk_map = {c.chunk_id: c for c in chunks}
    try:
        from backend.rag.retrieve import _get_chunk_meta, _to_chunk
        meta = _get_chunk_meta()
        for step in checklist.steps:
            for cid in step.source_chunk_ids:
                if cid not in chunk_map and cid in meta:
                    extra_c = _to_chunk(cid, meta[cid].get("text", ""), {})
                    chunk_map[cid] = extra_c
    except Exception:
        pass

    sources = [
        SourceRef(
            chunk_id=c.chunk_id,
            source_url=c.source_url,
            snippet=c.text[:200],
            title=c.section_title or c.procedure_name,
            department=c.department,
            jurisdiction=c.jurisdiction,
            last_verified=c.last_verified,
        )
        for c in chunk_map.values()
    ]
    low_confidence = checklist.confidence < 0.6

    return ChatResponse(
        assistant_message=(
            f"Here's the complete process for {checklist.procedure_name.lower()}."
        ),
        checklist=checklist,
        sources=sources,
        low_confidence=low_confidence,
    )