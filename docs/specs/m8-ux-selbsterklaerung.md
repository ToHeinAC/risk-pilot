# Pflichtenheft M8 — UX und Selbsterklärung

**Stand:** 29. Oktober 2026, Entwurf, auf NiceGUI überführt (M7 abgeschlossen,
[m7-neue-oberflaeche.md](m7-neue-oberflaeche.md)); E2–E14 bestätigt (E12–E14 am 29.10.2026) ·
**Bezug:** [PRD.md](../../PRD.md), Meilenstein M8 (AK 1–5, Edge cases) · **Voraussetzung:** M1–M7

Dieses Pflichtenheft legt fest, **wie** M8 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Umfang

**In M8:** einheitlicher Seitenkopf mit Zweck und nächstem Schritt (AK 1), Auswertungsblöcke mit
Frage, Lesebeispiel am Modell, Lesart und Grenze (AK 2), Glossar als Seite und als Tooltips
(AK 3), geführter Rundgang an T2 (AK 4), Begründung leerer Auswertungen (Edge cases),
Beobachtungsbogen für den Durchgang mit einer Fachperson (AK 5).

**Bestätigt, über das bisherige PRD hinaus (E7, E8):** Modellseite als Arbeitsfläche mit Graph,
Karte und Probelauf; Knotentabelle mit Kurzangabe und Mini-Verteilung; Spanne als erste
Eingabeart. Mit M7 bereits geliefert: Graph-Klick wählt Karte, Probelauf mit P10/P50/P90 je
Knoten, Kurzangabe und Mini-Verteilung (Abschnitt 8). In M8 offen: Spanne als erste Eingabeart.

**Nicht in M8:** What-if-Regler auf der Ergebnisseite (E9), neue Auswertungen, neue
Verteilungsfamilien, Mehrsprachigkeit.

***

## 2. Leitbilder (E1)

Drei Referenzen für drei Aufgaben. Übernommen wird jeweils das Bedienprinzip; die Optik wird
auf der neuen Oberfläche aus M7 eigens gestaltet (kein Nachbau der Vorbilder).

| Referenz | Aufgabe in Risk Pilot | Übernommenes Prinzip | Wo |
|---|---|---|---|
| Hex (App-Ansicht, What-if-Beispiel) | Ergebnisse, Vergleich, Analyse lesen | Antwort zuerst; erklärender Text direkt an der Grafik; wenige Eingaben oben, Ergebnis darunter | Auswertungsblock (Abschnitt 4), Seitenkopf (Abschnitt 3) |
| GoRules (JDM-Editor mit Simulator) | Modell bauen, Logik prüfen | Graph, Bearbeitung und Probelauf in einem Arbeitskontext; Trace je Knoten zeigt, was dort herauskommt | Modellseite (Abschnitt 8, E7) |
| Guesstimate | Unsicherheit eingeben und sehen | Unsicherheit als Spanne eingeben; jede Größe zeigt ihre Verteilung klein an Ort und Stelle; Abhängigkeiten sichtbar | Formular und Knotentabelle (Abschnitt 8, E8) |

Bewusst **nicht** übernommen: Hex' Notebook-Zellen (Risk Pilot ist kein Notebook), GoRules'
Entscheidungstabellen (Expertenlogik steckt hier in Ausdrücken und Ereignissen), Guesstimates
Tabellenraster und freie Zellplatzierung (das Modell bleibt YAML mit Formular).

***

## 3. Seitenkopf (AK 1, E2, E12)

- Jede Seite beginnt mit Titel, **einem** Absatz „Wofür ist diese Seite da?“ und einer Zeile
  „Nächster Schritt“ mit Link zur Folgeseite.
- Zentral über ein Verzeichnis in `present/guide.py` (rein: Seitenpfad → Text-Schlüssel,
  Folgeseite); der nächste Schritt hängt vom Zustand ab (kein Modell offen → Start; Modell ohne
  Lauf → Simulation; Lauf vorhanden → Ergebnisse).
