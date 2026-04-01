from sqlalchemy.orm import Session

from app.models.canonical_listing import CanonicalListing  # ORM model for DB ops
from app.models.raw_listing import RawListing
from app.services.dedupe import build_dedupe_key


def normalize_raw_listing(
    db: Session,
    source_id: int,
    source_name: str,
    raw_listing: RawListing,
    payload: dict,
) -> CanonicalListing:  # return the ORM instance, not a Pydantic schema
    title = str(payload.get("title", "")).strip()
    city = str(payload.get("city", "")).strip()
    country = str(payload.get("country", "")).strip()
    postal_code = str(payload.get("postal_code", "")).strip() or None
    street = str(payload.get("street", "")).strip() or None
    description = str(payload.get("description", "")).strip() or None
    listing_url = str(payload.get("listing_url", "")).strip() or None
    contact_name = str(payload.get("contact_name", "")).strip() or None
    contact_type = str(payload.get("contact_type", "")).strip() or None
    external_id = str(payload.get("external_id", "")).strip()

    monthly_rent = float(payload.get("monthly_rent", 0) or 0)
    deposit = float(payload.get("deposit", 0) or 0)
    fees = float(payload.get("fees", 0) or 0)

    bedrooms = int(payload.get("bedrooms", 0) or 0)
    bathrooms = int(payload.get("bathrooms", 0) or 0)
    size_m2 = float(payload.get("size_m2", 0) or 0)
    scam_score = int(payload.get("scam_score", 0) or 0)

    furnished = bool(payload.get("furnished", False))
    utilities_included = bool(payload.get("utilities_included", False))

    dedupe_key = build_dedupe_key(
        title=title,
        city=city,
        street=street,
        postal_code=postal_code,
        monthly_rent=monthly_rent,
    )

    existing = (
        db.query(CanonicalListing)
        .filter(CanonicalListing.dedupe_key == dedupe_key)
        .first()
    )

    if existing:
        existing.source_id = source_id
        existing.raw_listing_id = raw_listing.id
        existing.external_id = external_id
        existing.source_name = source_name
        existing.title = title
        existing.description = description
        existing.country = country
        existing.city = city
        existing.postal_code = postal_code
        existing.street = street
        existing.monthly_rent = monthly_rent
        existing.deposit = deposit
        existing.fees = fees
        existing.bedrooms = bedrooms
        existing.bathrooms = bathrooms
        existing.size_m2 = size_m2
        existing.furnished = furnished
        existing.utilities_included = utilities_included
        existing.scam_score = scam_score
        existing.listing_url = listing_url
        existing.contact_name = contact_name
        existing.contact_type = contact_type
        existing.is_active = True

        db.commit()
        db.refresh(existing)
        return existing

    item = CanonicalListing(  # use the ORM model, not the Pydantic schema
        source_id=source_id,
        raw_listing_id=raw_listing.id,
        external_id=external_id,
        source_name=source_name,
        title=title,
        description=description,
        country=country,
        city=city,
        postal_code=postal_code,
        street=street,
        monthly_rent=monthly_rent,
        deposit=deposit,
        fees=fees,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        size_m2=size_m2,
        furnished=furnished,
        utilities_included=utilities_included,
        scam_score=scam_score,
        listing_url=listing_url,
        contact_name=contact_name,
        contact_type=contact_type,
        dedupe_key=dedupe_key,
        is_active=True,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item