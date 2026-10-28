"""Correlation groups: checks (never repairs), Spearman -> latent correlation, matrix factor."""

# numpy stubs mark ArrayLike as partially Unknown under pythonVersion 3.11 (Buffer type).
# pyright: reportUnknownMemberType=false
from collections import Counter
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from app.dists.registry import get_family
from app.errors import Issue, Notice
from app.model.schema import CorrelationGroup, EventNode, Model, UncertainNode

EIGEN_TOLERANCE = -1e-10
MEMBER_TYPES = ("uncertain", "event")


@dataclass(frozen=True)
class Group:
    id: str
    nodes: tuple[str, ...]
    spearman: NDArray[np.float64]
    factor: NDArray[np.float64]  # F with F Fᵀ = latent matrix; z' = F z


def latent(spearman: NDArray[np.float64]) -> NDArray[np.float64]:
    """Pearson correlation of the copula's normals for a target Spearman ρ: 2 sin(π ρ / 6)."""
    return 2 * np.sin(np.pi * spearman / 6)


def factor(matrix: NDArray[np.float64]) -> NDArray[np.float64]:
    """Cholesky factor; for singular (semidefinite) matrices a symmetric root."""
    try:
        return np.linalg.cholesky(matrix)
    except np.linalg.LinAlgError:
        values, vectors = np.linalg.eigh(matrix)
        return vectors * np.sqrt(np.clip(values, 0.0, None))


def _member_issues(model: Model, gid: str, group: CorrelationGroup) -> list[Issue]:
    base = {"group": gid}
    if len(group.nodes) < 2:
        return [Issue("corr.too_small", params=base)]
    issues: list[Issue] = []
    for name in group.nodes:
        node = model.nodes.get(name)
        if node is None:
            issues.append(Issue("corr.node_unknown", params={**base, "name": name}))
        elif node.type not in MEMBER_TYPES:
            issues.append(Issue("corr.node_type", name, params={**base, "type": node.type}))
    return issues


def _first_asymmetry(m: NDArray[np.float64]) -> tuple[int, int] | None:
    rows, cols = np.nonzero(m != m.T)
    return (int(rows[0]) + 1, int(cols[0]) + 1) if rows.size else None


def matrix_issues(gid: str, k: int, rows: list[list[float]]) -> list[Issue]:
    """Shape, diagonal, range, symmetry and positive semidefiniteness (input and latent)."""
    base = {"group": gid, "k": k}
    if len(rows) != k or any(len(r) != k for r in rows):
        return [Issue("corr.shape", params=base)]
    m = np.array(rows, dtype=np.float64)
    if np.any(np.diag(m) != 1.0):
        return [Issue("corr.diagonal", params=base)]
    if np.any(np.abs(m) > 1.0):
        return [Issue("corr.range", params=base)]
    asym = _first_asymmetry(m)
    if asym is not None:
        return [Issue("corr.asymmetric", params={**base, "row": asym[0], "col": asym[1]})]
    for code, matrix in (("corr.not_psd", m), ("corr.latent_not_psd", latent(m))):
        smallest = float(np.linalg.eigvalsh(matrix).min())
        if smallest < EIGEN_TOLERANCE:
            return [Issue(code, params={**base, "eig": f"{smallest:.4f}".replace(".", ",")})]
    return []


def _discrete(model: Model, name: str) -> bool:
    node = model.nodes[name]
    if isinstance(node, EventNode):
        return True
    family = get_family(node.dist) if isinstance(node, UncertainNode) else None
    return family is not None and family.kind == "discrete"


def check_groups(model: Model) -> tuple[list[Group], list[Issue], list[Notice]]:
    """Validated groups, the problems found and hints (discrete members tie)."""
    groups: list[Group] = []
    issues: list[Issue] = []
    notices: list[Notice] = []
    counts = Counter(n for g in model.correlations.values() for n in set(g.nodes))
    for name, count in sorted(counts.items()):
        if count > 1:
            owners = [gid for gid, g in model.correlations.items() if name in g.nodes]
            issues.append(Issue("corr.node_twice", name, params={"groups": owners}))
    for gid, group in model.correlations.items():
        found = _member_issues(model, gid, group) or matrix_issues(
            gid, len(group.nodes), group.spearman
        )
        if found:
            issues += found
            continue
        m = np.array(group.spearman, dtype=np.float64)
        groups.append(Group(gid, tuple(group.nodes), m, factor(latent(m))))
        ties = [n for n in group.nodes if _discrete(model, n)]
        if ties:
            notices.append(Notice("corr.discrete_ties", params={"group": gid, "nodes": ties}))
    return groups, issues, notices
