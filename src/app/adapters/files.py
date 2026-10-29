"""File adapter: model files (read, list, copy as template, save atomically) and CSV import."""

import csv
import hashlib
import io
import math
import os
import re
from pathlib import Path

from app.errors import InputError, Issue
from app.model.schema import Model, id_problem
from app.model.yaml_io import model_from_yaml

_MODEL_LINE = re.compile(r"^model:\s*(\S+).*$", re.MULTILINE)
_TEMPLATE = re.compile(r"^# Kopie von ([a-z][a-z0-9_]*)\s*$", re.MULTILINE)


def template_of(text: str) -> str | None:
    """The tutorial a model was copied from (recorded as a comment by ``copy_model``)."""
    found = _TEMPLATE.search(text)
    return found.group(1) if found else None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_model(path: Path) -> Model:
    """Read a UTF-8 YAML model file and validate it."""
    return model_from_yaml(read_text(path))


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def list_models(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.yaml")) if directory.is_dir() else []


def suggest_id(base: str, existing: set[str]) -> str:
    """``base`` if free, else the first free ``base_2``, ``base_3``, …"""
    if base not in existing:
        return base
    number = 2
    while f"{base}_{number}" in existing:
        number += 1
    return f"{base}_{number}"


def create_model_text(directory: Path, new_id: str, text: str) -> Path:
    """Write ``text`` as a new model ``new_id``; never overwrites an existing model."""
    reason = id_problem(new_id)
    if reason:
        raise InputError(Issue("node.id_invalid", params={"id": new_id, "reason": reason}))
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{new_id}.yaml"
    try:
        with target.open("x", encoding="utf-8") as handle:
            handle.write(_MODEL_LINE.sub(f"model: {new_id}", text, count=1))
    except FileExistsError as exc:
        existing = {p.stem for p in list_models(directory)}
        params = {"name": new_id, "suggestion": suggest_id(new_id, existing)}
        raise InputError(Issue("files.exists", params=params)) from exc
    return target


def copy_model(source: Path, directory: Path, new_id: str) -> Path:
    """Copy the model text with a new ID; never overwrites, the source stays byte-identical.

    The copy records its original tutorial in a comment, so the app can tell an unchanged copy
    (analytic overlay applies) from a changed one (notice instead).
    """
    text = read_text(source)
    if template_of(text) is None:
        found = _MODEL_LINE.search(text)
        if found:
            text = f"# Kopie von {found.group(1)}\n{text}"
    return create_model_text(directory, new_id, text)


def save_model_text(path: Path, text: str, expected_hash: str | None) -> None:
    """Write atomically; refuse if the file changed since it was opened (``expected_hash``)."""
    if expected_hash is not None and path.exists() and text_hash(read_text(path)) != expected_hash:
        raise InputError(Issue("files.changed", params={"name": path.name}))
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def _csv_rows(data: bytes) -> tuple[list[list[str]], str]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise InputError(Issue("csv.encoding")) from None
    try:
        delimiter = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t").delimiter
    except (csv.Error, IndexError):
        delimiter = ","
    return list(csv.reader(io.StringIO(text), delimiter=delimiter)), delimiter


def csv_columns(data: bytes) -> list[str]:
    """Header names of an uploaded CSV file."""
    rows, _ = _csv_rows(data)
    return rows[0] if rows else []


def csv_column(data: bytes, column: str) -> tuple[list[float], int]:
    """Numbers of one column and the count of empty cells skipped.

    With ``;`` or tab as delimiter a decimal comma is accepted. A cell that is no number stops
    the import with its line number; nothing is guessed.
    """
    rows, delimiter = _csv_rows(data)
    header = rows[0] if rows else []
    if column not in header:
        raise InputError(Issue("csv.column", params={"column": column, "columns": header}))
    index = header.index(column)
    values: list[float] = []
    skipped = 0
    for line, row in enumerate(rows[1:], start=2):
        cell = row[index].strip() if index < len(row) else ""
        if not cell:
            skipped += 1
            continue
        try:
            value = float(cell.replace(",", ".") if delimiter != "," else cell)
            if not math.isfinite(value):
                raise ValueError(cell)
            values.append(value)
        except ValueError:
            raise InputError(
                Issue("csv.number", line=line, params={"value": cell, "column": column})
            ) from None
    return values, skipped