- **NiceGUI (E12):** Die Hülle in `web/main.py` rendert den Kopf **einmal** vor jeder Seite
  (dort, wo heute die Fehlergrenze je Seite sitzt); die Seiten-Builder setzen keinen eigenen
  Titel mehr. Das Navigationsverzeichnis `main.PAGES` und das Verzeichnis in `present/guide.py`
  werden per Test abgeglichen. Der Link ist ein `ui.link` auf den Seitenpfad
  (`ui.sub_pages`), damit der Zustand der Sitzung erhalten bleibt.
- Bestehende Einleitungen (`ui.start_intro`, `ui.lernpfad_intro`, `analysis.intro`) gehen in
  dieses Verzeichnis über.
- Test (`tests/test_web_guide.py`): jede Seite der Navigation hat einen Eintrag; ein
  Oberflächentest öffnet jede Seite und prüft Absatz und Link; der nächste Schritt wechselt mit
  dem Zustand (ohne Modell, mit Modell, mit Lauf).

***

## 4. Auswertungsblock (AK 2, E3, E4)

Jede Auswertung (Ergebnisse je Ausgabe, Vergleich je Ausgabe, jeder Reiter der Analyse) hat
dieselbe Reihenfolge, nach dem Hex-Prinzip „Antwort zuerst“:

1. **Frage** als Zwischenüberschrift („Welche Eingabe verschiebt das Ergebnis am stärksten?“).
2. **Lesebeispiel am geöffneten Modell:** ein Satz mit echten Zahlen und Knotennamen aus dem
   aktuellen Lauf, z. B. „Im Modell verschiebt *Vorgang B* das *Projektende* von 27,1 d auf
   33,4 d, wenn er von P10 auf P90 geht – mehr als jede andere Eingabe.“
3. **Grafik bzw. Tabelle** (wie bisher).
4. **Aufklappbar „Lesart und Grenze“:** wie man die Grafik liest und was sie nicht sagt
   (übernimmt die heutigen `analysis.help_*`-Texte, ergänzt um Ergebnisse und Vergleich).

- Lesebeispiele sind reine Funktionen in `present/reading.py`, eine je Auswertung:
  `(Lauf/Auswertungsergebnis) → Sentence | Empty`. `Empty` trägt den Grund (Abschnitt 7).
- Ein Baustein `evaluation_block(key, reading, draw)` in `web/explain.py` rendert die vier Teile
  einheitlich: Frage als Zwischenüberschrift, Lesebeispiel in der Antwort-Schrift
  (`rp-answer`), Grafik bzw. Tabelle über `draw()`, „Lesart und Grenze“ als `ui.expansion`.
  Er ersetzt die heutigen „Was zeigt dieser Reiter?“-Aufklapper der Analyse und ergänzt
  `results_view` (Ergebnisse, Läufe, Lernpfad) und `compare_page`.
- Die Antwortkarten der Ergebnisseite (M7) bleiben oberhalb der Blöcke: sie sind die Antwort,
  der Block erklärt sie.
- Tests: je Auswertung ein Lesebeispiel an T2 bzw. T4/T5 mit den erwarteten Knotennamen und
  Zahlen aus derselben Quelle wie die Grafik (keine zweite Rechnung).

***

## 5. Glossar (AK 3, E5)

- Begriffe als Daten in `present/glossary.py`: `Term(key, label, short, long, example)`;
  `short` ist ein Satz (Tooltip), `long` ein Absatz, `example` bezieht sich auf T2.
- **Pflichtliste** (PRD): Iteration, Seed, Quantil, Intervall, Szenario, Override, kritischer
  Pfad, Tornado, Spearman-ρ; dazu aus der Oberfläche u. a. Verteilung, P10/P50/P90, Median,
  Erwartungswert, Standardabweichung, Ereignis, Ausgabe, Zielwert, Horizont, Korrelation,
  Rangkorrelation, Sweep, Risikomatrix, VaR/ES, Standardfehler, Konfidenz.
- **Erreichbar von jeder Seite:** eigene Seite „Glossar“ (`/glossar`) in der Navigation; dazu
  Tooltips an Feldern und Kennzahlen (aus `short`) über NiceGUIs `.tooltip()`. Im Glossar ist
  jeder Begriff ansprungfähig (`/glossar#quantil`), Tooltips verweisen nicht weiter.
