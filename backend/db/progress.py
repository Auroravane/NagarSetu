"""
NagarSetu — Persistent storage and verified progress management.

Supports both PostgreSQL (via DATABASE_URL on Antideploy) and SQLite fallback.
Binds progress tracking to authenticated user IDs or an isolated, validated demo identity.
Enforces procedure validity and step bounds per procedure.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
from typing import Generator, Optional, Tuple, Any

try:
    import psycopg
    from psycopg.rows import dict_row
    HAS_PSYCOPG = True
except ImportError:
    HAS_PSYCOPG = False

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Supported procedure registry with step limits
SUPPORTED_PROCEDURES = {
    "chandigarh_trade_license": {
        "name": "Trade License — Chandigarh Municipal Corporation",
        "max_steps": 8,
    },
    "water_connection": {
        "name": "New Water Connection — Punjab / Chandigarh",
        "max_steps": 8,
    },
    "property_tax": {
        "name": "Property Tax Payment — Chandigarh Municipal Corporation",
        "max_steps": 7,
    },
}

DEMO_PRINCIPAL_PREFIX = "demo-sess-"

PG_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  language TEXT DEFAULT 'en'
);

CREATE TABLE IF NOT EXISTS progress (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
  procedure_id TEXT NOT NULL,
  step_number INTEGER NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  completed_at TIMESTAMP WITH TIME ZONE,
  UNIQUE(session_id, procedure_id, step_number)
);

CREATE TABLE IF NOT EXISTS saved_procedures (
  id TEXT PRIMARY KEY,
  principal_id TEXT NOT NULL,
  procedure_id TEXT NOT NULL,
  procedure_name TEXT NOT NULL,
  jurisdiction TEXT DEFAULT 'Chandigarh',
  status TEXT DEFAULT 'in_progress',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(principal_id, procedure_id)
);

CREATE INDEX IF NOT EXISTS idx_progress_lookup 
  ON progress(session_id, procedure_id);

CREATE INDEX IF NOT EXISTS idx_saved_procedures_lookup
  ON saved_procedures(principal_id);
"""

SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  language TEXT DEFAULT 'en'
);

CREATE TABLE IF NOT EXISTS progress (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  procedure_id TEXT NOT NULL,
  step_number INTEGER NOT NULL,
  completed BOOLEAN DEFAULT 0,
  completed_at TIMESTAMP,
  UNIQUE(session_id, procedure_id, step_number),
  FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE IF NOT EXISTS saved_procedures (
  id TEXT PRIMARY KEY,
  principal_id TEXT NOT NULL,
  procedure_id TEXT NOT NULL,
  procedure_name TEXT NOT NULL,
  jurisdiction TEXT DEFAULT 'Chandigarh',
  status TEXT DEFAULT 'in_progress',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(principal_id, procedure_id)
);

CREATE INDEX IF NOT EXISTS idx_progress_lookup 
  ON progress(session_id, procedure_id);

CREATE INDEX IF NOT EXISTS idx_saved_procedures_lookup
  ON saved_procedures(principal_id);
"""


def _get_sqlite_path() -> Path:
    _env_db = os.getenv("SQLITE_PATH")
    if not _env_db:
        return (REPO_ROOT / "progress.db").resolve()
    _p = Path(_env_db)
    return _p.resolve() if _p.is_absolute() else (REPO_ROOT / _p).resolve()


DB_PATH = _get_sqlite_path()
_pg_initialized = False


def is_postgres() -> bool:
    return bool(os.getenv("DATABASE_URL") and HAS_PSYCOPG)


def _init_pg(conn: psycopg.Connection) -> None:
    global _pg_initialized
    if not _pg_initialized:
        with conn.cursor() as cur:
            cur.execute(PG_SCHEMA)
        conn.commit()
        _pg_initialized = True


def validate_procedure_and_step(procedure_id: str, step_number: int | None = None) -> None:
    """Validate that procedure_id is supported and step_number is within valid range."""
    if procedure_id not in SUPPORTED_PROCEDURES:
        raise ValueError(f"Unsupported procedure_id '{procedure_id}'.")
    if step_number is not None:
        max_steps = SUPPORTED_PROCEDURES[procedure_id]["max_steps"]
        if step_number < 1 or step_number > max_steps:
            raise ValueError(
                f"Invalid step_number {step_number} for procedure '{procedure_id}'. "
                f"Must be between 1 and {max_steps}."
            )


def _ensure_session_sqlite(session_id: str, language: str = "en") -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        conn.execute(
            "INSERT OR IGNORE INTO sessions (session_id, language) VALUES (?, ?)",
            (session_id, language),
        )


def ensure_session(session_id: str, language: str = "en") -> None:
    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sessions (session_id, language) 
                        VALUES (%s, %s)
                        ON CONFLICT (session_id) DO NOTHING
                        """,
                        (session_id, language),
                    )
                conn.commit()
            return
        except Exception:
            pass
    _ensure_session_sqlite(session_id, language)


