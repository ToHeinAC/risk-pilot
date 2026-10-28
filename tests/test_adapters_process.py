"""App shutdown and Streamlit configuration (M2 AK 1, 7)."""

import os
import signal
import tomllib
from pathlib import Path

import pytest

from app.adapters import process

ROOT = Path(__file__).resolve().parent.parent


def test_shutdown_sends_sigterm_to_own_pid(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[int, int]] = []
    monkeypatch.setattr(os, "kill", lambda pid, sig: calls.append((pid, sig)))
    process.shutdown()
    assert calls == [(os.getpid(), signal.SIGTERM)]


def test_streamlit_port_is_not_default() -> None:
    config = tomllib.loads((ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
    assert config["server"]["port"] == 8642
    assert config["server"]["headless"] is True
    assert config["browser"]["gatherUsageStats"] is False
