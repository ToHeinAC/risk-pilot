# Pflichtenheft M6 — Formular-Editor und Export

**Stand:** 29. Oktober 2026, Entscheidungen E1–E12 bestätigt, E4 und E7 geändert (Abschnitt 11) ·
**Bezug:** [PRD.md](../../PRD.md), Meilenstein M6 (AK 1–5, Edge cases) · **Voraussetzung:** M1–M5

Dieses Pflichtenheft legt fest, **wie** M6 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M6:** Formular-Editor auf der Modellseite (Modellkopf, Einstellungen, Knotentabelle,
Knotenkarten), Verteilungsvorschau je unsicherem Knoten, neues leeres Modell, Export
(Kennzahlen-CSV, Rohstichproben-Parquet, HTML-Bericht), Erweiterungspunkt „neue
Verteilungsfamilie“ mit Test, `docs/model-semantics.md`, `docs/statistical-methods.md`.

**Nicht in M6:** Korrelationsgruppen und Unterszenarien im Formular (bleiben YAML bzw. Seite
„Szenarien“, E3), Umbenennen von Knoten mit Nachziehen der Referenzen (E6), grafischer Editor
(Nicht-Ziel), Hilfetexte und Glossar (M7), Export von Vergleich und Analyse (E10).

***

## 2. Modulstruktur

```text
src/app/
    model/form.py             rein: Model <-> Formularwerte je Knoten, Knoten anlegen/löschen,
                              Feldliste je Typ und Verteilung (aus Family.modes)
    model/edits.py            + set_node, add_node, remove_node, set_header (neue Modelle)
    model/yaml_patch.py       rein: Entwurfstext + neues Model -> Text, Kommentare bleiben (E4)
    present/preview.py        Vorschau eines Knotens: Kennzahlen, Dichte, CDF, Anteil außerhalb
    present/export.py         rein: Kennzahlen-Tabelle (Zeilen), HTML-Bericht (Text)
    adapters/export.py        Parquet-Bytes (pyarrow), CSV-Bytes
    ui/pages/modell.py        Reiter „Formular“ | „YAML“; Hinweis auf verlorene Kommentare
    ui/form.py                Knotentabelle, Knotenkarten, Widgets je ParamSpec
    ui/pages/start.py         + „Neues Modell“
    ui/pages/ergebnisse.py    + drei Download-Schaltflächen
docs/
    model-semantics.md        Modellformat, Knotentypen, Ausdrücke, Szenarien, Korrelationen
    statistical-methods.md    Ziehen, Kennzahlen, Intervalle, Auswertungen; Erweiterungspunkte
```

- Neue Abhängigkeiten: `pyarrow` (Apache-2.0, im PRD unter Constraints bereits genannt),
  `ruamel.yaml` (MIT) für kommentarerhaltendes Schreiben (E4).
- Schema-Version bleibt 1; am Modellformat ändert sich nichts.

***

## 3. Formular (AK 2, 3)

### 3.1 Aufbau (E1, E2)

- Die Modellseite bekommt zwei Reiter: **Formular** und **YAML**. Beide bearbeiten denselben
  Entwurf (`OpenModel.draft`); gespeichert wird wie bisher über „Speichern“.
- **Modellkopf:** `model` (nur anzeigen), `title`, `description`, `illustrative`,
  `settings.n`, `settings.seed`.
- **Knotentabelle:** eine Zeile je Knoten (ID, Typ, Name, Einheit, Kurzangabe, Begründung
  vorhanden ja/nein); Auswahl einer Zeile öffnet ihre Knotenkarte.
- **Knotenkarte** je Typ:

| Typ | Felder |
|---|---|
| alle | `name`, `unit`, `description`, `why` (Text; Links und Datum, wenn vorhanden), `tags`, `bounds.min`, `bounds.max`, `track` |
| constant | `value` |
| uncertain | `dist` (Auswahl aus `families()`), `input` (Modi der Familie), Parameter aus `Family.modes[input]` |
| event | `p` (Zahl oder Ausdruck) |
| choice | Optionsliste (`label`, `weight`), Zeilen anlegen und löschen |
| derived | `expr` |
| output | `expr`, `target` (Operator + Wert), `better`, `horizon`, `loss_reference` |

- **Parameterfelder** werden aus `ParamSpec` erzeugt: Pflichtfeld ohne Vorgabe, optionales mit
  Vorgabe als Platzhalter, `is_list` als Zahlenliste (Textfeld, Komma oder Leerzeichen getrennt).
  Ein Parameter darf Zahl oder Ausdruck sein (wie im YAML); das Feld ist ein Textfeld, Zahlen
  werden als Zahl geschrieben.
