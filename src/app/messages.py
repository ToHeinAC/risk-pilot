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
    "files.exists": "Ein Modell „{name}“ gibt es schon. Vorschlag: „{suggestion}“.",
    "files.changed": "Die Datei „{name}“ wurde seit dem Öffnen verändert. Bitte neu laden.",
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


# Texts of the user interface (not issues): key -> template, rendered with ``t()``.
UI: dict[str, dict[str, str]] = {
    "de": {
        "result.quantile": "Im Modell liegen {pct} % der Werte höchstens bei {value}{unit} "
        "({conf}-%-Intervall {lo} … {hi}{unit}).",
        "result.target": "Im Modell wird das Ziel {op} {value}{unit} in {p} der Iterationen "
        "erreicht ({lo} … {hi} %).",
        "result.share": "Im Modell trifft die Aussage in {p} der Iterationen zu ({lo} … {hi} %).",
        "result.validity": "Dieses Ergebnis gilt für Modell {model} (Hash {hash}), Szenario "
        "{scenario}, N = {n}, Seed {seed}, berechnet am {time} UTC.",
        "result.precision_wide": "Die Unsicherheit von {what} ist größer als ±1 Prozentpunkt. "
        "Mehr Iterationen (N) verkleinern sie.",
        "result.mean": "Mittelwert",
        "result.median": "Median",
        "result.sd": "Standardabweichung",
        "result.min": "Kleinster Wert",
        "result.max": "Größter Wert",
        "result.quantile_label": "P{pct} ({pct}-%-Quantil)",
        "result.target_label": "P(Ziel erreicht)",
        "result.share_label": "Anteil „trifft zu“",
        "result.se": "Standardfehler",
        "result.points": "{diff} Prozentpunkte",
        "result.points_unit": "Prozentpunkte",
        "result.relative": "Relative Genauigkeit (SE / |Mittelwert|)",
        "result.change_up": "{label} steigt um {amount} (von {before} auf {after}).",
        "result.change_down": "{label} sinkt um {amount} (von {before} auf {after}).",
        "result.change_same": "{label} bleibt gleich ({before}).",
        "ref.analytic": "Analytisch",
        "ref.grid": "Numerische Faltung",
        "ref.grid_note": "Numerische Faltung auf dem Gitter (Schrittweite 0,001): größte "
        "Abweichung zur analytischen CDF {deviation}.",
        "ref.clark_note": "Mittelwert nach Clark (1961): {clark} – simuliert: {mean}.",
        "ref.ks": "Größter Abstand der CDFs: {ks} – zulässig bei N = {n}: {eps} "
        "(DKW-Schranke, α = 0,001).",
        "ref.changed": "Die analytische Lösung gilt für das unveränderte Tutorial.",
        "fig.value": "Wert",
        "fig.value_unit": "Wert ({unit})",
        "fig.density": "Dichte",
        "fig.cdf": "Anteil ≤ Wert",
        "fig.share": "Anteil",
        "fig.true": "trifft zu",
        "fig.false": "trifft nicht zu",
        "fig.simulation": "Simulation",
        "ui.page_start": "Start",
        "ui.page_lernpfad": "Lernpfad",
        "ui.page_modell": "Modell",
        "ui.page_simulation": "Simulation",
        "ui.page_ergebnisse": "Ergebnisse",
        "ui.page_laeufe": "Läufe",
        "ui.start_intro": "Weltmodelle aus Bausteinen bauen, per Monte Carlo simulieren und die "
        "Ergebnisse mit ihrer numerischen Unsicherheit lesen. Tutorials und Lektionen sind "
        "schreibgeschützt; „Als Vorlage kopieren“ legt ein eigenes Modell an.",
        "ui.lernpfad_intro": "Elf kurze Lektionen zu Abhängigkeitsmustern: Serie, Parallelität, "
        "Schwellen, bedingte Verteilungen, gemeinsame Ursachen – jeweils mit Vorhersage, "
        "Stellschraube und analytischer Referenz.",
        "ui.open_lernpfad": "Lernpfad öffnen",
        "ui.tutorials": "Tutorials",
        "ui.own_models": "Eigene Modelle",
        "ui.no_own_models": "Noch keine eigenen Modelle. Ein Tutorial als Vorlage kopieren.",
        "ui.open": "Öffnen",
        "ui.copy": "Als Vorlage kopieren",
        "ui.copy_name": "Name der Kopie",
        "ui.copied": "Modell „{name}“ angelegt. Es steht unter „Eigene Modelle“.",
        "ui.no_model": "Kein Modell geöffnet. Auf der Startseite ein Tutorial oder eigenes "
        "Modell öffnen.",
        "ui.readonly": "schreibgeschützt – zum Ändern als Vorlage kopieren",
        "ui.explanation": "Erklärung",
        "ui.editor": "Modell (YAML)",
        "ui.at_line": " (Zeile {line})",
        "ui.col_id": "ID",
        "ui.col_type": "Typ",
        "ui.col_name": "Name",
        "ui.col_unit": "Einheit",
        "ui.col_detail": "Verteilung / Ausdruck",
        "ui.unsaved": "Ungespeicherte Änderungen.",
        "ui.save": "Speichern",
        "ui.discard": "Verwerfen",
        "ui.to_simulation": "Weiter zur Simulation",
        "ui.n": "Iterationen (N)",
        "ui.seed": "Seed",
        "ui.simulate": "Simulieren",
        "ui.running": "Simuliere …",
        "ui.sim_blocked": "Das Modell hat noch Probleme (Seite Modell); Simulieren ist gesperrt.",
        "ui.sim_done": "Fertig: {n} Iterationen in {seconds} s.",
        "ui.unexpected": "Unerwarteter Fehler: {detail}. Die App läuft weiter; bitte die Eingabe "
        "prüfen oder die Seite neu laden.",
        "ui.saved": "Gespeichert.",
        "ui.saved_invalid": "Gespeichert, aber das Modell ist ungültig; "
        "Simulieren bleibt gesperrt.",
        "ui.save_force": "Trotzdem überschreiben",
        "ui.run_large": "Dieser Lauf belegt etwa {mb} MB; das Speichern kann dauern.",
        "type.constant": "Konstante",
        "type.uncertain": "Unsicher",
        "type.event": "Ereignis",
        "type.choice": "Auswahl",
        "type.derived": "Berechnet",
        "type.output": "Ausgabe",
        "ui.to_results": "Zu den Ergebnissen",
        "ui.main_scenario": "Hauptszenario",
        "ui.no_run": "Noch keine Simulation. Auf der Seite Simulation starten.",
        "ui.metric": "Kennzahl",
        "ui.value": "Wert",
        "ui.save_run": "Lauf speichern",
        "ui.run_saved": "Lauf gespeichert: {name}",
        "ui.no_runs": "Keine gespeicherten Läufe für dieses Modell.",
        "ui.run_broken": "Das gespeicherte Modell dieses Laufs ist nicht mehr gültig.",
        "ui.run_mismatch": "Gespeicherte und neu berechnete Kennzahlen weichen ab.",
        "ui.exit": "App beenden",
        "ui.exit_question": "Die App wirklich beenden? Nur dieser Prozess wird beendet.",
        "ui.exit_unsaved": "Ungespeicherte Änderungen im Editor gehen verloren.",
        "ui.exit_confirm": "Ja, beenden",
        "ui.exit_cancel": "Abbrechen",
        "ui.exit_done": "Die App wird beendet. Das Browserfenster kann geschlossen werden.",
        "lesson.choose": "Lektion",
        "lesson.model_yaml": "Mini-Modell (YAML)",
        "lesson.sources": "**Zum Weiterlesen:**",
        "lesson.illustrative": "Illustrative Zahlen: didaktisch gesetzt, "
        "keine Rechercheergebnisse.",
        "lesson.predict": "1. Vorhersage",
        "lesson.simulate": "2. Simulieren",
        "lesson.run": "Simulieren (Ausgangswert)",
        "lesson.turn": "3. Stellschraube drehen",
        "lesson.turn_run": "Mit diesem Wert neu rechnen (gleicher Seed)",
        "lesson.copy": "4. Als Vorlage übernehmen",
        "lesson.before": "Vorher",
        "lesson.after": "Nachher",
        "lesson.diff": "Differenz",
        "lesson.rule": "Faustregel: {rule}",
        "lesson.prediction": "Deine Vorhersage: {prediction} – Ergebnis: {result}",
        "lesson.result": "Ergebnis: {result}",
        "lesson.done": " · durchgearbeitet",
        "lesson.seen": " · angesehen",
        "lesson.progress": "{done} von {total} Lektionen durchgearbeitet",
        "lesson.missing": "Dateien der Lektion fehlen: {files}.",
        "lesson.invalid": "Die Lektion passt nicht zum Manifest: {problem}.",
        "lesson.knob_scenario": "Stellschraube {label} = {value}",
        "lesson.passed": "erfüllt",
        "lesson.failed": "nicht erfüllt",
        "lesson.check_ks": "Größter CDF-Abstand zur analytischen Lösung {observed} "
        "(DKW-Schranke {expected})",
        "lesson.check_mean": "Mittelwert analytisch {expected}, simuliert {observed} "
        "(4 Standardfehler)",
        "lesson.check_share": "Anteil analytisch {expected}, simuliert {observed} (Wilson 99,9 %)",
        "lesson.check_var": "Varianz analytisch {expected}, simuliert {observed} (±2 %)",
        "ui.model_blank": "Noch kein Modelltext. Ein Tutorial öffnen oder YAML eintragen.",
        "ui.status_valid": "Gültig – {nodes} Knoten, {outputs}",
        "ui.outputs_one": "1 Ausgabe",
        "ui.outputs_many": "{n} Ausgaben",
        "ui.problems_one": "1 Problem",
        "ui.problems_many": "{n} Probleme",
    }
}


def t(key: str, lang: str = "de", **params: object) -> str:
    """Render a UI text; unknown languages fall back to German."""
    catalog = UI.get(lang, UI["de"])
    template = catalog.get(key) or UI["de"][key]
    return template.format(**params)
