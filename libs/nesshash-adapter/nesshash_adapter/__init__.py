
# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations
import os, json, hashlib

def _canonical(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")

def hash_record(payload: dict, prev_hash: str | None = None) -> str:
    """
    Returns a hex digest over the canonicalized payload, optionally chaining to prev_hash.
    If env NESSHASH_BACKEND == 'nesshash' and library present, use it.
    """
    backend = os.getenv("NESSHASH_BACKEND", "auto")
    data = {"payload": payload, "prev": prev_hash}
    try:
        if backend in ("auto", "nesshash"):
            import nesshash  # type: ignore
            # Assume nesshash has a simple API; adapt as needed in real integration.
            return nesshash.hash_bytes(_canonical(data))
    except Exception:
        pass

    # Fallback: BLAKE2b (fast, strong) with personalization
    h = hashlib.blake2b(person=b"AQUEA-LEDGER")
    h.update(_canonical(data))
    return h.hexdigest()
