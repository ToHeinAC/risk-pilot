"""App shutdown (M2 AK 1)."""

import os
import signal

import pytest

from app.adapters import process


def test_shutdown_sends_sigterm_to_own_pid(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[int, int]] = []
    monkeypatch.setattr(os, "kill", lambda pid, sig: calls.append((pid, sig)))
    process.shutdown()
    assert calls == [(os.getpid(), signal.SIGTERM)]
