"""Registry of distribution families by YAML name."""

from app.dists.base import Family
from app.dists.families import BUILTIN

_REGISTRY: dict[str, Family] = {}


def register(family: Family) -> None:
    """Make ``family`` available under ``family.name`` (also for new families, M6)."""
    _REGISTRY[family.name] = family


def get_family(name: str) -> Family | None:
    return _REGISTRY.get(name)


def families() -> list[str]:
    return list(_REGISTRY)


for _family in BUILTIN:
    register(_family)
