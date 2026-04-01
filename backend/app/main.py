from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
from pythonjsonlogger import jsonlogger
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.core.config import settings
from app.core.db import Base, engine
from app.routers.ingest import router as ingest_router
from app.routers.listings import router as listings_router


# Ensure DB tables exist for simple deployments (Alembic is used for migrations)
Base.metadata.create_all(bind=engine)


# Structured JSON logging setup
root_logger = logging.getLogger()
if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
    handler = logging.StreamHandler()
    fmt = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(fmt)
    root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)


app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
)

# Alias for common typo when launching uvicorn (allows `app.main:aap`)
aap = app

# Initialize Sentry if DSN provided
if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=settings.sentry_traces_sample_rate, environment=settings.environment)
    app.add_middleware(SentryAsgiMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(listings_router)


@app.get("/")
def root():
    return {"message": "OpenRent EU API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}