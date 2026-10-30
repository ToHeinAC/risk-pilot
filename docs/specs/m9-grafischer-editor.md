# Pflichtenheft M9 — Grafischer Editor

**Stand:** 30. Oktober 2026, umgesetzt; E1–E10 bestätigt (30.10.2026); AP1–AP7 erledigt ·
**Bezug:** [PRD.md](../../PRD.md), Meilenstein M9 · **Voraussetzung:** M1–M8

Dieses Pflichtenheft legt fest, **wie** M9 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Warum

Ein Modell entsteht heute über Knotentabelle, Knotenkarte und YAML; Abhängigkeiten entstehen
nur indirekt, indem ein Ausdruck einen anderen Knoten nennt (`max(a + 15, 24)`). Szenarien
werden auf einer eigenen Seite per Formular gepflegt. Rückmeldung vom 30.10.2026: Projekte und
Szenarien zusammenzustellen ist noch zu komplex. Gewünscht ist ein Aufbau auf einer
Zeichenfläche wie in n8n: Knoten platzieren, verbinden, und die Art der Verknüpfung in einem
Dialog mit Vorauswahlen festlegen.

**Leitbild:** n8n (Workflow-Canvas). Übernommen wird das Bedienprinzip: Palette → Knoten auf
die Fläche, Ausgang → Eingang ziehen, Dialog zur Konfiguration, Fläche zeigt den Zustand. Nicht
übernommen: Ausführung entlang der Kanten (in Risk Pilot rechnet die Engine das ganze Modell),
n8n-Optik.

## 2. Umfang

**In M9:** Zeichenfläche (Canvas) auf der Modellseite mit Palette, Verbinden mit
Verknüpfungsdialog, Kanten löschen, Knoten verschieben, Layout im YAML, Szenario-Modus mit
Override-Dialog, Spike zur Wahl der Canvas-Komponente.

**Nicht in M9:** visuelles Programmieren freier Formeln (Ausdrücke bleiben Text), neue
Knotentypen, Ausführung oder Vorschau entlang einzelner Kanten, Gruppen/Unterflüsse,
Mehrbenutzer-Bearbeitung, Undo über die Sitzung hinaus.

## 3. Grundsatz: YAML bleibt die Quelle (E1)

- Die Fläche ist eine **Ansicht mit Bearbeitung**, kein zweites Modell. Jede Aktion auf der
  Fläche ist eine reine Funktion `Data → Data` in `src/app/model/canvas.py` und wird wie die
  Formular-Änderungen über `yaml_patch.patch` geschrieben (Kommentare und Formatierung bleiben).
- Kanten werden **aus dem Modell abgeleitet** (`graph.edges`): eine Kante existiert genau dann,
  wenn ein Ausdruck die Quelle nennt (Arten `ausdruck`, `parameter`) oder beide Knoten in einer
  Korrelationsgruppe stehen (`korrelation`). Es gibt keine gespeicherten Kanten.
- Keine stille Reparatur (PRD §3): lässt sich eine Kante nicht eindeutig aus einem Ausdruck
  entfernen, öffnet der Dialog den Ausdruck zur Bearbeitung, statt ihn umzuschreiben.
- Formular, Tabelle und YAML-Editor bleiben erhalten und zeigen denselben Entwurf.

## 4. Verknüpfungsdialog (E4)

Zieht man eine Verbindung von A nach B, öffnet sich ein Dialog. Angeboten wird nur, was für den
Typ von B (und A) gültig ist; die Vorauswahl ist die erste Zeile.

| Ziel B | Vorauswahlen | Ergebnis im YAML |
|---|---|---|
| `derived`, `output` ohne Ausdruck | Serie (Summe), Parallel – alle fertig (Maximum), Erster fertig (Minimum), Produkt, Übernehmen | `expr: "a"`, später `"a + b"`, `"max(a, b)"`, … |
| `derived`, `output` mit Vorauswahl-Ausdruck | „A zur Summe/zum Maximum … hinzufügen“ | Argument wird angehängt: `max(a, b)` → `max(a, b, c)` |
| `derived`, `output` mit freiem Ausdruck | „Ausdruck bearbeiten“ mit `a` an der Schreibmarke eingefügt | Nutzer prüft und bestätigt |
| beliebig, Quelle ist `event` | Verzögerung bei Eintritt (Wert oder Knoten), Wahl zwischen zwei Werten | `b + where(e, x, 0)`, `where(e, x, y)` |
| `uncertain` | Parameter von B hängt von A ab (Parameter wählen, Faktor) | `mean: "a * 1.0"` |
| `event` | Eintrittswahrscheinlichkeit aus A | `p: "a"` (Prüfung [0, 1] wie bisher) |
| zwei `uncertain` (eigener Griff) | korreliert mit ρ (Gruppe wählen oder neu) | Eintrag in `correlations` |

