# Pflichtenheft M9 — Grafischer Editor

**Stand:** 30. Oktober 2026, Entwurf; E1–E3 bestätigt (30.10.2026), E4–E10 offen bis nach
dem Spike · **Bezug:** [PRD.md](../../PRD.md), Meilenstein M9 · **Voraussetzung:** M1–M8

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

## 5. Palette und neue Knoten (E5)

Palette am linken Rand mit den sechs Knotentypen. Ziehen auf die Fläche öffnet einen kurzen
Dialog: ID (Vorschlag aus dem Namen), Name, Einheit; ein unsicherer Knoten startet mit der
Spanne P10/P50/P90 (E14 aus M8). Der Knoten erscheint an der Ablagestelle; seine Karte öffnet
sich rechts wie heute nach einem Graph-Klick.

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
| E4 | Vorauswahlen | Vorschlag Abschnitt 4; zu bestätigen |
| E5 | Palette | Vorschlag Abschnitt 5; zu bestätigen |
| E6 | Canvas-Komponente | nach dem Spike (Vue Flow oder Drawflow) |
| E7 | Ort auf der Modellseite | Vorschlag: Fläche ersetzt den Plotly-Graphen im Reiter „Formular“; Tabelle darunter bleibt |
| E8 | Szenarienseite | Vorschlag: bleibt für Baum, Diff, Duplizieren und Ablösen; Overrides auch dort weiter möglich |
| E9 | Kante löschen bei freiem Ausdruck | Vorschlag: Ausdruck öffnen, nie automatisch umschreiben |
| E10 | Schlüssel `layout` | Vorschlag: oberste Ebene statt je Knoten, damit Knotendefinitionen kurz bleiben |

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
