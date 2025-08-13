import os
import importlib


def test_fallback_blake2b(monkeypatch):
    monkeypatch.setenv("NESSHASH_BACKEND", "auto")
    # Force import path
    mod = importlib.import_module("nesshash_adapter")
    h = mod.hash_record({"a": 1}, None)
    assert isinstance(h, str)
    assert len(h) >= 16



