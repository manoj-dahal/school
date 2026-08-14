# Deploy — get a permanent public URL (free)

The repo ships a `Dockerfile` and a `render.yaml` blueprint, so a one-click
deploy on [Render](https://render.com) (free tier) gives you a permanent
public URL like `https://siddeshwor-school.onrender.com`.

## Option A — Render (recommended, ~3 minutes)

1. Open **https://render.com/deploy?repo=https://github.com/manoj-dahal/school**
2. Sign in with your GitHub account.
3. Click **Deploy Blueprint** — Render reads `render.yaml`, builds the
   Dockerfile, seeds the database, and starts the server.
4. Your public URL appears on the service page, e.g.
   `https://siddeshwor-school.onrender.com`.

Notes:
- Free tier sleeps after 15 min of inactivity; the first request after
  a sleep takes ~30–60 s to wake.
- The SQLite database is re-seeded on every deploy/restart (no persistent
  disk on the free tier). Upgrade to a paid plan and attach a disk at
  `/app/data` if you need submitted applications/messages to persist.

## Option B — Railway / Fly.io

Both auto-detect the `Dockerfile`:

- **Railway**: https://railway.app → New Project → Deploy from GitHub repo →
  `manoj-dahal/school`.
- **Fly.io**: `fly launch` in the repo root, accept the Dockerfile.

## Option C — Your own server (VPS)

`.github/workflows/deploy.yml` already automates this. Add these repository
secrets (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `DEPLOY_HOST` | server IP / hostname |
| `DEPLOY_USER` | SSH user |
| `DEPLOY_KEY`  | private SSH key |

Every push to `main` then builds the image, pushes it to GHCR, and
restarts the container on your server (port 3000). Put nginx/Caddy in
front for HTTPS and a domain.
