import json

from fastapi import APIRouter, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.adapters.csv_adapter import CSVAdapter
from app.core.db import SessionLocal
from app.models.raw_listing import RawListing
from app.models.source import Source
from app.services.normalization import normalize_raw_listing

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/csv")
def ingest_csv_from_sample():
    db: Session = SessionLocal()

    try:
        source = db.query(Source).filter(Source.name == "csv_import").first()
        if not source:
            raise HTTPException(status_code=400, detail="Source 'csv_import' not found")

        adapter = CSVAdapter()
        rows = adapter.load("data/sample_listings.csv")

        imported_count = 0

        for row in rows:
            external_id = row.get("external_id")
            if not external_id:
                continue

            raw = RawListing(
                source_id=source.id,
                external_id=external_id,
                raw_payload=json.dumps(row),
                listing_url=row.get("listing_url"),
            )
            db.add(raw)
            db.commit()
            db.refresh(raw)

            normalize_raw_listing(
                db=db,
                source_id=source.id,
                source_name=source.name,
                raw_listing=raw,
                payload=row,
            )

            imported_count += 1

        return {
            "message": "Sample CSV import completed",
            "imported_count": imported_count,
        }

    finally:
        db.close()


@router.post("/csv-upload")
async def ingest_uploaded_csv(file: UploadFile = File(...)):
    db: Session = SessionLocal()

    try:
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Please upload a CSV file")

        source = db.query(Source).filter(Source.name == "csv_import").first()
        if not source:
            raise HTTPException(status_code=400, detail="Source 'csv_import' not found")

        content = await file.read()
        text = content.decode("utf-8-sig")

        adapter = CSVAdapter()
        rows = adapter.load_from_text(text)

        imported_count = 0
        skipped_count = 0

        for row in rows:
            external_id = row.get("external_id")
            title = row.get("title")
            city = row.get("city")
            country = row.get("country")

            if not external_id or not title or not city or not country:
                skipped_count += 1
                continue

            raw = RawListing(
                source_id=source.id,
                external_id=external_id,
                raw_payload=json.dumps(row),
                listing_url=row.get("listing_url"),
            )
            db.add(raw)
            db.commit()
            db.refresh(raw)

            normalize_raw_listing(
                db=db,
                source_id=source.id,
                source_name=source.name,
                raw_listing=raw,
                payload=row,
            )

            imported_count += 1

        return {
            "message": "Uploaded CSV import completed",
            "filename": file.filename,
            "imported_count": imported_count,
            "skipped_count": skipped_count,
        }

    finally:
        db.close()