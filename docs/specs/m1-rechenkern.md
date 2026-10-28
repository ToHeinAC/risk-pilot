# Pflichtenheft M1 — Rechenkern

**Stand:** 27. Oktober 2026, Entscheidungen Q1–Q11 eingearbeitet · **Bezug:** [PRD.md](../../PRD.md), Meilenstein M1 (AK 1–12, Edge
cases) · **Herleitung:** [ideas/concept-v2.md](../../ideas/concept-v2.md), Abschnitte 4 und 7

Dieses Pflichtenheft legt fest, **wie** M1 umgesetzt wird: Module, Schnittstellen, Modellformat,
Verteilungsverträge, Ausdruckssprache, Zufallszahlen, Statistik, Fehlerbilder, Tests und
Arbeitspakete. Das PRD bleibt der Vertrag für das **Was**; bei Widerspruch gilt das PRD, und der
Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M1:**

- Modellschema mit sechs Knotentypen, YAML-Lesen (Text → Modell) und Datei-Adapter.
- Validierung und Kompilierung: Namensauflösung, Graph, Zyklen, Parameterprüfung, Ausdrücke.
- 14 Verteilungsfamilien mit Eingabemodi, kanonischen Parametern und Inversionsmethode.
- Vektorisierte Engine mit einem Zufallsstrom je Knoten.
- Grundstatistik je Ausgabe.
- Analytische Referenzen für T1 und T2, Gitterfaltung.
- `examples/t1_faltung.yaml`, `examples/t2_terminplan.yaml`.

**Nicht in M1** (spätere Meilensteine): Szenarien und Overrides (M3), Kritikalität und
Gewinnerverfolgung in `max`/`min` (M4), Korrelationsgruppen, Stützstellen-/empirische
Verteilung, Quantil-Fit, Horizont (M5), Oberfläche (M2), Export (M6). Das Schema wird so
angelegt, dass diese Erweiterungen additiv möglich sind (Abschnitt 3.6).

***

## 2. Modulstruktur und Abhängigkeiten

```text
src/app/
    __init__.py
    errors.py              Fehler- und Hinweisklassen (Abschnitt 9)
    messages.py            Meldungskatalog de (en vorbereitet), render()
    model/
        schema.py          Pydantic-Modelle des YAML-Formats
        yaml_io.py         model_from_yaml(text) – rein, ohne Datei-I/O
        compile.py         compile_model(model) -> CompiledModel
        graph.py           Referenzen sammeln, topologische Ordnung, Zyklen
    expr/
        parser.py          ast-Whitelist, Grenzen, Namensauflösung -> ExprNode-Baum
        functions.py       Funktionsregister
        evaluate.py        vektorisierte Auswertung eines ExprNode-Baums
    dists/
        base.py            Family-Protokoll, Param-Spezifikation
        registry.py        register(), get_family(), families()
        families.py        die 14 Familien
    engine/
        streams.py         Zufallsströme je Knoten
        simulate.py        simulate(compiled, n, seed) -> SimulationResult
    analysis/
        stats.py           summarize(), wilson(), quantile_ci()
        analytic.py        Referenzlösungen T1/T2, Gitterfaltung, ks_distance()
    adapters/
        files.py           load_model(path) – einzige Stelle mit Datei-I/O in M1
examples/
    t1_faltung.yaml
    t2_terminplan.yaml
```

- Der Platzhalter `src/app/core.py` und `tests/test_core.py` (slugify) werden entfernt.
- **Laufzeitabhängigkeiten** (`uv add`): `numpy`, `scipy`, `pydantic>=2`, `pyyaml`.
- **Entwicklungsabhängigkeiten** (`uv add --dev`): `scipy-stubs`, `types-pyyaml` (für pyright
  strict in `src/`).
- Lizenzen: BSD (NumPy, SciPy, scipy-stubs), MIT (Pydantic, PyYAML), Apache-2.0 (types-pyyaml).
- Topologische Sortierung über `graphlib` aus der Standardbibliothek; NetworkX erst ab M4.
- Funktionen ≤ 40 Zeilen, Komplexität ≤ 10 (Gate); Familien als kleine Klassen, Dispatch über
  Register statt `if`-Ketten.

***

## 3. Modellformat (YAML, Schema-Version 1)

### 3.1 Aufbau

```yaml
schema_version: 1                # Pflicht, in M1 nur 1
model: t2_terminplan             # Modell-ID, Regeln wie Knoten-IDs
title: "Mini-Terminplan"         # optional, Anzeige
description: "…"                 # optional
settings: {n: 100000, seed: 20261027}   # optional; Standard n = 10000, seed = 0
nodes:
  <knoten_id>: { type: …, … }
```

- **Unbekannte Schlüssel werden abgewiesen** (`extra="forbid"`) – Tippfehler wie `sdd` fallen auf.
- **Doppelte YAML-Schlüssel werden abgewiesen** (eigener `SafeLoader`, Fehler mit Zeilennummer);
  PyYAML würde sonst still den letzten Wert nehmen und einen Knoten verschlucken.