Der Dialog zeigt vor dem Übernehmen den entstehenden Ausdruck in Klartext und in Modellsprache
(„Ende = Maximum aus Pfad 1 und Pfad 2“). Ungültige Verbindungen (Zyklus, Ausgang als Quelle
eines `choice`, A = B) lehnt die Fläche mit der bekannten Meldung ab.

**Kante löschen:** Bei Vorauswahl-Ausdrücken wird das Argument entfernt (`max(a, b, c)` →
`max(a, b)`; bleibt ein Argument, wird es `a`). Bei freien Ausdrücken öffnet sich der Ausdruck.

**Umgesetzt (AP3, 30.10.2026)** in `src/app/model/canvas.py`: `presets` (prüft A = B und Kreis,
liefert die Vorauswahlen, freie Ausdrücke als `edit`), `connect` (Summe, Maximum, Minimum,
Produkt, Verzögerung `+ where(e, x, 0)`, Parameter mit Faktor `a * f`, Wahrscheinlichkeit),
`disconnect` (entfernt ein Argument; sonst Fehler mit dem zu öffnenden Feld), `correlate` und
`uncorrelate` (Gruppe anlegen, erweitern, Eintrag setzen; unkorrelierte Mitglieder und Gruppen
unter zwei Knoten fallen weg). Noch nicht umgesetzt: „Wahl zwischen zwei Werten“
(`where(e, x, y)`) und „Übernehmen“ – beide nur für leere Ausdrücke sinnvoll; mit E4 zu klären.

**Fläche (AP4, 30.10.2026):** `src/app/web/canvas/` (Vue-Flow-Element, Bündel in `lib/`,
THIRD_PARTY_NOTICES.md), `present/canvas_view.py` (Knoten und Kanten aus dem Roh-Entwurf, auch
bei ungültigem Modell; Kanten-ID `art:quelle->ziel`), Werkbank: Verschieben schreibt `layout`,
Klick öffnet die Karte, „Neu anordnen“, „Ansicht einpassen“; die Ansicht wird nur beim ersten
Zeichnen eingepasst, spätere Änderungen behalten Zoom und Ausschnitt. Tutorials sind nur
Ansicht. Verbinden und Kante löschen sind bis AP5 abgeschaltet. Die Farbe nach relativer
Streuung des alten Graphen entfällt; die Tabelle darunter zeigt P10/P50/P90.

**Dialog (AP5, 30.10.2026):** `web/canvas_dialogs.py`. Vorauswahl, Parameter, Faktor,
Verzögerung oder ρ; davor der Satz in Klartext (`canvas_view.describe`) und das geänderte Feld
in Modellsprache. Abweichungen vom Entwurf: Korrelation wird im selben Dialog angeboten, wenn
Quelle und Ziel zufällig sind (unsicher oder Ereignis), nicht über einen eigenen Griff; „Ausdruck
bearbeiten“ öffnet die Karte des Ziels, die Quelle wird nicht an der Schreibmarke eingefügt.
Abgelehnte Verbindungen (Kreis, A = B, Ziel ohne Vorauswahl) melden sich mit einem Hinweis.

## 5. Palette und neue Knoten (E5)

Palette am linken Rand mit den sechs Knotentypen. Ziehen auf die Fläche öffnet einen kurzen
Dialog: ID (Vorschlag aus dem Namen), Name, Einheit; ein unsicherer Knoten startet mit der
Spanne P10/P50/P90 (E14 aus M8). Der Knoten erscheint an der Ablagestelle; seine Karte öffnet
sich rechts wie heute nach einem Graph-Klick.

