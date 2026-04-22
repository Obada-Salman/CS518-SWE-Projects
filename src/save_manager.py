from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from resource_path import get_user_data_path


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class SaveSlotInfo:
    slot: int
    exists: bool
    username: str
    max_unlocked_level: int
    updated_at: str | None


class SaveManager:
    def __init__(self, app_name: str = "vegtable_wars", slot_count: int = 3):
        self.slot_count = max(1, int(slot_count))
        self.save_dir = Path(get_user_data_path(app_name)) / "saves"
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def get_slot_path(self, slot: int) -> Path:
        clamped = self._sanitize_slot(slot)
        return self.save_dir / f"slot_{clamped}.json"

    def list_slots(self) -> list[SaveSlotInfo]:
        slots: list[SaveSlotInfo] = []
        for slot in range(1, self.slot_count + 1):
            payload = self.load_slot(slot)
            if payload is None:
                slots.append(
                    SaveSlotInfo(
                        slot=slot,
                        exists=False,
                        username="",
                        max_unlocked_level=1,
                        updated_at=None,
                    )
                )
                continue

            slots.append(
                SaveSlotInfo(
                    slot=slot,
                    exists=True,
                    username=str(payload.get("username", "player1")),
                    max_unlocked_level=max(1, int(payload.get("max_unlocked_level", 1))),
                    updated_at=payload.get("updated_at"),
                )
            )

        return slots

    def load_slot(self, slot: int) -> dict[str, Any] | None:
        path = self.get_slot_path(slot)
        if not path.exists():
            return None

        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return None

        if not isinstance(content, dict):
            return None

        return content

    def save_slot(self, slot: int, payload: dict[str, Any]) -> None:
        path = self.get_slot_path(slot)
        cleaned = self._normalize_payload(payload)
        path.write_text(json.dumps(cleaned, indent=2), encoding="utf-8")

    def delete_slot(self, slot: int) -> bool:
        path = self.get_slot_path(slot)
        if not path.exists():
            return False
        path.unlink()
        return True

    def _sanitize_slot(self, slot: int) -> int:
        try:
            parsed = int(slot)
        except (TypeError, ValueError):
            parsed = 1
        return min(max(parsed, 1), self.slot_count)

    def _normalize_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        username = str(payload.get("username", "player1")).strip() or "player1"
        max_unlocked_level = max(1, int(payload.get("max_unlocked_level", 1)))
        water_collected = int(payload.get("water_collected", 0))
        sunlight_collected = int(payload.get("sunlight_collected", 0))
        nutrients_collected = int(payload.get("nutrients_collected", 0))
        current_story_level = int(payload.get("current_story_level", 1))

        return {
            "username": username[:32],
            "max_unlocked_level": max_unlocked_level,
            "water_collected": max(0, water_collected),
            "sunlight_collected": max(0, sunlight_collected),
            "nutrients_collected": max(0, nutrients_collected),
            "current_story_level": max(1, current_story_level),
            "updated_at": _now_utc_iso(),
        }