- **Tests:**
  - Pflichtliste ⊆ Glossar.
  - Jeder Glossarbegriff kommt in mindestens einem UI-Text (`messages.py`) vor (kein toter
    Eintrag).
  - Jeder Fachbegriff einer festen Liste von UI-Schlüsseln (Kennzahl-Labels, Reiter, Felder) hat
    einen Glossareintrag (kein unerklärter Begriff).
  - Oberflächentest: Glossarseite zeigt alle Begriffe.

***

## 6. Geführter Rundgang (AK 4, E6)

- Start auf der Startseite („Rundgang an T2 starten“). Fünf Schritte:
  1. T2 öffnen, 2. Basis simulieren, 3. Szenario „nacharbeit“ simulieren,
  4. Vergleich Basis ↔ nacharbeit ansehen, 5. Analyse, Reiter Tornado.
- Solange er läuft, steht oben auf jeder Seite ein Banner: „Rundgang, Schritt 3 von 5: …“ mit
  Link zur passenden Seite und „Rundgang beenden“.
- Fortschritt wird **aus dem Zustand erkannt**, nicht abgehakt (Modell T2 offen, Lauf Basis
  vorhanden, Lauf nacharbeit vorhanden, Vergleichsseite besucht, Analyse besucht). Ein Schritt
  außer der Reihe wird angenommen, der Banner zeigt dann den ersten offenen Schritt.
- T2 ist eine Vorlage und schreibgeschützt; der Rundgang ändert nichts am Modell.
- Logik rein in `present/guide.py` (`tour_step(facts) → Step`). Die Fakten liefert die
  Sitzung (`web/session.py`): offenes Modell, Szenario-IDs der Läufe im Lauf-Cache, besuchte
  Seiten (neu: `Session.visited`, gesetzt von der Hülle beim Seitenwechsel).
- **NiceGUI (E13):** Der Banner steht in der Hülle (`web/main.py`) zwischen Kopfzeile und
  Seitenkopf und wird bei jedem Seitenwechsel neu aufgebaut; Läufe im Hintergrund-Thread
  aktualisieren ihn nach Abschluss (`refresh`), damit Schritt 2 und 3 ohne Seitenwechsel
  weiterschalten.
- Test (`tests/test_web_tour.py`): Oberflächentest läuft alle fünf Schritte durch und prüft den
  Banner nach jedem Schritt; „Rundgang beenden“ blendet ihn aus.

***

## 7. Leere Auswertungen (Edge cases)

Statt einer leeren Fläche ein Satz mit Grund und, wo möglich, was man tun kann:

Die heutigen Einzelhinweise (z. B. `analysis.no_events`, `compare.need_two`,
`analysis.crit_no_extremum`) gehen in diese Gründe über.

| Fall | Auswertung | Satz (sinngemäß) |
|---|---|---|
| keine Ereignisse | Risikomatrix | „Das Modell hat keine Ereignisse; die Risikomatrix braucht mindestens eines.“ |
| keine unsicheren Eingaben | Tornado, Sweep, Spearman-ρ | „Ohne unsichere Eingaben gibt es nichts, das das Ergebnis verschiebt.“ |
| keine Unterszenarien | Vergleich | „Das Modell hat nur die Basis; ein Szenario anlegen unter „Szenarien“.“ |
| kein max/min im Modell | kritischer Pfad | „Kritischer Pfad gibt es nur bei max/min-Verzweigungen.“ |
| ja/nein-Ausgabe | Quantile, Histogramm | „Bei einer Ja/Nein-Ausgabe zählt nur der Anteil.“ |
| kein Zielwert, kein Horizont | Zielsatz, Überschreitung | kein Satz, Hinweis in „Lesart“ |

Die Gründe kommen aus `present/reading.py` (`Empty.reason`); je Fall ein Test an einem kleinen
synthetischen Modell.

***

## 8. Modellseite als Arbeitsfläche (E7, E8, Scope-Erweiterung)