- Nur `yaml.safe_load`-Semantik; keine Tags, keine Python-Objekte.
- Zahlen: YAML-Ganzzahl oder Gleitkommazahl; `1e5` wird als Zahl akzeptiert (PyYAML liest es als
  String – der Lader wandelt Strings, die als Gleitkommazahl parsebar sind, nur in **Zahlenfeldern**
  um; `n` muss ganzzahlig sein).

### 3.2 Knoten-IDs

- Regex `^[a-z][a-z0-9_]{0,63}$`.
- Verboten: Namen der Ausdrucksfunktionen (`min`, `max`, …), Python-Schlüsselwörter, `true`,
  `false`.
- Die ID ist die stabile Identität (Zufallsstrom, Referenzen). Der Anzeigename steht in `name`.

### 3.3 Gemeinsame Felder aller Knoten

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `type` | Enum | ja | `constant`, `uncertain`, `event`, `choice`, `derived`, `output` |
| `name` | str | nein | Anzeigename; Standard = ID |
| `unit` | str | nein | Freitext in M1 (keine Einheitenprüfung); wird unverändert gespeichert und durchgereicht |
| `description` | str | nein | Beschreibung |
| `why` | str oder `{text, links[], date}` | nein | Begründung, Recherchenotiz |
| `tags` | list[str] | nein | Gruppierung (ab M4 genutzt) |
| `bounds` | `{min?, max?}` | nein | Zulässiger Wertebereich; Verletzung → Hinweis mit Anteil, **keine Kappung** |
| `track` | bool | nein | Stichproben im Ergebnis behalten (Standard: nur bei `output`) |

### 3.4 Typspezifische Felder

| Typ | Felder | Ergebnis je Iteration |
|---|---|---|
| `constant` | `value: Zahl` | float, überall gleich |
| `uncertain` | `dist: <familie>`, `input: <modus>` (Standard `params`), Parameterfelder (Abschnitt 4) | float |
| `event` | `p: Zahl oder Ausdruck` | bool |
| `choice` | `options: [{label: str, weight: Zahl ≥ 0}, …]` (≥ 2 Optionen, Labels eindeutig) | Optionscode 0…k−1 |
| `derived` | `expr: Ausdruck` | float oder bool |
| `output` | `expr: Ausdruck`, `target: {le|lt|ge|gt: Zahl}` (optional, genau ein Operator) | float oder bool |

- **Parameter als Ausdruck:** Jeder Verteilungsparameter und `p` darf statt einer Zahl ein
  Ausdrucks-String sein (`mean: "12 - 4 * durchbruch_a"`). Strings in Parameterfeldern sind immer
  Ausdrücke.
- **Mindestens ein `output`** ist Pflicht (`model.no_output`).
- `choice`-Gewichte sind **relative** Gewichte (Summe > 0); das ist dokumentierte Semantik, keine
  Reparatur.

### 3.5 Beispiel

```yaml
schema_version: 1
model: t2_terminplan
title: "Mini-Terminplan: Serie und Parallelität"
settings: {n: 100000, seed: 20261027}
nodes:
  a: {type: uncertain, dist: normal, mean: 10, sd: 2, unit: d, name: "Vorgang A"}
  b: {type: uncertain, dist: normal, mean: 15, sd: 3, unit: d, name: "Vorgang B"}
  c: {type: uncertain, dist: normal, mean: 24, sd: 4, unit: d, name: "Vorgang C"}
  pfad1: {type: derived, expr: "a + b", unit: d, track: true}
  ende: {type: output, expr: "max(pfad1, c)", unit: d, target: {le: 30}}
```

### 3.6 Erweiterbarkeit des Schemas

Spätere Meilensteine ergänzen Schlüssel auf oberster Ebene (`scenarios`, `correlations`) und
Felder an Knoten (`horizon`) **additiv** bei `schema_version: 1`. Eine inkompatible Änderung
erhöht die Version; der Lader weist unbekannte Versionen mit `model.schema_version` ab.

***

## 4. Verteilungen

### 4.1 Vertrag einer Familie

Jede Familie implementiert das Protokoll `Family` (`dists/base.py`):

| Element | Bedeutung |
|---|---|
| `name` | Schlüssel im YAML (`dist:`) |
| `kind` | `continuous` oder `discrete` |
| `modes` | Eingabemodus → Liste der Parameterfelder (Pflicht/optional mit Standard) |
| `to_canonical(mode, params)` | Eingabeparameter → kanonische Parameter; arbeitet elementweise auf Arrays |
| `check(canonical)` | Liefert je Bedingung eine boolesche Maske „verletzt“ plus Fehlercode |
| `ppf(u, canonical)` | Inversionsmethode, vektorisiert über u und Parameterarrays |
| `reference(canonical)` | Eingefrorene SciPy-Verteilung für Tests (nur skalare Parameter) |

- **Literal-Parameter** werden beim Kompilieren geprüft (Fehler ohne Simulation).
- **Ausdrucks-Parameter** werden zur Laufzeit geprüft; verletzt eine Iteration eine Bedingung,
  bricht die Simulation mit `runtime.param_invalid` ab (Knoten, Parameter, Anteil betroffener
  Iterationen). Keine Kappung.