**Umgesetzt (AP5, 30.10.2026):** Palette in der Fläche (`flow_canvas.js`), Ziehen oder Klick
(Mitte der sichtbaren Fläche); `canvas.suggest_id` (Umlaute als ae/oe/ue/ss, freie und gültige
ID), `canvas.place`. Pflichtfelder bleiben leer und werden gemeldet, bis die Karte sie füllt.

## 6. Layout im YAML (E2)

```yaml
layout:
  a: [0, 120]
  ende: [480, 60]
```

- Optionaler Block `layout: {Knoten-ID: [x, y]}` auf oberster Ebene; schema_version bleibt 1.
- Zählt nicht zum Inhalts-Hash (wie `title`, `description`): Verschieben ändert keine Zahl und
  macht keinen Lauf ungültig.
- Knoten ohne Position werden nach dem bestehenden Schichten-Layout (`structure.positions`)
  platziert; ein Schalter „Neu anordnen“ setzt alle Positionen danach.
- Positionen unbekannter Knoten sind ein Hinweis (`Notice`), kein Fehler; „Speichern“ entfernt
  sie nicht still, der Hinweis bietet das Entfernen an.
- Tutorials in `examples/` erhalten ein Layout, damit sie beim Öffnen aufgeräumt aussehen.
- Umgesetzt (AP2, 30.10.2026): `model/layout.py` (`move`, `arrange`, `placed`, `prune`,
  `without`), Hinweis `layout.unknown_node` mit Knopf „Positionen unbekannter Knoten
  entfernen“ auf der Modellseite; Löschen eines Knotens entfernt seine Position mit. Neue
  Listen aus reinen Werten schreibt `yaml_patch` im Flow-Stil (`a: [0, 120]`). Positionen sind
  ganze Pixel, ein Schichtabstand 220, ein Zeilenabstand 110.

## 7. Szenario-Modus (E3)

- Oben auf der Fläche wählt ein Auswahlfeld das Szenario (Vorgabe: Hauptszenario `basis`).
- Im Hauptszenario ist die Fläche voll bearbeitbar. In einem Unterszenario ist die Struktur
  gesperrt (keine neuen Knoten oder Kanten); Knoten mit Overrides sind markiert, die Zahl der
  Overrides steht am Knoten.
- Klick auf einen Knoten öffnet den Override-Dialog: Feld (nur überschreibbare Felder des Typs,
  `scenarios._allowed`), Wert des Elternszenarios zum Vergleich, neuer Wert, Begründung. Ein
  bestehender Override lässt sich dort ändern oder entfernen.
- Neues Szenario direkt im Auswahlfeld („+ Szenario aus aktuellem ableiten“).
- Abgelöste Szenarien (`nodes` eigenständig) zeigen ihre eigene Struktur, schreibgeschützt mit
  Hinweis; Bearbeitung weiter über YAML.

**Umgesetzt (AP6, 30.10.2026):** `web/canvas_panel.py` (Fläche, Werkzeugleiste, Szenario-Auswahl,
Ereignisse), `web/canvas_scenario.py` (Override-Dialog, „Unterszenario ableiten“ vom gewählten
Szenario), in `model/scenarios.py` `changed_nodes`, `overridable` (Parameter zuerst, dann `dist`
und `bounds`) und `parent_value`. Im Szenario sind Palette, Verbinden und Kante löschen aus;
Versuche melden „Struktur gesperrt“. Verschieben bleibt erlaubt, die Positionen gelten für alle
Szenarien. Die Karte rechts zeigt weiter die Werte des Hauptszenarios. Änderungen laufen über
`scenario_edit.apply` (nur gültige Modelle).

## 8. Phase 1 — Spike (E6)

Wie in M7: zeitlich begrenzt, Entscheidung mit Begründung, Abbruch erlaubt.

**Kandidaten** (MIT, lokal gebündelt, keine CDN-Abhängigkeit zur Laufzeit):

| Kandidat | Für | Gegen |
|---|---|---|
| Vue Flow | Vue 3 wie NiceGUI; n8n baut seinen Canvas darauf; eigene Knoten als Vue-Komponenten | braucht ESM-Bündel mit `vue` als extern; Einbindung in NiceGUI zu prüfen |
| Drawflow | reines JS ohne Abhängigkeiten, klein, einfach einzubinden | weniger gepflegt; eigene Knoten nur als HTML-Strings |

