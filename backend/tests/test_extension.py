import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXT_DIR = REPO_ROOT / "extension"


def test_manifest_structure_and_permissions():
    manifest_path = EXT_DIR / "manifest.json"
    assert manifest_path.exists(), "manifest.json must exist in extension directory"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_version"] == 3
    assert manifest["name"] == "NagarSetu Civic Companion"
    assert "side_panel" in manifest
    assert "background" in manifest

    required_permissions = {"sidePanel", "storage", "activeTab", "contextMenus", "scripting"}
    assert required_permissions.issubset(set(manifest["permissions"]))

    # Ensure CSP does not allow remote script execution
    csp = manifest.get("content_security_policy", {}).get("extension_pages", "")
    assert "script-src 'self'" in csp
    assert "unsafe-eval" not in csp


def test_extension_file_integrity():
    required_files = [
        EXT_DIR / "manifest.json",
        EXT_DIR / "background.js",
        EXT_DIR / "lib" / "providers.js",
        EXT_DIR / "lib" / "api.js",
        EXT_DIR / "lib" / "router.js",
        EXT_DIR / "popup" / "popup.html",
        EXT_DIR / "popup" / "popup.js",
        EXT_DIR / "popup" / "popup.css",
        EXT_DIR / "sidepanel" / "sidepanel.html",
        EXT_DIR / "sidepanel" / "sidepanel.js",
        EXT_DIR / "sidepanel" / "sidepanel.css",
        EXT_DIR / "icons" / "icon16.png",
        EXT_DIR / "icons" / "icon48.png",
        EXT_DIR / "icons" / "icon128.png",
    ]

    for f in required_files:
        assert f.exists() and f.stat().st_size > 0, f"Missing or empty extension file: {f}"


def test_router_prompt_guardrails():
    router_code = (EXT_DIR / "lib" / "router.js").read_text(encoding="utf-8")
    # Verify prompt guardrails against hallucinations
    assert "Do not invent any facts" in router_code or "Do not invent" in router_code
    assert "not official legal counsel" in router_code