- Ein neues Register-Element (Klasse + `register()` + Test) genügt für eine neue Familie
  (Vorbereitung für M6, AK 5).

### 4.2 Die 14 Familien

Notation: kanonische Parameter fett; SciPy-Abbildung für `ppf` und Referenztest.

| `dist` | Modi und Eingabefelder | Kanonisch | Bedingungen | SciPy |
|---|---|---|---|---|
| `uniform` | `params`: low, high | **low, high** | low ≤ high | `uniform(loc=low, scale=high−low)` |
| `triangular` | `params` ≡ `three_point`: low, mode, high | **low, mode, high** | low ≤ mode ≤ high, low < high | `triang(c=(mode−low)/(high−low), loc=low, scale=high−low)` |
| `pert` | `params` ≡ `three_point`: low, mode, high, lambda (Standard 4) | **α, β, low, high** mit α = 1 + λ(mode−low)/(high−low), β = 1 + λ(high−mode)/(high−low) | low ≤ mode ≤ high, low < high, λ > 0 | `beta(α, β, loc=low, scale=high−low)` |
| `normal` | `params` ≡ `mean_sd`: mean, sd | **mean, sd** | sd > 0 | `norm(mean, sd)` |
| `truncnormal` | `params`: mean, sd, lower (Standard −∞), upper (Standard +∞) | **mean, sd, lower, upper** | sd > 0, lower < upper, mindestens eine Grenze endlich, Masse P(lower < X < upper) ≥ 1e−9 | `truncnorm((lower−mean)/sd, (upper−mean)/sd, loc=mean, scale=sd)` |
| `lognormal` | `params`: mu, sigma (log-Skala); `mean_sd`: mean, sd (Originalskala) | **mu, sigma** mit σ² = ln(1 + sd²/mean²), μ = ln(mean) − σ²/2 | sigma > 0; mean > 0, sd > 0 | `lognorm(s=sigma, scale=exp(mu))` |
| `beta` | `params`: alpha, beta, low (0), high (1); `mean_sd`: mean, sd, low (0), high (1) | **alpha, beta, low, high**; aus m' = (mean−low)/(high−low), v' = sd²/(high−low)²: ν = m'(1−m')/v' − 1, α = m'ν, β = (1−m')ν | alpha, beta > 0, low < high; im Modus `mean_sd`: low < mean < high, v' < m'(1−m') | `beta(alpha, beta, loc=low, scale=high−low)` |
| `student_t` | `params`: df, loc, scale | **df, loc, scale** | df > 2, scale > 0 | `t(df, loc, scale)` |
| `exponential` | `params`: rate; `mean`: mean | **rate** (= 1/mean) | rate > 0 | `expon(scale=1/rate)` |
| `gamma` | `params`: shape, scale; `mean_sd`: mean, sd | **shape, scale** mit shape = mean²/sd², scale = sd²/mean | shape, scale > 0; mean, sd > 0 | `gamma(shape, scale=scale)` |
| `weibull` | `params`: shape, scale, loc (0) | **shape, scale, loc** | shape, scale > 0 | `weibull_min(shape, loc, scale)` |
| `bernoulli` | `params`: p | **p** | 0 ≤ p ≤ 1 | `bernoulli(p)`; Wert 1.0/0.0 |
| `discrete` | `params`: values (Liste), weights (Liste, relativ) | **values, cumulative probabilities** | ≥ 1 Wert, gleiche Länge, Gewichte ≥ 0, Summe > 0, Werte eindeutig | eigene Inversion; Referenz `rv_discrete` |
| `poisson` | `params`: rate | **rate** | rate ≥ 0 | `poisson(rate)`; Wert als float |

**Festlegungen und Grenzfälle:**

- `uniform` mit low = high → wird als **Konstante** ausgewertet, Hinweis `uniform.degenerate`
  (PRD, Edge case). Der Zufallsstrom wird trotzdem verbraucht (Abschnitt 6), damit sich nichts
  verschiebt.
- Der Hinweis `uniform.degenerate` gilt nur für **literale** Grenzen. Sind low und high Ausdrücke
  und fallen in einzelnen Iterationen zusammen, ist der Wert dort ebenfalls konstant; ein Hinweis
  je Iteration wäre Rauschen und entfällt (Festlegung nach Review, 28.10.2026).
- `pert` und `triangular` mit mode = low oder mode = high sind zulässig (Randmodus).
- `pert`: λ = 4 ist **Produktkonvention**, nicht naturgegeben; der Standard wird in der
  Ergebnis-Metadatenliste der kanonischen Parameter sichtbar gespeichert.
- `truncnormal`: `mean`, `sd` sind Parameter der **unbeschnittenen** Normalverteilung, nicht
  Mittelwert und Streuung des Ergebnisses. Das wird in der Fehlermeldung bzw. Doku erklärt.
- `discrete`/`poisson`/`bernoulli` liefern float-Arrays; `event` liefert bool (Abschnitt 4.3).
- `discrete`: Inversion `values[searchsorted(cum, u, side="right")]` mit `cum` = kumulierte
  normierte Gewichte, `cum[-1]` exakt 1.0 gesetzt. Reihenfolge = YAML-Reihenfolge.