**Spike-Aufgaben an T2:** Knoten aus `layout`/Auto-Layout zeichnen, verschieben → Position im
YAML, verbinden → Ereignis in Python → Dialog, Kante löschen, Szenario-Markierung, eine
Fläche mit 100 Knoten flüssig.

**Kriterien:** Ereignisse kommen als Python-Callbacks an; Bedienung ohne Neuladen der Fläche bei
jeder Änderung; Oberflächentests ohne Browser möglich (die Fläche sendet Ereignisse, die Tests
lösen dieselben Ereignisse aus); Lizenz und Bündelgröße; Darstellung hell/dunkel.

### 8.1 Ergebnis des Spikes (30.10.2026)

Branch `spike/canvas`, Worktree `../risk-pilot-spike-m9`, Seite `/spike` auf Port 8643. Beide
Kandidaten hinter denselben Props (`nodes`, `edges`) und Ereignissen (`connect`, `disconnect`,
`move`, `pick`). Code: `src/app/model/canvas.py` (Vorauswahlen verbinden/lösen, reine
Funktionen), `src/app/web/canvas/` (zwei Komponenten, gebündelte Bibliotheken),
`src/app/web/spike_canvas.py`; Tests `tests/test_canvas_spike.py` (13 Tests, offline).

| Kriterium | Vue Flow 1.48.2 | Drawflow 0.0.60 |
|---|---|---|
| Lizenz, Bündel | MIT, ESM 161 KB (esbuild, `vue` extern) | MIT, UMD 46 KB |
| Einbindung | als Vue-Komponente über die Importmap (`esm=`) | klassisches `<script>`, über `window` |
| Ereignisse in Python | Verbinden → Dialog, Verschieben, Kante löschen im Browser geprüft | ebenso |
| Ohne Neuladen | Props werden aktualisiert, Zoom und Ausschnitt bleiben | jede Änderung zeichnet neu, Zoom geht verloren |
| 100 Knoten | 25 ms Server, sichtbar nach 375 ms | gezeichnet |
| Tests ohne Browser | `trigger(event, args)` auf der Fläche | ebenso |
| Wartung | aktiv; Grundlage des n8n-Canvas | letzte Version 2022 |

**Entscheid E6:** Vue Flow, Urteil des Nutzers am laufenden Spike (30.10.2026). Der Spike-Code
bleibt auf seinem Branch und dient als Vorlage, nicht als Merge-Basis.

**Befunde für die Umsetzung:**

- Ansicht nach jedem Neuzeichnen einpassen (`fit-view-on-init` wirkt nur beim ersten Laden);
  Minimap und Zoom-Knöpfe als Zusatzpakete (MIT) prüfen.
- Gebündelte Dateien in THIRD_PARTY_NOTICES.md aufnehmen und von den Format-Hooks ausnehmen
  (`exclude` in `.pre-commit-config.yaml`), damit sie byte-gleich bleiben.
- Das Wurzelelement der Komponente darf keine Inline-Höhe setzen; sonst überschreibt sie die
  Klasse und die Fläche hat die Höhe 0.
- Freie Ausdrücke werden nie umgeschrieben: Kante `nacharbeit → pfad1` in T2 löschen ergibt
  einen Hinweis (stützt E9).
- Positionen hält der Spike nur im Speicher; Speichern im YAML ist AP2.

### 8.2 Nachträge nach dem Abschluss (30.10.2026)

- Analyse-Seite, Reiter „Graph“: dieselbe Fläche wie auf der Modellseite, nur Ansicht
  (`canvas_view.analysis_view`); der gewählte Wert (Sensitivität, Kritikalität, Begründung fehlt)
  steht als farbige Zahl am Knoten, Knoten ohne Pfad zur Ausgabe sind blass. Der Plotly-Graph
  (`structure.graph_figure`) ist entfernt.
- Befund aus der Prüfung: Ein unsicherer Knoten mit Eingabe als Spanne bekam beim Verbinden
  `p50: a`, was die Spanne nicht erlaubt. Jetzt bietet der Dialog dort nur die Korrelation an;
  sonst meldet `canvas.quantiles`, dass der Eingabemodus „params“ nötig ist.
