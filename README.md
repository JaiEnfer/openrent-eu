# OpenRent EU

**OpenRent** EU is an open-source rental aggregation platform for Europe.

It helps users **search, compare, and evaluate rental listings** across multiple sources, while allowing agencies and landlords to upload and manage inventory.

## 🚀 Features
For Renters
- 🔍 Search listings by city, country, and rent
- 📊 Compare up to 3 listings side-by-side
- 💰 Calculate total move-in cost (rent + deposit)
- ⚠️ View scam risk score and indicators
- 🌍 Multi-country support (Europe-focused)

For Agencies / Landlords
- 📤 Upload listings via CSV
- 🧩 Structured data ingestion pipeline
- 🔄 Automatic normalization and deduplication
- 📦 Centralized listing storage

## 🧠 Architecture Overview

OpenRent EU is designed as a data ingestion + normalization platform, not just a frontend app.

Core Layers
1. Ingestion Layer
2. Raw Data Layer
- Stores original listing payloads
- Preserves source data for auditing
4. Deduplication Engine
- Detects duplicate listings across sources
- Maintains a single canonical listing
5. Search API
- FastAPI-based backend
- Query by city, country, rent
6. Frontend
- React + Vite
- Search, compare, upload UI

## 🏗️ Tech Stack
Backend
- FastAPI
- Pydantic

- JavaScript (ES6)

Data / Processing
- CSV ingestion
- Normalization pipeline
```text
openrent-eu/
├── backend/
│   │   ├── routers/         # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│
├── frontend/
│   ├── src/
│   ├── index.html
│   └── vite.config.js
│
└── README.md
```

## ⚙️ Quickstart (development)

Clone the repo and open the workspace:

```sh
git clone https://github.com/your-username/openrent-eu.git
cd openrent-eu
```

Backend (PowerShell)

```ps1
cd backend
python -m venv .venv         # only once
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# start backend (from backend/)
python -m uvicorn app.main:app --reload --port 8000
# or, if you used the alias I added, you can run:
python -m uvicorn app.main:aap --reload --port 8000
```

Backend endpoints

- API root: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs

Notes:
- The configuration file is [backend/.env](backend/.env) — set `DATABASE_URL` and `FRONTEND_ORIGIN` there.
- I fixed a malformed `.env` and replaced a corrupted `requirements.txt` with a UTF‑8 list.

Frontend

```sh
cd frontend
npm install
# dev server (Vite)
npm run dev
# or force a specific port:
npx vite --port 5173
```

- Default dev URL: http://localhost:5173 (Vite may choose another free port if 5173 is in use).
- The frontend files are in [frontend/src](frontend/src) — I added UI polish, a hero, logo, and thumbnails.

## 📤 CSV Upload Format

Agencies can upload listings using CSV with the following columns:

```text
external_id,title,description,country,city,postal_code,street,monthly_rent,deposit,fees,bedrooms,bathrooms,size_m2,furnished,utilities_included,scam_score,listing_url,contact_name,contact_type
```

## 🔌 API Endpoints

### Listings

GET /api/listings/

Query params:

- city
- country
- max_rent

#### Ingest CSV (Sample)

POST /api/ingest/csv

#### Upload CSV

POST /api/ingest/csv-upload

Form-data:

- file: CSV file

## 🧪 Development Notes

Extra notes and troubleshooting
 - The backend runs Alembic migrations at container start (see `backend/entrypoint.sh`).
 - To create and manage migrations locally:

```sh
cd backend
. .venv\Scripts\Activate.ps1   # or source .venv/bin/activate
pip install -r requirements.txt
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

If you're using Docker Compose, the entrypoint already runs `alembic upgrade head` on startup.
- I added an alias in [backend/app/main.py](backend/app/main.py): `aap = app` so `uvicorn app.main:aap` works if you mistype the module target.
- If Vite reports port in use, kill the process using that port (e.g. `taskkill /PID <pid> /F` on Windows) or run `npx vite --port 5173`.

## 🛣️ Roadmap

Short-term


Mid-term
I implemented several of these already:

- Gunicorn + Uvicorn worker is used in the backend container (`backend/entrypoint.sh`).
- Alembic is configured; an initial baseline migration is provided in `backend/alembic/versions/0001_initial_baseline.py`.
- GitHub Actions CI workflow added at `.github/workflows/ci.yml` to build images and run a smoke test.
- Docker Compose updated to load `backend/.env` via `env_file` in the backend service (use Docker secrets in prod).

Remaining recommended steps (I can continue):

- Configure Traefik (or nginx reverse proxy) with TLS and Let’s Encrypt for production domains.
- Add k8s manifests / Helm chart for container orchestration.
- Add structured logging and Sentry integration.
- Add automated DB migration checks in CI and a staging rollout pipeline.

Tell me which of the remaining items you'd like me to implement next, or say "do all" and I'll continue working through them in order.
Long-term
- AI-powered rental assistant
- Fraud detection models
- Tenant rights RAG (per country)
- Multi-language support

## ⚖️ Legal & Compliance

OpenRent EU is designed with EU regulations in mind:

- GDPR-aware data handling
- Source attribution required
- No unauthorized scraping
- API/feed-first ingestion strategy

## 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork the repo
2. Create a feature branch
3. Submit a pull request


## 📄 License

MIT License (recommended for open-source projects)

## 💡 Vision

OpenRent EU aims to become:

The unified rental search and comparison layer for Europe

Connecting renters, agencies, and platforms through a transparent and standardized data ecosystem

## 🛡️ Production Hardening (recommended)

Short checklist to move from local dev to a production deployment:

- **Reverse proxy & TLS**: Use Traefik or a cloud load balancer with Let's Encrypt. I added example Traefik config in `traefik/traefik.yml` and `traefik/dynamic_conf.yml`.
- **Secrets**: Store `DATABASE_URL`, `SENTRY_DSN`, and other sensitive values in Docker secrets or your cloud provider's secret manager. See `k8s/` for Kubernetes secret references.
- **Structured logging & Sentry**: Backend now supports structured JSON logs and optional Sentry reporting. Set `SENTRY_DSN` in your environment (or secret) to enable it.

Example `.env` entries for production (DO NOT COMMIT):

```env
DATABASE_URL=postgresql://user:pass@db:5432/openrent
SENTRY_DSN=https://public@sentry.example.com/12345
FRONTEND_ORIGIN=https://openrent.example.com
```

I added basic Kubernetes manifests in `k8s/` (`backend-deployment.yaml`, `frontend-deployment.yaml`, `ingress.yaml`) and a Traefik configuration in `traefik/` to help bootstrap a production deployment. These are starting points — you'll want to wire in your CI/CD, registry, and cert-manager or cloud TLS solution.