"""Stored simulation runs in ``data/runs/<UTC time>_<model>_<hash8>/``."""

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from app.engine.simulate import SimulationResult

FORMAT_VERSION = 1


@dataclass(frozen=True)
class StoredRun:
    path: Path
    meta: dict[str, Any]
    model_text: str
    samples: dict[str, NDArray[Any]]
    summary: dict[str, Any]


def _folder_name(meta: Mapping[str, object]) -> str:
    stamp = str(meta["timestamp"]).replace("-", "").replace(":", "").replace("+0000", "Z")
    return f"{stamp}_{meta['model_id']}_{str(meta['model_hash'])[:8]}"


def _free_path(directory: Path, name: str) -> Path:
    path, number = directory / name, 2
    while path.exists():
        path, number = directory / f"{name}_{number}", number + 1
    return path


def save_run(
    directory: Path,
    meta: Mapping[str, object],
    model_text: str,
    samples: Mapping[str, NDArray[Any]],
    summary: Mapping[str, object],
    extra: Mapping[str, object],
) -> Path:
    """Write a run atomically (temporary folder, then rename) and return its folder."""
    directory.mkdir(parents=True, exist_ok=True)
    target = _free_path(directory, _folder_name(meta))
    temporary = target.with_name(target.name + ".tmp")
    temporary.mkdir()
    full_meta = {**meta, **extra, "format_version": FORMAT_VERSION}
    (temporary / "meta.json").write_text(json.dumps(full_meta, indent=2), encoding="utf-8")
    (temporary / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (temporary / "model.yaml").write_text(model_text, encoding="utf-8")
    np.savez_compressed(temporary / "samples.npz", **samples)  # pyright: ignore[reportUnknownMemberType, reportArgumentType]
    os.replace(temporary, target)
    return target


def _meta(path: Path) -> dict[str, Any]:
    return json.loads((path / "meta.json").read_text(encoding="utf-8"))


def list_runs(directory: Path, model_id: str | None = None) -> list[Path]:
    """Run folders, newest first; optionally only those of one model."""
    if not directory.is_dir():
        return []
    folders = [p for p in directory.iterdir() if p.is_dir() and not p.name.endswith(".tmp")]
    if model_id is not None:
        folders = [p for p in folders if _meta(p).get("model_id") == model_id]
    return sorted(folders, key=lambda p: p.name, reverse=True)


def load_run(path: Path) -> StoredRun:
    with np.load(path / "samples.npz") as data:
        samples = {key: data[key] for key in data.files}
    summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
    model_text = (path / "model.yaml").read_text(encoding="utf-8")
    return StoredRun(path, _meta(path), model_text, samples, summary)


def as_result(stored: StoredRun) -> SimulationResult:
    """The stored run as a simulation result (for the result view)."""
    return SimulationResult(stored.samples, stored.meta, {}, ())