- **Erweiterte Modi** über AK 2 hinaus (z. B. Quantil-Eingabe) kommen in M5.

### 4.3 Ereignis und Auswahl

- `event` mit Wahrscheinlichkeit p: **Ereignis tritt ein ⇔ u < p.** Damit ist bei gleichem
  Zufallsstrom ein größeres p immer eine Obermenge der Eintritte (monotone Kopplung für M3).
  p = 0 → nie, p = 1 → immer (AK 9; u ∈ (0, 1) garantiert das, Abschnitt 6).
- `choice`: Option j gewählt ⇔ cum[j−1] ≤ u < cum[j]; Ergebnis ist der Code j.

***

## 5. Ausdruckssprache

### 5.1 Syntax

Ausdrücke werden mit `ast.parse(text, mode="eval")` geparst und gegen eine **Whitelist von
AST-Knoten** geprüft. Alles andere ist verboten (`expr.forbidden`, mit Konstrukt in der Meldung).

| Erlaubt | Bedeutung |
|---|---|
| `Constant` | int, float, bool; str **nur** als Vergleichspartner eines `choice`-Knotens |
| `Name` | Knoten-ID oder Funktionsname (nur in Aufrufposition) |
| `BinOp` | `+ - * / ** %` |
| `UnaryOp` | `-x`, `+x`, `not x` |
| `BoolOp` | `and`, `or` (elementweise) |
| `Compare` | `< <= > >= == !=`, auch verkettet (`0 < x < 1` ≡ `0 < x and x < 1`) |
| `Call` | Whitelist-Funktion, nur Positionsargumente |
| `List`/`Tuple` | **nur** als 2. und 3. Argument von `interp`, nur Zahlenliterale |

**Ausdrücklich verboten** (je eigener Test): Attribute (`x.y`), Indizes (`x[0]`), `lambda`,
Comprehensions, `a if c else b` (Hinweis: „`where(c, a, b)` verwenden“), Schlüsselwortargumente,
`*args`, Walross-Operator, f-Strings, Aufrufe von Nicht-Namen, unbekannte Funktionen
(`expr.unknown_function`), unbekannte Namen (`expr.unknown_name`, mit ähnlichstem Vorschlag via
`difflib`).

**Grenzen:** Länge ≤ 1000 Zeichen (`expr.too_long`), AST-Tiefe ≤ 32 (`expr.too_deep`),
≤ 500 AST-Knoten je Ausdruck (`expr.too_large`). Die Prüfung von Länge geschieht **vor**
`ast.parse`.

### 5.2 Funktionen

| Funktion | Arität | Semantik (elementweise über N) |
|---|---|---|
| `min(a, b, …)`, `max(a, b, …)` | ≥ 2 | `np.minimum`/`np.maximum` reduziert |
| `sum(a, b, …)` | ≥ 1 | Summe |
| `abs, exp, log, sqrt, floor, ceil` | 1 | NumPy-Pendant; `log` = natürlicher Logarithmus |
| `clip(x, lo, hi)` | 3 | `np.clip`; lo > hi → Laufzeitfehler |
| `where(c, a, b)` | 3 | `np.where(c, a, b)`; c muss bool sein |
| `interp(x, xs, ys)` | 3 | `np.interp`; xs, ys Literallisten gleicher Länge ≥ 2, xs streng steigend; außerhalb konstant fortgesetzt |

- Das Funktionsregister enthält je Funktion Arität, Argumenttypen und Implementierung; neue
  Funktionen kommen per `register_function()` hinzu.
- **Vorbereitung M4:** `min`/`max` werden als eigene Klassen implementiert, damit später die
  Gewinnerindizes ohne Umbau erfasst werden können. In M1 keine Erfassung.

### 5.3 Typen

Statische Typprüfung beim Kompilieren mit drei Typen: `num`, `bool`, `choice(<knoten>)`.

- `event` → bool; `choice` → choice; `constant`, `uncertain` → num; `derived`/`output` → Typ des
  Ausdrucks.
- Arithmetik und Vergleiche `< <= > >=` auf bool → bool wird als 0/1 behandelt (erlaubt, z. B.
  `5 * nacharbeit`). Logische Operatoren und die `where`-Bedingung verlangen bool (`expr.type`).
- `choice`-Knoten dürfen **nur** in `==`/`!=` mit einem String-Literal vorkommen; das Literal muss
  ein Label des Knotens sein (`expr.unknown_label`) und wird beim Kompilieren in den Code
  übersetzt. Jede andere Verwendung → `expr.choice_usage`.

### 5.4 Numerische Semantik

- Alle Zahlen float64; bool als NumPy-bool.
- Auswertung mit `np.errstate(all="ignore")`; danach wird **das Ergebnis jedes Knotens** auf
  nicht-endliche Werte geprüft. Treffer → `runtime.non_finite` mit Knoten und Anteil
  betroffener Iterationen (PRD, Edge case). Dadurch stört `log(0)` im nicht gewählten Zweig von
  `where(...)` nicht, ein nicht-endliches Endergebnis aber immer.
- Division durch null, `sqrt` negativer Zahlen, `0 ** -1` usw. erzeugen inf/nan und fallen unter
  diese Regel.

