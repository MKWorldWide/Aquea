import json
import os
import tempfile
from pathlib import Path

from ledger import Ledger


def test_ledger_appends_and_chains():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "ledger.jsonl"
        ledger = Ledger(path)

        payload1 = {"a": 1}
        h1 = ledger.append(payload1)
        assert isinstance(h1, str) and len(h1) > 8
        assert ledger.count() == 1

        payload2 = {"a": 2}
        h2 = ledger.append(payload2)
        assert h2 != h1
        assert ledger.count() == 2

        # Ensure file contains chained entries
        lines = path.read_text(encoding="utf-8").splitlines()
        e1 = json.loads(lines[0])
        e2 = json.loads(lines[1])
        assert e1["record_hash"] == h1
        assert e2["prev"] == h1


def test_adapter_nesshash_env_toggle(monkeypatch):
    # Ensure fallback works even if nesshash import fails
    monkeypatch.setenv("NESSHASH_BACKEND", "nesshash")
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "ledger.jsonl"
        ledger = Ledger(path)
        h = ledger.append({"x": 1})
        assert isinstance(h, str)