def _upsert_progress_sqlite(principal_id: str, procedure_id: str, step_number: int, completed: bool) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        conn.execute(
            """
            INSERT INTO progress (session_id, procedure_id, step_number, completed, completed_at)
            VALUES (?, ?, ?, ?, CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE NULL END)
            ON CONFLICT(session_id, procedure_id, step_number)
            DO UPDATE SET completed = excluded.completed,
                          completed_at = excluded.completed_at
            """,
            (principal_id, procedure_id, step_number, completed, completed),
        )


def upsert_progress(
    principal_id: str,
    procedure_id: str,
    step_number: int,
    completed: bool,
) -> None:
    validate_procedure_and_step(procedure_id, step_number)
    ensure_session(principal_id)

    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO progress (session_id, procedure_id, step_number, completed, completed_at)
                        VALUES (%s, %s, %s, %s, CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE NULL END)
                        ON CONFLICT (session_id, procedure_id, step_number)
                        DO UPDATE SET completed = EXCLUDED.completed,
                                      completed_at = EXCLUDED.completed_at
                        """,
                        (principal_id, procedure_id, step_number, completed, completed),
                    )
                conn.commit()
            return
        except Exception:
            pass
    _upsert_progress_sqlite(principal_id, procedure_id, step_number, completed)


def get_progress(principal_id: str, procedure_id: str) -> tuple[list[int], int]:
    """Returns (completed_steps, total_steps) for the verified principal."""
    validate_procedure_and_step(procedure_id)

    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT step_number, completed FROM progress 
                        WHERE session_id = %s AND procedure_id = %s ORDER BY step_number ASC
                        """,
                        (principal_id, procedure_id),
                    )
                    rows = cur.fetchall()
            completed = [r[0] for r in rows if r[1]]
            configured_total = SUPPORTED_PROCEDURES[procedure_id]["max_steps"]
            return completed, configured_total
        except Exception:
            pass

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        rows = conn.execute(
            "SELECT step_number, completed FROM progress "
            "WHERE session_id = ? AND procedure_id = ? ORDER BY step_number ASC",
            (principal_id, procedure_id),
        ).fetchall()

    completed = [r[0] for r in rows if r[1]]
    configured_total = SUPPORTED_PROCEDURES[procedure_id]["max_steps"]
    return completed, configured_total