***

## 6. Zufallszahlen und Simulation

### 6.1 Ströme je Knoten

- Lauf-Seed `seed` (int ≥ 0). Je zufälligem Knoten (`uncertain`, `event`, `choice`):
  `SeedSequence(entropy=seed, spawn_key=(key(node_id),))` mit
  `key(id) = int.from_bytes(sha256(id.encode("utf-8")).digest()[:8], "big")`.
- Generator: `numpy.random.Generator(PCG64(seq))`.
- Jeder zufällige Knoten verbraucht **genau N Gleichverteilte**: `u = gen.random(N)`, danach
  `u[u == 0.0] = 2**-53` → u ∈ (0, 1). Damit ist `ppf(u)` für alle Familien endlich.
- Folgen:
  - Ein neuer, unabhängiger Knoten ändert keine bestehenden Ziehungen (AK 8).
  - Ein geänderter Anzeigename ändert nichts; eine geänderte ID ändert den Strom des Knotens
    (dokumentiert).
  - Die ersten n Ziehungen eines Laufs mit N > n stimmen mit einem Lauf der Länge n überein
    (Präfixeigenschaft; Test).
- Die Inversionsmethode ist Pflicht für alle Familien (PRD Constraints): Gleiche u, geänderter
  Parameter → monoton gekoppelte Werte (Voraussetzung für M3 AK 6).

### 6.2 Ablauf von `simulate(compiled, n, seed)`

1. n ∈ [1, 2 000 000] prüfen (`sim.n_range`), Standard aus `settings`.
2. Knoten in topologischer Reihenfolge auswerten; jeder Knoten **genau einmal** je Lauf, sein
   Array wird für alle Referenzen wiederverwendet (AK 7).
3. Je zufälligem Knoten: Ströme erzeugen → Parameterausdrücke auswerten → kanonisch umrechnen →
   Laufzeitprüfung → `ppf`.
4. Nach jedem Knoten: Endlichkeitsprüfung (5.4) und `bounds`-Prüfung (Hinweis
   `range.violation` mit Anteil unter `min` bzw. über `max`).
5. Arrays nicht mehr benötigter, nicht getrackter Knoten freigeben (Referenzzählung), damit der
   Speicher bei großen Modellen begrenzt bleibt.
6. Ergebnis zusammenstellen.

### 6.3 `SimulationResult`

| Feld | Inhalt |
|---|---|
| `samples` | dict ID → Array (alle `output`- und `track: true`-Knoten) |
| `meta` | `model_id`, `model_hash` (SHA-256 über kanonisches JSON des validierten Modells), `schema_version`, `n`, `seed`, `generator: "PCG64"`, `stream_derivation: "sha256-spawn-key-v1"`, Versionen von risk-pilot, NumPy, SciPy, Python, Zeitstempel (UTC) |
| `canonical` | dict ID → kanonische Parameter literaler Verteilungen (AK 2: Modus **und** kanonische Werte) |
| `warnings` | Liste von `Notice` (Abschnitt 9) |

- Die Paketversion in `meta` liest `importlib.metadata` aus den installierten Paketmetadaten. Das
  ist kein Modell-, Nutzer- oder Netzwerkzugriff und gilt nicht als I/O im Sinne der
  Kernregel (Festlegung nach Review, 28.10.2026).
- **Reproduzierbarkeit (AK 8):** gleiches Modell, `n`, `seed` und gleiche Paketversionen →
  `samples` bitgleich. Bitgleichheit wird nur innerhalb einer festen Umgebung zugesagt.

***

## 7. Statistik (`analysis/stats.py`)

`summarize(x, *, quantiles=(0.05, 0.1, 0.5, 0.9, 0.95), target=None, conf=0.95) -> Summary`

| Kennzahl | Verfahren |
|---|---|
| Mittelwert, Standardfehler | `mean`, `std(ddof=1)/√N`; bei N = 1 Standardfehler = nan mit Hinweis |
| Standardabweichung, Varianz | `ddof=1` |
| Quantile (Punkt) | `np.quantile(..., method="linear")` (Hyndman-Fan Typ 7); Verfahren steht in `Summary.method` |
| Quantil-Konfidenzintervall | Verteilungsfrei über Ordnungsstatistiken: Ränge l = `binom.ppf((1−conf)/2, N, q)`, u = `binom.ppf(1−(1−conf)/2, N, q) + 1`, begrenzt auf [1, N]; Intervall = (x₍l₎, x₍u₎) der sortierten Stichprobe |
| P(Ziel erreicht) | Anteil `x <op> wert` gemäß `target`; Intervall nach **Wilson** zum Niveau `conf` |
| Bool-Ausgaben | Nur Anteil `True` mit Wilson-Intervall |
| Min, Max | Stichprobenextreme |

- **Wilson:** p̂ = k/N, z = Φ⁻¹(1 − (1−conf)/2),
  Mitte = (p̂ + z²/2N)/(1 + z²/N), Halbbreite = z/(1 + z²/N) · √(p̂(1−p̂)/N + z²/4N²).
  Bei k = 0 ist die obere Grenze z²/(N + z²) > 0 (AK 10).
