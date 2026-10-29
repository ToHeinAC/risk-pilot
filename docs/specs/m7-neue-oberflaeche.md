# Pflichtenheft M7 — Neue Oberfläche

**Stand:** 29. Oktober 2026; Phase 1 (Spike) abgeschlossen, NiceGUI gewählt; Phase 2 als Nächstes ·
**Bezug:** [PRD.md](../../PRD.md), Meilenstein M7 (AK 1–5, Edge cases) · **Voraussetzung:** M1–M6 ·
**Folgt:** [M8 UX und Selbsterklärung](m8-ux-selbsterklaerung.md)

Dieses Pflichtenheft legt fest, **wie** M7 umgesetzt wird. Das PRD bleibt der Vertrag für das
**Was**; bei Widerspruch gilt das PRD, und der Widerspruch wird hier korrigiert.

***

## 1. Warum

Streamlit führt bei jeder Eingabe das ganze Seitenskript neu aus. Daraus folgen die
Hilfskonstrukte im Formular (Widget-Zustand nach Text-Hash zurücksetzen, Entwurf über
`session_state` spiegeln) und die festgelegte Optik: Spalten, Reiter, Expander, kein freies
Layout, keine Klick-Ereignisse auf Grafiken ohne Neulauf. Die Leitbilder aus M8 (Hex, GoRules,
Guesstimate) brauchen eine Arbeitsfläche mit nebeneinanderliegenden Bereichen, Auswahl per Klick
und Werten, die sich an Ort und Stelle aktualisieren.

## 2. Kandidat und Alternativen (E1)

| Option | Bewertung |
|---|---|
| **NiceGUI** (MIT) | reines Python, ereignisgesteuert, Quasar/Vue-Bausteine mit Tailwind-Klassen, Plotly mit Klick-Ereignissen, eigene Vue-Komponenten möglich; Tests ohne Browser über die `User`-Fixture (in-process). **Gewählt** (Abschnitt 3.1). |
| FastAPI + eigenes Frontend | größte Gestaltungsfreiheit, aber zweite Sprache, Node-Toolchain, API-Schicht, Browser-Tests; für ein lokales Ein-Personen-Werkzeug zu teuer |
| Reflex, Dash | Reflex braucht Node/Next.js-Build und ändert seine API häufig; Dash' Callback-Modell macht den Formular-Editor umständlich |

## 3. Phase 1 — Spike (AK 1)

Eigener Branch `spike/nicegui` in einem Worktree; wird **nicht** gemergt. Drei Ansichten,
gebaut nur aus vorhandenem `present/`, `model/`, `engine/`:

1. **Ergebnisse (Hex):** Antwortsatz zuerst als Kennzahlkarte, Text direkt an der Grafik,
   Kennzahlen kompakt, Ausgaben als Reiter.
2. **Modell-Arbeitsfläche (GoRules):** Graph links, Knotenkarte rechts; Klick auf einen Knoten
   wählt die Karte; „Probelauf“ füllt die Knotentabelle mit P10/P50/P90 je Knoten.
3. **Unsicherheit (Guesstimate):** Knotentabelle mit Kurzangabe und Mini-Verteilung je Zeile;
   Karte eines unsicheren Knotens mit Eingabe als Spanne (low/mode/high), Vorschau aktualisiert
   sich beim Tippen.

**Prüfpunkte, die der Spike beantwortet:**

| Nr. | Frage | Maß |
|---|---|---|
| S1 | Wirkt die Bedienung deutlich besser als heute? | Urteil des Nutzers am laufenden Spike |
| S2 | Tempo | Reaktion auf Eingabe/Klick ohne spürbare Verzögerung (T5: < 0,2 s Server-Zeit) |
| S3 | Tests offline | `User`-Fixture läuft unter der Socket-Sperre aus `tests/conftest.py` |
| S4 | Typen | pyright strict ohne Datei-Pragmas über das heutige Maß hinaus |
| S5 | Betrieb | Port 8642 konfigurierbar, Beenden beendet nur den eigenen Prozess |
| S6 | Lizenzen | NiceGUI und transitive Abhängigkeiten Apache-2.0-kompatibel |

**Abbruch:** S1 nein oder S3 nicht lösbar → Streamlit bleibt, M8 baut auf Streamlit.

### 3.1 Ergebnis des Spikes (29.10.2026)

Branch `spike/nicegui`, Worktree `../risk-pilot-spike`, NiceGUI 3.18.0; Start
`uv run python -m app.web.main`, Port 8643. Code: `src/app/web/` (≈ 550 Zeilen),
`src/app/present/brief.py` (Kurzangabe, Mini-Verteilung, Werte je Knoten), Tests
`tests/test_web_spike.py`.