- Ein Wechsel von `dist` oder `input` behält nur die Parameter, die im neuen Modus vorkommen.
- **Knoten anlegen:** ID und Typ eingeben; die ID wird mit `id_problem` geprüft; Pflichtfelder
  bekommen keine erfundenen Werte, der Knoten ist bis zum Ausfüllen als Fehler markiert (E5).
- **Knoten löschen:** nur, wenn kein anderer Knoten, keine Korrelationsgruppe und kein Szenario
  ihn referenziert; sonst Liste der Verweise (E6).
- Validierung und Hinweise erscheinen wie im YAML-Reiter (dieselbe `check_text`-Ausgabe).

### 3.2 Verlustfreiheit (AK 2, E4)

- Jede Formularänderung erzeugt über `model/edits.py` ein **neues `Model`**.
  `yaml_patch.patch(text, model)` liest den Entwurf mit `ruamel.yaml` (Round-Trip-Modus) und
  gleicht den Baum rekursiv an `model.model_dump(mode="json", exclude_unset=True)` an: geänderte
  Werte ersetzen, neue Schlüssel anhängen, entfernte Schlüssel löschen, unveränderte Teile nicht
  anfassen. Kommentare, Schlüsselreihenfolge, Flow-Stil (`{type: …}`) und Anführungszeichen
  unveränderter Teile bleiben erhalten; ein Kommentar, der an einem gelöschten Schlüssel hängt,
  geht mit ihm.
- Felder, die im Formular nicht vorkommen (Korrelationen, Szenarien, Links und Datum von `why`),
  bleiben unverändert.
- Sicherheit: Nach dem Patchen muss `model_from_yaml(neuer_text) == model` gelten, sonst wird
  nichts geschrieben und ein Fehler gemeldet (kein stiller Datenverlust).
- `form.values(model, node_id)` → Formularwerte; `form.apply(model, node_id, values)` → Modell.
  Eigenschaft: `apply(m, i, values(m, i)) == m` für jeden Knoten jedes Tutorials und jeder
  Lernpfad-Lektion; `patch(text, m) == text` (keine Änderung, kein Unterschied im Text); nach
  einer Feldänderung stehen alle Kommentarzeilen des Originals noch im Text.

### 3.3 Gleichzeitige Bearbeitung und Kommentare (Edge cases, E7)

- **Letzte Änderung gewinnt:** Das Formular liest bei jedem Lauf den aktuellen Entwurf; eine
  Formularänderung überschreibt den Entwurf, eine YAML-Änderung ändert das Formular. Nach einer
  Formularänderung, die einen von Hand geänderten YAML-Entwurf ersetzt, erscheint der Hinweis
  „Formular hat den YAML-Entwurf neu geschrieben“.
- Ist der Entwurf kein gültiges Modell, ist das Formular gesperrt mit Verweis auf den YAML-Reiter.
- **Kommentare** bleiben beim Bearbeiten im Formular erhalten (3.2); ein Hinweis vor dem
  Speichern entfällt. Beim Löschen eines Knotens nennt die Bestätigung, dass seine Kommentare
  mit ihm verschwinden.

### 3.4 Neues Modell (AK 3)

- Startseite: „Neues Modell“ mit ID; legt `data/models/<id>.yaml` mit `schema_version`,
  `model`, leeren `nodes` an (über `files.create_model_text`) und öffnet es.

***

## 4. Verteilungsvorschau (AK 1, E8)

- Auf der Knotenkarte jedes `uncertain`-Knotens, sobald der Entwurf kompiliert:
  das Modell wird mit N = 20 000 und dem Seed des Modells simuliert (`keep="all"`), gezeigt werden
  die Ziehungen dieses Knotens: Dichte (Histogramm), CDF, Mittelwert, Median, P5, P95 und der
  **Anteil unzulässiger Werte** = Anteil außerhalb `bounds` (unter/über getrennt), ohne `bounds`
  „keine Grenzen gesetzt“.
- Dadurch funktioniert die Vorschau auch, wenn Parameter Ausdrücke anderer Knoten sind.
- Kann das Modell nicht laufen (Fehler in einem anderen Knoten), nennt die Vorschau den Grund.
- Zwischenspeicher je (Modell-Hash, Knoten); Ziel < 1 s für T5.

***

## 5. Export (AK 4)

Auf der Seite „Ergebnisse“ drei Download-Schaltflächen (`st.download_button`); nichts wird
ungefragt in `data/` geschrieben (E9).