- `quantiles` sind frei wählbar, jedes q ∈ (0, 1) (`stats.quantile_range` sonst).
- Ergebnistexte erzeugt M2; `Summary` enthält nur Zahlen und Verfahrensnamen.

***

## 8. Analytische Referenzen (`analysis/analytic.py`)

| Funktion | Inhalt |
|---|---|
| `ks_distance(x, cdf)` | D = max(maxᵢ(i/N − F(x₍ᵢ₎)), maxᵢ(F(x₍ᵢ₎) − (i−1)/N)) |
| `dkw_epsilon(n, alpha=0.001)` | √(ln(2/α)/(2n)); bei n = 100 000 ≈ 0.00616 |
| `sum_uniform01_pdf/cdf(s)` | Dreieck auf [0, 2] |
| `grid_convolve(pdf1, pdf2, lo1, hi1, lo2, hi2, h)` | Dichten auf Gitter mit Schrittweite h abtasten, Trapezgewichte an den Rändern, `np.convolve`·h, CDF per kumulativer Trapezregel; liefert (Gitter, pdf, cdf) |
| `max_of_normals_cdf(t, m1, s1, m2, s2)` | Φ((t−m1)/s1)·Φ((t−m2)/s2) |
| `clark_mean(m1, s1, m2, s2)` | m1Φ(α) + m2Φ(−α) + θφ(α), θ = √(s1² + s2²), α = (m1−m2)/θ |
| `p_greater_normal(m1, s1, m2, s2)` | Φ((m1−m2)/θ) (für M4 AK 2) |

- Gemessen am 27.10.2026: Gitterfaltung U(0,1) ⋆ U(0,1) mit h = 10⁻³ weicht höchstens 4·10⁻⁷ von
  der analytischen CDF ab; AK 11 verlangt ≤ 0.001.
- Referenzwerte T2: Clark-Mittelwert 26.6853; P(P₁ > P₂) = 0.57366 (per Simulation mit N = 10⁶
  bestätigt).

***

## 9. Fehler und Hinweise (`errors.py`)

```text
RiskPilotError
├── ModelError          (enthält list[Issue]; alle Probleme eines Modells auf einmal)
└── SimulationError     (enthält genau ein Issue; Abbruch zur Laufzeit)
Issue  = {code, node_id | None, field | None, line | None, params: dict}
Notice = {code, node_id | None, share | None, params: dict}   (Hinweis, kein Abbruch)
```

- **Kein Text im Fehlerobjekt.** `code` ist stabil und englisch, `params` enthält die Werte für
  die Meldung (z. B. `{"value": -1, "cycle": ["a", "b"]}`). Tests prüfen Codes und Parameter.
- **Meldungskatalog** `messages.py`: `CATALOG: dict[str, dict[str, str]]` (Sprache → Code →
  Vorlage mit `{platzhaltern}`) und `render(item: Issue | Notice, lang: str = "de") -> str`.
  In M1 ist nur `de` befüllt; fehlt eine Sprache, fällt `render` auf `de` zurück. Englisch
  kommt ohne Umbau hinzu; ab M2 nutzt die UI denselben Mechanismus.
- **Vollständigkeitstest:** Jeder in `errors.py` definierte Code hat eine `de`-Vorlage, und jede
  Vorlage lässt sich mit den dokumentierten Parametern ohne `KeyError` formatieren.
- Die Validierung **sammelt** alle Probleme eines Modells, statt beim ersten abzubrechen.

| Code | Wann |
|---|---|
| `yaml.syntax` | YAML nicht parsebar (mit Zeile) |
| `yaml.duplicate_key` | Doppelter Schlüssel (mit Zeile) |
| `model.schema` | Schemaverletzung (Pydantic-Fehler in Issue übersetzt: Feldpfad, Ursache) |
| `model.schema_version` | Unbekannte Version |
| `model.no_output` | Kein `output`-Knoten |
| `model.empty` | Keine Knoten |
| `node.id_invalid` | ID verletzt Regex oder ist reserviert |
| `dist.unknown` / `dist.mode_unknown` | Unbekannte Familie bzw. Eingabemodus |
| `param.missing` / `param.unknown` | Pflichtparameter fehlt / Parameter gehört nicht zum Modus |
| `param.invalid` | Literalparameter verletzt Bedingung (Feld = Parametername) |
| `expr.syntax`, `expr.forbidden`, `expr.unknown_name`, `expr.unknown_function`, `expr.arity`, `expr.type`, `expr.too_long`, `expr.too_deep`, `expr.too_large`, `expr.unknown_label`, `expr.choice_usage`, `expr.interp_table` | Ausdrucksfehler |
| `graph.cycle` | Zyklus; Meldung nennt die Knoten in Zyklusreihenfolge |
| `sim.n_range` | n außerhalb [1, 2 000 000] |
| `runtime.param_invalid` | Ausdrucksparameter in einem Anteil der Iterationen ungültig |
| `runtime.non_finite` | Knotenergebnis nicht endlich (Anteil) |
| `runtime.clip_bounds` | `clip` mit lo > hi |
| Hinweis `range.violation` | Werte außerhalb `bounds` (Anteil unter/über) |
| Hinweis `uniform.degenerate` | low = high, als Konstante ausgewertet |
| Hinweis `stats.single_sample` | N = 1, kein Standardfehler |

