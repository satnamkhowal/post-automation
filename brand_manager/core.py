from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from secrets import token_urlsafe


@dataclass(frozen=True)
class Location:
    id: str
    name: str
    address: str
    brand_id: str


@dataclass(frozen=True)
class Brand:
    id: str
    name: str
    locations: tuple[Location, ...]


class DemoProvider:
    """Safe local provider; no network calls and no live publication."""

    def __init__(self) -> None:
        self.brands = (
            Brand("demo-brand", "Demo Brand", (Location("demo-location", "Demo Location", "Local only", "demo-brand"),)),
        )
        self.published: list[dict] = []

    def list_brands(self) -> list[dict]:
        return [{"id": b.id, "name": b.name, "locations": len(b.locations)} for b in self.brands]

    def list_locations(self, brand_id: str) -> list[dict]:
        brand = next((b for b in self.brands if b.id == brand_id), None)
        if not brand:
            raise ValueError("Unknown brand")
        return [{"id": l.id, "name": l.name, "address": l.address} for l in brand.locations]

    def get_profile(self, location_id: str) -> dict:
        for brand in self.brands:
            for loc in brand.locations:
                if loc.id == location_id:
                    return {"id": loc.id, "name": loc.name, "address": loc.address, "brand_id": brand.id, "source": "demo"}
        raise ValueError("Unknown location")

    def publish(self, preview: dict) -> dict:
        result = {**preview, "published_at": datetime.now(timezone.utc).isoformat(), "source": "demo"}
        self.published.append(result)
        return result


class DraftStore:
    def __init__(self) -> None:
        self._drafts: dict[str, dict] = {}

    def create(self, location_id: str, text: str, call_to_action: str | None) -> dict:
        token = token_urlsafe(18)
        preview = {"location_id": location_id, "text": text, "call_to_action": call_to_action, "confirmation_token": token}
        self._drafts[token] = preview
        return preview

    def confirm(self, token: str, confirm: bool) -> dict:
        if not confirm:
            raise ValueError("Explicit confirm=true is required")
        if token not in self._drafts:
            raise ValueError("Invalid or already used confirmation token")
        return self._drafts.pop(token)

