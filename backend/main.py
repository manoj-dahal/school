"""
Shree Siddeshwor Secondary School — backend API + static frontend.

Public API matches the live site:
  POST /api/apply
  POST /api/contact

Plus a full REST layer and admin dashboard.
"""
from __future__ import annotations

import json
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from db import get_db, init_db, prune_sessions, row_to_dict, verify_password
from seed import seed

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ADMIN = ROOT / "admin"
UPLOADS_DIR = ROOT / "data" / "uploads"
SESSION_TTL = 60 * 60 * 12  # 12 hours

MAX_UPLOAD_BYTES = 8 * 1024 * 1024  # 8 MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
IMAGE_MAGIC = {
    ".jpg": (b"\xff\xd8\xff",),
    ".jpeg": (b"\xff\xd8\xff",),
    ".png": (b"\x89PNG\r\n\x1a\n",),
    ".webp": (b"RIFF",),  # plus WEBP at offset 8
    ".gif": (b"GIF87a", b"GIF89a"),
}

app = FastAPI(
    title="Siddeshwor School API",
    description="Backend for Shree Siddeshwor Secondary School — cloned from siddeshwor.edu.np",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    seed(reset=False)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_all(sql: str, params: tuple = ()):
    with get_db() as conn:
        return [row_to_dict(r) for r in conn.execute(sql, params).fetchall()]


def fetch_one(sql: str, params: tuple = ()):
    with get_db() as conn:
        return row_to_dict(conn.execute(sql, params).fetchone())


# ---------------------------------------------------------------------------
# Upload helpers (gallery photos + notice pages)
# ---------------------------------------------------------------------------
def validate_image(filename: str, content_type: str | None, data: bytes) -> str:
    ext = Path(filename or "").suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTS:
        raise HTTPException(400, "Only JPEG, PNG, WebP and GIF images are allowed")
    if content_type and content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Only JPEG, PNG, WebP and GIF images are allowed")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(400, "Image is too large (8 MB maximum)")
    magic_ok = False
    for magic in IMAGE_MAGIC[ext]:
        if data[: len(magic)] == magic:
            magic_ok = True
            break
    if ext == ".webp" and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        magic_ok = True
    if not magic_ok:
        raise HTTPException(400, "File content does not match the image type")
    return ext


def save_upload(data: bytes, ext: str, prefix: str = "") -> str:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    name = f"{prefix}{secrets.token_hex(8)}{ext}"
    (UPLOADS_DIR / name).write_bytes(data)
    return name


def upload_path_of(url: str) -> Path | None:
    """Map a stored '/uploads/<name>' URL to its file on disk, or None."""
    url = (url or "").strip()
    if not url.startswith("/uploads/"):
        return None
    name = url[len("/uploads/"):]
    if not name or "/" in name or "\\" in name or name in {".", ".."}:
        return None
    target = (UPLOADS_DIR / name).resolve()
    try:
        target.relative_to(UPLOADS_DIR.resolve())
    except ValueError:
        return None
    return target


def delete_upload_file(url: str) -> bool:
    target = upload_path_of(url)
    if target and target.is_file():
        target.unlink()
        return True
    return False


async def read_upload(file: UploadFile) -> tuple[str, bytes]:
    """Validate an uploaded image and return (extension, content)."""
    data = await file.read()
    ext = validate_image(file.filename or "", file.content_type, data)
    return ext, data


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
class LoginIn(BaseModel):
    username: str
    password: str


def current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Not authenticated")
    token = authorization.split(" ", 1)[1].strip()
    row = fetch_one(
        """SELECT s.token, s.created_at, u.id, u.username, u.name, u.role
           FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ?""",
        (token,),
    )
    if not row or time.time() - row["created_at"] > SESSION_TTL:
        raise HTTPException(401, "Session expired")
    return row


# ---------------------------------------------------------------------------
# Public models (match live site field names)
# ---------------------------------------------------------------------------
class ApplyIn(BaseModel):
    firstName: str
    lastName: str
    dob: str
    grade: str
    parentName: str
    relationship: str
    contact: str
    email: str
    address: str
    previousSchool: str | None = ""
    additional: str | None = ""


class ContactIn(BaseModel):
    name: str
    email: str
    phone: str | None = ""
    message: str


class SubscribeIn(BaseModel):
    email: str


class SuggestIn(BaseModel):
    name: str | None = ""
    role: str | None = "Parent"
    email: str | None = ""
    phone: str | None = ""
    category: str | None = "General"
    message: str
    anonymous: int | None = 0


# ---------------------------------------------------------------------------
# Public API — same paths as siddeshwor.edu.np
# ---------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {"ok": True, "school": "Shree Siddeshwor Secondary School", "time": now_iso()}


@app.get("/api/school")
def school_info():
    rows = fetch_all("SELECT key, value FROM settings")
    return {r["key"]: r["value"] for r in rows}


@app.get("/api/hero")
def hero():
    return fetch_all("SELECT * FROM hero_slides ORDER BY sort_order")


@app.get("/api/news")
def list_news():
    return fetch_all(
        "SELECT id, slug, title, date_bs, date_ad, excerpt, cover, created_at FROM news WHERE published = 1 ORDER BY id DESC"
    )


@app.get("/api/news/{slug}")
def get_news(slug: str):
    item = fetch_one("SELECT * FROM news WHERE slug = ? AND published = 1", (slug,))
    if not item:
        raise HTTPException(404, "News not found")
    return item


@app.get("/api/staff")
def list_staff(department: str | None = None):
    if department:
        return fetch_all("SELECT * FROM staff WHERE department = ? ORDER BY sort_order", (department,))
    return fetch_all("SELECT * FROM staff ORDER BY sort_order")


@app.get("/api/facilities")
def list_facilities():
    return fetch_all("SELECT * FROM facilities ORDER BY sort_order")


@app.get("/api/academics")
def list_academics():
    return fetch_all("SELECT * FROM academics ORDER BY sort_order")


@app.get("/api/notices")
def list_notices():
    return fetch_all("SELECT * FROM notices ORDER BY page_num, sort_order, id")


@app.post("/api/apply")
async def apply(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    required_keys = [
        "firstName", "lastName", "dob", "grade",
        "parentName", "relationship", "contact", "email", "address",
    ]
    if not all(str(data.get(k) or "").strip() for k in required_keys):
        return JSONResponse({"error": "Missing required fields"}, status_code=400)
    payload = ApplyIn(**{**{k: "" for k in required_keys}, **data})
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO applications
               (firstName, lastName, dob, grade, parentName, relationship, contact, email, address, previousSchool, additional, status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,'new',?)""",
            (
                payload.firstName.strip(), payload.lastName.strip(), payload.dob,
                payload.grade, payload.parentName.strip(), payload.relationship,
                payload.contact.strip(), payload.email.strip(), payload.address.strip(),
                payload.previousSchool or "", payload.additional or "", now_iso(),
            ),
        )
        new_id = cur.lastrowid
    return {
        "ok": True,
        "id": new_id,
        "message": f"Thank you {payload.parentName}. Your application for {payload.firstName} {payload.lastName} has been received.",
    }


@app.post("/api/contact")
async def contact(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    if not all(str(data.get(k) or "").strip() for k in ("name", "email", "message")):
        return JSONResponse({"error": "Missing required fields"}, status_code=400)
    payload = ContactIn(name=data.get("name",""), email=data.get("email",""), phone=data.get("phone") or "", message=data.get("message",""))
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO contacts (name, email, phone, message, status, created_at)
               VALUES (?,?,?,?, 'new', ?)""",
            (payload.name.strip(), payload.email.strip(), payload.phone or "", payload.message.strip(), now_iso()),
        )
        new_id = cur.lastrowid
    log_activity("contact", f"Message from {payload.name}")
    return {"ok": True, "id": new_id, "message": "Message sent! We will get back to you soon."}


@app.post("/api/suggest")
async def suggest(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    if not isinstance(data, dict):
        data = {}
    anon = str(data.get("anonymous") or "").lower() in {"1", "true", "on", "yes"}
    message = str(data.get("message") or "").strip()
    name = str(data.get("name") or "").strip()
    if not message or (not anon and not name):
        return JSONResponse({"error": "Missing required fields"}, status_code=400)
    if len(message) > 800:
        return JSONResponse({"error": "Suggestion is too long"}, status_code=400)
    name = name or "Anonymous"
    role = str(data.get("role") or "Parent").strip() or "Parent"
    email = str(data.get("email") or "").strip()
    phone = str(data.get("phone") or "").strip()
    category = str(data.get("category") or "General").strip() or "General"
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO suggestions (name, role, email, phone, category, message, status, created_at, public, anonymous)
               VALUES (?,?,?,?,?,?,'new',?,0,?)""",
            (name, role, email, phone, category, message, now_iso(), 1 if anon else 0),
        )
        new_id = cur.lastrowid
    log_activity("suggestion", f"Suggestion from {name} · {category}")
    ref = f"SSN-{new_id:04d}"
    return {"ok": True, "id": new_id, "ref": ref, "message": f"Thank you. Your suggestion {ref} has reached the school office."}


@app.get("/api/suggestions/public")
def public_suggestions():
    rows = fetch_all(
        """SELECT category, message, status FROM suggestions
           WHERE public = 1 AND status IN ('done','reviewing')
           ORDER BY CASE status WHEN 'done' THEN 0 ELSE 1 END, id DESC LIMIT 9"""
    )
    out = []
    for r in rows:
        msg = (r.get("message") or "").strip()
        out.append({
            "category": r.get("category") or "General",
            "title": msg[:110] + ("…" if len(msg) > 110 else ""),
            "status": r.get("status") or "reviewing",
        })
    return out


@app.api_route("/api/suggest", methods=["GET", "OPTIONS"])
def suggest_meta(request: Request):
    if request.method == "OPTIONS":
        return JSONResponse({}, status_code=204, headers={"Allow": "OPTIONS, POST"})
    return JSONResponse({"error": "Method not allowed"}, status_code=405, headers={"Allow": "OPTIONS, POST"})


@app.post("/api/newsletter")
def newsletter(payload: SubscribeIn):
    email = payload.email.strip().lower()
    if not email or "@" not in email:
        return JSONResponse({"error": "Missing required fields"}, status_code=400)
    with get_db() as conn:
        existing = conn.execute("SELECT id FROM subscribers WHERE email = ?", (email,)).fetchone()
        if existing:
            return {"ok": True, "message": "You are already subscribed."}
        conn.execute(
            "INSERT INTO subscribers (email, created_at) VALUES (?,?)",
            (email, now_iso()),
        )
    return {"ok": True, "message": "Thank you for subscribing to Siddeshwor School updates!"}


# ---------------------------------------------------------------------------
# Admin API
# ---------------------------------------------------------------------------
@app.post("/api/admin/login")
def admin_login(payload: LoginIn):
    user = fetch_one("SELECT * FROM users WHERE username = ?", (payload.username.strip(),))
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(401, "Invalid username or password")
    token = secrets.token_urlsafe(32)
    with get_db() as conn:
        prune_sessions(conn)
        conn.execute(
            "INSERT INTO sessions (token, user_id, created_at) VALUES (?,?,?)",
            (token, user["id"], int(time.time())),
        )
    return {
        "token": token,
        "user": {"id": user["id"], "username": user["username"], "name": user["name"], "role": user["role"]},
    }


@app.post("/api/admin/logout")
def admin_logout(user=Depends(current_user), authorization: str | None = Header(default=None)):
    token = authorization.split(" ", 1)[1].strip()
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    return {"ok": True}


@app.get("/api/admin/me")
def admin_me(user=Depends(current_user)):
    return {"id": user["id"], "username": user["username"], "name": user["name"], "role": user["role"]}


@app.get("/api/admin/stats")
def admin_stats(user=Depends(current_user)):
    def count(table, where="1=1"):
        row = fetch_one(f"SELECT COUNT(*) AS n FROM {table} WHERE {where}")
        return row["n"] if row else 0

    return {
        "applications_new": count("applications", "status='new'"),
        "applications_total": count("applications"),
        "contacts_new": count("contacts", "status='new'"),
        "contacts_total": count("contacts"),
        "subscribers": count("subscribers"),
        "news": count("news"),
        "staff": count("staff"),
        "notices": count("notices"),
        "gallery": count("gallery"),
        "suggestions_new": count("suggestions", "status='new'"),
        "suggestions_total": count("suggestions"),
    }


@app.get("/api/admin/applications")
def admin_applications(user=Depends(current_user)):
    return fetch_all("SELECT * FROM applications ORDER BY id DESC")


class StatusIn(BaseModel):
    status: str


@app.patch("/api/admin/applications/{item_id}")
def update_application(item_id: int, payload: StatusIn, user=Depends(current_user)):
    if payload.status not in {"new", "reviewing", "accepted", "rejected"}:
        raise HTTPException(400, "Invalid status")
    with get_db() as conn:
        conn.execute("UPDATE applications SET status = ? WHERE id = ?", (payload.status, item_id))
    return {"ok": True}


@app.get("/api/admin/contacts")
def admin_contacts(user=Depends(current_user)):
    return fetch_all("SELECT * FROM contacts ORDER BY id DESC")


@app.patch("/api/admin/contacts/{item_id}")
def update_contact(item_id: int, payload: StatusIn, user=Depends(current_user)):
    if payload.status not in {"new", "read", "replied"}:
        raise HTTPException(400, "Invalid status")
    with get_db() as conn:
        conn.execute("UPDATE contacts SET status = ? WHERE id = ?", (payload.status, item_id))
    return {"ok": True}


@app.get("/api/admin/suggestions")
def admin_suggestions(user=Depends(current_user)):
    return fetch_all("SELECT * FROM suggestions ORDER BY id DESC")


class SuggestAdminIn(BaseModel):
    status: str | None = None
    notes: str | None = None
    public: int | None = None


@app.patch("/api/admin/suggestions/{item_id}")
def update_suggestion(item_id: int, payload: SuggestAdminIn, user=Depends(current_user)):
    row = fetch_one("SELECT * FROM suggestions WHERE id = ?", (item_id,))
    if not row:
        raise HTTPException(404, "Not found")
    if payload.status and payload.status not in {"new", "reviewing", "done", "archived"}:
        raise HTTPException(400, "Invalid status")
    next_status = payload.status if payload.status else row["status"]
    next_notes = payload.notes if payload.notes is not None else (row.get("notes") or "")
    next_public = int(bool(payload.public)) if payload.public is not None else int(bool(row.get("public")))
    if next_status == "done" and not str(next_notes).strip():
        raise HTTPException(400, "Office notes are required before marking done")
    if next_public and next_status == "new":
        raise HTTPException(400, "Review the suggestion before publishing")
    if next_public and next_status == "archived":
        raise HTTPException(400, "Archived suggestions cannot be public")
    with get_db() as conn:
        if payload.status:
            conn.execute("UPDATE suggestions SET status = ? WHERE id = ?", (payload.status, item_id))
        if payload.notes is not None:
            conn.execute("UPDATE suggestions SET notes = ? WHERE id = ?", (payload.notes, item_id))
        if payload.public is not None:
            conn.execute("UPDATE suggestions SET public = ? WHERE id = ?", (1 if payload.public else 0, item_id))
    if payload.status and payload.status != row["status"]:
        log_activity("suggestion", f"Suggestion SSN-{item_id:04d} marked {payload.status}")
    return {"ok": True}


@app.delete("/api/admin/suggestions/{item_id}")
def delete_suggestion(item_id: int, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM suggestions WHERE id = ?", (item_id,))
    return {"ok": True}


@app.get("/api/admin/subscribers")
def admin_subscribers(user=Depends(current_user)):
    return fetch_all("SELECT * FROM subscribers ORDER BY id DESC")


class NewsIn(BaseModel):
    slug: str
    title: str
    date_bs: str
    excerpt: str
    body: str
    cover: str
    images: list[dict] = Field(default_factory=list)
    published: int = 1


@app.post("/api/admin/news")
def create_news(payload: NewsIn, user=Depends(current_user)):
    with get_db() as conn:
        try:
            cur = conn.execute(
                """INSERT INTO news (slug, title, date_bs, excerpt, body, cover, images, published, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (
                    payload.slug, payload.title, payload.date_bs, payload.excerpt,
                    payload.body, payload.cover, json.dumps(payload.images),
                    payload.published, now_iso(),
                ),
            )
            new_id = cur.lastrowid
        except Exception as exc:
            raise HTTPException(400, str(exc))
    return {"ok": True, "id": new_id}


@app.put("/api/admin/news/{item_id}")
def update_news(item_id: int, payload: NewsIn, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute(
            """UPDATE news SET slug=?, title=?, date_bs=?, excerpt=?, body=?, cover=?, images=?, published=?
               WHERE id=?""",
            (
                payload.slug, payload.title, payload.date_bs, payload.excerpt,
                payload.body, payload.cover, json.dumps(payload.images),
                payload.published, item_id,
            ),
        )
    return {"ok": True}


@app.delete("/api/admin/news/{item_id}")
def delete_news(item_id: int, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM news WHERE id = ?", (item_id,))
    return {"ok": True}


@app.get("/api/admin/news")
def admin_news(user=Depends(current_user)):
    return fetch_all("SELECT * FROM news ORDER BY id DESC")


class StaffIn(BaseModel):
    staff_key: str
    name: str
    role: str
    subject: str | None = None
    department: str | None = None
    level: str = "faculty"
    image: str | None = None
    sort_order: int = 0


@app.post("/api/admin/staff")
def create_staff(payload: StaffIn, user=Depends(current_user)):
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO staff (staff_key, name, role, subject, department, level, image, sort_order)
               VALUES (?,?,?,?,?,?,?,?)""",
            (payload.staff_key, payload.name, payload.role, payload.subject,
             payload.department, payload.level, payload.image, payload.sort_order),
        )
        return {"ok": True, "id": cur.lastrowid}


@app.put("/api/admin/staff/{item_id}")
def update_staff(item_id: int, payload: StaffIn, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute(
            """UPDATE staff SET staff_key=?, name=?, role=?, subject=?, department=?, level=?, image=?, sort_order=?
               WHERE id=?""",
            (payload.staff_key, payload.name, payload.role, payload.subject,
             payload.department, payload.level, payload.image, payload.sort_order, item_id),
        )
    return {"ok": True}


@app.delete("/api/admin/staff/{item_id}")
def delete_staff(item_id: int, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM staff WHERE id = ?", (item_id,))
    return {"ok": True}


def log_activity(kind: str, summary: str):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO activity (kind, summary, created_at) VALUES (?,?,?)",
            (kind, summary, now_iso()),
        )


@app.get("/api/faq")
def list_faq():
    return fetch_all("SELECT * FROM faqs ORDER BY sort_order, id")


@app.get("/api/search")
def search(q: str = ""):
    q = (q or "").strip()
    if len(q) < 2:
        return {"news": [], "staff": [], "pages": []}
    like = f"%{q}%"
    news = fetch_all(
        """SELECT slug, title, date_bs, excerpt, cover FROM news
           WHERE published = 1 AND (title LIKE ? OR excerpt LIKE ? OR body LIKE ?)
           ORDER BY id DESC LIMIT 8""",
        (like, like, like),
    )
    staff = fetch_all(
        """SELECT name, role, department, subject, image FROM staff
           WHERE name LIKE ? OR role LIKE ? OR subject LIKE ? OR department LIKE ?
           LIMIT 8""",
        (like, like, like, like),
    )
    pages = [
        {"title": "About Us", "path": "/about", "hint": "History, mission, vision"},
        {"title": "Siddeshwor Family", "path": "/family", "hint": "Staff and organization"},
        {"title": "Academics", "path": "/academics", "hint": "ECD, Basic, Secondary"},
        {"title": "Facilities", "path": "/facilities", "hint": "Labs, library, sports"},
        {"title": "News", "path": "/news", "hint": "Events and updates"},
        {"title": "Notice Board", "path": "/notice", "hint": "School routine"},
        {"title": "Apply / Admission", "path": "/apply", "hint": "Admission form"},
        {"title": "Contact", "path": "/contact", "hint": "Phone, email, map"},
        {"title": "Why Us", "path": "/why-us", "hint": "Why choose Siddeshwor"},
        {"title": "Gallery", "path": "/gallery", "hint": "Photo gallery"},
        {"title": "Suggestion desk", "path": "/suggest", "hint": "Share an idea with the school"},
        {"title": "Privacy", "path": "/privacy", "hint": "Privacy policy"},
    ]
    ql = q.lower()
    pages = [p for p in pages if ql in p["title"].lower() or ql in p["hint"].lower()]
    return {"news": news, "staff": staff, "pages": pages}


@app.get("/api/gallery")
def gallery():
    items, seen = [], set()
    # Managed photos come first, before hero slides and news images.
    for g in fetch_all("SELECT * FROM gallery ORDER BY sort_order, id"):
        url = (g.get("url") or "").strip()
        if url and url not in seen:
            seen.add(url)
            items.append({
                "url": url,
                "alt": g.get("alt") or g.get("category") or "Photo",
                "category": g.get("category") or "Gallery",
            })
    try:
        for slide in fetch_all("SELECT url, alt FROM hero_slides ORDER BY sort_order"):
            if slide.get("url") and slide["url"] not in seen:
                seen.add(slide["url"])
                items.append({"url": slide["url"], "alt": slide.get("alt") or "Campus", "category": "Campus"})
        for n in fetch_all("SELECT title, cover, images FROM news WHERE published = 1"):
            if n.get("cover") and n["cover"] not in seen:
                seen.add(n["cover"])
                items.append({"url": n["cover"], "alt": n.get("title") or "News", "category": "News"})
            imgs = n.get("images") or []
            if isinstance(imgs, str):
                try:
                    imgs = json.loads(imgs)
                except Exception:
                    imgs = []
            for im in imgs:
                url = alt = None
                if isinstance(im, dict):
                    url, alt = im.get("url"), im.get("alt")
                elif isinstance(im, (list, tuple)) and im:
                    url = im[0]
                    alt = im[1] if len(im) > 1 else n.get("title")
                if url and url not in seen:
                    seen.add(url)
                    items.append({"url": url, "alt": alt or n.get("title") or "News", "category": "News"})
    except Exception:
        pass
    return items


@app.api_route("/api/apply", methods=["GET", "OPTIONS"])
def apply_meta(request: Request):
    if request.method == "OPTIONS":
        return JSONResponse({}, status_code=204, headers={"Allow": "OPTIONS, POST"})
    return JSONResponse({"error": "Method not allowed"}, status_code=405, headers={"Allow": "OPTIONS, POST"})


@app.api_route("/api/contact", methods=["GET", "OPTIONS"])
def contact_meta(request: Request):
    if request.method == "OPTIONS":
        return JSONResponse({}, status_code=204, headers={"Allow": "OPTIONS, POST"})
    return JSONResponse({"error": "Method not allowed"}, status_code=405, headers={"Allow": "OPTIONS, POST"})


@app.get("/api/admin/recent")
def admin_recent(user=Depends(current_user)):
    return {
        "applications": fetch_all("SELECT id, firstName, lastName, grade, status, created_at FROM applications ORDER BY id DESC LIMIT 5"),
        "contacts": fetch_all("SELECT id, name, email, status, created_at FROM contacts ORDER BY id DESC LIMIT 5"),
        "activity": fetch_all("SELECT * FROM activity ORDER BY id DESC LIMIT 12"),
        "suggestions": fetch_all("SELECT id, name, category, status, created_at FROM suggestions ORDER BY id DESC LIMIT 5"),
    }


@app.get("/api/admin/export/applications")
def export_applications(user=Depends(current_user)):
    import csv
    import io
    from fastapi.responses import StreamingResponse
    rows = fetch_all("SELECT * FROM applications ORDER BY id DESC")
    buf = io.StringIO()
    fields = ["id", "firstName", "lastName", "dob", "grade", "parentName", "relationship",
              "contact", "email", "address", "previousSchool", "additional", "status", "created_at"]
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=applications.csv"},
    )


@app.get("/api/admin/export/suggestions")
def export_suggestions(user=Depends(current_user)):
    import csv
    import io
    from fastapi.responses import StreamingResponse
    rows = fetch_all("SELECT * FROM suggestions ORDER BY id DESC")
    buf = io.StringIO()
    fields = ["id", "name", "role", "email", "phone", "category", "message", "status", "public", "anonymous", "notes", "created_at"]
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    buf.seek(0)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=suggestions.csv"},
    )


class SettingsIn(BaseModel):
    settings: dict[str, str]


@app.put("/api/admin/settings")
def update_settings(payload: SettingsIn, user=Depends(current_user)):
    with get_db() as conn:
        for k, v in payload.settings.items():
            conn.execute(
                "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (str(k), str(v)),
            )
    log_activity("settings", "School settings updated")
    return {"ok": True}


@app.delete("/api/admin/applications/{item_id}")
def delete_application(item_id: int, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM applications WHERE id = ?", (item_id,))
    return {"ok": True}


@app.delete("/api/admin/contacts/{item_id}")
def delete_contact(item_id: int, user=Depends(current_user)):
    with get_db() as conn:
        conn.execute("DELETE FROM contacts WHERE id = ?", (item_id,))
    return {"ok": True}


# ---------------------------------------------------------------------------
# Admin — gallery manager
# ---------------------------------------------------------------------------
class GalleryIn(BaseModel):
    url: str
    alt: str = ""
    category: str = "General"
    sort_order: int = 0


class GalleryPatchIn(BaseModel):
    url: str | None = None
    alt: str | None = None
    category: str | None = None
    sort_order: int | None = None


@app.get("/api/admin/gallery")
def admin_gallery(user=Depends(current_user)):
    return fetch_all("SELECT * FROM gallery ORDER BY sort_order, id")


@app.post("/api/admin/gallery")
def create_gallery(payload: GalleryIn, user=Depends(current_user)):
    url = (payload.url or "").strip()
    if not url:
        raise HTTPException(400, "Photo URL is required")
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO gallery (url, alt, category, sort_order, uploaded, created_at)
               VALUES (?,?,?,?,0,?)""",
            (url, (payload.alt or "").strip(), (payload.category or "General").strip(),
             int(payload.sort_order or 0), now_iso()),
        )
        new_id = cur.lastrowid
    log_activity("gallery", f"Gallery photo added by URL ({url[:60]})")
    return {"ok": True, "id": new_id}


@app.patch("/api/admin/gallery/{item_id}")
def update_gallery(item_id: int, payload: GalleryPatchIn, user=Depends(current_user)):
    row = fetch_one("SELECT * FROM gallery WHERE id = ?", (item_id,))
    if not row:
        raise HTTPException(404, "Photo not found")
    url = payload.url if payload.url is not None else row["url"]
    url = (url or "").strip()
    if not url:
        raise HTTPException(400, "Photo URL is required")
    uploaded = int(row["uploaded"] or 0)
    if uploaded and url != row["url"]:
        delete_upload_file(row["url"])
        uploaded = 0
    with get_db() as conn:
        conn.execute(
            """UPDATE gallery SET url=?, alt=?, category=?, sort_order=?, uploaded=? WHERE id=?""",
            (
                url,
                (payload.alt if payload.alt is not None else (row["alt"] or "")).strip(),
                (payload.category if payload.category is not None else (row["category"] or "General")).strip(),
                int(payload.sort_order if payload.sort_order is not None else (row["sort_order"] or 0)),
                uploaded,
                item_id,
            ),
        )
    return {"ok": True}


@app.delete("/api/admin/gallery/{item_id}")
def delete_gallery(item_id: int, user=Depends(current_user)):
    row = fetch_one("SELECT * FROM gallery WHERE id = ?", (item_id,))
    if not row:
        raise HTTPException(404, "Photo not found")
    if row["uploaded"]:
        delete_upload_file(row["url"])
    with get_db() as conn:
        conn.execute("DELETE FROM gallery WHERE id = ?", (item_id,))
    log_activity("gallery", f"Gallery photo {item_id} deleted")
    return {"ok": True}


@app.post("/api/admin/gallery/upload")
async def upload_gallery_photo(
    user=Depends(current_user),
    file: UploadFile = File(...),
    caption: str = Form(""),
    category: str = Form("General"),
    sort_order: int = Form(0),
):
    ext, data = await read_upload(file)
    name = save_upload(data, ext)
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO gallery (url, alt, category, sort_order, uploaded, created_at)
               VALUES (?,?,?,?,1,?)""",
            (f"/uploads/{name}", caption.strip(), (category or "General").strip(),
             int(sort_order or 0), now_iso()),
        )
        new_id = cur.lastrowid
    log_activity("gallery", f"Gallery photo uploaded ({caption or name})")
    return {"ok": True, "id": new_id, "url": f"/uploads/{name}"}


# ---------------------------------------------------------------------------
# Admin — notices manager
# ---------------------------------------------------------------------------
class NoticeIn(BaseModel):
    title: str
    image: str
    page_num: int = 1
    sort_order: int = 0


class NoticePatchIn(BaseModel):
    title: str | None = None
    image: str | None = None
    page_num: int | None = None
    sort_order: int | None = None


def _notice_fields(title, image, page_num):
    title = str(title or "").strip()
    image = str(image or "").strip()
    if not title:
        raise HTTPException(400, "Title is required")
    if not image:
        raise HTTPException(400, "Image URL is required")
    try:
        page = int(page_num)
    except (TypeError, ValueError):
        raise HTTPException(400, "Page number must be a number")
    if page < 1:
        raise HTTPException(400, "Page number must be 1 or greater")
    return title, image, page


@app.get("/api/admin/notices")
def admin_notices(user=Depends(current_user)):
    return fetch_all("SELECT * FROM notices ORDER BY page_num, sort_order, id")


@app.post("/api/admin/notices")
def create_notice(payload: NoticeIn, user=Depends(current_user)):
    title, image, page = _notice_fields(payload.title, payload.image, payload.page_num)
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO notices (title, image, page_num, sort_order) VALUES (?,?,?,?)",
            (title, image, page, int(payload.sort_order or 0)),
        )
        new_id = cur.lastrowid
    log_activity("notices", f"Notice page {page} added")
    return {"ok": True, "id": new_id}


@app.patch("/api/admin/notices/{item_id}")
def update_notice(item_id: int, payload: NoticePatchIn, user=Depends(current_user)):
    row = fetch_one("SELECT * FROM notices WHERE id = ?", (item_id,))
    if not row:
        raise HTTPException(404, "Notice not found")
    title = payload.title if payload.title is not None else row["title"]
    image = payload.image if payload.image is not None else row["image"]
    page = payload.page_num if payload.page_num is not None else row["page_num"]
    title, image, page = _notice_fields(title, image, page)
    if image != row["image"]:
        delete_upload_file(row["image"])
    with get_db() as conn:
        conn.execute(
            "UPDATE notices SET title=?, image=?, page_num=?, sort_order=? WHERE id=?",
            (title, image, page,
             int(payload.sort_order if payload.sort_order is not None else (row["sort_order"] or 0)),
             item_id),
        )
    return {"ok": True}


@app.delete("/api/admin/notices/{item_id}")
def delete_notice(item_id: int, user=Depends(current_user)):
    row = fetch_one("SELECT * FROM notices WHERE id = ?", (item_id,))
    if not row:
        raise HTTPException(404, "Notice not found")
    delete_upload_file(row["image"])
    with get_db() as conn:
        conn.execute("DELETE FROM notices WHERE id = ?", (item_id,))
    log_activity("notices", f"Notice page {row['page_num']} deleted")
    return {"ok": True}


@app.post("/api/admin/notices/upload")
async def upload_notice_image(
    user=Depends(current_user),
    file: UploadFile = File(...),
    title: str = Form(""),
    page_num: int = Form(1),
    sort_order: int = Form(0),
):
    title, _, page = _notice_fields(title, "/uploads/notice-", page_num)
    ext, data = await read_upload(file)
    name = save_upload(data, ext, prefix="notice-")
    image = f"/uploads/{name}"
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO notices (title, image, page_num, sort_order) VALUES (?,?,?,?)",
            (title, image, page, int(sort_order or 0)),
        )
        new_id = cur.lastrowid
    log_activity("notices", f"Notice image uploaded ({title})")
    return {"ok": True, "id": new_id, "image": image, "page_num": page}


# ---------------------------------------------------------------------------
# Static frontend + admin
# ---------------------------------------------------------------------------
def _safe_file(folder: Path, rel: str):
    target = (folder / rel).resolve()
    try:
        target.relative_to(folder.resolve())
    except ValueError:
        return None
    if target.is_file():
        return target
    index = target / "index.html"
    if index.is_file():
        return index
    return None


@app.get("/{full_path:path}")
async def spa_or_static(full_path: str):
    """Serve the cloned frontend and admin UI."""
    if full_path.startswith("api/"):
        raise HTTPException(404, "Not found")
    if full_path == "uploads" or full_path.startswith("uploads/"):
        rel = full_path[len("uploads"):].lstrip("/")
        found = _safe_file(UPLOADS_DIR, rel)
        if found:
            return FileResponse(found)
        raise HTTPException(404, "Not found")
    if full_path == "" or full_path == "/":
        return FileResponse(FRONTEND / "index.html")
    if full_path == "admin" or full_path.startswith("admin/"):
        rel = full_path[6:].lstrip("/") or "index.html"
        found = _safe_file(ADMIN, rel)
        if found:
            return FileResponse(found)
        raise HTTPException(404, "Not found")
    found = _safe_file(FRONTEND, full_path)
    if found:
        return FileResponse(found)
    raise HTTPException(404, "Not found")
