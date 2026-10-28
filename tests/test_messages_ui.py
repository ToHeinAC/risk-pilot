"""Every UI text used in the code has a German template (M2 AK 8)."""

import re
from pathlib import Path

import pytest

from app.messages import UI, t

SRC = Path(__file__).resolve().parent.parent / "src" / "app"
KEY = re.compile(r'\bt\(\s*f?"([a-z_]+\.[a-z_]+)"')
DYNAMIC = re.compile(r'\bt\(\s*f"([a-z_]+\.[a-z_]*)\{')


def used_keys() -> set[str]:
    keys: set[str] = set()
    for path in SRC.rglob("*.py"):
        keys |= set(KEY.findall(path.read_text(encoding="utf-8")))
    return keys


def test_all_used_keys_exist() -> None:
    assert used_keys() - set(UI["de"]) == set()


def test_dynamic_lesson_check_keys_exist() -> None:
    for path in SRC.rglob("*.py"):
        for prefix in DYNAMIC.findall(path.read_text(encoding="utf-8")):
            assert any(k.startswith(prefix) for k in UI["de"]), prefix
    for kind in ("ks", "mean", "share", "var"):
        assert f"lesson.check_{kind}" in UI["de"]


@pytest.mark.parametrize("key", sorted(UI["de"]))
def test_templates_have_no_english_placeholder_text(key: str) -> None:
    template = UI["de"][key]
    assert template.strip()
    assert "TODO" not in template


def test_unknown_language_falls_back() -> None:
    assert t("ui.save", lang="en") == "Speichern"