***

## 10. Öffentliche Schnittstellen

```python
# model/yaml_io.py
def model_from_yaml(text: str) -> Model: ...            # ModelError bei Syntax/Schema

# adapters/files.py
def load_model(path: Path) -> Model: ...                # liest UTF-8, ruft model_from_yaml

# model/compile.py
def compile_model(model: Model) -> CompiledModel: ...   # ModelError mit allen Issues

# engine/simulate.py
def simulate(compiled: CompiledModel, n: int | None = None,
             seed: int | None = None) -> SimulationResult: ...

# analysis/stats.py
def summarize(x: NDArray[np.float64] | NDArray[np.bool_], *,
              quantiles: Sequence[float] = (0.05, 0.1, 0.5, 0.9, 0.95),
              target: Target | None = None, conf: float = 0.95) -> Summary: ...

# dists/registry.py, expr/functions.py
def register(family: Family) -> None: ...
def register_function(fn: ExprFunction) -> None: ...
```

- `CompiledModel` ist unveränderlich (frozen dataclass): topologische Ordnung, kompilierte
  Ausdrucksbäume, Familien und kanonische Literalparameter, Typen, Modell-Hash.
- Alle Typen sind vollständig annotiert (pyright strict in `src/`).

***

## 11. Tests

### 11.1 Zuordnung zu den Abnahmekriterien

| PRD-AK | Testdatei | Kernprüfungen |
|---|---|---|
| 1 | `tests/test_dists.py` | Je kontinuierliche Familie (parametrisiert): N = 100 000, fester Seed, `ks_distance` gegen `reference().cdf` < `dkw_epsilon`. Diskrete Familien: Häufigkeiten je Wert im Wilson-Intervall 99.9 % um die Sollwahrscheinlichkeit |
| 2 | `tests/test_dists.py` | Lognormal `mean_sd` → exakte Formel (rel. 1e−12); Beta und Gamma `mean_sd` → Momente der Referenzverteilung treffen mean/sd (rel. 1e−9); PERT/Dreieck-Abbildung; `canonical` im Ergebnis enthält Modus und kanonische Werte |
| 3 | `tests/test_validation.py` | Je Bedingung aus Tabelle 4.2 ein ungültiger Fall → `param.invalid` mit richtiger `node_id` und `field` |
| 4 | `tests/test_expr.py` | Jede Funktion und jeder Operator gegen NumPy-Erwartung; jedes verbotene Konstrukt aus 5.1 → passender Code; Grenzen Länge/Tiefe/Größe; Typfehler; `choice`-Vergleich |
| 5 | `tests/test_engine.py` | Bedingte Verteilung: `b ~ normal(mean = "10 * e", sd = 1)` mit Ereignis e → bedingte Mittelwerte je Zweig im Mittelwert-Kriterium; ungültiger Ausdrucksparameter → `runtime.param_invalid` mit Anteil |
| 6 | `tests/test_graph.py` | Zyklus a→b→c→a → `graph.cycle` mit allen drei Knoten; Selbstreferenz; unverbundene Knoten erlaubt |
| 7 | `tests/test_engine.py` | `a = x`, `b = x` → `a == b` überall; `x - x == 0` überall |
| 8 | `tests/test_engine.py` | Zwei Läufe bitgleich; zusätzlicher unabhängiger Knoten → bestehende Arrays bitgleich; geänderter `name` → bitgleich; Präfixeigenschaft n < N |
| 9 | `tests/test_engine.py` | Konstante exakt; `event` p = 0 nie, p = 1 immer; Monotonie: p₁ < p₂ → Eintritte(p₁) ⊆ Eintritte(p₂) |
| — | `tests/test_messages.py` | Jeder Code hat eine `de`-Vorlage; `render` formatiert jede Vorlage; Rückfall auf `de` bei unbekannter Sprache |
| — | `tests/test_yaml_io.py` | `unit` (z. B. `"Mio. EUR"`, Sonderzeichen, Umlaute) kommt unverändert im Modell an |
| 10 | `tests/test_stats.py` | Mittelwert/SE an bekannten Arrays; Quantil-KI-Ränge gegen manuelle Binomialrechnung; Überdeckung des Quantil-KI für den Median von U(0,1) über 200 kleine Läufe ≥ 0.9; Wilson gegen Literaturwert; k = 0 → obere Grenze > 0 |
| 11 | `tests/test_examples.py` | T1 aus `examples/`: KS < ε, Mittelwert-Kriterium gegen 1, Varianz ±2 % um 1/6; `grid_convolve` ≤ 0.001 gegen analytische CDF |
| 12 | `tests/test_examples.py` | T2 aus `examples/`: KS gegen `max_of_normals_cdf`, Mittelwert-Kriterium gegen `clark_mean` |
| Edge cases | `tests/test_validation.py`, `tests/test_yaml_io.py` | uniform a = b → Konstante + Hinweis; PERT Randmodus; `bounds` → `range.violation` mit Anteil, Werte unverändert; `log(0)` → `runtime.non_finite`; `log(0)` im nicht gewählten `where`-Zweig → kein Fehler; ungültiges YAML → `yaml.syntax` mit Zeile; doppelte Knoten-ID → `yaml.duplicate_key` |