| Nr. | Ergebnis |
|---|---|
| S1 | erfüllt: Urteil des Nutzers am laufenden Spike (29.10.2026): „Die Bedienung wirkt deutlich besser.“ |
| S2 | erfüllt: gemessen 51 ms (T2) und 112 ms (T5) für je zwei Änderungen samt YAML-Patch, Prüfung, Probelauf 5 000, Tabelle und Graph, also ≈ 25 bzw. 55 ms je Änderung; der Probelauf selbst 1–2 ms |
| S3 | erfüllt: `user_simulation` läuft in-process (httpx ASGI) unter der Socket-Sperre; 4 Tests in ≈ 2 s; ohne pytest-asyncio (`asyncio.run`) |
| S4 | erfüllt: pyright strict grün; NiceGUI bringt `py.typed`, eine Unterdrückung an `ui.run`; Plotly-Pragmas wie bisher |
| S5 | erfüllt: Port im Code (8643 im Spike, 8642 nach dem Wechsel); Beenden über `app.shutdown()` beendet nur den eigenen Server, mit Rückfrage |
| S6 | erfüllt nach Freigabe: alles MIT/BSD/Apache bis auf `bidict` (MPL-2.0, über python-socketio) und `docutils` (Public Domain/BSD, einzelne Teile GPL); MPL-2.0 ist bereits über `certifi` im Projekt. Beide werden unverändert als Bibliothek genutzt; der Nutzer hat beide am 29.10.2026 zugelassen (PRD §3) |

**Entscheid:** NiceGUI. Alle Prüfpunkte erfüllt, Abbruchbedingung nicht eingetreten; Phase 2
beginnt. Der Spike-Code bleibt auf seinem Branch und dient als Vorlage, nicht als Merge-Basis.

**Befunde aus dem Spike:**

- Umstellen eines Knotens auf „Spanne“ (P10/P50/P90) macht Szenario-Overrides des alten
  Modus ungültig (T2: `b_schneller` setzt `mean`). Die Karte zeigt den Grund; M8 muss die
  Umstellung die Overrides mitnehmen lassen oder sie mit Hinweis sperren.
- Eine Normalverteilung kann eine schiefe Spanne nur angenähert treffen (Quantil-Fit); die
  Vorschau macht das sofort sichtbar. M8: bei schiefer Spanne Lognormal vorschlagen.
- Inhalte in Tabellen-Slots sieht `User.should_see` nicht; Tests prüfen dort die Zeilendaten.
- Firefox headless (`--screenshot`) reicht für Sichtprüfungen im Entwicklungsablauf.

## 4. Phase 2 — Migration (AK 2–5)

- Neues Paket `src/app/web/` (Seiten, Bausteine, Zustand je Browser-Tab); `src/app/ui/`
  (Streamlit) wird am Ende gelöscht.
- Seiten wie heute: Start, Lernpfad, Modell (Formular | YAML), Szenarien, Simulation,
  Ergebnisse, Vergleich, Analyse, Läufe. Navigation als feste Seitenleiste.
- Zustand: ein `Session`-Objekt je Tab (offenes Modell, Entwurf, Läufe); Formular und YAML
  schreiben in denselben Entwurf, ohne Hash-Trick (Edge case).
- Lange Läufe in `run.io_bound`/Thread, Fortschrittsanzeige, Oberfläche bleibt bedienbar.
- Tests: jede heutige AppTest-Prüfung bekommt ein Gegenstück mit `User`; Liste der Zuordnung in
  Abschnitt 6 (beim Umsetzen gefüllt).
- Doku: README (Start, Port, Beenden), `docs/architecture.md`, PRD-Constraints (Streamlit →
  NiceGUI), `.streamlit/` entfernt.
- Gestaltung: ein kleines Designsystem (Farben, Abstände, Schrift, Kennzahlkarte,
  Auswertungsblock) als Tokens an einer Stelle; Ausgang ist die Optik des Spikes (hell). Ein
  dunkler Modus kommt später; die Tokens bleiben dafür an einer Stelle.

## 5. Entscheidungen

| Nr. | Frage | Vorschlag | Stand |
|---|---|---|---|
| E1 | Framework | NiceGUI, Entscheid nach Spike | entschieden: NiceGUI (29.10.2026) |
| E2 | Spike-Ort | Worktree, Branch `spike/nicegui`, kein Merge | umgesetzt |
| E3 | Migration | in einem Zug, Seite für Seite, Streamlit bis zum Ende lauffähig | entschieden (29.10.2026) |
| E4 | Optik | Optik des Spikes (Tokens aus `web/theme.py`), zunächst nur hell; dunkler Modus später | entschieden (29.10.2026) |

### 4.1 Fortschritt

