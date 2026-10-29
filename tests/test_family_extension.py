"""A distribution family registered in a test works without changes to engine or UI (M6 AK 5)."""

from collections.abc import Mapping
from typing import ClassVar, Literal

import numpy as np
import pytest
from nicegui.testing import User
from scipy import stats
from web_util import drive, open_model, value

from app.adapters import files, settings
from app.analysis.analytic import dkw_epsilon, ks_distance
from app.dists import registry
from app.dists.base import FloatArray, Frozen, Params, ParamSpec, Violation, violation
from app.engine.simulate import simulate
from app.messages import t
from app.model import form
from app.model.compile import compile_model
from app.model.yaml_io import model_from_yaml
from app.model.yaml_patch import load_data
from app.present.preview import node_preview

N = 20_000
TEXT = (
    "schema_version: 1\nmodel: logistik\nsettings: {seed: 4}\nnodes:\n"
    "  x: {type: uncertain, dist: test_logistik, loc: 5, scale: 2}\n"
    "  y: {type: output, expr: 'x'}\n"
)


class Logistic:
    """Only the ``Family`` protocol, no base class from the app."""

    name = "test_logistik"
    kind: Literal["continuous"] = "continuous"
    modes: ClassVar[Mapping[str, tuple[ParamSpec, ...]]] = {
        "params": (ParamSpec("loc"), ParamSpec("scale"))
    }

    def to_canonical(self, mode: str, p: Params) -> dict[str, FloatArray]:
        return {k: np.asarray(v, dtype=np.float64) for k, v in p.items()}

    def check(self, mode: str, p: Params) -> list[Violation]:
        return [violation("scale", "scale > 0", p["scale"] <= 0)]

    def ppf(self, u: FloatArray, c: Params) -> FloatArray:
        return np.asarray(c["loc"] + c["scale"] * np.log(u / (1 - u)), dtype=np.float64)

    def reference(self, c: Mapping[str, float]) -> Frozen:
        return stats.logistic(loc=c["loc"], scale=c["scale"])


@pytest.fixture(autouse=True)
def _registered(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(registry._REGISTRY, Logistic.name, Logistic())  # pyright: ignore[reportPrivateUsage]


def test_new_family_compiles_simulates_and_passes_ks() -> None:
    x = simulate(compile_model(model_from_yaml(TEXT)), n=N).samples["y"]
    reference = Logistic().reference({"loc": 5, "scale": 2})
    assert ks_distance(x, reference.cdf) < dkw_epsilon(N)


def test_new_family_in_form_and_preview() -> None:
    data = load_data(TEXT)
    assert [s.name for s in form.param_fields(data, "x")] == ["loc", "scale"]
    assert "test_logistik" in registry.families()
    p = node_preview(compile_model(model_from_yaml(TEXT)), "x", n=N)
    assert p.median == pytest.approx(5, abs=0.1)


def test_new_family_card_shows_its_fields() -> None:
    files.create_model_text(settings.models_dir(), "logistik", TEXT)

    async def steps(user: User) -> None:
        await open_model(user, "logistik")
        user.find(marker="nodes").trigger("pick", "x")
        await user.should_see(marker="form.x.param.scale")
        assert value(user, "form.x.dist") == "test_logistik"
        assert value(user, "form.x.param.loc") == "5"
        assert value(user, "form.x.param.scale") == "2"
        await user.should_see(t("form.preview"))

    drive(steps)
