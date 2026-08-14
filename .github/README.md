# GitHub deploy

Workflows in this folder build, test, and publish Shree Siddeshwor Secondary School.

| File | When | What |
|---|---|---|
| `workflows/ci.yml` | Every push / PR / manual | Compile Python, seed DB, start API, hit pages, check apply/contact/**suggest** `400 {"error":"Missing required fields"}` |
| `workflows/deploy.yml` | Push to `main` or `master`, or manual | Build Docker image and push to GitHub Container Registry |
| `dependabot.yml` | Weekly | Bump pip, Actions, and the Dockerfile base image |

## First-time setup

1. Create a **public** GitHub repository.
2. From this project root:

```bash
git init
git add .
git commit -m "Siddeshwor school site"
git branch -M main
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

3. In the repo: **Settings → Actions → General → Workflow permissions → Read and write** (needed so Deploy can push to GHCR).
4. After the first green **Deploy** run, the image is at:

`ghcr.io/YOUR_USER/YOUR_REPO:latest`

The package is private until you open **Packages → package settings → Change visibility → Public**.

Run it anywhere Docker is installed:

```bash
docker run -d --name siddeshwor -p 3000:3000 \
  -v siddeshwor-data:/app/data \
  ghcr.io/YOUR_USER/YOUR_REPO:latest
```

## Optional: deploy to your own server

Add these repository secrets. The SSH job only runs when `DEPLOY_HOST` is set.

| Secret | Example |
|---|---|
| `DEPLOY_HOST` | `203.0.113.10` |
| `DEPLOY_USER` | `ubuntu` |
| `DEPLOY_KEY` | private SSH key with access to that host |

Leave `DEPLOY_HOST` empty to skip SSH and only publish the image.

The server must have Docker installed. The job logs in to GHCR, pulls `:latest`, and restarts the `siddeshwor` container on port 3000 with a named volume for SQLite.

## Local Docker

```bash
docker compose up --build
```

Website: http://localhost:3000  
Admin: http://localhost:3000/admin

## What CI proves

- `backend/main.py`, `db.py`, `seed.py` compile
- Seed creates `data/siddeshwor.db`
- `/`, `/admin/`, `/suggest/`, `/api/health`, `/api/news`, `/api/suggestions/public` return 200
- Empty `POST /api/apply`, `/api/contact`, `/api/suggest` return `400` with `Missing required fields`
