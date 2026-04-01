from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.db import Base


class CanonicalListing(Base):
    __tablename__ = "canonical_listings"

    id = Column(Integer, primary_key=True, index=True)

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False, index=True)
    raw_listing_id = Column(Integer, ForeignKey("raw_listings.id"), nullable=False, index=True)

    external_id = Column(String, nullable=False, index=True)
    source_name = Column(String, nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    postal_code = Column(String, nullable=True, index=True)
    street = Column(String, nullable=True)

    monthly_rent = Column(Float, nullable=False, index=True)
    deposit = Column(Float, nullable=True)
    fees = Column(Float, nullable=True, default=0)

    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    size_m2 = Column(Float, nullable=True)

    furnished = Column(Boolean, default=False)
    utilities_included = Column(Boolean, default=False)
    scam_score = Column(Integer, nullable=False, default=0)

    listing_url = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    contact_type = Column(String, nullable=True)

    dedupe_key = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )