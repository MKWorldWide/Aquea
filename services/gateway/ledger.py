
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
import json, pathlib
from typing import Optional
from nesshash_adapter import hash_record

class Ledger:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._last_hash: Optional[str] = None
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                try:
                    entry = json.loads(line)
                    self._last_hash = entry["record_hash"]
                except Exception:
                    continue

    def append(self, payload: dict) -> str:
        rec_hash = hash_record(payload, self._last_hash)
        entry = {"payload": payload, "record_hash": rec_hash, "prev": self._last_hash}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")
        self._last_hash = rec_hash
        return rec_hash

    def count(self) -> int:
        if not self.path.exists():
            return 0
        return sum(1 for _ in self.path.open("r", encoding="utf-8"))
