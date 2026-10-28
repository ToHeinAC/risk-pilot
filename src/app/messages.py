"""Message catalogue: code -> template per language, and rendering."""

from collections.abc import Mapping, Sequence
from typing import cast

from app.errors import Issue, Notice

_DE: dict[str, str] = {
    "yaml.syntax": "YAML ist nicht lesbar{at_line}: {problem}.",
    "yaml.duplicate_key": "Der Schlüssel „{key}“ kommt doppelt vor{at_line}.",
    "model.schema": "Ungültige Angabe bei {loc}: {msg}.",
    "model.schema_version": "Schema-Version {version} wird nicht unterstützt (erwartet: 1).",
    "model.no_output": "Das Modell braucht mindestens einen Knoten vom Typ „output“.",
    "model.empty": "Das Modell enthält noch keine Knoten.",
    "node.id_invalid": "Die ID „{id}“ ist nicht zulässig: {reason}.",
    "dist.unknown": "{node}: Unbekannte Verteilung „{dist}“. Verfügbar: {known}.",
    "dist.mode_unknown": "{node}: Verteilung „{dist}“ kennt den Eingabemodus „{mode}“ nicht "
    "(möglich: {modes}).",
    "param.missing": "{node}: Parameter „{field}“ fehlt für {dist} im Modus „{mode}“.",
    "param.unknown": "{node}: Parameter „{field}“ gehört nicht zu {dist} im Modus „{mode}“ "
    "(erlaubt: {allowed}).",
    "param.invalid": "{node}: Parameter „{field}“ = {value} ist ungültig, verlangt ist {rule}.",
    "expr.syntax": "{node}: Ausdruck „{expr}“ ist nicht lesbar: {problem}.",
    "expr.forbidden": "{node}: „{construct}“ ist in Ausdrücken nicht erlaubt. {hint}",
    "expr.unknown_name": "{node}: Unbekannter Name „{name}“. {suggestion}",
    "expr.unknown_function": "{node}: Unbekannte Funktion „{name}“.",
    "expr.arity": "{node}: {name}() erwartet {expected} Argumente, erhalten: {got}.",
    "expr.type": "{node}: {context} erwartet {expected}, erhalten: {got}.",
    "expr.too_long": "{node}: Ausdruck ist {length} Zeichen lang (höchstens {limit}).",
    "expr.too_deep": "{node}: Ausdruck ist {depth} Ebenen tief verschachtelt (höchstens {limit}).",
    "expr.too_large": "{node}: Ausdruck hat {size} Bestandteile (höchstens {limit}).",
    "expr.unknown_label": "{node}: „{label}“ ist keine Option von „{choice}“ (Optionen: {labels}).",
    "expr.choice_usage": "{node}: Auswahl „{choice}“ darf nur mit == oder != gegen eine Option "
    'verglichen werden, z. B. {choice} == "…".',
    "expr.interp_table": "{node}: Tabelle von interp() ist ungültig: {reason}.",
    "graph.cycle": "Zyklus zwischen Knoten: {cycle}.",
    "sim.n_range": "Anzahl Iterationen {n} ist keine ganze Zahl zwischen 1 und 2 000 000.",
    "sim.seed_range": "Seed {seed} ist keine ganze Zahl ≥ 0.",
    "runtime.param_invalid": "{node}: Parameter „{field}“ verletzt {rule} in {share_pct} "
    "der Iterationen.",
    "runtime.non_finite": "{node}: Ergebnis ist in {share_pct} der Iterationen nicht endlich "
    "(z. B. log(0) oder Division durch 0).",
    "runtime.clip_bounds": "{node}: clip() mit Untergrenze über Obergrenze in {share_pct} "
    "der Iterationen.",
    "range.violation": "{node}: {below} der Werte liegen unter dem zulässigen Minimum, "
    "{above} über dem Maximum. Die Werte wurden nicht verändert.",
    "uniform.degenerate": "{node}: Gleichverteilung mit gleichen Grenzen, wird als Konstante "
    "{value} ausgewertet.",
    "stats.single_sample": "Nur eine Iteration: kein Standardfehler bestimmbar.",
    "stats.quantile_range": "Quantil {q} liegt nicht strikt zwischen 0 und 1.",
}

CATALOG: dict[str, dict[str, str]] = {"de": _DE}

_SHARE_KEYS = ("below", "above")


def percent(share: float) -> str:
    """Format a share in [0, 1] as German percent text, e.g. 0.025 -> '2,5 %'."""
    return f"{share * 100:.3g} %".replace(".", ",")


def _format(key: str, value: object) -> str:
    if isinstance(value, list | tuple):
        items = [str(v) for v in cast(Sequence[object], value)]
        return (" → " if key == "cycle" else ", ").join(items)
    if key in _SHARE_KEYS and isinstance(value, float):
        return percent(value)
    return str(value)


def _fields(item: Issue | Notice) -> Mapping[str, str]:
    line = item.line if isinstance(item, Issue) else None
    values = {k: _format(k, v) for k, v in item.params.items()}
    return {
        "node": f"Knoten „{item.node_id}“" if item.node_id else "Modell",
        "field": (item.field if isinstance(item, Issue) else None) or "",
        "line": str(line or ""),
        "at_line": f" in Zeile {line}" if line else "",
        "share_pct": percent(item.share) if item.share is not None else "einem Teil",
        **values,
    }


def render(item: Issue | Notice, lang: str = "de") -> str:
    """Return the message text for an issue or notice; unknown languages fall back to German."""
    catalog = CATALOG.get(lang, CATALOG["de"])
    template = catalog.get(item.code) or CATALOG["de"][item.code]
    return template.format_map(_fields(item))