| Datei | Inhalt |
|---|---|
| `<modell>_<szenario>_kennzahlen.csv` | eine Zeile je Ausgabe × Kennzahl: `output`, `metric`, `value`, `lo`, `hi`, `unit`; dazu Kopfzeilen mit Modell-Hash, N, Seed, Szenario (E11) |
| `<modell>_<szenario>_stichproben.parquet` | eine Spalte je gehaltenem Knoten (Ausgaben und `track`), Metadaten (Hash, N, Seed, Szenario) im Schema |
| `<modell>_<szenario>_bericht.html` | eigenständig (Plotly eingebettet, keine Netzabfrage): Titel, Gültigkeitszeile, Hinweis „illustrative Zahlen“, je Ausgabe Kennzahlen-Tabelle, Sätze, Histogramm und CDF, erreichte Korrelationen, am Ende das Modell-YAML |

- CSV und HTML entstehen rein in `present/export.py`; Parquet über `adapters/export.py` in einen
  Speicherpuffer.
- Gespeicherte Läufe (Seite „Läufe“) lassen sich nach dem Laden genauso exportieren.

***

## 6. Neue Verteilungsfamilie (AK 5)

- Ein Test registriert eine Familie (`register(...)`, z. B. `test_dreieck` mit `low`, `mode`,
  `high`) und zeigt: Modell mit `dist: test_dreieck` kompiliert, simuliert, besteht das
  KS-Kriterium, erscheint in der Formularauswahl mit genau ihren Parameterfeldern und in der
  Vorschau. Kein Code außerhalb des Tests ändert sich.
- Der Test entfernt die Familie wieder (Registry-Fixture), damit andere Tests unberührt bleiben.
- `docs/statistical-methods.md` beschreibt den Erweiterungspunkt (Protocol `Family`, `ParamSpec`,
  `register`), dazu neue Funktionen in Ausdrücken und wo Meldungstexte stehen.

***

## 7. Dokumentation

- `docs/model-semantics.md`: Modellformat Feld für Feld, Knotentypen, Ausdrücke (erlaubte
  Funktionen, `where`, Vergleich), Ströme und Seed, Szenarien (Vererbung, Overrides, Abkoppeln),
  Korrelationsgruppen, Horizont, `illustrative`.
- `docs/statistical-methods.md`: Inversionsmethode, Gaussian Copula, Quantil-Fit, Kennzahlen mit
  Intervallen (Wilson, Quantil-KI, Welch), Zensierung, VaR/ES, Mehrgipfligkeit, Kritikalität,
  Tornado, Sweep, Rangkorrelation, Risikomatrix; Toleranzen der Abnahmen; Erweiterungspunkte.
- Inhalte stammen aus den Pflichtenheften M1–M5; die Pflichtenhefte bleiben Herleitung, die
  beiden Dokumente sind die Referenz für Nutzer.

***

## 8. Tests

| AK | Test | Prüft |
|---|---|---|
| 1 | `test_preview.py` | Kennzahlen gegen Ziehungen; Anteil außerhalb `bounds` unter/über; Ausdrucksparameter; Modell mit Fehler → Grund |
| 2 | `test_form.py`, `test_yaml_patch.py` | `apply(values)` = Modell für alle Knoten aller Tutorials und Lektionen; `patch` ohne Änderung gibt denselben Text; nach Änderung bleiben alle Kommentare und der Flow-Stil; `dist`-Wechsel behält nur passende Parameter; Löschen mit Verweisen abgewiesen |
| 3 | `test_app_form.py` | T2 über „Neues Modell“ + Formular + Seite „Szenarien“ nachgebaut: gleicher Inhalts-Hash der Knoten und gleiche Kennzahlen je Szenario wie `examples/t2_terminplan.yaml` |
| 4 | `test_export.py` | CSV-Zeilen und Kopf; Parquet liest zurück (Spalten, Werte, Metadaten); HTML enthält Kennzahlen und Plotly ohne externe Skripte |
| 5 | `test_family_extension.py` | wie Abschnitt 6 |
| Edge | `test_app_form.py` | Kommentare von T2 bleiben nach Formularänderung und Speichern erhalten; YAML- und Formularänderung nacheinander, letzte gewinnt mit Hinweis; ungültiger Entwurf sperrt das Formular |

- AK 3 vergleicht Modelle über `content_hash` (Kommentare und Schlüsselreihenfolge zählen nicht).

***

## 9. Arbeitspakete und Abschluss