**GoRules-Prinzip (E7):**
- Graph (aus M4) links, Knotenkarte rechts; Klick auf einen Knoten im Graph wählt die Karte
  (Klick-Ereignis des Graphen).
- „Probelauf“ auf der Modellseite (kleines N, Seed des Modells): die Knotentabelle zeigt danach
  je Knoten P10/P50/P90 – der „Trace“, was an jedem Knoten herauskommt. Nutzt die vorhandene
  Vorschau-Rechnung (ein Lauf des ganzen Modells, `keep="all"`).

**Guesstimate-Prinzip (E8):**
- Knotentabelle mit **Kurzangabe** („10 bis 20 d, meist 15“; offener Punkt aus M6) und
  **Mini-Verteilung** (kleines Histogramm mit ~20 Klassen je Zeile).
- Beim Anlegen eines unsicheren Knotens steht die Eingabe als **Spanne** vorn:
  `three_point` (low/mode/high) bzw. `quantiles` (P10/P50/P90), mit einem Satz, was die Spanne
  bedeutet. Neue Eingabearten gibt es nicht; die Modi existieren seit M1.

Beides ist bestätigt (E7, E8). **Stand nach M7:** Arbeitsfläche, Graph-Klick, Probelauf mit
P10/P50/P90, Kurzangabe und Mini-Verteilung sind geliefert (`web/workbench.py`,
`present/brief.py`). Offen für M8 (E14): Ein neuer unsicherer Knoten startet mit Eingabeart
`quantiles` (P10/P50/P90) und einem Satz zur Bedeutung der Spanne; `three_point` und `params`
bleiben über die Auswahl „Eingabe“ erreichbar. Das betrifft nur den Vorschlag beim Anlegen im
Formular, nicht das Schema.

***

## 9. Durchgang mit einer Fachperson (AK 5, E11)

- Beobachtungsbogen hier im Pflichtenheft (Anhang A): fünf Aufgaben ohne Hilfe der
  beobachtenden Person, je Aufgabe Zeit, Stolperstellen und Zitat.
  1. „Wie wahrscheinlich ist das Projekt bis Tag 30 fertig?“ (T2)
  2. „Was ändert die Nacharbeit daran?“
  3. „Welcher Vorgang ist das größte Risiko?“
  4. „Was bedeutet P90 hier?“ (Glossar)
  5. „Lege einen eigenen Vorgang mit 5 bis 8 Tagen an.“
- Befunde: behoben oder als offene Punkte im PRD (§5 oder M8-Status).

***

## 10. Entscheidungen

| Nr. | Frage | Vorschlag |
|---|---|---|
| E1 | Referenzen | Hex für Ergebnisse, GoRules für die Modellseite, Guesstimate für die Unsicherheitseingabe; Bedienprinzip übernehmen, Optik neu gestalten auf der Oberfläche aus M7 (geändert 29.10.2026) |
| E2 | Seitenkopf | zentrales Verzeichnis, Zweck + zustandsabhängiger nächster Schritt |
| E3 | Auswertungsblock | Frage → Lesebeispiel → Grafik → aufklappbar Lesart/Grenze; ersetzt die Hilfe-Expander |
| E4 | Lesebeispiele | aus dem aktuellen Lauf berechnet, mit Knotennamen und Zahlen; leer → Grund |
| E5 | Glossar | eigene Seite + Tooltips; Tests in beide Richtungen (Pflichtliste, kein toter, kein unerklärter Begriff) |
| E6 | Rundgang | Banner auf jeder Seite, Fortschritt aus dem Zustand, T2 unverändert, Szenario „nacharbeit“ |
| E7 | GoRules-Arbeitsfläche | Probelauf mit Trace in der Knotentabelle: **ja**; Graph-Klick wählt Karte: **ja** |
| E8 | Guesstimate-Eingabe | Kurzangabe + Mini-Verteilung in der Tabelle: **ja**; Spanne als erste Eingabeart: **ja** |
| E9 | Hex-What-if-Regler auf Ergebnisseite | **nein**: Szenarien + Vergleich und Sweep decken das ab; ein dritter Weg zum selben Ziel erklärt sich schlechter |
| E10 | Ort der Texte | `messages.py` wie bisher; Glossar als Daten in `present/glossary.py` |
| E11 | Durchgang | Beobachtungsbogen mit fünf Aufgaben (Abschnitt 9) |
| E12 | Seitenkopf in NiceGUI | **bestätigt:** einmal in der Hülle (`web/main.py`), Seiten setzen keinen eigenen Titel |
| E13 | Rundgang-Banner in NiceGUI | **bestätigt:** in der Hülle; besuchte Seiten in der Sitzung; nach Hintergrundläufen aktualisiert |
| E14 | Spanne als erste Eingabeart | **bestätigt:** neuer unsicherer Knoten startet mit `quantiles` (P10/P50/P90) |

