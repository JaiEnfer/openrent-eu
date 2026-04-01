import csv
import io

from app.adapters.base import BaseAdapter


class CSVAdapter(BaseAdapter):
    def load(self, file_path: str) -> list[dict]:
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            content = file.read()
        return self.load_from_text(content)

    def load_from_text(self, content: str) -> list[dict]:
        rows = []
        file_like = io.StringIO(content)
        reader = csv.DictReader(file_like)

        for row in reader:
            rows.append(
                {
                    "external_id": row.get("external_id", "").strip(),
                    "title": row.get("title", "").strip(),
                    "description": row.get("description", "").strip(),
                    "country": row.get("country", "").strip(),
                    "city": row.get("city", "").strip(),
                    "postal_code": row.get("postal_code", "").strip(),
                    "street": row.get("street", "").strip(),
                    "monthly_rent": float(row.get("monthly_rent", 0) or 0),
                    "deposit": float(row.get("deposit", 0) or 0),
                    "fees": float(row.get("fees", 0) or 0),
                    "bedrooms": int(row.get("bedrooms", 0) or 0),
                    "bathrooms": int(row.get("bathrooms", 0) or 0),
                    "size_m2": float(row.get("size_m2", 0) or 0),
                    "furnished": str(row.get("furnished", "false")).lower() == "true",
                    "utilities_included": str(row.get("utilities_included", "false")).lower() == "true",
                    "scam_score": int(row.get("scam_score", 0) or 0),
                    "listing_url": row.get("listing_url", "").strip(),
                    "contact_name": row.get("contact_name", "").strip(),
                    "contact_type": row.get("contact_type", "").strip(),
                }
            )

        return rows