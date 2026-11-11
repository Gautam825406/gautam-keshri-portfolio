# Gautam Keshri — Portfolio (editable)

A portfolio website you can edit yourself. Frontend and backend are in
**separate folders**, like RegLens / IncidentPilot — the frontend never
contains backend code, and the backend never contains frontend code. The
public page fetches all content from the API, so edits in the admin page
show up immediately with no rebuild.

## Structure

```
portfolio/
├── backend/      FastAPI + SQLite (REST API only)
│   ├── app/      main.py, models.py, schemas.py, seed.py, security.py, database.py
│   ├── tests/    test_api.py
│   ├── requirements.txt, Dockerfile, run.py, .env.example
├── frontend/     Vite + React + TypeScript (showcase + /admin editor)
│   ├── src/      App.tsx, api.ts, types.ts, styles.css, main.tsx
│   ├── vite.config.ts, package.json, Dockerfile, nginx.conf, .env.example
├── docker-compose.yml
└── README.md
```

## Run locally (two terminals)

```bash
# 1. Backend — http://localhost:8000  (API docs: /docs)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then edit ADMIN_KEY inside .env
python run.py

# 2. Frontend — http://localhost:5173
cd frontend
npm install
npm run dev
```

On first run the backend seeds the database (`backend/portfolio.db`) with
the verified portfolio content — 9 projects, profile, skills — only if the
database is empty. Your edits are saved in that file; deleting it re-seeds
on the next start.

## Run with Docker

```bash
# From the portfolio/ root. Set a real admin key first:
ADMIN_KEY='your-strong-key-here' docker compose up --build
# Frontend: http://localhost:5173   API: http://localhost:8000
```

## Editing content (admin)

1. Open **http://localhost:5173/admin**
2. Enter the admin key (from `backend/.env` → `ADMIN_KEY`, default dev
   value `change-me`) and click **Save key in this browser**. The key is
   kept only in that tab's `sessionStorage` — it is never stored on the
   server and never leaves your browser except as the `X-Admin-Key`
   header on admin requests.
3. Add / edit / delete projects, edit the profile (name, title, summary,
   email, LinkedIn, GitHub, location) and skills, then save. The public
   page at `/` reflects the change immediately — no rebuild.

## API

Public (no key): `GET /api/health`, `GET /api/profile`,
`GET /api/projects`, `GET /api/skills`.

Admin (header `X-Admin-Key: <key>`, wrong/missing key → 401):
`PUT /api/profile`, `POST /api/projects`, `PUT /api/projects/{id}`,
`DELETE /api/projects/{id}`, `PUT /api/skills`.

## Admin key — read this

- The default key `change-me` is for local development only.
- Before deploying anywhere public, set a long random `ADMIN_KEY` in
  `backend/.env` (local) or in your host's environment variables
  (Render / Vercel / VPS), and never commit a real `.env` — only
  `.env.example` is in the repo. `.gitignore` covers `.env` and `*.db`.
- Anyone with the key can edit or delete your portfolio content.

## Tests

```bash
cd backend
python -m pytest -q
```

## Deploy notes (not done for you)

- Backend: any Python host (Render free web service works — set
  `ADMIN_KEY` in env vars, start command `python run.py`).
- Frontend: Vercel / Netlify, or the included Docker image. If the API
  is on a different origin, set `VITE_API_URL` in the frontend build
  (e.g. `VITE_API_URL=https://your-api.onrender.com`).
- Do **not** commit `portfolio.db` or `.env`.