| AP | Inhalt | Fertig, wenn |
|---|---|---|
| AP1 | `model/form.py`, `model/yaml_patch.py`, Erweiterung `edits.py` | AK 2 grün |
| AP2 | `present/preview.py` | AK 1 (Kern) grün |
| AP3 | Formular-UI, „Neues Modell“, Kommentar- und Konflikt-Hinweis | AK 3, Edge cases grün |
| AP4 | Export (CSV, Parquet, HTML) | AK 4 grün |
| AP5 | Familien-Erweiterungstest | AK 5 grün |
| AP6 | `docs/model-semantics.md`, `docs/statistical-methods.md` | Checkliste unten |
| AP7 | README, `docs/architecture.md`, Review, PRD-Status, manueller Durchlauf | Checkliste unten |

**Reihenfolge:** AP1 → AP2 → AP3 → AP4 → AP5 → AP6 → AP7.

- [ ] PRD M6 AK 1–5 und Edge cases durch Tests belegt; Gate grün.
- [ ] Manuell: T2 im Formular nachbauen, Vorschau prüfen, alle drei Exporte öffnen.
- [ ] Streamlit-Risiko aus PRD §5 bewertet (Formular flüssig bedienbar?).
- [ ] README, `docs/`; PRD M6 **Status** `done (verified by: …)`; Review.

***

## 10. Risiken

- **Streamlit-Neuläufe:** Jede Formularänderung läuft die Seite neu und schreibt YAML. Bei
  spürbarer Trägheit (> 0,5 s je Änderung an T5) werden Felder in `st.form` je Karte gebündelt
  (Änderung erst mit „Übernehmen“). Bleibt es zäh, greift der NiceGUI-Trigger aus PRD §5.
- **`ruamel.yaml` und Flow-Stil:** Lange Flow-Zeilen können beim Ändern umgebrochen werden;
  Breite deshalb hoch setzen (`width = 4096`). Test an allen Tutorials.
- **HTML-Größe:** eingebettetes Plotly ≈ 4,5 MB je Bericht; akzeptiert für Eigenständigkeit.

***

## 11. Entscheidungen

Am 29.10.2026 bestätigt; E4 und E7 nach Rückmeldung geändert (Kommentare bleiben erhalten),
E3, E6, E11, E12 ausdrücklich bestätigt, die übrigen wie vorgeschlagen.

| Nr | Frage | Vorschlag |
|---|---|---|
| E1 | Wo lebt das Formular? | **Reiter „Formular“ neben „YAML“ auf der Modellseite**, ein gemeinsamer Entwurf, ein „Speichern“ |
| E2 | Sofort übernehmen oder mit Knopf? | **Sofort je Feld** (wie der YAML-Editor); Fallback `st.form` je Karte, falls zu träge (Abschnitt 10) |
| E3 | Korrelationen und Szenarien im Formular? | **Nein:** Szenarien hat die Seite „Szenarien“ (M3), Korrelationen bleiben YAML; das Formular erhält sie unverändert |
| E4 | Wie schreibt das Formular? | **Neues `Model`, dann den bestehenden YAML-Baum mit `ruamel.yaml` angleichen:** Kommentare und Formatierung bleiben erhalten; Prüfung `model_from_yaml(text) == model` nach jedem Patch |
| E5 | Pflichtfelder beim Anlegen | **Leer lassen, als Fehler zeigen** (keine erfundenen Vorgaben, passend zu „keine stille Reparatur“) |
| E6 | Umbenennen und Löschen | **Löschen nur ohne Verweise; kein Umbenennen in M6** (Referenzen in Ausdrücken umzuschreiben ist eigener Aufwand) |
| E7 | Hinweis auf verlorene Kommentare | **Entfällt** (E4); nur beim Löschen eines Knotens wird gesagt, dass seine Kommentare mitgehen |
| E8 | Vorschau: nur der Knoten oder ganzes Modell? | **Ganzes Modell mit N = 20 000**, Ziehungen des Knotens: funktioniert auch mit Ausdrucksparametern und Korrelationen |
| E9 | Export als Download oder Datei in `data/`? | **Download im Browser**; keine Dateien ohne Anfrage |
| E10 | Was wird exportiert? | **Ergebnisse eines Laufs** (PRD AK 4); Vergleich und Analyse später bei Bedarf |
| E11 | CSV-Format | **Maschinenlesbar:** Komma als Trenner, Dezimalpunkt, UTF-8, Kennzahl-Schlüssel englisch (`p50`, `mean`); deutsche Bezeichnung als eigene Spalte `label` |
| E12 | HTML-Bericht | **Plotly eingebettet** (offline lesbar, ≈ 4,5 MB) statt CDN-Verweis |