| Schritt | Inhalt | Stand |
|---|---|---|
| 1 | Grundgerüst: `web/main.py` (Seitenleiste, Beenden, Fehlergrenze), `web/session.py` (Zustand je Tab, auch von `ui/state.py` genutzt), `web/theme.py`, Port `RISK_PILOT_PORT` (8643) | erledigt |
| 2 | Start und Modell: Arbeitsfläche (Graph, Knotentabelle mit Kurzangabe, Mini-Verteilung und P10/P50/P90 aus einem Probelauf, Knotenkarte mit Vorschau), Modellkopf, YAML-Editor auf demselben Entwurf (`web/editing.py`), Speichern mit Konfliktschutz, Verwerfen, Kopieren, CSV-Import, Stützstellen-Angebot | erledigt |
| 3 | Simulation, Ergebnisse | offen |
| 4 | Szenarien, Vergleich | offen |
| 5 | Analyse | offen |
| 6 | Lernpfad, Läufe | offen |
| 7 | Umschalten: Port 8642, Streamlit und AppTest entfernen, Doku, PRD-Constraints | offen |

## 6. Testzuordnung AppTest → User

| Heute (AppTest) | Neu (`tests/test_web_*.py`) |
|---|---|
| `test_app.py::test_exit_sends_sigterm_to_own_pid` | `test_web_shell.py::test_exit_asks_first_and_ends_only_this_process` |
| — (neu) Warnung bei ungespeicherten Änderungen | `test_web_shell.py::test_exit_warns_about_unsaved_changes` |
| — (neu) unerwarteter Fehler wird Meldung, Hülle läuft weiter | `test_web_shell.py::test_unexpected_error_in_a_page_becomes_a_message` |
| — (neu) alle Seiten in der Navigation | `test_web_shell.py::test_navigation_lists_every_page_and_opens_it` |
| `test_adapters_process.py`: Port nicht Standard | `test_web_shell.py::test_port_defaults_beside_streamlit_and_is_configurable` |

| `test_app.py::test_start_page_lists_tutorials_and_learning_path` | `test_web_start.py::test_start_lists_tutorials_and_learning_path` |
| `test_app.py::test_t1_open_simulate_and_show_metrics` (Öffnen, Prüfung) | `test_web_start.py::test_open_tutorial_shows_model_page_and_name` |
| `test_app.py::test_copy_template_keeps_source_and_refuses_existing_name` | `test_web_start.py::test_copy_template_keeps_source_and_refuses_existing_name` |
| `test_app_form.py::test_new_model_from_start_page_opens_in_the_form` | `test_web_start.py::test_new_model_opens_empty_in_the_form` |
| `test_app.py::test_tutorials_t3_to_t5_listed_copyable_and_marked_illustrative` | `test_web_start.py::test_tutorials_t3_to_t5_copy_as_illustrative` |
| `test_app.py::test_non_utf8_model_file_does_not_crash_start` | `test_web_start.py::test_unreadable_model_file_does_not_break_start` |
| `test_app.py::test_tutorial_is_read_only`, `test_app_form.py::test_tutorial_form_is_read_only` | `test_web_model.py::test_tutorial_is_read_only` |
| `test_app.py::test_validation_messages_in_german_without_crash` | `test_web_model.py::test_validation_messages_in_german` (Simulationsteil folgt in Schritt 3) |
| `test_app.py::test_edit_and_save_own_model`, `…::test_editor_draft_survives_page_change` | `test_web_model.py::test_edit_save_and_draft_survives_page_change` |
| `test_app.py::test_save_conflict_offers_overwrite_and_invalid_draft_warns` | `test_web_model.py::test_save_conflict_offers_overwrite_and_invalid_draft_warns` |
| — (neu) Verwerfen | `test_web_model.py::test_discard_restores_the_file` |
| `test_app.py::test_model_page_offers_copy_for_tutorial` | `test_web_model.py::test_model_page_offers_copy_for_tutorial` |
| — (neu) Graph-Klick und Tabellenauswahl, Probelauf in der Tabelle | `test_web_model.py::test_graph_click_and_table_pick_open_the_node_card` |
| `test_app_form.py::test_form_edit_keeps_comments_after_saving` | `test_web_model.py::test_form_edit_keeps_comments_after_saving` |
| `test_app_form.py::test_last_change_wins_between_yaml_and_form` | `test_web_model.py::test_last_change_wins_between_yaml_and_form` |
| `test_app_form.py::test_unreadable_yaml_locks_the_form_and_invalid_model_has_no_preview` | `test_web_model.py::test_unreadable_yaml_locks_the_form_and_invalid_model_has_no_preview` |
| `test_app_form.py::test_delete_needs_confirmation_and_no_references` | `test_web_model.py::test_delete_needs_confirmation_and_no_references` |
| `test_app_form.py::test_t2_rebuilt_through_the_form_gives_the_same_model_and_numbers` | `test_web_model.py::test_t2_rebuilt_through_the_form_gives_the_same_basis_model` (Szenarien folgen in Schritt 4) |
| `test_app.py::test_csv_column_becomes_empirical_distribution` | `test_web_model.py::test_csv_column_becomes_empirical_distribution` |
| `test_app.py::test_quantile_conflict_offers_piecewise_in_own_model` | `test_web_model.py::test_quantile_conflict_offers_piecewise_in_own_model` |

Weitere Zeilen kommen mit jedem Schritt dazu.