- Kanten-Dialog (Wunsch des Nutzers): Klick auf eine Kante öffnet „Verknüpfung A → B“. Bei einem
  Vorauswahl-Ausdruck wechselt „Art der Verknüpfung“ die Art für alle Argumente
  (`canvas.retype`: `max(pfad1, c)` → `pfad1 + c`), bei einer Korrelation lässt sich ρ ändern
  (`canvas.rho`); beides mit Klartext vor dem Übernehmen, dazu „Verknüpfung entfernen“. Freie
  Ausdrücke und Parameter-Kanten öffnen die Karte des Ziels; im Szenario-Modus gesperrt.

## 9. Tests

- `tests/test_canvas.py` (Kern, offline): jede Aktion `Data → Data` – Vorauswahlen erzeugen
  den erwarteten Ausdruck, Anhängen und Entfernen von Argumenten, Ablehnung bei Zyklus,
  Korrelation anlegen und lösen, Layout lesen/schreiben, Hash unverändert nach Verschieben.
- Eigenschaftstest: T2 lässt sich über Canvas-Aktionen nachbauen und liefert dieselben Zahlen
  wie `examples/t2_terminplan.yaml` (Gegenstück zu M6 AK 3).
- `tests/test_web_canvas.py`: Fläche erzeugt Ereignisse → Dialog → Entwurf geändert; Szenario-
  Modus sperrt Struktur und schreibt Overrides.

## 10. Entscheidungen

| Nr | Frage | Entscheidung |
|---|---|---|
| E1 | Quelle der Wahrheit | **bestätigt:** YAML; Kanten abgeleitet, Aktionen als reine Funktionen |
| E2 | Layout | **bestätigt (30.10.2026):** optionaler Block `layout` im Modell-YAML, nicht im Inhalts-Hash |
| E3 | Szenarien | **bestätigt (30.10.2026):** Szenario-Modus auf derselben Fläche, Override-Dialog je Knoten |
| E4 | Vorauswahlen | **bestätigt (30.10.2026):** wie in AP3 gebaut, ohne „Wahl zwischen zwei Werten“ und „Übernehmen“ |
| E5 | Palette | **bestätigt (30.10.2026):** Abschnitt 5, umgesetzt in AP5 |
| E6 | Canvas-Komponente | **bestätigt (30.10.2026):** Vue Flow (Abschnitt 8.1) |
| E7 | Ort auf der Modellseite | **umgesetzt (AP4, 30.10.2026):** Fläche ersetzt den Plotly-Graphen im Reiter „Formular“; Tabelle darunter bleibt |
| E8 | Szenarienseite | **bestätigt (30.10.2026):** bleibt für Baum, Diff, Duplizieren und Ablösen; Overrides auch dort weiter möglich |
| E9 | Kante löschen bei freiem Ausdruck | **bestätigt (30.10.2026):** Ausdruck öffnen, nie automatisch umschreiben |
| E10 | Schlüssel `layout` | **bestätigt (30.10.2026):** oberste Ebene statt je Knoten, damit Knotendefinitionen kurz bleiben |

## 11. Arbeitspakete

| AP | Inhalt | Tests |
|---|---|---|
| AP1 | Spike (Abschnitt 8), Entscheidung E6 hier dokumentiert | Spike-Bericht |
| AP2 | Schema `layout`, Hash-Ausnahme, Notice für unbekannte IDs, Tutorials mit Layout | Schema- und Hash-Tests |
| AP3 | `model/canvas.py`: Verbinden mit Vorauswahlen, Kante löschen, Korrelation | `test_canvas.py` |
| AP4 | Fläche auf der Modellseite: Zeichnen, Verschieben, Auswahl → Karte | `test_web_canvas.py` |
| AP5 | Verknüpfungsdialog und Palette mit Neuer-Knoten-Dialog | Oberflächentest, T2-Nachbau |
| AP6 | Szenario-Modus und Override-Dialog | Oberflächentest |
| AP7 | Doku: README, `docs/model-semantics.md` (`layout`), `docs/architecture.md`, Glossar, PRD-Status | Doku-Links-Test |
