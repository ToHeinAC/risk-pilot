"""File adapter: the only place in M1 that reads from disk."""

from pathlib import Path

from app.model.schema import Model
from app.model.yaml_io import model_from_yaml


def load_model(path: Path) -> Model:
    """Read a UTF-8 YAML model file and validate it."""
    return model_from_yaml(path.read_text(encoding="utf-8"))
