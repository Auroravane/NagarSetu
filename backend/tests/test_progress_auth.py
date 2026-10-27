"""
Tests for Progress Endpoint Authorization and Ownership Validation (AGENTS.md Phase 3).
"""

from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from backend.main import app
from backend.routers import auth
from backend.db import progress as db_progress


@pytest.fixture
def auth_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    test_db = tmp_path / "progress_auth_test.sqlite3"
    monkeypatch.setattr(auth, "DB_PATH", test_db)
    monkeypatch.setattr(db_progress, "DB_PATH", test_db)
    with TestClient(app) as client:
        yield client


def _register_user(client: TestClient, email: str, name: str) -> str:
    res = client.post(
        "/api/auth/register",
        json={
            "full_name": name,
            "email": email,
            "password": "Password123!",
            "address": "123 Civic St",
            "city": "Chandigarh",
            "state": "Chandigarh",
            "postal_code": "160017",
        },
    )
    assert res.status_code == 201
    cookie = client.cookies.get(auth.SESSION_COOKIE)
    assert cookie
    return cookie


def test_unauthenticated_access_without_demo_rejected(auth_client: TestClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEMO_MODE", "false")
    # No auth cookie, no valid demo session
    r = auth_client.get("/api/progress?procedure_id=chandigarh_trade_license")
    assert r.status_code == 401

    r_post = auth_client.post(
        "/api/progress",
        json={
            "session_id": "random-attacker-session",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 1,
            "completed": True,
        },
    )
    assert r_post.status_code == 401


def test_cross_user_isolation(auth_client: TestClient):
    # Register User A
    cookie_a = _register_user(auth_client, "user_a@test.com", "User Alpha")

    # User A completes Step 1 & 2
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_a)
    up1 = auth_client.post(
        "/api/progress",
        json={
            "session_id": "ignored_in_auth_mode",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 1,
            "completed": True,
        },
    )
    assert up1.status_code == 200

    up2 = auth_client.post(
        "/api/progress",
        json={
            "session_id": "ignored_in_auth_mode",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 2,
            "completed": True,
        },
    )
    assert up2.status_code == 200

    # User A checks their progress
    res_a = auth_client.get("/api/progress?procedure_id=chandigarh_trade_license")
    assert res_a.status_code == 200
    assert res_a.json()["completed_steps"] == [1, 2]

    # Register User B
    auth_client.cookies.clear()
    cookie_b = _register_user(auth_client, "user_b@test.com", "User Beta")
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_b)

    # User B checks progress — MUST be empty (cannot see User A's data)
    res_b = auth_client.get("/api/progress?procedure_id=chandigarh_trade_license")
    assert res_b.status_code == 200
    assert res_b.json()["completed_steps"] == []

    # User B cannot alter User A's progress even if supplying User A's identifier in body
    up_b = auth_client.post(
        "/api/progress",
        json={
            "session_id": "user_a_identifier",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 3,
            "completed": True,
        },
    )
    assert up_b.status_code == 200

    # Switch back to User A to verify User A was unaffected by User B's actions
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_a)
    check_a = auth_client.get("/api/progress?procedure_id=chandigarh_trade_license")
    assert check_a.json()["completed_steps"] == [1, 2]


def test_invalid_procedure_and_step_bounds(auth_client: TestClient):
    cookie = _register_user(auth_client, "bounds_user@test.com", "Bounds Tester")
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie)

    # Invalid procedure
    r_bad_proc = auth_client.post(
        "/api/progress",
        json={
            "session_id": "unused",
            "procedure_id": "fake_procedure_hack",
            "step_number": 1,
            "completed": True,
        },
    )
    assert r_bad_proc.status_code == 400
    assert "Unsupported procedure_id" in r_bad_proc.json()["detail"]

    # Invalid step number: negative or 0
    r_step_zero = auth_client.post(
        "/api/progress",
        json={
            "session_id": "unused",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 0,
            "completed": True,
        },
    )
    # Pydantic ge=1 triggers 422
    assert r_step_zero.status_code == 422

    # Invalid step number: exceeds max_steps (8 for trade license)
    r_step_high = auth_client.post(
        "/api/progress",
        json={
            "session_id": "unused",
            "procedure_id": "chandigarh_trade_license",
            "step_number": 99,
            "completed": True,
        },
    )
    assert r_step_high.status_code == 400
    assert "Invalid step_number 99" in r_step_high.json()["detail"]