### 11.2 Eigenschaftstests (ohne neue Abhängigkeit, parametrisiert)

- Umbenennen des Anzeigenamens ändert keine Zahl (siehe AK 8).
- Ein ungenutzter Knoten ändert keine Ausgabe.
- Skalierung: `output = k * x` mit k > 0 skaliert Mittelwert und Quantile exakt um k.
- Additive Erhöhung: Erhöhen des Mittelwerts eines Summanden senkt keine Iteration des Ergebnisses
  (Kopplung über Inversionsmethode).
- `model_from_yaml(dump(model))` ergibt dasselbe Modell (Rundlauf).

### 11.3 Laufzeit

- Ziel für die M1-Tests zusammen: ≤ 15 s, damit die Gesamtsuite im 60-s-Gate bleibt. Gemessen
  27.10.2026: `ppf` für 100 000 Werte ≤ 0.12 s je Familie (beta, student_t am langsamsten).
- Größere Stichproben (N = 10⁶) nur in einem Benchmarkskript `scripts/bench_m1.py` außerhalb der
  Suite. Ziel aus dem PRD (30 Knoten × 100 000 Iterationen < 5 s) wird damit gemessen und im
  Abschlussbericht von M1 berichtet.
  **Gemessen 28.10.2026:** 0,51 s (bestes von drei Läufen, Entwicklungsrechner, 32 Kerne);
  Gesamtsuite 425 Tests in 1,7 s.
- Alle Zufallstests mit festem Seed; Toleranzen aus PRD Abschnitt 3 (α = 0.001).

***

## 12. Beispieldateien

**`examples/t1_faltung.yaml`**

```yaml
schema_version: 1
model: t1_faltung
title: "Faltung: Summe zweier Unsicherheiten"
description: "Zwei unabhängige Gleichverteilungen; die Summe ist dreieckverteilt."
settings: {n: 100000, seed: 20261027}
nodes:
  x1: {type: uncertain, dist: uniform, low: 0, high: 1, name: "Unsicherheit 1"}
  x2: {type: uncertain, dist: uniform, low: 0, high: 1, name: "Unsicherheit 2"}
  s:  {type: output, expr: "x1 + x2", name: "Summe"}
```

**`examples/t2_terminplan.yaml`**: wie Abschnitt 3.5.

Beide Dateien tragen kein `why`, weil ihre Werte didaktisch gesetzt und nicht recherchiert sind;
die Erklärtexte der Tutorials kommen mit M2.

***

## 13. Arbeitspakete

Jedes Paket: Test zuerst, Fehlschlag aus dem erwarteten Grund zeigen, minimal implementieren, Gate,
kleiner Commit (auf Anweisung).

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP0 | Abhängigkeiten hinzufügen, Paketgerüst, Platzhalter `slugify` entfernen | Gate grün mit leerem Gerüst |
| AP1 | `errors.py`, `messages.py`, `schema.py`, `yaml_io.py` (inkl. Duplikat-Loader) | Tests für Schema, IDs, YAML-Fehler grün |
| AP2 | `expr/` Parser, Typprüfung, Funktionen, Auswertung | `test_expr.py` grün |
| AP3 | `dists/` Register und 14 Familien | `test_dists.py` grün (AK 1–3) |
| AP4 | `graph.py`, `compile.py` | `test_graph.py`, `test_validation.py` grün (AK 6) |
| AP5 | `engine/` Ströme und `simulate` | `test_engine.py` grün (AK 5, 7–9) |
| AP6 | `analysis/stats.py` | `test_stats.py` grün (AK 10) |
| AP7 | `analysis/analytic.py`, Beispiele, `adapters/files.py` | `test_examples.py` grün (AK 11–12) |
| AP8 | Benchmark, Dokumentation, PRD-Status | Siehe Abschnitt 14 |

**Reihenfolge:** AP0 → AP1 → (AP2 ∥ AP3) → AP4 → AP5 → AP6 → AP7 → AP8.

***

## 14. Abschluss von M1

- [ ] PRD M1 AK 1–12 und alle Edge cases durch die Tests in Abschnitt 11 belegt.
- [ ] `uv run pre-commit run --all-files` grün; neue Dateien vorher `git add`.
- [ ] Benchmarkergebnis (30 Knoten × 100 000) dokumentiert; bei Verfehlen Risiko im PRD
      aktualisieren.
- [ ] `docs/architecture.md`: Tabelle der Codeschichten auf die Pakete aus Abschnitt 2
      aktualisiert.
- [ ] README: Abschnitt „Risk Pilot“ mit Zweck und Verweis auf PRD (Template-Text bleibt bis M2).
- [ ] PRD M1 **Status:** `done (verified by: tests/test_dists.py, test_expr.py, test_graph.py,
      test_validation.py, test_engine.py, test_stats.py, test_examples.py, test_yaml_io.py)`.
- [ ] Review durch den `reviewer`-Agenten gegen PRD M1 und dieses Pflichtenheft.