def save_procedure(
    principal_id: str,
    procedure_id: str,
    procedure_name: Optional[str] = None,
    jurisdiction: Optional[str] = "Chandigarh",
) -> dict:
    """Save or update a procedure for a verified principal."""
    validate_procedure_and_step(procedure_id)
    ensure_session(principal_id)

    name = procedure_name or SUPPORTED_PROCEDURES[procedure_id]["name"]
    proc_uuid = f"proc-{principal_id.replace(':', '-')}-{procedure_id}"
    now_iso = datetime.now(timezone.utc).isoformat()

    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO saved_procedures (id, principal_id, procedure_id, procedure_name, jurisdiction, updated_at)
                        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (principal_id, procedure_id)
                        DO UPDATE SET procedure_name = EXCLUDED.procedure_name,
                                      jurisdiction = EXCLUDED.jurisdiction,
                                      updated_at = CURRENT_TIMESTAMP
                        RETURNING id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at
                        """,
                        (proc_uuid, principal_id, procedure_id, name, jurisdiction or "Chandigarh"),
                    )
                    row = cur.fetchone()
                conn.commit()
                if row:
                    completed, total = get_progress(principal_id, procedure_id)
                    return {
                        "id": row[0],
                        "procedure_id": row[1],
                        "procedure_name": row[2],
                        "jurisdiction": row[3],
                        "status": row[4],
                        "completed_steps": completed,
                        "total_steps": total,
                        "created_at": str(row[5]),
                        "updated_at": str(row[6]),
                    }
        except Exception:
            pass

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        conn.execute(
            """
            INSERT INTO saved_procedures (id, principal_id, procedure_id, procedure_name, jurisdiction, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (principal_id, procedure_id)
            DO UPDATE SET procedure_name = excluded.procedure_name,
                          jurisdiction = excluded.jurisdiction,
                          updated_at = excluded.updated_at
            """,
            (proc_uuid, principal_id, procedure_id, name, jurisdiction or "Chandigarh", now_iso, now_iso),
        )
        row = conn.execute(
            "SELECT id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at "
            "FROM saved_procedures WHERE principal_id = ? AND procedure_id = ?",
            (principal_id, procedure_id),
        ).fetchone()

    completed, total = get_progress(principal_id, procedure_id)
    return {
        "id": row[0],
        "procedure_id": row[1],
        "procedure_name": row[2],
        "jurisdiction": row[3],
        "status": row[4],
        "completed_steps": completed,
        "total_steps": total,
        "created_at": str(row[5]),
        "updated_at": str(row[6]),
    }


def list_saved_procedures(principal_id: str) -> list[dict]:
    """List all saved procedures for a principal."""
    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at
                        FROM saved_procedures
                        WHERE principal_id = %s
                        ORDER BY updated_at DESC
                        """,
                        (principal_id,),
                    )
                    rows = cur.fetchall()
            results = []
            for r in rows:
                completed, total = get_progress(principal_id, r[1])
                results.append({
                    "id": r[0],
                    "procedure_id": r[1],
                    "procedure_name": r[2],
                    "jurisdiction": r[3],
                    "status": r[4],
                    "completed_steps": completed,
                    "total_steps": total,
                    "created_at": str(r[5]),
                    "updated_at": str(r[6]),
                })
            return results
        except Exception:
            pass

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        rows = conn.execute(
            "SELECT id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at "
            "FROM saved_procedures WHERE principal_id = ? ORDER BY updated_at DESC",
            (principal_id,),
        ).fetchall()

    results = []
    for r in rows:
        completed, total = get_progress(principal_id, r[1])
        results.append({
            "id": r[0],
            "procedure_id": r[1],
            "procedure_name": r[2],
            "jurisdiction": r[3],
            "status": r[4],
            "completed_steps": completed,
            "total_steps": total,
            "created_at": str(r[5]),
            "updated_at": str(r[6]),
        })
    return results


def get_saved_procedure(principal_id: str, procedure_id: str) -> Optional[dict]:
    """Retrieve single procedure for principal."""
    validate_procedure_and_step(procedure_id)
    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at
                        FROM saved_procedures
                        WHERE principal_id = %s AND (procedure_id = %s OR id = %s)
                        """,
                        (principal_id, procedure_id, procedure_id),
                    )
                    r = cur.fetchone()
            if r:
                completed, total = get_progress(principal_id, r[1])
                return {
                    "id": r[0],
                    "procedure_id": r[1],
                    "procedure_name": r[2],
                    "jurisdiction": r[3],
                    "status": r[4],
                    "completed_steps": completed,
                    "total_steps": total,
                    "created_at": str(r[5]),
                    "updated_at": str(r[6]),
                }
            return None
        except Exception:
            pass

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        r = conn.execute(
            "SELECT id, procedure_id, procedure_name, jurisdiction, status, created_at, updated_at "
            "FROM saved_procedures WHERE principal_id = ? AND (procedure_id = ? OR id = ?)",
            (principal_id, procedure_id, procedure_id),
        ).fetchone()

    if not r:
        return None
    completed, total = get_progress(principal_id, r[1])
    return {
        "id": r[0],
        "procedure_id": r[1],
        "procedure_name": r[2],
        "jurisdiction": r[3],
        "status": r[4],
        "completed_steps": completed,
        "total_steps": total,
        "created_at": str(r[5]),
        "updated_at": str(r[6]),
    }


def delete_saved_procedure(principal_id: str, procedure_id: str) -> bool:
    """Delete a saved procedure for principal."""
    if is_postgres():
        try:
            db_url = os.environ["DATABASE_URL"].strip("'\"")
            with psycopg.connect(db_url) as conn:
                _init_pg(conn)
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM saved_procedures WHERE principal_id = %s AND (procedure_id = %s OR id = %s)",
                        (principal_id, procedure_id, procedure_id),
                    )
                    deleted = cur.rowcount > 0
                conn.commit()
            return deleted
        except Exception:
            pass

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SQLITE_SCHEMA)
        cur = conn.execute(
            "DELETE FROM saved_procedures WHERE principal_id = ? AND (procedure_id = ? OR id = ?)",
            (principal_id, procedure_id, procedure_id),
        )
        return cur.rowcount > 0