def test_demo_session_isolation(auth_client: TestClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEMO_MODE", "true")
    auth_client.cookies.clear()

    # Demo session 1
    d1 = auth_client.post(
        "/api/progress",
        json={
            "session_id": "demo-sess-alpha-1234",
            "procedure_id": "water_connection",
            "step_number": 1,
            "completed": True,
        },
    )
    assert d1.status_code == 200

    r_d1 = auth_client.get("/api/progress?procedure_id=water_connection&session_id=demo-sess-alpha-1234")
    assert r_d1.status_code == 200
    assert r_d1.json()["completed_steps"] == [1]

    # Demo session 2 is isolated from Demo session 1
    r_d2 = auth_client.get("/api/progress?procedure_id=water_connection&session_id=demo-sess-beta-5678")
    assert r_d2.status_code == 200
    assert r_d2.json()["completed_steps"] == []


def test_saved_procedures_crud_and_ownership(auth_client: TestClient):
    cookie_a = _register_user(auth_client, "owner_a@test.com", "Owner Alpha")
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_a)

    # User A saves a procedure
    create_res = auth_client.post(
        "/api/procedures",
        json={
            "procedure_id": "chandigarh_trade_license",
            "procedure_name": "Trade License — Chandigarh Municipal Corporation",
            "jurisdiction": "Chandigarh",
        },
    )
    assert create_res.status_code == 200
    created_data = create_res.json()
    assert created_data["procedure_id"] == "chandigarh_trade_license"
    assert created_data["total_steps"] == 8

    # User A lists procedures
    list_res = auth_client.get("/api/procedures")
    assert list_res.status_code == 200
    items = list_res.json()["procedures"]
    assert len(items) == 1
    assert items[0]["procedure_id"] == "chandigarh_trade_license"

    # User A retrieves single procedure
    detail_res = auth_client.get("/api/procedures/chandigarh_trade_license")
    assert detail_res.status_code == 200
    assert detail_res.json()["procedure_id"] == "chandigarh_trade_license"

    # User B logs in and should NOT see User A's procedure
    auth_client.cookies.clear()
    cookie_b = _register_user(auth_client, "owner_b@test.com", "Owner Beta")
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_b)

    list_b = auth_client.get("/api/procedures")
    assert list_b.status_code == 200
    assert len(list_b.json()["procedures"]) == 0

    detail_b = auth_client.get("/api/procedures/chandigarh_trade_license")
    assert detail_b.status_code == 404

    # User B cannot delete User A's saved procedure
    del_b = auth_client.delete("/api/procedures/chandigarh_trade_license")
    assert del_b.status_code == 404

    # Switch back to User A to delete
    auth_client.cookies.set(auth.SESSION_COOKIE, cookie_a)
    del_a = auth_client.delete("/api/procedures/chandigarh_trade_license")
    assert del_a.status_code == 200
    assert del_a.json()["ok"] is True

    # Listing should now be empty
    list_after = auth_client.get("/api/procedures")
    assert len(list_after.json()["procedures"]) == 0


def test_bearer_token_saved_procedures(auth_client: TestClient):
    auth_client.cookies.clear()
    reg = auth_client.post(
        "/api/auth/register",
        json={
            "full_name": "Bearer Extension User",
            "email": "extension_bearer@test.com",
            "password": "Password123!",
            "address": "456 Civic Blvd",
            "city": "Chandigarh",
            "state": "Chandigarh",
            "postal_code": "160017",
        },
    )
    assert reg.status_code == 201
    token = reg.json()["token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}
    auth_client.cookies.clear()

    # Save procedure via Bearer token
    save_res = auth_client.post(
        "/api/procedures",
        headers=headers,
        json={
            "procedure_id": "water_connection",
            "procedure_name": "New Water Connection",
        },
    )
    assert save_res.status_code == 200
    assert save_res.json()["procedure_id"] == "water_connection"

    # Fetch list via Bearer token
    list_res = auth_client.get("/api/procedures", headers=headers)
    assert list_res.status_code == 200
    assert list_res.json()["count"] == 1

