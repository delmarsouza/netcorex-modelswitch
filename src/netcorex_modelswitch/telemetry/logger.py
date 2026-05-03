from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from netcorex_modelswitch.telemetry.events import TokenLedgerEvent


class TelemetryLogger:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: TokenLedgerEvent, extra: dict[str, Any] | None = None) -> None:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event": asdict(event),
            "extra": extra or {},
        }
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
