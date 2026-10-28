"""Locations of user data and tutorials, configurable by environment variables."""

import os
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]


def data_dir() -> Path:
    """Runtime data (gitignored); ``RISK_PILOT_DATA_DIR``, default ``data/``."""
    return Path(os.environ.get("RISK_PILOT_DATA_DIR", "data"))


def models_dir() -> Path:
    return data_dir() / "models"


def runs_dir() -> Path:
    return data_dir() / "runs"


def examples_dir() -> Path:
    """Versioned tutorials; ``RISK_PILOT_EXAMPLES_DIR``, default ``examples/`` of the repo."""
    return Path(os.environ.get("RISK_PILOT_EXAMPLES_DIR", str(_REPO / "examples")))
