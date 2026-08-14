# Full-stack audit — Shree Siddeshwor Secondary School

Checked **2026-08-14** against the running site on port 3000.  
Five suites, **0 failures**.

| Suite | Scope | Result |
|---|---|---|
| Full-stack walkthrough | Interface → API → DB → cross-layer (12 steps) | **190 / 190** |
| Original function pack | Pages, assets, apply/contact, suggest, admin | **93 / 93** |
| Deep API pack | Field-by-field contracts, inbox rules, CRUD | **301 / 301** |
| Admin panel pack | UI wiring, lockout, inbox, CMS, CSV | **199 / 199** |
| Database pack | Integrity, schema, seed, constraints | **93 / 93** |

---

## Step 1 — Server

- `GET /api/health` → `ok: true`, school name present
- Public site `/` → 200
- Admin `/admin/` → 200

## Step 2 — Interface: every public page

All 21 HTML pages return 200, name the school, mount `#site-header` / `#site-footer`, and load `style.css` + `main.js`.

Home, About, Academics, Apply, Contact, Facilities, Family, Gallery, News (index + 7 articles), Notice, Privacy, Sitemap, Suggest, Why Us.

Unknown URL → **404**.

## Step 3 — Interface: assets and scripts

| Asset | Size | Role |
|---|---|---|
| `style.css` | 42 KB | Letterhead / gazette, ticker |
| `prof.css` | 170 B | Overlay |
| `main.js` | 36 KB | Nav, forms, ticker, search, gallery |
| Logo + favicon | present | Branding |
| `gallery.json` | 5 KB | Photo fallback |

`main.js` wires `/api/apply`, `/api/contact`, `/api/suggest`, `/api/newsletter`, `/api/search`, `/api/gallery`, `/api/faq`, `/api/news`, **Latest news** ticker, home + drawer suggestion forms, and the public idea board. Both `main.js` and admin JS parse cleanly in Node.

## Step 4 — Interface: forms

- **Apply** — live-site fields: `firstName lastName dob grade parentName relationship contact email address previousSchool`
- **Contact** — `name email phone message`
- **Suggest** (home + `/suggest/`) — `name role email phone category message anonymous`, max 800
- Sitemap lists the suggestion desk

## Step 5 — Interface: admin

- Login first; app shell hidden; **no password printed** on the card
- Eight tabs: Dashboard, **Suggestions** (2nd), Applications, Messages, News, Staff, Subscribers, Settings
- Required inbox: badge, need-bar, topic + status filters, new-row highlight, auto-open when work waits, review-before-publish, notes required for done
- CSV export buttons for applications and suggestions

## Step 6 — Backend: public reads

| Endpoint | Result |
|---|---|
| `/api/school` | Name, phone `01-4622730`, email, address, tagline |
| `/api/news` | 7 published articles; missing slug → 404 |
| `/api/staff` | 34 |
| `/api/facilities` | 13 |
| `/api/academics` | 3 |
| `/api/notices` | 4 |
| `/api/hero` | 4 |
| `/api/faq` | 6 |
| `/api/gallery` | 38 photos |
| `/api/search?q=suggest` | Finds `/suggest` |

## Step 7 — Backend: write contracts (match siddeshwor.edu.np)

- `POST /api/apply` and `/api/contact` empty or any required field blank → **`400 {"error":"Missing required fields"}`**
- Valid apply / contact store a row and return `{ok, id, message}`
- `GET` those paths → **405**; `OPTIONS` → **204**
- Suggest: empty / named-without-name → 400; anon + named issue `SSN-####`; 800 chars OK; 801 → 400
- Public board: only `reviewing` / `done`, **no name / email / phone**

## Step 8 — Newsletter and docs

New subscribe 200, duplicate “already subscribed”, bad email 400.  
`/api/docs` and OpenAPI expose apply, contact, suggest (37 paths).

## Step 9 — Admin auth

Every admin GET is **401** without a token. Bad password 401. Good login returns token + user. `/api/admin/me` matches.

## Step 10 — Admin inbox and mutations

- Stats include `suggestions_new` / `suggestions_total`
- Cannot publish while `new`
- Cannot mark `done` without office notes
- Review + notes + public works
- Archived cannot be public
- Application / contact status changes; illegal statuses 400
- CSV exports include planted rows
- Logout kills that session

## Step 11 — Database

- `PRAGMA integrity_check = ok`, no orphan FKs, WAL
- 15 tables; suggestions has `public anonymous notes phone status`
- Seed counts: 1 user, 7 news, 34 staff, 13 facilities, 21 settings, 6 FAQ
- No public+new rows; every `done` row has notes
- Password hash verifies; wrong password fails; duplicate username rejected
- Indexes on suggestion/application/contact status

## Step 12 — Cross-layer

- Apply form fields ⊇ API required ⊆ DB columns
- Contact and suggest form names exist on the matching tables
- The 7 news folders on disk **equal** the 7 slugs in SQLite
- Home ticker label is **Latest news**

---

## What this site does end-to-end

1. Public visitors use the gazette site (nav, search, news ticker, apply, contact, suggestion desk).
2. Forms POST the same field names as the live school site.
3. FastAPI validates, writes SQLite, returns the same 400 shape when data is missing.
4. Office signs in at `/admin`. New suggestions are a required inbox (badge, highlight, review before the public board).
5. Only reviewed notes marked public appear on the home / suggest idea board — without names.

Nothing in this pass failed. The stack is consistent from the page, through the API, into the database.
