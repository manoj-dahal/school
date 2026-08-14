# Shree Siddeshwor Secondary School — Full Stack Clone

Complete copy of [https://www.siddeshwor.edu.np](https://www.siddeshwor.edu.np) including **frontend**, **backend API**, **SQLite database**, and **admin panel**.

## What’s included

| Layer | Location | Notes |
|---|---|---|
| Frontend | `frontend/` | All public pages (Home, About, Family, Academics, Facilities, News, Notice, Apply, Contact…) |
| Backend API | `backend/main.py` | FastAPI — same contracts as the live site |
| Database | `data/siddeshwor.db` | SQLite, seeded with live-site content |
| Admin CMS | `admin/` | Applications, messages, news, staff, subscribers |
| API docs | `/api/docs` | Interactive Swagger UI |

## Live-site API compatibility

The original Vercel app exposes:

- `POST /api/apply` — `{ firstName, lastName, dob, grade, parentName, relationship, contact, email, address, previousSchool, additional }`
- `POST /api/contact` — `{ name, email, phone, message }`

Both return `400 { "error": "Missing required fields" }` when required data is missing — this clone matches that.

Extra public endpoints:

- `GET /api/health` `GET /api/school` `GET /api/news` `GET /api/news/{slug}`
- `GET /api/staff` `GET /api/facilities` `GET /api/academics` `GET /api/notices` `GET /api/hero`
- `GET /api/faq` `GET /api/search?q=` `GET /api/gallery`
- `POST /api/newsletter` `POST /api/suggest`
- `GET /api/suggestions/public`

Admin extras: required suggestion inbox, CSV export, settings editor, activity feed.

## Admin

- URL: `/admin`
- Sign in with the office account created at seed time. Credentials are not published.

## Run

```bash
cd siddeshwor-school/backend
python3 seed.py          # first time (or --reset) — creates data/siddeshwor.db
python3 -m uvicorn main:app --host 0.0.0.0 --port 3000
```

The SQLite file is created locally and is not committed.

Then open:

- Website: http://localhost:3000
- Admin: http://localhost:3000/admin
- API docs: http://localhost:3000/api/docs

## GitHub deploy

This repo includes `.github/workflows`:

- **CI** — compile, seed, check `/api/health` and apply/contact 400 contracts
- **Deploy** — build a Docker image and push to `ghcr.io/<user>/<repo>`

```bash
git init
git add .
git commit -m "Siddeshwor school site"
git branch -M main
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

Turn on **Settings → Actions → Read and write** permissions so the image can be published. Optional SSH secrets (`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`) restart the container on your server. See [`.github/README.md`](.github/README.md).

```bash
docker compose up --build
```

## Database tables

`users`, `sessions`, `settings`, `news`, `staff`, `facilities`, `academics`, `notices`, `hero_slides`, `applications`, `contacts`, `subscribers`
