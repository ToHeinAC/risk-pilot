"""Scenario edits on the draft text; no UI import (M7 step 4)."""

from collections.abc import Callable

from app.errors import ModelError
from app.messages import render
from app.model.schema import Model
from app.model.yaml_io import model_from_yaml, model_to_yaml
from app.model.yaml_patch import patch
from app.present.validation import check_text


def apply(text: str, change: Callable[[Model], Model]) -> tuple[str, str | None]:
    """(new draft, None), or the unchanged draft and why the change was refused.

    A change is kept only if the result is a valid model; comments and layout stay (M6 E4).
    """
    try:
        changed = change(model_from_yaml(text))
    except (ValueError, ModelError) as exc:
        issues = exc.issues if isinstance(exc, ModelError) else []
        return text, "; ".join(render(i) for i in issues) or str(exc)
    problems = check_text(model_to_yaml(changed)).rows
    if problems:
        return text, "; ".join(row.message for row in problems)
    return patch(text, changed.model_dump(mode="json", exclude_unset=True)), None
