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
    "fit.deviation": "{node}: Quantil-Fit {dist} trifft P10/P50/P90 = {given} mit {fitted}; "
    "größte Abweichung {deviation} der Spanne P90 − P10.",
    "fit.conflict": "{node}: Die drei Werte P10/P50/P90 = {given} passen nicht zu einer "
    "{dist}-Verteilung: Der beste Fit liefert {fitted}, die größte Abweichung beträgt "
    "{deviation} der Spanne P90 − P10 (mehr als 2 %). Eine Stützstellen-Verteilung (piecewise) "
    "übernimmt die Werte genau.",
    "fit.bounds": "{node}: P0 muss unter P10 = {p10} liegen und P100 über P90 = {p90}.",
    "stats.single_sample": "Nur eine Iteration: kein Standardfehler bestimmbar.",
    "stats.quantile_range": "Quantil {q} liegt nicht strikt zwischen 0 und 1.",
    "files.exists": "Ein Modell „{name}“ gibt es schon. Vorschlag: „{suggestion}“.",
    "scenario.id_invalid": "Die Szenario-ID „{id}“ ist nicht zulässig: {reason}.",
    "scenario.parent_unknown": "Das Eltern-Szenario „{parent}“ gibt es nicht.",
    "scenario.parent_cycle": "Die Elternkette bildet einen Zyklus: {cycle}.",
    "scenario.node_unknown": "{node} gibt es nicht (mehr). Override entfernen oder mit "
    "„inactive: true“ als inaktiv markieren.",
    "scenario.field_invalid": "{node}: Das Feld „{field}“ lässt sich in einem Szenario nicht "
    "überschreiben.",
    "scenario.type_change": "{node}: Der Knotentyp lässt sich in einem Szenario nicht ändern.",
    "scenario.corr_unknown": "Die Korrelationsgruppe „{group}“ gibt es nicht.",
    "scenario.corr_field": "Korrelationsgruppe „{group}“: In Szenarien lassen sich nur "
    "„spearman“ und „why“ überschreiben.",
    "corr.too_small": "Korrelationsgruppe „{group}“ braucht mindestens zwei Knoten.",
    "corr.node_unknown": "Korrelationsgruppe „{group}“: Knoten „{name}“ gibt es nicht.",
    "corr.node_type": "Korrelationsgruppe „{group}“: {node} hat den Typ „{type}“; erlaubt sind "
    "unsichere Knoten und Ereignisse.",
    "corr.node_twice": "{node} steht in mehreren Korrelationsgruppen ({groups}); erlaubt ist eine.",
    "corr.node_repeated": "Korrelationsgruppe „{group}“: {node} steht mehrfach in der Liste; "
    "jeder Knoten darf nur einmal vorkommen.",
    "corr.shape": "Korrelationsgruppe „{group}“: Die Matrix muss {k} Zeilen mit je {k} "
    "Werten haben.",
    "corr.diagonal": "Korrelationsgruppe „{group}“: Auf der Diagonale muss überall 1 stehen.",
    "corr.range": "Korrelationsgruppe „{group}“: Rangkorrelationen müssen zwischen −1 und 1 "
    "liegen.",
    "corr.asymmetric": "Korrelationsgruppe „{group}“: Die Matrix ist nicht symmetrisch (Zeile "
    "{row}, Spalte {col}).",
    "corr.not_psd": "Korrelationsgruppe „{group}“: Die Matrix ist nicht positiv semidefinit "
    "(kleinster Eigenwert {eig}), die Paare widersprechen sich. Sie wird nicht repariert; bitte "
    "die Werte anpassen.",
    "corr.latent_not_psd": "Korrelationsgruppe „{group}“: Nach der Umrechnung der "
    "Rangkorrelation für die Copula (2·sin(π·ρ/6)) ist die Matrix nicht positiv semidefinit "
    "(kleinster Eigenwert {eig}). Sie wird nicht repariert; bitte die Werte etwas abschwächen.",
    "corr.discrete_ties": "Korrelationsgruppe „{group}“ enthält diskrete Knoten ({nodes}): "
    "Wegen gleicher Werte (Bindungen) liegt die erreichte Rangkorrelation unter dem Ziel.",
    "scenario.inactive": "{node}: Override ist inaktiv (Knoten gibt es nicht mehr) und wird nicht "
    "angewandt.",
    "scenario.same_value": "{node}: Override von „{field}“ hat denselben Wert wie das "
    "Eltern-Szenario.",
    "files.changed": "Die Datei „{name}“ wurde seit dem Öffnen verändert. Bitte neu laden.",
    "csv.encoding": "Die CSV-Datei ist nicht in UTF-8 gespeichert. Bitte als „CSV UTF-8“ "
    "exportieren und erneut hochladen.",
    "csv.column": "Die CSV-Datei hat keine Spalte „{column}“ (vorhanden: {columns}).",
    "form.no_mapping": "Das Formular braucht gültiges YAML mit Schlüsseln auf oberster Ebene; "
    "bitte erst im Reiter „YAML“ korrigieren.",
    "form.patch_failed": "Die Änderung ließ sich nicht verlustfrei ins YAML schreiben; nichts "
    "wurde geändert.",
    "form.list": "„{value}“ ist keine Zahl. Listen trennen Werte mit Semikolon oder Leerzeichen.",
    "form.number": "„{value}“ ist keine Zahl (Beispiele: 2,5 oder 2.5 oder 1e3).",
    "form.exists": "Einen Knoten „{id}“ gibt es schon.",
    "form.referenced": "{node} lässt sich nicht löschen, solange darauf verwiesen wird: {refs}.",
    "csv.number": "CSV-Spalte „{column}“{at_line}: „{value}“ ist keine Zahl. Der Import wurde "
    "abgebrochen.",
    "csv.too_many": "Die Spalte hat {count} Werte; übernehmen lassen sich 1 bis {limit}.",
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
    text = template.format_map(_fields(item))
    return f"Szenario „{item.scenario}“: {text}" if item.scenario else text


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
        "compare.p10": "P10 (10-%-Quantil)",
        "compare.direction": "Im Modell ist „{b}“ in {lower} der Iterationen kleiner als „{a}“, "
        "in {ties} gleich und in {higher} größer.",
        "compare.same_bool": "Im Modell stimmen „{b}“ und „{a}“ in {ties} der Iterationen überein.",
        "compare.ties_label": "Anteil B = A",
        "compare.stale": "Das Modell hat sich seit dem letzten Vergleich geändert; bitte neu "
        "vergleichen.",
        "compare.d_table": "Kennzahlen der Differenz B − A je Iteration",
        "compare.p90": "P90 (90-%-Quantil)",
        "compare.points": "{diff} Prozentpunkte [{lo} … {hi}]",
        "compare.better": "Im Modell ist „{b}“ in {p} der Iterationen besser als „{a}“ "
        "({lo} … {hi} %), in {ties} gleich und in {worse} schlechter.",
        "result.beyond": "Im Modell wird der Horizont {horizon} in {p} der Iterationen nicht "
        "erreicht ({lo} … {hi} %).",
        "result.beyond_label": "Anteil nicht im Horizont",
        "result.beyond_value": "> Horizont {horizon}",
        "result.quantile_beyond": "Im Modell liegen weniger als {pct} % der Werte innerhalb des "
        "Horizonts {horizon}: P{pct} liegt jenseits des Horizonts.",
        "result.censored": "nicht bestimmbar: {p} jenseits des Horizonts",
        "result.p_loss": "P(Verlust)",
        "result.var": "VaR {pct} %",
        "result.es": "ES {pct} %",
        "result.multimodal": "Die Verteilung hat mehrere Gipfel: Median ({median}) und häufigster "
        "Bereich ({mode}) fallen auseinander; der Mittelwert beschreibt hier keinen typischen "
        "Fall.",
        "result.all_beyond": "Alle Werte liegen jenseits des Horizonts; Histogramm und Kurve "
        "zeigen nur Rohwerte, die im Modell als „nicht erreicht“ gelten.",
        "result.corr_title": "Erreichte Rangkorrelation (Spearman) der Korrelationsgruppen",
        "result.corr_group": "Gruppe",
        "result.corr_pair": "Paar",
        "result.corr_target": "Ziel ρ",
        "result.corr_achieved": "erreicht ρ",
        "result.horizon_raw": "Hinweis: {name} hat einen Horizont ({horizon}); diese Seite rechnet "
        "mit den Rohwerten, auch jenseits des Horizonts.",
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
        "preview.mean": "Mittelwert",
        "preview.median": "Median",
        "preview.invalid": "Unzulässig (unter Untergrenze / über Obergrenze)",
        "preview.no_bounds": "keine Grenzen gesetzt",
        "model.tab_form": "Formular",
        "model.tab_yaml": "YAML",
        "form.header": "Modellkopf und Einstellungen (ID {model})",
        "form.f_title": "Titel",
        "form.f_description": "Beschreibung",
        "form.f_n": "Iterationen (N)",
        "form.f_seed": "Seed",
        "form.f_illustrative": "Illustrative Zahlen (keine Rechercheergebnisse)",
        "form.yes": "ja",
        "form.no": "nein",
        "form.col_why": "Begründung",
        "form.no_nodes": "Das Modell hat noch keine Knoten. Lege unten den ersten an.",
        "form.written": "Das Formular hat den Entwurf geändert; der Reiter „YAML“ zeigt denselben "
        "Stand. Es gilt die letzte Änderung, egal in welchem Reiter.",
        "form.pick": "Knoten bearbeiten",
        "form.add": "Knoten anlegen",
        "form.new_id": "ID des neuen Knotens",
        "form.new_type": "Typ",
        "form.add_button": "Anlegen",
        "form.preview": "Vorschau der Verteilung",
        "form.preview_needs_valid": "Die Vorschau erscheint, sobald das Modell fehlerfrei ist. "
        "Zuerst: {reason}",
        "form.preview_failed": "Keine Vorschau, weil das Modell nicht rechnet: {reason}",
        "form.col_metric": "Kennzahl",
        "form.col_value": "Wert",
        "form.f_name": "Name",
        "form.f_unit": "Einheit",
        "form.f_why": "Begründung (Quelle, Annahme)",
        "form.f_tags": "Schlagworte (mit Komma getrennt)",
        "form.f_bounds_min": "Untergrenze (zulässig ab)",
        "form.f_bounds_max": "Obergrenze (zulässig bis)",
        "form.f_track": "Werte im Lauf behalten",
        "form.f_value": "Wert",
        "form.f_p": "Wahrscheinlichkeit p (Zahl oder Ausdruck)",
        "form.f_expr": "Ausdruck",
        "form.f_better": "Besser ist (ohne Ziel)",
        "form.f_horizon": "Horizont",
        "form.f_loss_reference": "Verlust-Bezugswert (VaR/ES)",
        "form.f_target_op": "Ziel: Vergleich (le ≤, lt <, ge ≥, gt >)",
        "form.f_target_value": "Ziel: Wert",
        "form.f_dist": "Verteilung",
        "form.f_input": "Eingabemodus",
        "form.f_options": "Optionen (je Zeile „Name: Gewicht“)",
        "form.delete_confirm": "Ja, diesen Knoten löschen (Kommentarzeilen direkt über ihm "
        "gehen mit)",
        "form.delete": "Knoten {node} löschen",
        "export.model_text": "Modell (YAML)",
        "export.title": "Exportieren",
        "export.csv": "Kennzahlen (CSV)",
        "export.parquet": "Rohstichproben (Parquet)",
        "export.html": "Bericht (HTML)",
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
        "ui.new_model": "Neues leeres Modell",
        "ui.new_model_id": "ID (a–z, 0–9, _)",
        "ui.new_model_create": "Anlegen und öffnen",
        "ui.page_simulation": "Simulation",
        "ui.page_ergebnisse": "Ergebnisse",
        "ui.page_laeufe": "Läufe",
        "web.page_follows": "Diese Seite wird gerade umgestellt. Bis dahin steht sie in der "
        "bisherigen App auf Port 8642 bereit.",
        "web.no_model": "Kein Modell geöffnet",
        "web.col_node": "Knoten",
        "web.col_brief": "Eingabe",
        "web.col_spark": "Verteilung",
        "web.spread": "Relative Streuung",
        "web.graph_needs_valid": "Der Graph erscheint, sobald das Modell fehlerfrei ist und eine "
        "Ausgabe hat.",
        "web.graph_caption": "Farbe: relative Streuung (P90 − P10) / P50 im Probelauf, dunkel = "
        "breit. Einen Knoten anklicken öffnet ihn rechts.",
        "web.pick_node": "Einen Knoten im Graph oder in der Tabelle anklicken.",
        "web.more_fields": "Beschreibung, Begründung, Grenzen",
        "web.trial": "Probelauf in {ms} ms",
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
        "ui.page_szenarien": "Szenarien",
        "ui.page_vergleich": "Vergleich",
        "ui.scenario": "Szenario",
        "scen.pick": "Szenario",
        "scen.why": "**Begründung:** {why}",
        "scen.overrides": "{n} Overrides",
        "scen.detached": "losgelöst",
        "scen.no_overrides": "Dieses Szenario überschreibt noch nichts.",
        "scen.col_node": "Knoten",
        "scen.col_field": "Feld",
        "scen.col_parent": "Eltern",
        "scen.col_value": "Szenario",
        "scen.col_why": "Begründung",
        "scen.col_status": "Status",
        "scen.readonly": "Tutorial: Szenarien ansehen, simulieren und vergleichen; ändern erst in "
        "einer Kopie.",
        "scen.invalid_model": "Das Modell hat noch Probleme (Seite Modell); Szenarien lassen sich "
        "erst danach bearbeiten.",
        "scen.new": "Neues Unterszenario",
        "scen.new_id": "ID (a bis z, 0 bis 9, _)",
        "scen.new_name": "Name",
        "scen.new_why": "Begründung",
        "scen.new_parent": "Eltern-Szenario",
        "scen.add": "Szenario anlegen",
        "scen.override": "Wert überschreiben",
        "scen.value_hint": "Neuer Wert (Zahl, Ausdruck oder YAML)",
        "scen.value_missing": "Bitte einen Wert eintragen.",
        "scen.set": "Override setzen",
        "scen.remove_pick": "Override entfernen",
        "scen.remove": "Entfernen",
        "scen.duplicate": "Duplizieren",
        "scen.detach": "Loslösen",
        "scen.detach_question": "Loslösen friert das Szenario mit allen Werten ein; spätere "
        "Änderungen am Eltern-Szenario wirken dann nicht mehr. Fortfahren?",
        "scen.detach_confirm": "Ja, loslösen",
        "scen.mark_inactive": "Overrides gelöschter Knoten inaktiv setzen",
        "compare.ref": "Referenz A",
        "compare.others": "Vergleichen mit (bis zu drei)",
        "compare.run": "Vergleichen",
        "compare.same_seed": "Alle Szenarien laufen mit demselben Seed: Unterschiede entstehen nur "
        "durch die Overrides (gemeinsame Zufallszahlen).",
        "compare.need_two": "Für einen Vergleich braucht das Modell mindestens ein Unterszenario.",
        "compare.pair": "„{b}“ gegen „{a}“",
        "compare.diff": "Differenz B − A [95-%-Intervall]",
        "compare.d_caption": "Verteilung der Differenz B − A je Iteration",
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
        "ui.status_scenarios": ", {n} Unterszenarien",
        "ui.outputs_one": "1 Ausgabe",
        "ui.outputs_many": "{n} Ausgaben",
        "ui.problems_one": "1 Problem",
        "ui.problems_many": "{n} Probleme",
        "ui.page_analyse": "Analyse",
        "model.p0": "P0 (kleinster möglicher Wert)",
        "model.p100": "P100 (größter möglicher Wert)",
        "model.to_piecewise": "Als Stützstellen-Verteilung übernehmen",
        "model.csv_title": "Werte aus CSV übernehmen (empirische Verteilung)",
        "model.csv_file": "CSV-Datei",
        "model.csv_column": "Spalte",
        "model.csv_node": "Knoten",
        "model.csv_import": "Werte übernehmen",
        "model.csv_done": "{n} Werte in „{node}“ übernommen ({skipped} leere Zellen übersprungen). "
        "Noch nicht gespeichert.",
        "analysis.intro": "Struktur-Auswertungen eines Szenarios: Graph und Rangkorrelation "
        "rechnen aus einem Lauf, Tornado und Sweep starten eigene Läufe mit demselben Seed.",
        "analysis.output": "Ausgabe",
        "analysis.guide_label": "Wann welche Auswertung?",
        "analysis.guide": "- **Graph:** zuerst – stimmt die Struktur, fehlen Begründungen?\n"
        "- **Kritikalität:** bei Wettläufen (max/min) und Verzweigungen (where): welcher Pfad "
        "entscheidet wie oft?\n"
        "- **Tornado:** wo lohnt genaueres Schätzen? Rangfolge der unsicheren Eingaben nach "
        "Wirkung auf die Kennzahl.\n"
        "- **Sweep:** was-wäre-wenn für einen einzelnen Planwert, z. B. ab welcher Dauer das "
        "Ziel kippt.\n"
        "- **Rangkorrelation:** schneller Überblick aus einem Lauf, welche Eingaben mit dem "
        "Ergebnis gleichlaufen.\n"
        "- **Risikomatrix:** Ereignisse nach Wahrscheinlichkeit und Folge einordnen.",
        "analysis.help_label": "Was zeigt dieser Reiter?",
        "analysis.help_graph": "**Frage:** Wie hängen die Knoten zusammen?\n\n"
        "**Lesart:** Pfeile laufen von links (Eingaben) nach rechts (Ausgabe). Das Symbol zeigt "
        "den Knotentyp, die Linienart, ob ein Knoten in einer Formel oder in einem "
        "Verteilungsparameter steckt. Die Farbe zeigt die gewählte Einfärbung; blasse Knoten "
        "wirken nicht auf die Ausgabe.\n\n"
        "**Grenze:** Der Graph zeigt Struktur, keine Stärke der Wirkung.",
        "analysis.help_crit": "**Frage:** Welche Knoten bestimmen das Ergebnis tatsächlich?\n\n"
        "**Lesart:** Bei max/min zählt nur der Gewinner, bei where nur der gewählte Zweig. Der "
        "Index ist der Anteil der Iterationen, in denen ein Knoten so auf dem entscheidenden "
        "Pfad liegt – wie der Kritikalitätsindex im Terminplan. Die Konstellationen zeigen, "
        "welche Eingaben gemeinsam entscheiden.\n\n"
        "**Grenze:** Ein Index von 100 % heißt nicht „wichtig“, nur „immer beteiligt“; wie stark "
        "ein Knoten wirkt, zeigen Tornado und Sweep.",
        "analysis.help_tornado": "**Frage:** Welche unsichere Eingabe verschiebt das Ergebnis am "
        "stärksten?\n\n"
        "**Lesart:** Je Eingabe wird das Modell zweimal gerechnet, mit der Eingabe fest auf "
        "ihrem P10 und ihrem P90; alles andere bleibt zufällig wie im Ausgangslauf. Der Balken "
        "reicht von der Kennzahl bei P10 bis zu der bei P90; oben steht die Eingabe mit dem "
        "größten Ausschlag.\n\n"
        "**Grenze:** Jede Eingabe wird einzeln bewegt; Wechselwirkungen mehrerer Eingaben zeigt "
        "der Tornado nicht.",
        "analysis.help_sweep": "**Frage:** Wie ändert sich das Ergebnis, wenn ich einen Wert "
        "gezielt verändere?\n\n"
        "**Lesart:** Ein Planwert (Konstante, Verteilungsparameter oder Wahrscheinlichkeit) "
        "läuft über k Werte; je Wert ein Lauf mit demselben Seed. Die Kurve zeigt die gewählte "
        "Kennzahl, die Balken ihre numerische Unsicherheit.\n\n"
        "**Grenze:** Alle anderen Werte bleiben wie im Modell; der Sweep sagt nicht, welcher "
        "Wert realistisch ist.",
        "analysis.help_rho": "**Frage:** Welche Eingaben laufen mit dem Ergebnis gleich?\n\n"
        "**Lesart:** ρ nach Spearman zwischen −1 und 1: nahe 1 heißt „hohe Eingabe, hohes "
        "Ergebnis“, nahe 0 kein monotoner Zusammenhang. Berechnet aus einem Lauf, daher "
        "schnell.\n\n"
        "**Grenze:** Deskriptiv: keine Ursache und keine Wirkungsstärke; Eingaben mit kleiner "
        "Streuung können trotz starker Wirkung ein kleines ρ haben.",
        "analysis.help_risk": "**Frage:** Welche Ereignisse sind wahrscheinlich und "
        "folgenreich?\n\n"
        "**Lesart:** Waagerecht die Eintrittswahrscheinlichkeit, senkrecht, um wie viel das "
        "Ergebnis im Mittel höher liegt, wenn das Ereignis eintritt – wie eine klassische "
        "Risikomatrix, aber aus der Simulation. Die Balken zeigen die Unsicherheit.\n\n"
        "**Grenze:** Die Differenz ist keine kausale Wirkung, wenn Ereignisse gemeinsame "
        "Ursachen haben oder zusammenwirken.",
        "analysis.run": "Analysieren",
        "analysis.memory": "Dieser Lauf hält alle {nodes} Knoten im Speicher, etwa {mb} MB.",
        "analysis.stale": "Modell, Szenario oder Einstellungen haben sich geändert; bitte neu "
        "analysieren.",
        "analysis.tab_graph": "Graph",
        "analysis.tab_crit": "Kritikalität",
        "analysis.tab_tornado": "Tornado",
        "analysis.tab_sweep": "Sweep",
        "analysis.tab_rho": "Rangkorrelation",
        "analysis.tab_risk": "Risikomatrix",
        "analysis.color": "Einfärbung",
        "analysis.color_sensitivity": "Sensitivität (|ρ| nach Spearman)",
        "analysis.color_criticality": "Kritikalitätsindex",
        "analysis.color_why": "Begründung fehlt",
        "analysis.graph_caption": "Symbole: Kreis unsicher, Raute Ereignis, Quadrat Konstante, "
        "Dreieck Auswahl, Punkt berechnet, Stern Ausgabe. Linien: durchgezogen Ausdruck, "
        "gestrichelt Parameter, gepunktet Korrelation. Blass: kein Pfad zur Ausgabe.",
        "analysis.edge_ausdruck": "Ausdruck",
        "analysis.edge_parameter": "Parameter",
        "analysis.edge_korrelation": "Korrelation",
        "analysis.crit_sentence": "Im Modell liegt {name} in {p} der Iterationen auf dem "
        "entscheidenden Pfad ({lo} … {hi} %).",
        "analysis.crit_no_extremum": "Das Modell enthält kein max, min oder where. Dann liegt jede "
        "Eingabe mit Pfad zur Ausgabe in jeder Iteration auf dem entscheidenden Pfad, und der "
        "Kritikalitätsindex trägt keine Information.",
        "analysis.crit_note": "Der Index zählt die Iterationen, in denen ein Knoten das Ergebnis "
        "über max/min oder den gewählten where-Zweig mitbestimmt. Indizes summieren nicht zu "
        "100 % (bei Gleichstand zählen alle Gewinner); die Pfadkonstellationen summieren zu 100 %.",
        "analysis.crit_axis": "Anteil der Iterationen auf dem entscheidenden Pfad",
        "analysis.constellations": "Pfadkonstellationen (kritische unsichere Eingaben und "
        "Ereignisse je Iteration)",
        "analysis.constellation_none": "keine unsichere Eingabe",
        "analysis.constellation_rest": "übrige ({n} Konstellationen)",
        "analysis.col_node": "Knoten",
        "analysis.col_index": "Index [95-%-Intervall]",
        "analysis.col_constellation": "Konstellation",
        "analysis.col_share": "Anteil [95-%-Intervall]",
        "analysis.metric": "Kennzahl",
        "analysis.metric_mean": "Mittelwert der Ausgabe",
        "analysis.metric_median": "Median der Ausgabe",
        "analysis.metric_target": "P(Ziel erreicht)",
        "analysis.metric_quantile": "Quantil der Ausgabe",
        "analysis.metric_share": "Anteil „trifft zu“",
        "analysis.tornado_n": "Iterationen je Lauf",
        "analysis.tornado_run": "Tornado rechnen",
        "analysis.tornado_runs": "Der Tornado braucht {runs} Läufe mit je N = {n}.",
        "analysis.tornado_many": "Mehr als 50 Läufe: Die Rechnung kann länger dauern.",
        "analysis.tornado_caption": "Je unsichere Eingabe zwei Läufe mit demselben Seed, die "
        "Eingabe auf ihr P10 bzw. P90 fixiert; alle anderen Knoten ziehen dieselben "
        "Zufallszahlen. Ausgangswert: {base}.",
        "analysis.no_uncertain": "Das Modell hat keine unsicheren Eingaben.",
        "analysis.col_p10": "P10",
        "analysis.col_p90": "P90",
        "analysis.at_p10": "Eingabe auf P10",
        "analysis.at_p90": "Eingabe auf P90",
        "analysis.col_swing": "Ausschlag",
        "analysis.sweep_param": "Parameter",
        "analysis.sweep_from": "von",
        "analysis.sweep_to": "bis",
        "analysis.sweep_k": "Anzahl Werte (k)",
        "analysis.sweep_q": "Quantil (0 bis 1)",
        "analysis.sweep_run": "Sweep rechnen",
        "analysis.sweep_invalid": "Diese Werte sind im Modell nicht zulässig; der Sweep läuft "
        "erst mit einem gültigen Bereich:",
        "analysis.sweep_none": "Das Modell hat keine literalen Zahlen, die sich verändern lassen.",
        "analysis.col_value": "Wert",
        "analysis.col_estimate": "Schätzung",
        "analysis.col_interval": "95-%-Intervall",
        "analysis.rho_caption": "Deskriptiv: zeigt Gleichlauf im Modell, keine Ursache und keine "
        "Wirkungsstärke.",
        "analysis.col_rho": "ρ (Spearman)",
        "analysis.undefined": "nicht bestimmbar",
        "analysis.risk_caption": "Die Differenz ist keine kausale Wirkung, wenn Ereignisse "
        "gemeinsame Ursachen haben oder zusammenwirken.",
        "analysis.no_events": "Das Modell hat keine Ereignisse.",
        "analysis.col_p": "p̂ [95-%-Intervall, Wilson]",
        "analysis.col_diff": "E[Y | Ereignis] − E[Y | kein Ereignis] [95 %, Welch]",
        "analysis.risk_undefined": "y nicht bestimmbar",
        "analysis.risk_x": "Eintrittswahrscheinlichkeit p̂",
        "analysis.risk_y": "E[Y | Ereignis] − E[Y | kein Ereignis]",
    }
}


def t(key: str, lang: str = "de", **params: object) -> str:
    """Render a UI text; unknown languages fall back to German."""
    catalog = UI.get(lang, UI["de"])
    template = catalog.get(key) or UI["de"][key]
    return template.format(**params)