E7 und E8 erweitern den Lieferumfang. Der größte Teil ist mit M7 geliefert; das PRD führt den Rest (E14) seit
der Freigabe am 29.10.2026 in M8.

***

## 11. Arbeitspakete

| AP | Inhalt | Tests |
|---|---|---|
Reihenfolge wie in M7: ein Commit je Arbeitspaket auf `main`, Tests zuerst, Gate grün.

**Stand:** AP1 erledigt (`present/guide.py`, Kopf in `web/main.py`, `tests/test_present_guide.py`,
`tests/test_web_guide.py`); AP2 erledigt (`present/reading.py`, `web/explain.py`,
Blöcke in Ergebnissen, Vergleich und allen Analyse-Reitern, Gründe leerer Auswertungen;
`tests/test_present_reading.py`, `tests/test_web_explain.py`); AP3 erledigt
(`present/glossary.py`, Seite `/glossar`, Tooltips; `tests/test_present_glossary.py`,
`tests/test_web_glossary.py`); AP4 erledigt (`guide.tour_step`, `Session.visited`, Banner in
`web/main.py`, Start auf der Startseite; `tests/test_present_tour.py`, `tests/test_web_tour.py`);
AP5 mit M7 geliefert; AP6 erledigt (`form.NEW_UNCERTAIN`: neuer unsicherer Knoten mit `normal`
und `quantiles`, Satz zur Spanne in der Knotenkarte; `tests/test_form.py`,
`tests/test_web_model.py`).

| AP | Inhalt | Tests |
|---|---|---|
| AP1 | `present/guide.py` Seitenverzeichnis, Seitenkopf in der Hülle, alle Seiten | `test_web_guide.py`: Kopf je Seite, nächster Schritt je Zustand |
| AP2 | `present/reading.py`, `web/explain.py`, Ergebnisse/Vergleich/Analyse umbauen, leere Fälle | Lesebeispiele T2/T4/T5, leere Fälle (synthetische Modelle), Oberflächentest |
| AP3 | `present/glossary.py`, Seite `/glossar`, Tooltips | drei Glossar-Tests, Oberflächentest |
| AP4 | Rundgang: `tour_step`, `Session.visited`, Banner in der Hülle | `test_web_tour.py`: fünf Schritte |
| AP5 | (E7) Probelauf + Trace, Graph-Klick | mit M7 geliefert (`test_web_model.py`) |
| AP6 | (E8, E14) Spanne als erste Eingabeart; Kurzangabe und Mini-Verteilung mit M7 geliefert | Formulartest: neuer Knoten startet mit P10/P50/P90 |
| AP7 | Doku: README (Rundgang, Glossar), `docs/architecture.md`, PRD-Status | Doku-Links-Test |
| AP8 | Durchgang mit Fachperson, Befunde | manuell |

***

## Anhang A — Beobachtungsbogen

| Aufgabe | Zeit | gelöst (ja/teilweise/nein) | Stolperstellen | Zitat |
|---|---|---|---|---|
| 1 Wahrscheinlichkeit bis Tag 30 | | | | |
| 2 Wirkung der Nacharbeit | | | | |
| 3 Größtes Risiko | | | | |
| 4 Bedeutung von P90 | | | | |
| 5 Eigener Vorgang 5–8 Tage | | | | |
