# OpenRent EU

[![CI](https://github.com/JaiEnfer/openrent-eu/actions/workflows/ci.yml/badge.svg)](https://github.com/JaiEnfer/openrent-eu/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Backend: FastAPI](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Frontend: React](https://img.shields.io/badge/frontend-React-20232A?logo=react&logoColor=61DAFB)](https://react.dev/)
[![Docker Ready](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes Manifests](https://img.shields.io/badge/k8s-manifests-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)

OpenRent EU is an open-source rental aggregation platform for Europe.

It helps users search, compare, and evaluate rental listings across multiple sources, while giving agencies and landlords a structured way to upload and manage inventory.

The project combines a FastAPI backend, a React frontend, and a normalization pipeline to turn fragmented rental data into a searchable, comparable rental experience.

## Overview

OpenRent EU is designed as a data ingestion and listing normalization platform, not just a property-search UI.

It is built to support:

- Cross-source rental search
- CSV-based listing ingestion
- Data normalization and deduplication
- Canonical listing storage
- Backend APIs for search and upload workflows
- A modern frontend for renters, agencies, and landlords

## Features

### For Renters

- Search listings by city, country, and rent
- Compare listings side by side
- Estimate move-in costs such as rent and deposit
- View scam risk indicators
- Browse a Europe-focused rental experience

### For Agencies and Landlords

- Upload listings via CSV
- Use a structured ingestion pipeline
- Normalize incoming listing data automatically
- Reduce duplicates across sources
- Manage inventory through a central backend

## Architecture

### Core Layers

1. Ingestion layer  
   Accepts raw listing data from supported sources and CSV uploads.
2. Raw data layer  
   Preserves original listing payloads for traceability and auditing.
3. Normalization layer  
   Converts heterogeneous source data into a consistent schema.
4. Deduplication layer  
   Detects duplicate listings and maintains canonical records.
5. Search API  
   Exposes listing data through FastAPI endpoints.
6. Frontend  
   Delivers a React-based interface for browsing and comparing listings.

## Tech Stack

### Backend

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Gunicorn + Uvicorn

### Frontend

- React
- Vite
- JavaScript

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions
- Kubernetes manifests
- Traefik configuration

### Data Processing

- CSV ingestion
- Listing normalization
- Deduplication workflows

## Project Structure

```text
openrent-eu/
|-- backend/
|   |-- alembic/
|   |-- app/
|   |   |-- adapters/      # Source ingestion adapters
|   |   |-- core/          # Configuration and database setup
|   |   |-- models/        # SQLAlchemy models
|   |   |-- routers/       # FastAPI endpoints
|   |   |-- schemas/       # Pydantic schemas
|   |   |-- services/      # Normalization and deduplication logic
|   |   `-- utils/
|   |-- data/
|   |-- Dockerfile
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |-- Dockerfile
|   `-- package.json
|-- k8s/
|-- traefik/
|-- docker-compose.yml
`-- README.md
```

## Quickstart

### Run with Docker

From the repository root:

```powershell
docker compose up --build
```

Application URLs:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

To stop the stack:

```powershell
docker compose down
```

### Run without Docker

Backend:

```powershell
cd backend
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Development URLs:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Configuration

The backend reads local configuration from `backend/.env`.

Example values:

```env
APP_NAME=OpenRent EU API
FRONTEND_ORIGIN=http://localhost:5173
DATABASE_URL=sqlite:///./openrent.db
```

For production, use secrets or your cloud provider's secret manager instead of committing sensitive values.

## API

### Key Endpoints

- `GET /`
- `GET /health`
- `GET /api/listings/`
- `POST /api/ingest/csv`
- `POST /api/ingest/csv-upload`

### Listings Query Parameters

- `city`
- `country`
- `max_rent`

### CSV Upload Format

Expected CSV columns:

```text
external_id,title,description,country,city,postal_code,street,monthly_rent,deposit,fees,bedrooms,bathrooms,size_m2,furnished,utilities_included,scam_score,listing_url,contact_name,contact_type
```

## Database and Migrations

Alembic is configured for schema migrations.

Run migrations locally:

```powershell
cd backend
. .venv\Scripts\Activate.ps1
alembic upgrade head
```

Create a new migration:

```powershell
cd backend
. .venv\Scripts\Activate.ps1
alembic revision --autogenerate -m "describe change"
```

The container entrypoint also runs `alembic upgrade head` on startup.

## CI/CD

GitHub Actions is configured in `.github/workflows/ci.yml` to:

- Install backend dependencies
- Build the frontend
- Build Docker images
- Run a backend smoke test

## Kubernetes

Starter manifests are available in `k8s/`:

- `k8s/backend-deployment.yaml`
- `k8s/frontend-deployment.yaml`
- `k8s/ingress.yaml`

These manifests are a starting point and still require environment-specific image names, secrets, ingress hosts, and production infrastructure choices.

## Production Notes

The repository includes production-oriented building blocks:

- Traefik configuration in `traefik/`
- Kubernetes manifests in `k8s/`
- Structured logging support in the backend
- Optional Sentry integration through environment variables

Example production environment values:

```env
DATABASE_URL=postgresql://user:pass@db:5432/openrent
SENTRY_DSN=https://public@sentry.example.com/12345
FRONTEND_ORIGIN=https://openrent.example.com
```

## Roadmap

### Near Term

- Improve production deployment workflows
- Expand backend validation and migration checks
- Strengthen ingestion coverage for additional sources

### Longer Term

- AI-powered rental assistant
- Fraud detection models
- Tenant-rights knowledge support by country
- Multi-language support

## Legal and Compliance

OpenRent EU is intended to align with responsible European data practices:

- GDPR-aware handling
- Source attribution
- Feed-first or authorized ingestion
- No unauthorized scraping

## Contributing

Contributions are welcome.

Typical workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

## License

This project is licensed under the MIT License.

## Vision

OpenRent EU aims to become the unified rental search and comparison layer for Europe, connecting renters, agencies, and platforms through a more transparent and standardized data ecosystem.
