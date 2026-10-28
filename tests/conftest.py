"""Shared fixtures. The suite is offline: any socket connect raises."""

import socket

import pytest


@pytest.fixture(autouse=True)
def _block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("tests must stay offline; use synthetic fixtures")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)


@pytest.fixture(autouse=True)
def _data_dir(tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch) -> None:
    """No test writes to the real data/ directory."""
    monkeypatch.setenv("RISK_PILOT_DATA_DIR", str(tmp_path_factory.mktemp("data")))
