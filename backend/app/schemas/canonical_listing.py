from pydantic import BaseModel


class CanonicalListingOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    country: str
    city: str
    postal_code: str | None = None
    street: str | None = None
    monthly_rent: float
    deposit: float | None = None
    fees: float | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    size_m2: float | None = None
    furnished: bool
    utilities_included: bool
    scam_score: int
    listing_url: str | None = None
    source_name: str
    contact_name: str | None = None
    contact_type: str | None = None

    class Config:
        from_attributes = True