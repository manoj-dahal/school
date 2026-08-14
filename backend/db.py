"""SQLite database for Shree Siddeshwor Secondary School."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "siddeshwor.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

ITERATIONS = 180_000


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
    return f"{salt}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS).hex()
    return hmac.compare_digest(check, digest)


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def get_db():
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row | None):
    if row is None:
        return None
    d = dict(row)
    for key in ("images", "items", "features"):
        if key in d and isinstance(d[key], str) and d[key]:
            try:
                d[key] = json.loads(d[key])
            except json.JSONDecodeError:
                pass
    return d


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'admin',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    date_bs TEXT NOT NULL,
    date_ad TEXT,
    excerpt TEXT NOT NULL,
    body TEXT NOT NULL,
    cover TEXT NOT NULL,
    images TEXT NOT NULL DEFAULT '[]',
    published INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    subject TEXT,
    department TEXT,
    level TEXT NOT NULL,
    image TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icon TEXT NOT NULL,
    title TEXT NOT NULL,
    short_desc TEXT NOT NULL,
    long_desc TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS academics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    tag TEXT NOT NULL,
    description TEXT NOT NULL,
    image TEXT NOT NULL,
    items TEXT NOT NULL DEFAULT '[]',
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    page_num INTEGER NOT NULL,
    image TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    alt TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'General',
    sort_order INTEGER NOT NULL DEFAULT 0,
    uploaded INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hero_slides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    alt TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    dob TEXT NOT NULL,
    grade TEXT NOT NULL,
    parentName TEXT NOT NULL,
    relationship TEXT NOT NULL,
    contact TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    previousSchool TEXT,
    additional TEXT,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL,
    notes TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    summary TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Parent',
    email TEXT,
    category TEXT NOT NULL DEFAULT 'General',
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL,
    phone TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    public INTEGER NOT NULL DEFAULT 0,
    anonymous INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status);
CREATE INDEX IF NOT EXISTS idx_suggestions_public ON suggestions(public, status);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status);
CREATE INDEX IF NOT EXISTS idx_news_published ON news(published);
CREATE INDEX IF NOT EXISTS idx_staff_department ON staff(department);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_created ON activity(created_at);
"""


SESSION_TTL_SECONDS = 60 * 60 * 12


def prune_sessions(conn=None, ttl: int = SESSION_TTL_SECONDS) -> int:
    cutoff = int(time.time()) - ttl
    if conn is not None:
        cur = conn.execute("DELETE FROM sessions WHERE created_at < ?", (cutoff,))
        return cur.rowcount
    with get_db() as owned:
        cur = owned.execute("DELETE FROM sessions WHERE created_at < ?", (cutoff,))
        return cur.rowcount


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)
        cols = [r[1] for r in conn.execute("PRAGMA table_info(applications)")]
        if "notes" not in cols:
            conn.execute("ALTER TABLE applications ADD COLUMN notes TEXT DEFAULT ''")
        scols = [r[1] for r in conn.execute("PRAGMA table_info(suggestions)")]
        if "phone" not in scols:
            conn.execute("ALTER TABLE suggestions ADD COLUMN phone TEXT DEFAULT ''")
        if "notes" not in scols:
            conn.execute("ALTER TABLE suggestions ADD COLUMN notes TEXT DEFAULT ''")
        if "public" not in scols:
            conn.execute("ALTER TABLE suggestions ADD COLUMN public INTEGER NOT NULL DEFAULT 0")
        if "anonymous" not in scols:
            conn.execute("ALTER TABLE suggestions ADD COLUMN anonymous INTEGER NOT NULL DEFAULT 0")
        gcols = [r[1] for r in conn.execute("PRAGMA table_info(gallery)")]
        if "uploaded" not in gcols:
            conn.execute("ALTER TABLE gallery ADD COLUMN uploaded INTEGER NOT NULL DEFAULT 0")
        prune_sessions(conn)
        conn.execute(
            """UPDATE suggestions SET notes = 'Recorded by the school office.'
               WHERE status = 'done' AND (notes IS NULL OR trim(notes) = '')"""
        )
        n = conn.execute("SELECT COUNT(*) FROM suggestions WHERE public = 1").fetchone()[0]
        if n == 0:
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            samples = [
                ("A parent", "Parent", "Facilities", "Drinking-water station near the junior block.", "done", "Installed near the junior block."),
                ("A student", "Student", "Academics", "Saturday reading club for Grade 4–6.", "reviewing", "Discuss at next staff meeting."),
                ("A teacher", "Staff", "General", "Publish the weekly routine as a downloadable PDF.", "done", "Added to the notice board."),
            ]
            for name, role, cat, msg, status, notes in samples:
                conn.execute(
                    """INSERT INTO suggestions (name, role, email, category, message, status, created_at, public, anonymous, notes)
                       VALUES (?,?,?,?,?,?,?,1,1,?)""",
                    (name, role, "", cat, msg, status, now, notes),
                )
