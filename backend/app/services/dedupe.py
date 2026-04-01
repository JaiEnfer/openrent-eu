from app.utils.text import clean_text


def build_dedupe_key(
    title: str,
    city: str,
    street: str | None,
    postal_code: str | None,
    monthly_rent: float,
) -> str:
    title_part = clean_text(title)
    city_part = clean_text(city)
    street_part = clean_text(street)
    postal_part = clean_text(postal_code)
    rent_part = str(int(monthly_rent)) if monthly_rent is not None else "0"

    return f"{title_part}|{city_part}|{street_part}|{postal_part}|{rent_part}"