from app.core.db import Base, SessionLocal, engine
from app.models.source import Source

Base.metadata.create_all(bind=engine)

db = SessionLocal()

existing = db.query(Source).filter(Source.name == "csv_import").first()

if not existing:
    db.add(
        Source(
            name="csv_import",
            source_type="csv",
            base_url=None,
            is_active=True,
        )
    )
    db.commit()

db.close()
print("Sources seeded successfully.")