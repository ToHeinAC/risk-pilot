# Erstanalyse: Evidenzbasiertes Risikomanagement

**Empfehlung:** Die App sollte als **evidenzbasiertes Entscheidungs- und Risikomodellierungssystem mit Monte-Carlo-Kern** konzipiert werden – nicht lediglich als Risikoregister mit angeschlossener Simulation. Der entscheidende Produktwert liegt in der nachvollziehbaren Kette **Quelle → Aussage → Modellannahme → Unsicherheitsmodell → Szenario → Simulation → Entscheidung**; etablierte Modellierungssoftware zeigt bereits, dass Einflussmodelle, Szenarien und Monte-Carlo-Simulation sinnvoll zusammengehören. [analytica](https://analytica.com/why-analytica/what-is-analytica/)

**Dieser Bericht trennt drei Ebenen:**
- **Wissenschaftliche Grundlagen:** Aussagen über Modellierung, Statistik und Unsicherheitsanalyse.
- **Entwurfsempfehlungen:** Vorgeschlagene Produkt-, Architektur- und Implementierungsentscheidungen.
- **Offene Prüfaufträge:** Punkte, die vor dem PRD oder vor einer kommerziellen Freigabe konkretisiert beziehungsweise gesondert geprüft werden müssen.

**Stand:** 24. Oktober 2026. Ziel ist eine belastbare Grundlage für die anschließende PRD-Erstellung mit Claude und die Umsetzung nach deinem Entwicklungsschema – noch kein abschließend festgelegtes PRD.

***

## Ausgangssituation

### Das eigentliche Problem

Die App soll nicht primär „Risiken sammeln“, sondern folgende Frage beantworten:

> **Welche Entscheidung ist unter den dokumentierten Annahmen, verfügbaren Erkenntnissen und verbleibenden Unsicherheiten vertretbar – und was könnte diese Beurteilung verändern?**

Daraus ergeben sich sechs miteinander verbundene Aufgaben:

- **Problem strukturieren:** Ziele, Entscheidungen, Einflussgrößen, Randbedingungen und Ergebnisgrößen definieren.
- **Evidenz aufbauen:** Informationen sammeln, prüfen, widersprüchliche Befunde sichtbar machen und Annahmen begründen.
- **Unsicherheit ausdrücken:** Wertebereiche, Verteilungen, Ereignisse und Abhängigkeiten modellieren.
- **Zukünfte unterscheiden:** Gegebenenfalls mehrere konsistente Szenarien beschreiben.
- **Auswirkungen berechnen:** Unsicherheit durch ein explizites Modell propagieren.
- **Handlungen ableiten:** Alternativen, Maßnahmen, zusätzliche Informationsbeschaffung und Überwachung bewerten.

**Zentrale Abgrenzung:** Monte-Carlo-Simulation berechnet Konsequenzen eines Modells und seiner Annahmen. Sie repariert weder unvollständige Modelle noch unrealistische Eingaben. [help-risk.lumivero](https://help-risk.lumivero.com/v8_5/en/Guides/@RISK-Getting-Started-Guide.pdf)

### Einordnung deiner Referenzen

- **Brenk-Referenz:** Der angegebene Download liefert trotz seines URL-Namens das Whitepaper *Monte-Carlo-Risikomanagement*, Dr. Tobias Hein, Februar 2024. Es demonstriert unsichere Terminpfade und nichtlineare Projektabläufe. [Whitepaper](https://www.brenk.com/download/stilllegung-und-rueckbau-kerntechnischer-anlagen-erfahrungen-und-perspektiven-4-neu-bearbeitete-auflage-2/?wpdmdl=8735&refresh=6adcad67eae191792847207)
- **Video-Referenz:** Das Gespräch behandelt mögliche Zukunftsbilder, Einflussfaktoren, Projektionen und deren Konsistenz statt einer einzigen Zukunftsprognose. [Fraunhofer-IEM-Gespräch](https://www.youtube.com/watch?v=ptJklX6QU2E&t=362s)
- **Entwicklungsschema:** Dein Repository legt unter anderem einen Python-Kern, getrennte I/O-Adapter, kurze verbindliche Dokumente, testgetriebene Änderungen und ein automatisiertes Qualitätsgate nahe. Diese Vorgaben sollten die Implementierungsplanung tatsächlich bestimmen. [Entwicklungsschema](https://github.com/ToHeinAC/claude-dev-schema)

### Empfohlene Produktdefinition

> **Eine projektzentrierte Anwendung, mit der Nutzer Entscheidungen und Risiken als nachvollziehbare Modelle strukturieren, Eingaben anhand von Evidenz begründen, Unsicherheiten und alternative Zukunftsbilder untersuchen und reproduzierbare Entscheidungsergebnisse erzeugen.**

**Nicht gleichsetzen:**

| Begriff | Bedeutung im vorgeschlagenen Produkt |
|---|---|
| Projekt | Abgegrenzter Entscheidungs- oder Untersuchungsraum |
| Risiko | Unsicherer Einfluss auf ein Ziel; gegebenenfalls mit Chancen und negativen Folgen |
| Modell | Explizite Beziehungen zwischen Eingangsgrößen und Ergebnissen |
| Evidenz | Informationen, die Aussagen oder Modellannahmen stützen, einschränken oder widerlegen |
| Szenario | Konsistentes Zukunftsbild beziehungsweise ein festgelegter Bedingungsrahmen |
| Simulationslauf | Numerische Auswertung einer konkreten Modell- und Szenarioversion |
| Entscheidung | Auswahl einer beeinflussbaren Handlungsalternative |
| Maßnahme | Eingriff, der Modellstruktur, Eintrittswahrscheinlichkeiten, Auswirkungen oder Kosten verändert |

Die Definitionen in dieser Tabelle sind **vorgeschlagene Produktbegriffe**, keine behauptete vollständige Übernahme einer Norm.

***

## Phase 1 – Dekonstruktion

### Fundamentale Komponenten

Von Grundprinzipien aus betrachtet sind nur wenige Dinge zwingend erforderlich:

| Fundamentale Komponente | Warum erforderlich? | Konsequenz für die App |
|---|---|---|
| Zielgröße | Ohne Ziel ist „Risiko“ nicht bewertbar | Mindestens eine messbare Ergebnisgröße |
| Entscheidungskontext | Derselbe Ausgang kann je nach Ziel gut oder schlecht sein | Zielrichtung, Schwellen und Zeithorizont speichern |
| Eingangsannahmen | Ergebnisse benötigen Ausgangsbedingungen | Jede relevante Eingabe explizit darstellen |
| Wirkungsmodell | Einzelne Verteilungen ergeben noch kein Projektmodell | Beziehungen und Berechnungslogik modellieren |
| Unsicherheitsbeschreibung | Unbekannte Größen dürfen nicht als sicher erscheinen | Unsicherheit strukturiert erfassen |
| Abhängigkeiten | Gemeinsame Ursachen können mehrere Größen beeinflussen | Unabhängigkeit nicht stillschweigend voraussetzen |
| Herkunft und Begründung | Eine Zahl ohne Kontext ist kaum prüfbar | Quellen- und Annahmenbezug |
| Auswertungsregel | Ergebnisse müssen interpretierbar sein | Kennzahlen und Entscheidungskriterien definieren |
| Versionsstand | Veränderte Annahmen verändern die Bedeutung des Ergebnisses | Unveränderliche Auswertungsstände |
| Verantwortlichkeit | Daten und Annahmen benötigen fachliche Freigabe | Eigentümer und Reviewstatus |

**Entwurfsfolgerung:** Das zentrale Datenobjekt sollte nicht die isolierte „Risikokarte“, sondern das **versionierte Entscheidungsmodell mit begründeten Annahmen** sein.

### Unveränderliche methodische Grenzen

- **Eine Verteilung ist keine Wirkungsbeziehung.** Sie beschreibt Unsicherheit einer Größe; erst Modellbeziehungen bestimmen, wie daraus Ergebnisse entstehen. Einflussdiagramme trennen deshalb unsichere Knoten von berechneten Größen und Entscheidungen. [analytica](https://analytica.com/blog/influence-diagrams-and-a-darwinian-take-on-decision-support-graphics/)
- **Mehr Simulationen reduzieren nicht automatisch die Unsicherheit des realen Projekts.** Sie verbessern zunächst die numerische Beschreibung des gewählten Modells. [docs.analytica](https://docs.analytica.com/images/3/33/Uncertainty.pdf)
- **Abhängigkeiten gehören zum Modell.** Auch bei unveränderten Einzelverteilungen beeinflusst ihre gemeinsame Struktur, welche Wertekombinationen auftreten. [help-risk.lumivero](https://help-risk.lumivero.com/v8_5/en/Guides/@RISK-Getting-Started-Guide.pdf)
- **Ein plausibles Zukunftsbild ist nicht automatisch ein wahrscheinliches Zukunftsbild.** Szenarioverfahren können bewusst ohne Eintrittswahrscheinlichkeiten arbeiten. [scmi](https://www.scmi.de/images/downloads/dateien/scmi-umweltbundesamt-szenariostudie.pdf)
- **Modellprüfung ist mehr als Parameteranpassung.** Vorhersageprüfungen untersuchen, ob ein Modell überhaupt relevante Merkmale möglicher beziehungsweise beobachteter Daten reproduzieren kann. [mc-stan](https://mc-stan.org/docs/2_36/stan-users-guide/posterior-predictive-checks.html)

### Vier Unsicherheitsebenen

Für das Produkt sollte folgende Unterscheidung verbindlich werden:

| Ebene | Beispiel | Behandlung |
|---|---|---|
| Prozessvariabilität | Bearbeitungszeiten schwanken unter gleichen Bedingungen | Zufallsvariable innerhalb eines Szenarios |
| Parameterunsicherheit | Der typische Bearbeitungsaufwand ist schlecht bekannt | Unsicherheit über Verteilungsparameter |
| Strukturunsicherheit | Ein zusätzlicher Genehmigungsschritt könnte notwendig werden | Alternatives Modell oder Szenario |
| Numerische Unsicherheit | Das geschätzte P95 schwankt zwischen Simulationsläufen | Konvergenzdiagnostik und Schätzunsicherheit |

Die Unterscheidung zwischen Zufallsvariation und Unsicherheit geschätzter Parameter ist auch in prädiktiven statistischen Modellen wesentlich. [github](https://github.com/stan-dev/docs/blob/master/docs/2_34/stan-users-guide/posterior-prediction.html)

**Produktregel:** Diese Ebenen dürfen im Ergebnisbild nicht zu einer einzigen scheinbar selbsterklärenden „Konfidenz“ verschmelzen.

### Notwendigkeit versus Konvention

**Nicht fundamental erforderlich sind:**

- Eine 5×5-Risikomatrix.
- Ein Risikoscore als Produkt ordinaler Kategorien.
- Genau drei Szenarien.
- Eine Wahrscheinlichkeitsangabe für jedes Zukunftsbild.
- Excel als primäres Modellformat.
- Eine KI-Komponente im Berechnungspfad.
- Microservices.
- Kubernetes.
- Ein frei programmierbarer Formeleditor.
- Ein grafischer Node-Editor als zwingender Einstieg.

**Tatsächlich erforderlich sind dagegen:**

- Ein korrektes und verständliches Modell.
- Explizite Annahmen.
- Passende Unsicherheitsmodelle.
- Nachvollziehbare Abhängigkeiten.
- Fachlich verständliche Ergebnisse.
- Reproduzierbare Auswertungen.

***

## Phase 2 – Annahmen-Check

### Kritische Ausgangsannahmen

| Naheliegende Annahme | Problem | Empfohlene Alternative |
|---|---|---|
| „Jede Eingabe muss eine Verteilung haben“ | Konstanten, Entscheidungen und Ereignisse sind unterschiedliche Objekttypen | Typisierte Modellknoten |
| „Mehr Quellen bedeuten mehr Sicherheit“ | Mehrere Veröffentlichungen können dieselbe Ursprungsinformation wiederholen | Quellenfamilien und Ursprungsbezüge |
| „Web-Recherche verifiziert die Zukunft“ | Recherche kann Annahmen stützen, aber Zukunftsaussagen nicht beweisen | Evidenzstatus statt Wahrheitsstempel |
| „Minimum und Maximum sind P10 und P90“ | Harte Grenzen und Quantile sind semantisch verschieden | Unterschiedliche Eingabemodi |
| „P95 bedeutet 95% Sicherheit“ | Das verwechselt Modellaussage, Prognose und Schätzunsicherheit | Präzise Ergebnisbeschriftung |
| „Szenarien sind Best/Base/Worst“ | Damit werden häufig nur Parameter verschoben | Zukunftsbilder mit unterschiedlichen Strukturen |
| „Korrelation bildet Kausalität ab“ | Gemeinsame Ursachen und Wirkungsrichtungen bleiben sonst unsichtbar | Gemeinsame Treiber und explizite Wirkungsmodelle |
| „Ein universeller Formeleditor macht die App generisch“ | Er verschiebt Modellierungsaufwand und Fehler zum Nutzer | Generischer Kern plus Fachvorlagen |
| „Ein SaaS ist später nur ein Deployment“ | Mandantentrennung, Betrieb und Verantwortung fehlen damit | Frühe Sicherheitsgrenzen, spätere Betriebsfreigabe |
| „KI kann die Verteilung auswählen“ | Sprachliche Plausibilität ersetzt keine statistische oder fachliche Begründung | KI-Vorschlag mit nachvollziehbarer Prüfung |

**Wissenschaftlich besonders relevant:** Die Eingabeverteilungen, ihre Abhängigkeiten und die Modellstruktur müssen gemeinsam plausibel sein; ein komfortabler Simulationsstart allein genügt nicht. [analytica](https://analytica.com/blog/monte-carlo-analysis-for-schedules-more-than-just-a-mouse-click/)

### Was „generisch“ heißen sollte

**Empfehlung: semantisch generisch, nicht oberflächlich beliebig.**

Der Kern soll wenige universelle Bausteine unterstützen:

- Feste Größen.
- Unsichere kontinuierliche Größen.
- Unsichere diskrete Größen.
- Ereignisse.
- Berechnete Größen.
- Entscheidungen.
- Abhängigkeiten.
- Szenarien.
- Ergebnisgrößen.
- Evidenz und Freigaben.

Fachvorlagen übersetzen diese Bausteine in verständliche Begriffe:

- **Terminplanung:** Vorgang, Dauer, Vorgänger, Meilenstein.
- **Projektwirtschaftlichkeit:** Menge, Aufwand, Preis, Kosten, Erlös.
- **Investmentanalyse:** Cashflow, Kapitalbindung, Rendite, Verlust.
- **Strategie:** Einflussfaktor, Projektion, Handlungsoption, Zielerreichung.

**Nicht empfehlen:** Für jeden Bereich eine eigene Simulationsengine zu entwickeln.

***

## Phase 3 – Neuaufbau

### Die minimale Wertschöpfungskette

Der vorgeschlagene fachliche Ablauf lautet:

```text
Entscheidungsfrage
        ↓
Ziele und Ergebnisgrößen
        ↓
Einflussmodell
        ↓
Evidenz und Annahmen
        ↓
Verteilungen und Abhängigkeiten
        ↓
Szenario beziehungsweise Szenarien
        ↓
Validierung und Freigabe
        ↓
Monte-Carlo-Simulation
        ↓
Ergebnis, Sensitivität und Maßnahmen
        ↓
Monitoring und Aktualisierung
```

**Wichtige Ergänzung:** Evidenzaufbau und Modellierung bilden keine einmalige Einbahnstraße. Neue Erkenntnisse können Eingabewerte, Verteilungsformen, Abhängigkeiten oder die gesamte Modellstruktur verändern.

### Drei getrennte Graphen

Für eine wissenschaftlich saubere Umsetzung sollten drei unterschiedliche Beziehungsarten getrennt werden:

| Graph | Knoten und Beziehungen | Aufgabe |
|---|---|---|
| Evidenzgraph | Quellen, Aussagen, Annahmen, Reviews | Begründung und Herkunft |
| Berechnungsgraph | Eingaben, Formeln, Ergebnisse | Numerische Auswertung |
| Szenariostruktur | Faktoren, Projektionen, Konsistenzregeln | Alternative Zukunftsbilder |

**Warum diese Trennung wichtig ist:**

- Eine Quelle kann mehrere Annahmen stützen.
- Eine Annahme kann durch mehrere Quellen gestützt oder infrage gestellt werden.
- Eine Evidenzbeziehung ist keine Rechenabhängigkeit.
- Die Konsistenz zweier Zukunftsprojektionen ist kein statistischer Korrelationskoeffizient.
- Änderungen müssen gezielt auf betroffene Modelle und Ergebnisse zurückverfolgbar sein.

***

## Evidenzanalyse als Fundament

### Was „aufbauend“ bedeuten sollte

Die Evidenzanalyse sollte sowohl **argumentativ aufbauend** als auch **zeitlich fortschreibbar** sein.

**Empfohlenes Objektmodell:**

| Objekt | Wesentliche Inhalte |
|---|---|
| Quelle | URL oder Datei, Urheber, Veröffentlichungsdatum, Abrufdatum, Nutzungsrechte |
| Fundstelle | Seite, Tabelle, Abschnitt oder Zeitmarke |
| Aussage | Konkreter überprüfbarer Inhalt |
| Geltungsbereich | Population, Region, Technologie, Zeitraum, Projektphase |
| Bewertung | Relevanz, methodische Eignung, Einschränkungen, Abhängigkeiten |
| Annahme | Für das konkrete Modell verwendete Festlegung |
| Ableitung | Begründeter Übergang von Aussage zu Eingabewert oder Verteilung |
| Review | Prüfer, Datum, Status, Kommentar |
| Versionsbezug | Modell- und Szenarioversion, für die die Annahme gilt |

**Beispiel einer nachvollziehbaren Kette:**

```text
Quelle mit historischen Bearbeitungsdaten
        ↓
Extrahierte Aussage zur untersuchten Fallgruppe
        ↓
Prüfung der Übertragbarkeit auf das eigene Projekt
        ↓
Festgelegtes Unsicherheitsmodell
        ↓
Freigabe einer konkreten Parameterversion
        ↓
Verwendung in einem reproduzierbaren Simulationslauf
```

**Entscheidend:** Die Übertragbarkeitsentscheidung muss sichtbar bleiben. Ein historischer Befund wird nicht allein durch seine Veröffentlichung zu einer gültigen Annahme für ein anderes Projekt.

### Keine eindimensionale Evidenznote

**Nicht empfehlen:** Einen einzigen „Evidenzscore“ von 0 bis 100 als vermeintlich wissenschaftliche Gewissheit anzuzeigen.

**Stattdessen mehrere nachvollziehbare Dimensionen:**

- **Direktheit:** Bezieht sich die Quelle auf genau diese Größe?
- **Kontextpassung:** Stimmen Projektart, Randbedingungen und Zeitraum?
- **Methodische Eignung:** Ist die Erhebungs- oder Auswertungsmethode geeignet?
- **Unabhängigkeit:** Gibt es eine gemeinsame Ursprungsquelle?
- **Aktualität:** Ist der zeitliche Bezug noch passend?
- **Vollständigkeit:** Sind Streuung, Stichprobengröße und Einschränkungen bekannt?
- **Widerspruchslage:** Existieren abweichende Befunde?
- **Nachprüfbarkeit:** Ist die relevante Fundstelle zugänglich?

Ein aggregierter Status kann zur Orientierung dienen, sollte aber nicht ohne begründetes statistisches Modell als Wahrscheinlichkeit interpretiert werden.

### Sinnvolle Evidenzzustände

**Vorgeschlagene Zustände:**

- Unbelegte Annahme.
- Experteneinschätzung dokumentiert.
- Quelle gefunden.
- Aussage extrahiert.
- Kontext geprüft.
- Teilweise gestützt.
- Gestützt unter Einschränkungen.
- Widersprüchliche Evidenz.
- Fachlich freigegeben.
- Überprüfung fällig.
- Ersetzt beziehungsweise zurückgezogen.

**Wichtig:** „Fachlich freigegeben“ bedeutet, dass die Annahme für einen bestimmten Zweck akzeptiert wurde – nicht, dass sie objektiv wahr oder künftig unveränderlich ist.

### Web-Recherche als überprüfbarer Prozess

**Empfohlener Ablauf:**

1. Der Nutzer wählt eine Eingabe oder Annahme.
2. Die App formuliert eine Recherchefrage aus Größe, Einheit, Kontext und Zeitraum.
3. Ein Rechercheadapter liefert Quellenkandidaten.
4. Die App extrahiert relevante Aussagen und Fundstellen.
5. Unterschiede im Kontext werden hervorgehoben.
6. Die App schlägt eine mögliche Interpretation vor.
7. Der Nutzer übernimmt, verändert oder verwirft diese Interpretation.
8. Erst eine ausdrücklich freigegebene Änderung erzeugt eine neue Modellversion.

**Nicht zulassen:**

- Automatisches Überschreiben freigegebener Eingaben.
- Eine Quelle als Beleg für etwas zu verwenden, das sie nicht aussagt.
- Suchtreffer-Snippets mit belastbarer Auswertung gleichzusetzen.
- Die Anzahl ähnlicher Webseiten als unabhängige Datenbasis zu behandeln.
- Aus einer einzelnen Zahl unbegründet eine Streuung abzuleiten.
- Vertrauliche Projektdetails ohne ausdrückliche Freigabe an externe Rechercheanbieter zu senden.

### Evidenz ist nicht automatisch Bayes

Ein sequenzieller Evidenzprozess kann bayesianische Aktualisierung unterstützen, muss aber nicht jede Quellenbewertung in ein Bayes-Modell verwandeln.

Die grundlegende Aktualisierung lautet:

\[
p(\theta \mid D)
\propto
p(D \mid \theta)\,p(\theta)
\]

Dafür müssen insbesondere ein sinnvolles Datenmodell und eine begründete Priorverteilung existieren; prädiktive Prüfungen helfen anschließend zu beurteilen, ob das Modell relevante Datenmerkmale abbildet. [mc-stan](https://mc-stan.org/docs/2_36/stan-users-guide/posterior-predictive-checks.html)

**Empfohlene Staffelung:**

- **Erste Version:** Dokumentierte Ableitung und manuelle Freigabe von Parametern.
- **Erweiterung:** Statistisch begründete Aktualisierung für klar definierte Modelle.
- **Später:** Hierarchische Modelle und systematische Parameterunsicherheit.

**Wissenschaftliche Mindestregel:** Dieselben Daten dürfen nicht mehrfach als scheinbar unabhängige Evidenz in die Aktualisierung eingehen.

### Unsicherheit nicht künstlich verengen

Neue Evidenz kann zu Folgendem führen:

- Engeren Wertebereichen.
- Breiteren Wertebereichen.
- Einer anderen Verteilungsform.
- Zusätzlichen Ereignisrisiken.
- Einer stärkeren Abhängigkeit.
- Einem neuen Szenario.
- Einer vollständigen Modellrevision.

**Produktprinzip:** „Mehr Evidenz“ darf nicht automatisch mit „kleinere Standardabweichung“ gleichgesetzt werden.

***

## Wissenschaftliches Verteilungsmodell

### Empfohlenes Startportfolio

Deine vier Mindestverteilungen sollten um **Beta**, **Beta-PERT** und **Student-t** ergänzt werden.

Zusätzlich sind **Konstanten**, **Bernoulli-Ereignisse** und eine **diskrete Auswahlverteilung** als grundlegende Modellbausteine erforderlich – unabhängig davon, wie viele kontinuierliche Verteilungen angeboten werden.

| Verteilung | Geeigneter Einsatz im Entwurf | Nutzerparameter | Zentrale Einschränkung |
|---|---|---|---|
| Rechteck / Uniform | Begründeter endlicher Wertebereich ohne bevorzugten Teilbereich | Unter- und Obergrenze | Gleichverteilung innerhalb des Bereichs ist eine Annahme |
| Dreieck | Einfache Experteneinschätzung mit begrenztem Bereich | Minimum, Modus, Maximum | Grenzen sind harte Grenzen |
| Normal / Gauß | Symmetrische Abweichungen um einen Lagewert | Mittelwert, Standardabweichung | Unbeschränkt; negative Werte gegebenenfalls unzulässig |
| Lognormal | Positive, rechtsschiefe Größen | Mittelwert und Streuung oder Quantile | Logarithmische und ursprüngliche Skala unterscheiden |
| Beta | Begrenzte Anteile oder normierte Größen | Formparameter oder zulässige Momentparameter | Wertebereich und Parameterrestriktionen beachten |
| Beta-PERT | Glatte, begrenzte Expertenverteilung | Minimum, Modus, Maximum, Konzentration | Konzentrationsparameter ist zusätzliche Modellannahme |
| Student-t | Symmetrische Größen mit stärkeren Randbereichen | Lage, Skala, Freiheitsgrade | Momente existieren nicht für alle Freiheitsgrade |

Die Lognormalparameterisierung und deren Abbildung auf Bibliotheksparameter müssen ausdrücklich spezifiziert werden; SciPy verwendet hierfür unter anderem `s` und `scale`, nicht unmittelbar den arithmetischen Mittelwert der Zielgröße. [docs.scipy](https://docs.scipy.org/doc/scipy-1.15.2/reference/generated/scipy.stats.lognorm.html)

### Eingabemodi statt Parameterverwirrung

**Empfohlene Eingabemodi:**

- **Wertebereich:** Harte Unter- und Obergrenze.
- **Drei-Punkt-Schätzung:** Minimum, wahrscheinlichster Wert, Maximum.
- **Lage und Streuung:** Beispielsweise Mittelwert und Standardabweichung.
- **Quantile:** Beispielsweise P10, P50, P90.
- **Historische Daten:** Beobachtungen mit Kontext.
- **Expertenmodus:** Direkte technische Parameter.

**Validierungsregel:** Nicht jeder Eingabemodus ist mit jeder Verteilung und jeder Kombination von Angaben vereinbar.

Beispiele:

- Drei beliebige Quantile lassen sich nicht immer exakt durch eine zweiparametrige Verteilung darstellen.
- Ein symmetrisches Normalmodell kann keine asymmetrischen Quantilabstände exakt wiedergeben.
- Ein Minimum ist nicht dasselbe wie ein niedriges Quantil.
- Ein „wahrscheinlichster Wert“ ist nicht automatisch Mittelwert oder Median.

**UI-Folge:** Wenn Angaben nicht zusammenpassen, muss die App den Konflikt erklären – nicht stillschweigend eine Näherung wählen.

### Rechteck und Dreieck

Für das Uniformmodell:

\[
X \sim U(a,b),
\qquad a < b
\]

**Produktregeln:**

- Gleiche Grenzen werden als Konstante behandelt.
- Harte Grenzen müssen begründet werden.
- Die Auswahl darf nicht als universell „annahmenfrei“ beschrieben werden.

Für das Dreiecksmodell:

\[
X \sim \operatorname{Triangular}(a,m,b),
\qquad a \leq m \leq b,\quad a < b
\]

**Produktregeln:**

- „Modus“ in der normalen Oberfläche als „am wahrscheinlichsten eingeschätzter Wert“ erläutern.
- Nicht verlangen, dass dieser Wert in der Mitte liegt.
- Die Modellannahme eines ausgeschlossenen Überschreitens der Grenzen deutlich anzeigen.

### Normal und abgeschnittene Normalverteilung

\[
X \sim \mathcal{N}(\mu,\sigma^2)
\]

**Empfohlene Schutzlogik:**

- Bei Größen mit zulässigem Minimum prüfen, ob das Modell unzulässige Werte erzeugen kann.
- Gegebenenfalls eine abgeschnittene Verteilung anbieten.
- Das Abschneiden als eigenständige Modelländerung dokumentieren.
- Keine negativen Dauern oder Kosten stillschweigend auf null setzen.

**Wichtig:** Abschneiden, Zurückweisen und „auf null begrenzen“ sind unterschiedliche Operationen und erzeugen unterschiedliche Verteilungen.

### Lognormal richtig parametrisieren

Für eine unverschobene Lognormalverteilung gilt:

\[
\ln(X) \sim \mathcal{N}(\mu_{\log},\sigma_{\log}^{2})
\]

Sind der arithmetische Mittelwert \(m_X\) und die Standardabweichung \(s_X\) vorgegeben, ergibt sich:

\[
\sigma_{\log}^{2}
=
\ln\left(1+\frac{s_X^{2}}{m_X^{2}}\right)
\]

\[
\mu_{\log}
=
\ln(m_X)-\frac{\sigma_{\log}^{2}}{2}
\]

Die dazu passende SciPy-Abbildung lautet `s = sigma_log`, `scale = exp(mu_log)` und für das unverschobene Modell `loc = 0`. [docs.scipy](https://docs.scipy.org/doc/scipy-1.15.2/reference/generated/scipy.stats.lognorm.html)

**PRD-relevante Anforderung:** Die Anwendung speichert sowohl den vom Nutzer gewählten Eingabemodus als auch die daraus abgeleiteten kanonischen Parameter.

### Beta und Beta-PERT

Für eine skalierte Beta-Verteilung:

\[
Z \sim \operatorname{Beta}(\alpha,\beta),
\qquad
X=a+(b-a)Z
\]

**Geeignete Produktverwendung:**

- Anteile zwischen 0 und 1.
- Begrenzte Auslastungsgrade.
- Begrenzte Wirkungsgrade.
- Allgemeine begrenzte Größen nach expliziter Skalierung.

**Wichtig:** Eine Beta-Verteilung über eine unbekannte Eintrittswahrscheinlichkeit ist eine andere Modellierungsebene als ein Bernoulli-Ereignis mit gegebener Eintrittswahrscheinlichkeit.

Für den vorgeschlagenen Beta-PERT-Vertrag:

\[
\alpha
=
1+\lambda\frac{m-a}{b-a}
\]

\[
\beta
=
1+\lambda\frac{b-m}{b-a}
\]

**Festzulegen sind:**

- Zulässiger Bereich für \(\lambda\).
- Bedeutung des Konzentrationsparameters.
- Verhalten bei Randmodi.
- Behandlung degenerierter Fälle.
- Ob und wie ein Standardwert verwendet wird.

**Empfehlung:** Ein gegebenenfalls verwendetes \(\lambda=4\) ausdrücklich als Produktkonvention kennzeichnen, nicht als naturgesetzlich richtigen Wert.

### Student-t mit Schutzregeln

**Sinnvolle Anwendung:** Symmetrische Residuen oder Abweichungen, bei denen ein Normalmodell die Randbereiche unzureichend abbilden könnte.

**Nicht sinnvoll als pauschaler Ersatz:**

- Für strikt positive Dauern.
- Für direkt modellierte Preise ohne Positivitätsschutz.
- Für einfache Renditen, wenn dadurch unzulässige Werte unter −100% zugelassen werden.
- Als angeblich automatisch „konservative“ Verteilung.

**Vorgeschlagene Regeln:**

- Freiheitsgrade sichtbar machen.
- Für Auswertungen mit endlicher Varianz im ersten Release Freiheitsgrade größer als 2 verlangen.
- Den Unterschied zwischen Skalenparameter und Standardabweichung erklären.
- Keine Kennzahl ausgeben, deren mathematische Voraussetzungen im gewählten Modell fehlen.

### Ereignisrisiken gesondert modellieren

Viele Risiken bestehen aus zwei getrennten Fragen:

1. Tritt ein Ereignis ein?
2. Wie groß ist seine Auswirkung, falls es eintritt?

Ein einfaches Modell lautet:

\[
I \sim \operatorname{Bernoulli}(p)
\]

\[
L=I\cdot S
\]

Dabei bezeichnet \(S\) die bedingte Auswirkung.

**Erforderliche Eingaben:**

- Eintrittswahrscheinlichkeit.
- Bezugszeitraum.
- Bedingte Schadens- oder Nutzenverteilung.
- Abhängigkeiten zu anderen Ereignissen oder Größen.
- Information darüber, ob dieses Risiko bereits in einer anderen Verteilung enthalten ist.

**Besonders wichtig:** Ein allgemeiner Risikozuschlag und ein separat simuliertes Ereignis können dieselbe Unsicherheit doppelt erfassen.

### Verteilungen aus Daten

**Für eine spätere Datenanpassung vorsehen:**

- Datenbereinigung mit dokumentierten Regeln.
- Prüfung auf Zensierung und Trunkierung.
- Zeitliche und fachliche Vergleichbarkeit.
- Grafische Verteilungsdiagnostik.
- Vergleich mehrerer Kandidaten.
- Unsicherheit der geschätzten Parameter.
- Prüfung außerhalb der Anpassungsdaten, soweit möglich.
- Prädiktive Prüfung statt bloßer Optimierung einer Anpassungskennzahl.

Prädiktive Prüfungen vergleichen modellgenerierte Daten unter anderem hinsichtlich Mittelwerten, Streuungen und Quantilen mit den relevanten Datenmerkmalen. [mc-stan](https://mc-stan.org/docs/2_36/stan-users-guide/posterior-predictive-checks.html)

**Nicht empfehlen:** Eine Schaltfläche „beste Verteilung“, die ohne Kontextprüfung eine endgültige wissenschaftliche Entscheidung suggeriert.

***

## Abhängigkeiten und Wirkungsmodelle

### Drei unterschiedliche Beziehungen

| Beziehung | Beispiel | Empfohlene Umsetzung |
|---|---|---|
| Deterministisch | Kosten = Menge × Einheitspreis | Berechneter Knoten |
| Gemeinsame Ursache | Inflation beeinflusst mehrere Preise | Gemeinsamer unsicherer Treiber |
| Verbleibende statistische Abhängigkeit | Zwei Eingaben bewegen sich gemeinsam | Explizites Abhängigkeitsmodell |

**Priorität:** Gemeinsame Ursachen möglichst explizit modellieren. Eine Korrelationsmatrix sollte nicht das Standardwerkzeug sein, um unbekannte Wirkungszusammenhänge zu kaschieren.

Die gemeinsame Abhängigkeitsstruktur kann die Simulationsergebnisse verändern, obwohl die einzelnen Eingangsverteilungen unverändert bleiben. [help-risk.lumivero](https://help-risk.lumivero.com/v8_5/en/Guides/@RISK-Getting-Started-Guide.pdf)

### Empfohlene erste Umsetzung

- Ein gemeinsamer Treiber wird pro Iteration genau einmal gezogen.
- Alle abhängigen Berechnungen verwenden denselben gezogenen Wert.
- Derselbe Quellknoten darf nicht bei jeder Referenz erneut gesampelt werden.
- Unabhängigkeit wird als dokumentierte Annahme gespeichert.
- Zusätzlich kann ein begrenzter Korrelationsmodus angeboten werden.

**Beispiel:**

```text
Inflation
   ├── beeinflusst Personalkosten
   ├── beeinflusst Materialkosten
   └── beeinflusst externe Dienstleistungen
```

Das ist fachlich informativer als drei separat gezogene Inflationszuschläge.

### Korrelationsmodell präzise spezifizieren

Für einen Gaussian-Copula-Ansatz kann die Erzeugung grundsätzlich über korrelierte latente Normalvariablen und anschließende Transformation in die Zielverteilungen erfolgen.

**Der technische Vertrag muss mindestens festlegen:**

- Welche Korrelation der Nutzer eingibt: latent, Pearson oder Rangkorrelation.
- Ob die gewünschte Zielkorrelation exakt oder nur näherungsweise erreicht wird.
- Symmetrie der Matrix.
- Einsen auf der Diagonalen.
- Endliche Einträge zwischen −1 und 1.
- Prüfung auf positive Semidefinitheit.
- Umgang mit numerischen Toleranzen.
- Umgang mit singulären Matrizen.
- Ausgabe empirisch erreichter Abhängigkeiten.

**Keinesfalls stillschweigend reparieren:** Eine auf eine gültige Matrix projizierte Eingabe ist eine Modelländerung und benötigt eine sichtbare Bestätigung.

**Weitere Grenze:** Eine Gaussian Copula bildet nicht automatisch jede fachlich relevante gemeinsame Extremwertstruktur ab. Komplexere Copulas gehören deshalb in eine spätere, begründete Erweiterung, nicht als unsichtbare Standardeinstellung in den MVP.

***

## Szenariotechnik richtig integrieren

### Szenario und Simulation trennen

**Empfohlene Definition:**

> Ein Szenario legt fest, unter welchen strukturellen und inhaltlichen Bedingungen simuliert wird. Die Monte-Carlo-Simulation untersucht Unsicherheit innerhalb dieses Bedingungsrahmens.

Szenarioverfahren entwickeln Zukunftsprojektionen für Schlüsselfaktoren und untersuchen deren Verträglichkeit; daraus entstehen unterscheidbare Zukunftsbilder. [scmi](https://www.scmi.de/images/downloads/dateien/scmi_szenariostudie_zukunft-nachhaltigkeit-finanzm%C3%A4rkte.pdf)

**Nicht gleichsetzen:**

| Objekt | Beispiel |
|---|---|
| Parameterunsicherheit | Die Marktwachstumsrate schwankt innerhalb eines angenommenen Umfelds |
| Szenario | Der Markt entwickelt sich unter einem anderen regulatorischen oder technologischen Regime |
| Entscheidung | Das Unternehmen wählt einen anderen Markteintritt |
| Maßnahme | Ein zusätzliches Team oder eine Versicherung verändert die Konsequenzen |

### Minimalumfang für deine erste Phase

Ein einziges Szenario ist ausreichend, sofern seine Annahmen explizit sind.

**Das Datenmodell sollte dennoch von Beginn an enthalten:**

- Szenarioname.
- Zweck.
- Zeithorizont.
- Beschreibung.
- Verwendete Modellversion.
- Einflussfaktoren.
- Gewählte Projektionen.
- Geänderte Parameter.
- Geänderte Ereignisse.
- Gegebenenfalls geänderte Modellstruktur.
- Konsistenzbegründung.
- Reviewstatus.
- Optionales Gewicht mit Begründung.

**Wichtig:** Ein einzelnes analysiertes Szenario bedeutet nicht, dass dessen Eintritt sicher ist. Die Ergebnisverteilung ist zunächst eine bedingte Aussage innerhalb dieses Szenarios.

### Vollständiger Szenarioprozess

**Für eine spätere Ausbaustufe:**

1. Entscheidungszweck und Betrachtungsraum festlegen.
2. Relevante Einflussfaktoren identifizieren.
3. Schlüsselfaktoren auswählen.
4. Alternative Projektionen formulieren.
5. Verträglichkeiten und Ausschlüsse beurteilen.
6. Konsistente Kombinationen bilden.
7. Unterscheidbare Zukunftsbilder auswählen.
8. Szenarien beschreiben.
9. Projektionen in quantitative Modellannahmen übersetzen.
10. Handlungsalternativen über die Szenarien hinweg bewerten.

Konsistenzanalyse und morphologische Szenariobildung sind bereits etablierte methodische Varianten; die App sollte sie als spätere Erweiterungen sauber vom Simulationskern trennen. [scmi](https://www.scmi.de/de/software/scenario-manager)

### Konsistenz ist keine Wahrscheinlichkeit

**Verbindliche Produktregel:**

- Ein Konsistenzwert darf nicht als Eintrittswahrscheinlichkeit verwendet werden.
- Eine gut formulierte Erzählung ist kein quantitativer Beleg.
- Paarweise verträgliche Projektionen garantieren nicht automatisch die Konsistenz der gesamten Kombination.
- Harte fachliche Ausschlüsse müssen unabhängig von einem aggregierten Score gelten.

Die Literatur aus der Szenariopraxis unterscheidet die Verträglichkeit von Projektionen von einer nachgelagerten Bewertung der Zukunftsbilder; Szenarien können ausdrücklich ohne Wahrscheinlichkeiten verwendet werden. [scmi](https://www.scmi.de/images/downloads/dateien/scmi_methoden-report_szenario-management.pdf)

### Keine automatische Szenariomischung

Nur unter ausdrücklich festgelegten Voraussetzungen ist eine Mischung sinnvoll:

\[
p(Y)=\sum_{s=1}^{K}w_s\,p(Y\mid S=s)
\]

**Dafür im Produkt verlangen:**

- Begründete Gewichte.
- Passende Interpretation der Szenarien als unterscheidbare Zustände.
- Keine unbemerkten Überschneidungen.
- Transparenz über nicht abgedeckte Zukunftsmöglichkeiten.
- Sensitivitätsanalyse gegenüber den Gewichten.

**Default:** Szenarien nebeneinander vergleichen, nicht automatisch zu einer einzigen scheinpräzisen Zukunftsverteilung zusammenfassen.

### Robustheit statt Scheinprognose

Auch ohne Szenariowahrscheinlichkeiten sind nützliche Vergleiche möglich.

**Vorgeschlagene spätere Auswertungen:**

- Zielerreichung je Szenario.
- Dominanz von Handlungsalternativen.
- Schlechtester betrachteter Ausgang.
- Bedauern gegenüber der jeweils besten Alternative.
- Maßnahmen, die in mehreren Szenarien helfen.
- Frühindikatoren, die eine Neubewertung auslösen.

**Nicht als gesicherte Zukunftsoptimierung verkaufen:** Das Ergebnis bleibt auf den untersuchten Zukunftsraum begrenzt.

***

## Monte-Carlo-Kern und Ergebnisse

### Berechnungsvertrag

Für eine Modellversion \(M\), ein Szenario \(S\), eine Entscheidung \(d\) und einen Eingabevektor \(X\):

\[
Y=f_{M,S}(X,d)
\]

Die Simulation erzeugt zulässige Realisierungen von \(X\), wertet das Modell wiederholt aus und beschreibt die resultierenden Ergebnisgrößen. [help-risk.lumivero](https://help-risk.lumivero.com/v8_5/en/Guides/@RISK-Getting-Started-Guide.pdf)

**Empfohlener Ablauf:**

1. Modell und Szenario einfrieren.
2. Einheiten, Parameter und Struktur prüfen.
3. Abhängigkeitsmodell validieren.
4. Samplingplan festlegen.
5. Eingaben ziehen.
6. Berechnungsgraph auswerten.
7. Ereignisse und Bedingungen anwenden.
8. Ergebnisse aggregieren.
9. Numerische Diagnostik durchführen.
10. Ergebnis mit vollständigem Herkunftsbezug speichern.

### Samplingstrategie

**Empfohlene Reihenfolge:**

| Stufe | Verfahren | Einsatz im Produkt |
|---|---|---|
| Start | Pseudozufälliges Monte Carlo | Referenzverfahren und gut prüfbarer Ausgangspunkt |
| Erweiterung | Latin Hypercube Sampling | Nur mit entsprechendem Test- und Fehlerkonzept |
| Später | Randomisierte Sobol-Sequenzen | Effizientere Auswertung geeigneter Modelle |

Bei Sobol-Sequenzen sind insbesondere Stichprobenumfänge als Zweierpotenzen und die Erhaltung der Balanceeigenschaften zu beachten; beliebiges Auslassen oder Ausdünnen von Punkten kann diese Eigenschaften zerstören. [docs.scipy](https://docs.scipy.org/doc/scipy-1.16.2/reference/generated/scipy.stats.qmc.Sobol.html)

**Wichtig:** Die Fehlerbewertung darf nicht unverändert vom unabhängigen Monte-Carlo-Sampling auf andere Samplingverfahren übertragen werden.

### Konvergenz statt fixer Iterationsmythen

Für unabhängige Ziehungen mit endlicher Varianz gilt für den Standardfehler des geschätzten Mittelwerts:

\[
SE(\bar{Y})\approx \frac{s_Y}{\sqrt{N}}
\]

Die bekannte Verbesserung mit der Quadratwurzel der Stichprobengröße betrifft die numerische Schätzung, nicht die Qualität der zugrunde liegenden Projektannahmen. [docs.analytica](https://docs.analytica.com/images/3/33/Uncertainty.pdf)

**Für das PRD festlegen:**

- Welche Kennzahlen stabil genug sein müssen.
- Welche absolute oder relative Toleranz gilt.
- Welcher maximale Rechenaufwand zulässig ist.
- Wie Randfälle behandelt werden.
- Wann das Ergebnis als numerisch unzureichend markiert wird.

**Nicht ausreichend:** „Nach 100.000 Iterationen ist das Ergebnis zuverlässig.“

Eine solche Zahl kann eine Produktvoreinstellung sein, ist aber kein universeller wissenschaftlicher Gütenachweis.

### Ereigniswahrscheinlichkeiten

Für eine Budgetüberschreitung:

\[
\hat{p}
=
\frac{1}{N}
\sum_{i=1}^{N}
\mathbf{1}(C_i>B)
\]

**Erforderlich:**

- Definition von Budget und Vergleichsoperator.
- Anzahl beobachteter Überschreitungen.
- Numerische Unsicherheit der Schätzung.
- Geeignetes Intervallverfahren für kleine Ereigniszahlen.

Wilson-Intervalle und exakte Binomialverfahren sind hierfür relevante Referenzen; einfache symmetrische Normalapproximationen sind insbesondere bei wenigen Ereignissen problematisch. [itl.nist](https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/propconf.htm)

**UI-Regel:** Null beobachtete Überschreitungen dürfen nicht ohne Einschränkung als „Risiko = 0%“ erscheinen.

### Quantile korrekt erklären

**Empfohlene Ergebnisformulierung:**

> „Im verwendeten Modell liegen 90% der simulierten Kosten höchstens bei diesem Betrag.“

**Nicht verwenden:**

> „Mit 90% Sicherheit kostet das Projekt höchstens diesen Betrag.“

**Zusätzliche Trennung:**

| Begriff | Bedeutung |
|---|---|
| Ergebnisquantil | Eigenschaft der modellierten Ergebnisverteilung |
| Prognosebereich | Bereich möglicher modellierter Ausgänge |
| Numerisches Konfidenzintervall | Unsicherheit einer aus endlich vielen Simulationen geschätzten Kennzahl |
| Glaubwürdigkeitsintervall | Bayesianische Aussage über eine entsprechend modellierte unbekannte Größe |

**Besonders wichtig für dein Whitepaper-Beispiel:** Median und wahrscheinlichster Wert sind nicht synonym. Bei mehrgipfligen Ergebnissen kann der Median gerade kein typischer Gipfel der Verteilung sein.

### Mindestumfang der Ergebnisansicht

**Für jede relevante Ergebnisgröße:**

- Einheit und Zielrichtung.
- Mittelwert, sofern sinnvoll.
- Median.
- Konfigurierbare Quantile.
- Kumulative Verteilung.
- Histogramm als ergänzende Sicht.
- Zielerreichungs- oder Überschreitungswahrscheinlichkeit.
- Numerischer Qualitätsstatus.
- Verwendetes Szenario.
- Modell- und Eingabeversion.
- Wichtigste Einschränkungen.
- Weiterleitung zu relevanten Annahmen.

Kumulative Verteilungen, Quantile und Sensitivitätsauswertungen gehören zum etablierten Werkzeugkasten der Unsicherheitsanalyse. [docs.analytica](https://docs.analytica.com/images/3/33/Uncertainty.pdf)

### Tail-Risiken

**Als Erweiterung vorsehen:**

- Value at Risk für klar definierte Verlustgrößen.
- Expected Shortfall.
- Wahrscheinlichkeit mehrerer gleichzeitiger Zielverletzungen.
- Extreme Stressfälle.
- Kennzeichnung unzureichend aufgelöster Randbereiche.

Für Expected Shortfall ist folgende Definition auch bei diskreten Verteilungen zweckmäßig:

\[
ES_{\alpha}
=
\frac{1}{1-\alpha}
\int_{\alpha}^{1}q_u(L)\,du
\]

**Implementierungswarnung:** Bei diskreten Verteilungen ist der einfache Mittelwert aller Werte „größer oder gleich VaR“ nicht immer dieselbe Größe.

### Adaptives Stoppen sorgfältig behandeln

**Nicht empfehlen:** Nach jedem kleinen Batch ein gewöhnliches Konfidenzintervall berechnen und beim ersten passenden Ergebnis stoppen, ohne die dadurch geänderte statistische Interpretation zu berücksichtigen.

**Pragmatischer Start:**

- Pilotlauf zur Aufwandsschätzung.
- Danach festgelegter Hauptlauf.
- Vorab definierte Qualitätsprüfungen.
- Bei Bedarf neuer, dokumentierter Lauf mit größerem Umfang.

Fortgeschrittene sequenzielle Verfahren können später ergänzt werden.

***

## Sensitivität und Entscheidungsnutzen

### Unterschiedliche Fragen getrennt beantworten

| Frage | Auswertung |
|---|---|
| Welche Eingaben bewegen sich mit dem Ergebnis? | Deskriptive Rang- oder Korrelationsanalyse |
| Welche Parameteränderung verändert das Ergebnis? | Parametervariation |
| Welche Unsicherheiten erklären Ergebnisstreuung? | Geeignete globale Sensitivitätsanalyse |
| Welche Maßnahme verbessert die Entscheidung? | Expliziter Alternativenvergleich |
| Welche Information wäre ihren Preis wert? | Value-of-Information-Analyse |

**Wichtig:** Eine hohe Korrelation mit dem Ergebnis ist nicht automatisch ein kausaler Hebel und kein prozentualer Beitrag zum Gesamtrisiko.

### Empfohlene erste Ausbaustufe

- Rangbasierte Sensitivitätsdarstellung als **deskriptiv** kennzeichnen.
- Einzelne Parameterbereiche gezielt variieren.
- Alternativen und Maßnahmen explizit vergleichen.
- Gemeinsame Ursachen im Einflussmodell sichtbar machen.
- Ergebnisse bei abhängigen Eingaben besonders vorsichtig interpretieren.

**Spätere Ausbaustufe:**

- Varianzbasierte Sensitivitätsverfahren mit überprüften Voraussetzungen.
- Verfahren für abhängige Eingaben.
- Interaktionsanalyse.
- Sensitivität gegenüber Verteilungsfamilien und Szenariogewichten.

**Produktregel:** Keine vermeintlichen „Risikobeiträge in Prozent“ aus gewöhnlichen Korrelationskoeffizienten erzeugen.

### Maßnahmen müssen im Modell wirken

Ein Risikomanagementsystem sollte mindestens festhalten:

- Welche Maßnahme betrachtet wird.
- Welche Eingaben oder Beziehungen sie verändert.
- Welche Kosten sie verursacht.
- Welche zusätzlichen Risiken sie erzeugt.
- Wer verantwortlich ist.
- Wann sie umgesetzt beziehungsweise überprüft wird.

**Beispiel:**

```text
Zusätzliches Prüfteam
        ↓
Höhere direkte Kosten
        ↓
Geänderte Bearbeitungsdauer
        ↓
Möglicherweise veränderte Fehlerwahrscheinlichkeit
        ↓
Neue Kosten- und Terminverteilung
```

**Nicht ausreichend:** Eine Maßnahme nur als Freitext an ein Risiko zu hängen und daneben unveränderte Simulationsergebnisse auszugeben.

### Wert zusätzlicher Informationen

Für einen späteren Ausbau kann der erwartete Wert perfekter Information auf einer geeigneten probabilistischen Entscheidungsgrundlage betrachtet werden:

\[
EVPI
=
\mathbb{E}_{\theta}
\left[
\max_d U(d,\theta)
\right]
-
\max_d
\mathbb{E}_{\theta}
\left[
U(d,\theta)
\right]
\]

**Voraussetzungen:**

- Definierte Entscheidungen.
- Definierte Nutzen- oder Verlustfunktion.
- Geeignete Wahrscheinlichkeitsgrundlage.
- Trennung von Information und tatsächlichem Eingriff.

**Pragmatischer MVP-Ersatz:** Eine priorisierte Liste „entscheidungssensitive und schwach begründete Annahmen“. Diese darf allerdings nicht als exakter monetärer Informationswert bezeichnet werden.

***

## Fachvorlagen und Anwendungsgrenzen

### Terminplanung als Referenzdomäne

**Empfehlung:** Die erste vollständig ausgearbeitete Referenzdomäne sollte Terminplanung mit Kostenbezug sein.

**Begründung als Produktentscheidung:**

- Enger Anschluss an dein Whitepaper.
- Anschauliche Ursache-Wirkungs-Struktur.
- Gut definierbare Testfälle.
- Sichtbare Bedeutung von Parallelität und Pfadwechseln.
- Gute Übertragbarkeit auf andere Bereiche.

Für einen einfachen Finish-to-Start-Netzplan:

\[
ES_j
=
\max_{i\in Pred(j)}
\left(EF_i+\ell_{ij}\right)
\]

\[
EF_j=ES_j+D_j
\]

**Im ersten Netzplanumfang eindeutig festlegen:**

- Zulässige Abhängigkeitsarten.
- Behandlung von Startknoten.
- Zeitbasis.
- Wartezeiten.
- Projektende.
- Kalender.
- Ressourcenannahmen.
- Gleichstände zwischen kritischen Pfaden.

### Wichtige Terminplanungsgrenzen

- In jeder Iteration muss der tatsächliche Projektabschluss berechnet werden.
- Kritische Pfade können zwischen Iterationen wechseln.
- Quantile einzelner Vorgänge dürfen nicht zu einem Projektquantil addiert werden.
- Ein bloßer Netzplan bildet keine konkurrierende Ressourcennutzung ab.
- Kalender- und Schichtlogik müssen ausdrücklich implementiert sein, bevor solche Aussagen angeboten werden.

Auch etablierte Terminrisikoansätze betonen, dass realistische Eingaben, Beziehungen und Abhängigkeiten entscheidend sind. [lumivero](https://lumivero.com/wp-content/uploads/Wallace_Schedule_Risk.pdf)

**Empfehlung:** Im MVP Ressourcenrestriktionen entweder explizit ausschließen oder in einer bewusst begrenzten, getesteten Form unterstützen. Keine implizite Behauptung eines vollständigen Ressourcenplaners.

### Kritikalitätsauswertung

**Sinnvolle Kennzahlen:**

- Anteil der Iterationen, in denen ein Vorgang kritisch ist.
- Häufigkeit bestimmter kritischer Pfadkonstellationen.
- Einfluss von Vorgängen auf den Projektabschluss.
- Wahrscheinlichkeit, einen Meilenstein zu verfehlen.
- Wirkung einer Maßnahme auf Termin und Kosten.

**Wichtig:** Vorgänge auf mehreren gleichzeitig kritischen Pfaden können gemeinsam kritisch sein. Kritikalitätswerte müssen deshalb nicht zu 100% summieren.

### Kosten und Wirtschaftlichkeit

**Geeignete Modellbausteine:**

- Mengen.
- Einheitspreise.
- Dauerabhängige Kosten.
- Fixkosten.
- Ereignisbedingte Zusatzkosten.
- Erlöse.
- Preisänderungen.
- Verzögerungsschäden.

**Zwingende Semantik:**

- Währung.
- Preisbasis.
- Betrachtungszeitpunkt.
- Nominal oder real.
- Brutto oder netto, sofern relevant.
- Zahlungszeitpunkte.
- Diskontierungsannahmen.

Für eine diskrete Cashflow-Bewertung kann beispielsweise gelten:

\[
NPV
=
-I_0+
\sum_{t=1}^{T}
\frac{CF_t}{(1+r)^t}
\]

**Produktgrenze:** Ein allgemeines Cashflow-Modell ist noch kein validiertes Modell für beliebige Kapitalmarktprodukte.

### Investments und Strategien

**Für Investments zunächst unterstützen:**

- Projekt- und Beteiligungscashflows.
- Verlustwahrscheinlichkeiten.
- Liquiditätsbedarf.
- Kapitalbindung.
- Alternative Annahmen und Stressfälle.

**Zunächst nicht als generisch gelöst darstellen:**

- Vollständige Marktpreisprozesse.
- Volatilitätsdynamik.
- Derivatebewertung.
- Handelsstrategien.
- Regulatorisch relevante Anlageberatung.

**Für Strategien unterstützen:**

- Handlungsalternativen.
- Zielgrößen und nachvollziehbare Gewichtungen.
- Szenarioabhängige Konsequenzen.
- Robustheitsvergleich.
- Maßnahmen und Frühindikatoren.

**Nicht empfehlen:** Qualitative SWOT-Begriffe ohne belastbare Operationalisierung direkt in Wahrscheinlichkeitsverteilungen zu übersetzen.

***

## Oberfläche mit geringer Einstiegshürde

### Einfache Bedienung durch Führung

**Kernprinzip:**

> Die Oberfläche soll die Komplexität schrittweise erschließen, nicht durch versteckte Annahmen beseitigen.

**Empfohlene Hauptnavigation:**

1. **Ziel**
2. **Modell**
3. **Annahmen**
4. **Szenarien**
5. **Ergebnisse**
6. **Maßnahmen**

Ein Quellenbereich und ein Versionsverlauf sind jederzeit erreichbar, müssen aber nicht den Einstieg dominieren.

### Einstieg über eine konkrete Frage

**Startdialog:**

- Was möchtest du entscheiden?
- Welche Ergebnisgröße ist wichtig?
- Was gilt als akzeptabel?
- Welcher Zeitraum wird betrachtet?
- Welche Vorlage passt am ehesten?

**Beispiele für Einstiegskarten:**

- „Wie wahrscheinlich ist die Einhaltung meines Projekttermins?“
- „Wie viel Budgetreserve wird benötigt?“
- „Welche Strategie ist über mehrere Zukünfte belastbar?“
- „Wie empfindlich ist mein Ergebnis gegenüber zentralen Annahmen?“

### Die Annahmenkarte

Jede Eingabe sollte in einer verständlichen Karte bearbeitet werden:

| Bereich | Inhalt |
|---|---|
| Bedeutung | Was wird beschrieben? |
| Einheit | Tage, Euro, Anteil usw. |
| Eingabe | Wert, Bereich, Quantile oder Daten |
| Unsicherheit | Gewählte Verteilung und Interpretation |
| Herkunft | Quellen und Experteneinschätzungen |
| Übertragbarkeit | Warum passt die Evidenz zu diesem Projekt? |
| Beziehungen | Gemeinsame Treiber und Abhängigkeiten |
| Status | Entwurf, geprüft, freigegeben, überfällig |

**Visualisierung:**

- Eine kleine Verteilungsdarstellung direkt neben den Angaben.
- Harte Grenzen anders markieren als Quantile.
- Warnungen textlich erläutern.
- Änderungen an Form und Lage unmittelbar sichtbar machen.

### Zwei Bedienebenen

| Ebene | Verhalten |
|---|---|
| Geführter Modus | Fachbegriffe erklären, Vorlagen anbieten, sinnvolle Prüfungen erzwingen |
| Expertenmodus | Technische Parameter, Abhängigkeitsdetails, Diagnostik und Konfiguration zeigen |

**Nicht empfehlen:**

- Zwei getrennte Modellwelten.
- Unterschiedliche Rechenergebnisse zwischen Anfänger- und Expertenmodus.
- Wissenschaftlich problematische Standardannahmen nur deshalb, weil sie einfacher aussehen.

### Ergebnisführung

**Die erste Ergebnisansicht sollte vier Fragen beantworten:**

- Wie häufig wird mein Ziel im Modell erreicht?
- Welche Ergebnisbereiche sind relevant?
- Welche Annahmen beeinflussen das Ergebnis besonders?
- Was sollte ich als Nächstes prüfen oder verändern?

**Zusätzlich sichtbar:**

- „Dieses Ergebnis gilt für …“
- „Diese Annahmen sind noch schwach begründet …“
- „Diese Einschränkungen wurden nicht modelliert …“
- „Letzter freigegebener Stand …“

### Vorgeschlagene UX-Abnahmekriterien

Die folgenden Werte sind **Produktziele**, keine empirisch nachgewiesenen Eigenschaften:

- Ein fachlich geeigneter Erstnutzer kann mit einer Vorlage ein kleines Modell in höchstens 20 Minuten aufbauen.
- Mindestens vier von fünf Testpersonen interpretieren ein angezeigtes Kostenquantil korrekt.
- Nutzer können die Quelle einer wesentlichen Eingabe ohne externe Hilfe finden.
- Eine Änderung mit Einfluss auf freigegebene Ergebnisse ist vor dem Speichern erkennbar.
- Die Oberfläche bleibt ohne KI-Funktion vollständig nutzbar.
- Warnungen funktionieren ohne reine Farbcodierung.

***

## Technische Zielarchitektur

### Modularer Monolith als Ausgangspunkt

**Empfehlung:** Ein modularer Monolith mit getrennt ausführbarem Simulationsworker.

```text
Browser-Oberfläche
        ↓
Anwendungs-API
        ↓
Anwendungsdienste
        ↓
Fachmodell und Validierung
        ↓
Reiner Simulationskern
```

**Seitliche Adapter:**

```text
Anwendungsdienste
   ├── Datenbank
   ├── Dokumentenspeicher
   ├── Rechercheanbieter
   ├── optionale LLM-Anbieter
   ├── Export
   └── Jobausführung
```

**Warum dieser Entwurf empfohlen wird:**

- Ein Rechenkern für lokale und gehostete Nutzung.
- Keine Netzwerkabhängigkeit innerhalb einer numerischen Auswertung.
- Isolierbare Tests.
- Kontrollierte spätere Skalierung.
- Weniger Betriebsaufwand als bei frühzeitiger Servicezerlegung.
- Gute Anschlussfähigkeit an die Adaptertrennung deines Entwicklungsschemas. [Repository-Regeln](https://github.com/ToHeinAC/claude-dev-schema/blob/main/AGENTS.md)

### Empfohlener Technologiepfad

Die folgende Auswahl ist eine **Entwurfsempfehlung**, keine Behauptung, dass nur dieser Stack geeignet wäre:

| Bereich | Vorschlag |
|---|---|
| Fach- und Rechenkern | Python |
| Numerik | NumPy und SciPy |
| Datenvalidierung | Explizite typisierte Schemas, beispielsweise Pydantic |
| API | FastAPI |
| Datenhaltung | PostgreSQL |
| Migrationen | Versionierte Datenbankmigrationen |
| Dokumente | Vom Datenbankmodell getrennter Objektspeicher |
| Jobausführung | Persistente Jobs mit separatem Worker |
| Oberfläche | Nach kurzem UX-Spike entscheiden |
| Reproduzierbarkeit | Versionsgebundene Laufumgebung und Lockfile |
| Tests | Unit-, Eigenschafts-, Integrations- und wissenschaftliche Referenztests |

### Die Frontendentscheidung

| Option | Rolle im Projekt | Zu prüfender Nachteil |
|---|---|---|
| Streamlit | Sehr schneller fachlicher Demonstrator | Eignung für komplexe Modellbearbeitung und Produktinteraktion nachweisen |
| Pythonzentrierte Weboberfläche, etwa NiceGUI | Kandidat für einen einheitlichen Python-Stack | Komponenten, Zustandsmodell und Langfristigkeit praktisch prüfen |
| React/TypeScript mit Python-API | Kandidat für stärker individualisiertes Produktfrontend | Zusätzlicher Stack und zusätzliche Qualitätsgates |

**Empfehlung:** Nicht allein aus Gewohnheit entscheiden. Ein kurzer Spike muss drei schwierige Abläufe tatsächlich abbilden:

- Annahmenkarte mit Evidenzvergleich.
- Bearbeitung eines kleinen Abhängigkeitsmodells.
- Interaktive Ergebnisinterpretation mit Versionsbezug.

**Für das PRD:** Danach genau einen Hauptpfad festlegen. Kein dauerhaftes paralleles Produktfrontend.

**Wichtig für dein Schema:** Bei TypeScript müssen zusätzliche Prüfungen für Typen, Tests, Formatierung, Abhängigkeiten und Build ergänzt werden. Das vorhandene Python-Gate prüft diesen Teil nicht automatisch. [Entwicklungsschema](https://github.com/ToHeinAC/claude-dev-schema)

### Modellrepräsentation

**Empfehlung:** Das Fachmodell ist ein versioniertes, serialisierbares Schema – nicht ein Python-Skript.

**Knotentypen:**

- `constant`
- `uncertain`
- `event`
- `derived`
- `decision`
- `output`

**Jeder Knoten enthält mindestens:**

- Stabile ID.
- Fachlichen Namen.
- Datentyp.
- Einheit.
- Beschreibung.
- Parameter oder Berechnungsregel.
- Eingehende Beziehungen.
- Annahmenbezug.
- Versionsinformation.

**Architekturregel:** Die Visualisierung ist eine Darstellung dieses Modells, nicht dessen einzige Speicherung.

### Sicherer Ausdruckseditor

**Nicht zulassen:**

- Beliebiges Python.
- `eval`.
- Dateizugriff.
- Netzwerkzugriff.
- Importe.
- Unbegrenzte Rekursion.
- Unbegrenztes Erzeugen großer Datenstrukturen.
- Ausführung von LLM-generiertem Code im Produktbetrieb.

**Stattdessen:**

- Kleine, explizit definierte Ausdruckssprache.
- Erlaubte mathematische Operatoren.
- Definierte Aggregationen.
- Bedingte Ausdrücke.
- Einheitenprüfung.
- Begrenzte Ausdruckstiefe.
- Begrenzte Modellgröße.
- Eindeutige Fehlerzustände.

**Wichtig:** Eine Syntax-Whitelist allein ersetzt keine Ressourcenbegrenzung und keine vollständige Sprachspezifikation.

### Simulation als persistenter Job

**Jobzustände:**

- Erstellt.
- Validiert.
- Wartend.
- Laufend.
- Abgebrochen.
- Fehlgeschlagen.
- Erfolgreich.
- Erfolgreich mit Qualitätswarnung.

**Für jeden Job speichern:**

- Modell- und Szenariosnapshot.
- Entscheidungskonfiguration.
- Seed und Generator.
- Samplingverfahren.
- Anzahl der Ziehungen.
- Batchkonfiguration.
- Softwareversionen.
- Laufzeitumgebung.
- Start und Ende.
- Qualitätsdiagnostik.
- Ergebnisdateien.
- Fehler beziehungsweise Warnungen.

**Empfehlung:** Rechenintensive Simulationen nicht als unkontrollierte Nebenaufgabe eines Webrequests ausführen.

### Reproduzierbare Zufallszahlen

NumPy stellt Konzepte zur Ableitung separater Zufallsströme für parallele Ausführungen bereit; stabile Identitäten und eine festgelegte Aufteilung der Ströme sind dabei wesentlich. [numpy](https://numpy.org/doc/1.24/reference/random/parallel.html)

**Produktanforderungen:**

- Ein Seed allein ist nicht die vollständige Reproduzierbarkeitsbeschreibung.
- Generator und Bibliotheksversionen speichern.
- Stromzuordnung stabil definieren.
- Änderungen der Parallelisierung berücksichtigen.
- Rechenpfad und Quantilalgorithmus versionieren.
- Bitgleiche Wiederholung nur für klar festgelegte Umgebungen zusagen.

**Für Alternativenvergleiche:** Gemeinsame Zufallszahlen können als bewusstes Verfahren vorgesehen werden. Die Zuordnung muss jedoch Abhängigkeiten erhalten und darf nicht nur zufällig durch dieselbe Seedzahl entstehen.

***

## Datenmodell und Lebenszyklus

### Fachliche Kernobjekte

| Objekt | Aufgabe |
|---|---|
| Workspace | Nutzer- beziehungsweise spätere Mandantengrenze |
| Project | Entscheidungsraum |
| Objective | Zielgröße und Bewertung |
| Model | Struktur des Wirkungsmodells |
| ModelVersion | Konkreter unveränderlicher Stand |
| Variable | Fachliche Eingangs- oder Rechengröße |
| DistributionSpec | Kanonische Verteilungsdefinition |
| DependencySpec | Abhängigkeitsdefinition |
| Scenario | Zukunfts- beziehungsweise Bedingungsrahmen |
| DecisionAlternative | Beeinflussbare Alternative |
| EvidenceSource | Dokument oder Webquelle |
| Claim | Extrahierte Aussage |
| Assumption | Für das Modell akzeptierte Festlegung |
| EvidenceAssessment | Bewertung und Übertragbarkeit |
| SimulationRun | Ausgeführter Rechenlauf |
| ResultArtifact | Kennzahlen und Ausgabedateien |
| Mitigation | Maßnahme |
| Review | Fachliche Prüfung |
| AuditEvent | Nachvollziehbare Änderung |

**Wichtig:** Quelle, Aussage und Annahme dürfen nicht zu einem einzigen Freitextfeld zusammengezogen werden.

### Veränderbare Entwürfe, feste Auswertungsstände

**Empfohlener Lebenszyklus:**

```text
Entwurf
   ↓
Validiert
   ↓
Fachlich freigegeben
   ↓
Snapshot für Auswertung
   ↓
Simulation
   ↓
Ergebnisfreigabe
   ↓
Entscheidung / Maßnahme
```

**Bei Änderungen:**

- Neue Version statt Überschreiben.
- Frühere Ergebnisse bleiben mit ihrem früheren Stand verbunden.
- Betroffene Ergebnisse werden als möglicherweise überholt markiert.
- Änderungen werden fachlich und technisch unterschieden.
- Eine Quellenaktualisierung erzeugt nicht automatisch eine neue freigegebene Annahme.

### Exporte und Portabilität

**Bereits für Selbstnutzung empfehlen:**

- Vollständiger Projekt-Export in einem dokumentierten Format.
- Tabellenexport zentraler Eingaben und Ergebnisse.
- Lesbarer Ergebnisbericht.
- Ein- und Ausgangsversionen im Export.
- Hinweise auf fehlende Quellenrechte.
- Wiederimport mit Validierung.

**Nicht empfehlen:** Ein Produkt, aus dem nur Diagrammbilder exportiert werden können.

***

## Sicherheit und späterer SaaS-Betrieb

### Früh vorsehen, später ausbauen

**Ab der ersten Version:**

- Projektbezogene Zugriffsgrenzen.
- Kein vertraulicher Inhalt in gewöhnlichen Fehlerlogs.
- Konfigurierbare externe Datenübermittlung.
- Getrennte Geheimnisverwaltung.
- Eingabe- und Uploadvalidierung.
- Beschränkter Recherchezugriff.
- Persistente Sicherungen.
- Wiederherstellungstest.
- Nachvollziehbare Änderungen.

**Vor Zugriff durch Dritte zusätzlich:**

- Sichere Authentisierung.
- Rollen und Berechtigungen.
- Mandantentrennung.
- Objekt- und dokumentbezogene Zugriffskontrolle.
- Jobquoten.
- Kostenlimits.
- Monitoring.
- Sicherheitsupdates.
- Incident-Prozess.
- Lösch- und Aufbewahrungsprozesse.

### Mandantentrennung nicht nur in der UI

Eine spätere Mehrmandantenfähigkeit betrifft:

- Datenbank.
- Dokumentenspeicher.
- Ergebnisdateien.
- Jobausführung.
- Caches.
- Suchindizes.
- Logs.
- Exporte.
- Supportzugriffe.

Row-Level Security kann eine zusätzliche Datenbankschutzschicht bilden; privilegierte Rollen und Tabelleneigentümer können solche Regeln aber je nach Konfiguration umgehen. [docs.cloud.google](https://docs.cloud.google.com/sql/docs/postgres/data-privacy-strategies)

**Daraus folgende Anforderungen:**

- Laufzeitanwendung nicht mit unnötig privilegierter Datenbankrolle betreiben.
- Isolation automatisiert testen.
- Benutzer- und Mandantenkontext in Jobs ausdrücklich übergeben.
- Objektpfade nicht als ausreichende Berechtigungsprüfung betrachten.
- Hintergrundprozesse denselben Zugriffsvorgaben unterwerfen.

### Recherche- und KI-Grenzen

**Vorgeschlagenes Sicherheitsmodell:**

- Webinhalte werden als nicht vertrauenswürdige Daten behandelt.
- Inhalte aus Quellen dürfen keine Systemanweisungen auslösen.
- Recherche kann keine Dateien aus dem internen Projektbereich versenden.
- URL-Abrufe blockieren interne Zieladressen und kontrollieren Weiterleitungen.
- Dateityp, Größe, Laufzeit und Parserressourcen werden begrenzt.
- LLM-Ausgaben müssen ein Schema erfüllen.
- Schemaerfüllung gilt nicht als Wahrheitsnachweis.
- Jede numerisch wirksame Übernahme benötigt Freigabe.

**Entscheidend:** Die KI darf den prüfbaren Kern unterstützen, aber nicht dessen Autorität ersetzen.

### Datenschutz und Rechtsprüfung

Für eine kommerzielle Freigabe sollte ein gesondertes Prüfpaket vorgesehen werden.

**Prüfgegenstände:**

- Datenschutzrollen und Vertragsbeziehungen.
- Verarbeitung personenbezogener Inhalte.
- Auftragsverarbeitung und Unterauftragnehmer.
- Internationale Datenübermittlungen.
- Löschung und Aufbewahrung.
- Rechte an hochgeladenen Dokumenten.
- Zulässigkeit von Quellenspeicherung und Weitergabe.
- Haftung und Leistungsbeschreibung.
- Einordnung konkret angebotener KI-Funktionen.
- Finanzaufsichtsrechtliche Fragen bei tatsächlichen Anlageempfehlungen.
- Besondere Anforderungen sicherheitsrelevanter Einsatzgebiete.

**Abgrenzung:** Dieser Bericht ist keine rechtliche Einstufung des späteren Produkts. Insbesondere sollte aus „generische Risikomanagementsoftware“ keine automatische regulatorische Freistellung abgeleitet werden.

### Lizenzhygiene

**Vor Produktfreigabe:**

- Softwarestückliste erstellen.
- Exakte Paketversionen erfassen.
- Lizenzen und transitive Abhängigkeiten prüfen.
- Hinweise und Weitergabepflichten erfüllen.
- PDF- und Dokumentenparser gesondert betrachten.
- Modellgewichte und KI-Dienste getrennt von Programmbibliotheken prüfen.
- Webdatenrechte getrennt von Softwarelizenzen behandeln.
- Lizenzprüfung nach Updates wiederholen.

**Wichtig:** Die technische Eignung einer Bibliothek beantwortet nicht automatisch die Frage nach ihrer Eignung für ein proprietäres oder gehostetes Geschäftsmodell.

***

## Anforderungen als PRD-Grundlage

### Funktionaler Mindestumfang

Die folgende Priorisierung ist ein **Vorschlag für das erste tatsächlich nutzbare Produkt**.

| ID | Anforderung | Priorität |
|---|---|---|
| FR-01 | Projekte mit Zielgrößen, Einheiten und Schwellen anlegen | Muss |
| FR-02 | Konstante, unsichere, berechnete und ereignisbezogene Größen definieren | Muss |
| FR-03 | Sieben vorgeschlagene kontinuierliche Verteilungsfamilien unterstützen | Muss |
| FR-04 | Parameter- und Wertebereichsprüfung durchführen | Muss |
| FR-05 | Einfachen gerichteten Berechnungsgraphen auswerten | Muss |
| FR-06 | Kleine Termin- und Kostenmodelle über Vorlagen aufbauen | Muss |
| FR-07 | Gemeinsame Treiber und dokumentierte Unabhängigkeit unterstützen | Muss |
| FR-08 | Quellen, Aussagen und Annahmen getrennt speichern | Muss |
| FR-09 | Recherche zu ausgewählten Eingaben durchführen und Befunde zur Freigabe vorlegen | Muss |
| FR-10 | Eingaben ohne Web- oder KI-Zugang manuell pflegen | Muss |
| FR-11 | Mindestens ein explizites Szenario unterstützen | Muss |
| FR-12 | Modellstände einfrieren und reproduzierbar simulieren | Muss |
| FR-13 | Quantile, Zielerreichung und Qualitätsstatus darstellen | Muss |
| FR-14 | Einfache Sensitivitäts- und Maßnahmenvergleiche ermöglichen | Muss |
| FR-15 | Projekt und Ergebnisse exportieren | Muss |

### Frühe Erweiterungen

| ID | Anforderung | Priorität |
|---|---|---|
| FR-16 | Mehrere Szenarien mit nachvollziehbaren Unterschieden vergleichen | Soll |
| FR-17 | Explizite Korrelationsgruppen mit validierter Semantik | Soll |
| FR-18 | Historische Daten importieren und Verteilungsanpassung unterstützen | Soll |
| FR-19 | Parameterunsicherheit getrennt fortpflanzen | Soll |
| FR-20 | Reviews und Verantwortlichkeiten für mehrere Personen | Soll |
| FR-21 | Konsistenzgestützte Szenariogenerierung | Später |
| FR-22 | Fortgeschrittene globale Sensitivität und Informationswert | Später |
| FR-23 | Abrechnung, Kontingente und Selbstbedienungsregistrierung | Vor öffentlichem Produkt |
| FR-24 | Komplexe Ressourcen-, Kalender- und Finanzmodelle | Fachlich begrenzte Erweiterungen |

### Nichtfunktionale Anforderungen

| ID | Vorgeschlagene Anforderung |
|---|---|
| NFR-01 | Numerischer Kern ohne Netzwerk- und Datenbankzugriffe testbar |
| NFR-02 | Jeder Ergebnisstand auf Modell, Annahmen und Konfiguration zurückführbar |
| NFR-03 | Keine stillschweigende Reparatur ungültiger Eingaben |
| NFR-04 | Keine Ausführung beliebigen Nutzer- oder KI-Codes |
| NFR-05 | Vollständige Nutzung ohne verpflichtenden KI-Anbieter |
| NFR-06 | Abbruch und Fehler eines Jobs beschädigen keine freigegebenen Ergebnisse |
| NFR-07 | Vertrauliche Inhalte werden nicht standardmäßig extern übertragen |
| NFR-08 | Projektdaten bleiben exportierbar |
| NFR-09 | Sicherheitsgrenzen werden automatisiert geprüft |
| NFR-10 | Performanceziele basieren auf definierten Referenzmodellen |
| NFR-11 | Ergebniswarnungen sind verständlich und maschinenlesbar |
| NFR-12 | Die vorhandenen Repository-Qualitätsregeln bleiben verbindlich |

### Bewusste Nichtziele

**Für die erste Phase ausschließen:**

- Automatische Entscheidungen ohne Nutzerfreigabe.
- Vollständige Abdeckung sämtlicher Branchenstandards.
- Vollständiger Ersatz professioneller Terminplanungssoftware.
- Beliebige Python-Skripte als Nutzermodell.
- Selbstständig handelnde Rechercheagenten mit breiten Berechtigungen.
- Automatischer Finanzhandel.
- Sicherheitsnachweise für kerntechnische oder vergleichbar kritische Anlagen.
- Vollständige bayesianische Inferenz für jedes Modell.
- Automatisch richtige Szenariowahrscheinlichkeiten.
- Ein eigener allgemeiner Workflow- oder Agentenbaukasten.

***

## Wissenschaftliche Qualitätssicherung

### Mehr als Softwaretests

**Vier getrennte Prüfebenen:**

| Ebene | Leitfrage |
|---|---|
| Implementierungsprüfung | Rechnet der Code entsprechend seiner Spezifikation? |
| Mathematische Verifikation | Stimmen Algorithmen und Kennzahlen? |
| Modellvalidierung | Bildet das konkrete Modell den Entscheidungsraum angemessen ab? |
| Entscheidungsvalidierung | Sind die Ergebnisse für den vorgesehenen Zweck ausreichend? |

**Wichtig:** Hohe Testabdeckung allein belegt keine fachliche Modellgültigkeit.

### Verifikation des Rechenkerns

**Erforderliche Referenztests:**

- Konstantenmodell liefert exakt konstantes Ergebnis.
- Summe unabhängiger geeigneter Größen erfüllt bekannte Momentbeziehungen.
- Einheitenfehler werden erkannt.
- Verteilungsparameter werden korrekt transformiert.
- Quantile werden mit dem festgelegten Verfahren berechnet.
- Ereignisse mit Wahrscheinlichkeit 0 oder 1 verhalten sich korrekt.
- Derselbe gemeinsame Treiber wird pro Iteration nur einmal gezogen.
- Einfache serielle und parallele Netzpläne liefern die erwartete Struktur.
- Ungültige Zyklen werden abgewiesen.
- Ungültige Korrelationsmatrizen werden nicht stillschweigend akzeptiert.
- Nichtendliche Ergebnisse führen zu einem erklärten Fehlerzustand.

### Eigenschaften statt Zufallsglück

**Sinnvolle Eigenschaftstests:**

- Skalierung einer positiven Kostenbasis skaliert entsprechende Ergebnisse konsistent.
- Erhöhung einer strikt additiven Kostenkomponente senkt nicht die Gesamtkosten.
- Umbenennen eines Knotens verändert keine numerischen Ergebnisse.
- Entfernen einer ungenutzten Eingabe verändert das Ergebnis nicht.
- Export und Import erhalten die Modellbedeutung.
- Reproduktionskonfiguration erzeugt im festgelegten Umfeld denselben Lauf.

**Nicht empfehlen:** Tests, die wegen zufälliger Stichprobenschwankungen regelmäßig fehlschlagen.

### Statistische Prüfungen

**Separat planen:**

- Verteilungsdiagnostik.
- Konvergenztests.
- Korrelationsdiagnostik.
- Vergleich von Samplingverfahren.
- Quantilgenauigkeit.
- Seltene Ereignisse.
- Parametergrenzfälle.
- Große Modellgrößen.

**Wichtig:** Statistische Tests benötigen Toleranzen, Fehlerbudgets und eine begründete Interpretation. Ein einzelner nicht signifikanter Anpassungstest ist kein allgemeiner Beweis für ein korrektes Modell.

### Prüfbare Benchmarks

**Referenzmodelle definieren:**

- Kleines Kostenmodell.
- Serieller Terminplan.
- Paralleler Terminplan.
- Gemeinsamer Kostentreiber.
- Ereignisbedingte Verzögerung.
- Nichtlineare Bedingung.
- Mehrgipfliges Ergebnis.
- Mehrere Zielgrößen.
- Zwei explizit unterschiedliche Szenarien.

**Für jedes Referenzmodell speichern:**

- Zweck.
- Fachliche Annahmen.
- Erwartete strukturelle Eigenschaften.
- Analytische Vergleichswerte, soweit vorhanden.
- Numerische Toleranzen.
- Referenzumgebung.

**Keine Performancebehauptungen vor Messung:** „Sekundenschnell für beliebige Projekte“ sollte weder im PRD noch in der Vermarktung stehen.

***

## Phase 4 – Implementierung

### Echte Barrieren

| Barriere | Einordnung | Umgang |
|---|---|---|
| Unklare Modellsemantik | Echt | Fachvertrag vor UI-Optimierung festlegen |
| Schwache Datenbasis | Echt | Offenlegen, Expertenwissen strukturieren, Informationsbedarf priorisieren |
| Quellenrechte | Echt | Rechtmäßige Speicherung und Weitergabe klären |
| Abhängigkeiten unbekannt | Echt | Gemeinsame Treiber, Sensitivität und dokumentierte Annahmen |
| Einfache Bedienung bei komplexer Methodik | Echt | Geführte Abläufe und Nutzertests |
| „Dafür braucht man Excel“ | Konvention | Eigenständiges, exportierbares Modellformat |
| „SaaS braucht sofort Microservices“ | Keine fundamentale Notwendigkeit | Modular starten |
| „KI muss die Eingaben automatisch festlegen“ | Keine Notwendigkeit | Assistenz statt Autorität |
| „Alle Domänen müssen zum Start gleich gut sein“ | Vermeidbare Überforderung | Eine Referenzdomäne vollständig umsetzen |

### Empfohlene Meilensteine

| Meilenstein | Ergebnis | Zentrale Abnahme |
|---|---|---|
| M0 – Fachvertrag | Begriffe, Grenzen, Referenzfälle, UI-Spike | Modellsemantik und Frontendpfad entschieden |
| M1 – Rechenkern | Verteilungen, Ereignisse, DAG, einfache Netzpläne | Analytische und strukturelle Referenztests bestanden |
| M2 – Evidenzkette | Quellen, Aussagen, Annahmen, Recherchefreigabe | Jede wirksame Eingabe nachvollziehbar |
| M3 – Selbstnutzbare App | Durchgängiger Ablauf mit einem Szenario | Reales eigenes Projekt vollständig bearbeitbar |
| M4 – Methodische Erweiterung | Szenarienvergleich, explizite Abhängigkeiten, bessere Diagnostik | Definierte Vergleichs- und Grenzfälle bestanden |
| M5 – Geschlossene Pilotphase | Nutzung durch ausgewählte Dritte | Isolation, Restore, Betrieb und Support nachgewiesen |
| M6 – Bezahlprodukt | Verträge, Abrechnung, Kontingente, Freigaben | Produkt- und Betriebsfreigabe erteilt |

**Priorität:** M3 ist das Ziel der ersten Phase. M5 und M6 sind eigenständige Produktisierungsarbeit, keine bloßen Deployment-Aufgaben.

### Der entscheidende erste Prototyp

Der erste Prototyp sollte **einen vertikalen Durchstich** zeigen:

```text
Ein Projekt
   ↓
Eine konkrete Entscheidungsfrage
   ↓
Ein kleines Termin-/Kostenmodell
   ↓
Mehrere begründete Eingaben
   ↓
Eine widersprüchliche oder einschränkende Quelle
   ↓
Freigegebene Annahmen
   ↓
Ein Szenario
   ↓
Simulation
   ↓
Verständliches Ergebnis
   ↓
Eine verglichene Maßnahme
```

**Damit werden gleichzeitig geprüft:**

- Fachliche Konsistenz.
- Bedienbarkeit.
- Evidenzworkflow.
- Numerischer Kern.
- Versionierung.
- Praktischer Entscheidungsnutzen.

**Nicht als ersten Prototyp wählen:** Einen großen Verteilungskatalog mit schönem Dashboard, aber ohne durchgängige Herkunftskette.

### Zeit und Ressourcen

Eine belastbare Kalenderplanung lässt sich aus den Anforderungen allein noch nicht ableiten.

**Vor einer Aufwandsschätzung erforderlich:**

- Frontendentscheidung.
- Modellierungsumfang des MVP.
- Umfang der Terminplanlogik.
- Automatisierungsgrad der Recherche.
- Anforderungen an lokale beziehungsweise gehostete Nutzung.
- Exportformate.
- Gewünschte Prüfungstiefe.
- Verfügbare Entwicklungs- und Reviewkapazität.

**Minimal notwendige Rollen beziehungsweise Kompetenzen:**

- Produktverantwortung.
- Fachliche Modellierung und Statistik.
- Softwarearchitektur und Implementierung.
- UX-Prüfung mit tatsächlichen Nutzern.
- Unabhängiges Code- und Methodikreview.
- Vor Fremdnutzung zusätzlich Betriebs- und Sicherheitsverantwortung.

Diese Rollen können anfangs teilweise von derselben Person wahrgenommen werden. Fachliche Freigabe und unabhängige Prüfung sollten dadurch aber nicht vollständig entfallen.

***

## Anschluss an dein Claude-Schema

### Die Dokumente richtig verwenden

Dein Schema unterscheidet ausdrücklich zwischen Produktanforderungen, Implementierungsstatus und vertiefenden Komponentendokumenten. Unter anderem sind für `PRD.md` höchstens 800 Zeilen und für `IMPLEMENTATION.md` höchstens 500 Zeilen vorgesehen. [Repository-Regeln](https://github.com/ToHeinAC/claude-dev-schema/blob/main/AGENTS.md)

**Empfohlene Zuordnung:**

| Dokument | Inhalt für dieses Vorhaben |
|---|---|
| `PRD.md` | Problem, Nutzer, Ziele, Nichtziele, Anforderungen, Meilensteine, Abnahmen |
| `IMPLEMENTATION.md` | Aktueller Stand, Phasentabelle, Modulkarte, Ausführung und Prüfung |
| `docs/architecture.md` | Schichten, Datenflüsse, Grenzen und begründete Architekturentscheidungen |
| `docs/model-semantics.md` | Knotentypen, Einheiten, Ausdrücke, Szenarien und Ereignisse |
| `docs/statistical-methods.md` | Verteilungen, Parameter, Abhängigkeiten, Sampling und Kennzahlen |
| `docs/evidence.md` | Quellenmodell, Aussagen, Übertragbarkeit, Freigaben |
| `docs/validation.md` | Referenzfälle, Toleranzen, wissenschaftliche Prüfung |
| `docs/security.md` | Datenflüsse, Bedrohungsmodell und Schutzgrenzen |
| `docs/operations.md` | Deployment, Sicherung, Wiederherstellung, Monitoring |
| `docs/adr-*.md` | Wesentliche dokumentierte Entscheidungen, sofern diese Ablageform gewählt wird |

**Wichtig:** Diesen ausführlichen Bericht nicht unverändert in `PRD.md` kopieren. Er ist die Analysegrundlage; das PRD muss daraus einen überprüfbaren Produktvertrag machen.

### Vorgeschlagene Modulstruktur

Die Struktur ist ein Entwurf und sollte erst mit den tatsächlich freigegebenen Meilensteinen aufgebaut werden:

```text
src/app/
    domain/
        projects.py
        models.py
        evidence.py
        scenarios.py
        decisions.py

    core/
        distributions/
        expressions/
        dependencies/
        simulation/
        statistics/
        scheduling/

    services/
        model_validation.py
        evidence_review.py
        simulation_jobs.py
        comparisons.py

    adapters/
        database/
        documents/
        research/
        llm/
        exports/

    api/
    worker/
```

**Nicht vorsorglich alle Module ausbauen:** Erst Verantwortlichkeiten festlegen, dann entlang vertikaler Funktionen implementieren.

### Qualitätsgate erhalten

Dein Repository sieht unter anderem vor:

- Python ab 3.11.
- Verwaltung über `uv`.
- Strikte Typprüfung des Anwendungscodes.
- Funktionen mit höchstens 50 Zeilen.
- Zyklomatische Komplexität höchstens 10.
- Mindestens 85% Branch-Coverage.
- Eine schnelle, offline ausführbare Testsuite mit Zeitlimit.
- Review durch ein zweites Werkzeug. [Repository-Regeln](https://github.com/ToHeinAC/claude-dev-schema/blob/main/AGENTS.md)[Projektkonfiguration](https://github.com/ToHeinAC/claude-dev-schema/blob/main/pyproject.toml)

**Wichtiger Architekturpunkt:** Langlaufende wissenschaftliche Benchmarks und echte Providerintegration passen nicht unbesehen in eine auf höchstens 60 Sekunden ausgelegte Offline-Suite.

**Empfohlene Lösung:**

- Schnelles verbindliches Standardgate beibehalten.
- Kleine deterministische Referenztests darin ausführen.
- Langlaufende Statistik-, Performance- und Integrationstests getrennt definieren.
- Diese Trennung ausdrücklich im PRD und in der CI-Konfiguration genehmigen.
- Das Hauptgate nicht stillschweigend abschwächen.

### Arbeitsaufträge klein schneiden

**Guter Arbeitsauftrag:**

> „Implementiere die kanonische Lognormalparameterisierung einschließlich Eingabemodus, Grenzfallvalidierung und Referenztests.“

**Schlechter Arbeitsauftrag:**

> „Baue den statistischen Teil der App.“

**Empfohlene Reihenfolge pro Funktion:**

1. Fachlichen Vertrag lesen.
2. Akzeptanzkriterien konkretisieren.
3. Fehlenden Test schreiben.
4. Minimal implementieren.
5. Qualitätsgate ausführen.
6. Unabhängig reviewen.
7. Dokumentation gezielt aktualisieren.
8. Kleine Änderung einchecken.

Das entspricht dem test- und zielorientierten Vorgehen deines Schemas. [Repository-Regeln](https://github.com/ToHeinAC/claude-dev-schema/blob/main/AGENTS.md)

### Übergabeauftrag an Claude

Der folgende Text eignet sich als Ausgangspunkt für die nächste Arbeitsphase:

> **Aufgabe:** Erstelle auf Basis der Erstanalyse ein präzises `PRD.md` für eine evidenzbasierte Risikomanagement-App.
>
> **Verbindliche Rahmenbedingungen:**
> - Verwende die vorhandene PRD-Vorlage und die Regeln des Repositorys.
> - Trenne Produktanforderungen, Architekturentscheidungen und Implementierungsstatus.
> - Erste Produktphase: Selbstnutzung mit vollständig durchgängigem Workflow.
> - Spätere Zielrichtung: professionell gehostetes, bezahltes Produkt.
> - Implementiere keine spätere SaaS-Funktion vorsorglich ohne gegenwärtigen Bedarf; berücksichtige jedoch frühe Daten- und Sicherheitsgrenzen.
> - Behandle Quellen, Aussagen, Annahmen, Modellstruktur und Simulationsläufe als unterschiedliche Objekte.
> - Erhalte die Trennung zwischen Szenarien und Zufallsunsicherheit innerhalb eines Szenarios.
> - Verlange mindestens Rechteck-, Dreiecks-, Normal-, Lognormal-, Beta-, Beta-PERT- und Student-t-Verteilung sowie Konstanten und Ereignisse.
> - Definiere für jede Verteilung die Eingabesemantik, kanonischen Parameter, Grenzfälle und Prüfungen.
> - Web-Recherche darf Vorschläge erzeugen, aber keine freigegebenen numerischen Annahmen automatisch ersetzen.
> - Der numerische Kern muss ohne Netzwerk, Datenbank und LLM ausführbar sein.
> - Setze zunächst eine klar begrenzte Termin-/Kostenreferenzdomäne um.
> - Formuliere überprüfbare Akzeptanzkriterien und wissenschaftliche Referenztests.
> - Kennzeichne offene Entscheidungen ausdrücklich; erfinde keine Nutzeranforderungen, Benchmarks oder Rechtsfreigaben.
> - Erstelle noch keinen Anwendungscode.
>
> **Erwartetes Ergebnis:**
> - Ein priorisiertes PRD innerhalb der Dokumentationsgrenzen.
> - Eine Meilensteinstruktur mit jeweils eindeutigen Abnahmen.
> - Eine Liste begründeter Nichtziele.
> - Eine kurze Liste noch zu treffender Produktentscheidungen.
> - Eine Zuordnung vertiefender Inhalte zu Komponentendokumenten.

***

## Produktisierung und Wirtschaftlichkeit

### Ein realistisches Differenzierungsversprechen

**Nicht behaupten:** Monte-Carlo-Simulation, Szenarioanalyse oder visuelle Einflussmodelle seien für sich neu. Analytica verbindet diese Funktionen bereits, und @RISK unterstützt unter anderem Verteilungen, Korrelationen und Sensitivitätsanalysen. [analytica](https://analytica.com/risk-uncertainty/)

**Plausible Differenzierungshypothese:**

> Eine zugängliche, projektzentrierte Anwendung, die Evidenzherkunft, Annahmenfreigabe, Szenarien und quantitative Ergebnisse in einer überprüfbaren Arbeitskette verbindet.

Diese Differenzierung ist zunächst eine **zu validierende Produkthypothese**, kein nachgewiesenes Marktmerkmal.

### Was verkauft werden könnte

**Mögliche Leistungsstufen:**

- Einzelanwender.
- Kleines Team mit Reviews.
- Organisationsversion mit Berechtigungen und Vorlagen.
- Dedizierte Installation.
- Begleitende Modellierungs- und Methodenberatung.

**Für den frühen Markttest empfehlen:**

- Zuerst wenige fachlich passende Pilotanwender.
- Wiederkehrende Problemstellungen beobachten.
- Zahlungsbereitschaft für nachvollziehbare Entscheidungen prüfen.
- Modellierungsaufwand und Supportbedarf erfassen.
- Erst anschließend öffentliche Selbstbedienung und Tarifstruktur optimieren.

### Kostenmodell statt Fantasiepreise

Die variablen Kosten sollten entlang tatsächlicher Nutzung erfasst werden:

\[
K_{\mathrm{variabel}}
=
K_{\mathrm{Simulation}}
+
K_{\mathrm{Recherche}}
+
K_{\mathrm{Dokumentenverarbeitung}}
+
K_{\mathrm{KI}}
+
K_{\mathrm{Speicherung}}
\]

**Zusätzliche Fix- und Betriebskosten:**

- Entwicklung.
- Wartung.
- Sicherheitsupdates.
- Backups.
- Monitoring.
- Support.
- Vertrags- und Datenschutzarbeit.
- Methodische Qualitätssicherung.

**Produktfolgerung:**

- Rechenlimits.
- Recherchekontingente.
- Dokumentgrößenlimits.
- Aufbewahrungsregeln.
- Transparente Verbrauchsanzeige.
- Kein unkontrolliertes „unlimited AI“.

### Kommerzielle Freigabe als eigenes Gate

Vor einem Bezahlangebot sollten mindestens nachgewiesen sein:

- Kernfunktionen fachlich geprüft.
- Isolation getestet.
- Sicherungen wiederherstellbar.
- Fehler und Abbrüche kontrolliert.
- Nutzungsgrenzen definiert.
- Kosten begrenzbar.
- Supportverantwortung geklärt.
- Lizenzprüfung abgeschlossen.
- Rechtliche Leistungsbeschreibung geprüft.
- Exporte und Kündigungsfolgen geregelt.

**Wichtig:** Ein Haftungsausschluss ersetzt keine korrekte Modellierungslogik und keinen belastbaren Betrieb.

***

## Offene Entscheidungen vor dem PRD

Die folgenden Punkte sollten im nächsten Arbeitsschritt entschieden werden, ohne die gesamte Umsetzung erneut grundsätzlich zu öffnen:

| Entscheidung | Empfohlener Ausgangspunkt |
|---|---|
| Erste Referenzdomäne | Terminplanung mit Kostenbezug |
| Erste Nutzergruppe | Eigene fachliche Nutzung |
| Erstes vollständiges Modell | Kleines reales Projekt mit klarer Entscheidungsfrage |
| Frontend | Entscheidung nach begrenztem UX-Spike |
| Erstes Deployment | Kontrollierte Einzelinstallation |
| Datenbank | PostgreSQL als einheitlicher Ausgangspunkt |
| Szenarien im ersten Release | Ein explizites Szenario; Datenmodell für mehrere |
| Abhängigkeiten im ersten Release | Gemeinsame Treiber; Unabhängigkeit ausdrücklich dokumentiert |
| Recherche | Quellenkandidaten und Befunde mit manueller Freigabe |
| KI | Optionaler Adapter, kein Bestandteil der numerischen Autorität |
| Formeleditor | Begrenzte Ausdruckssprache |
| Kalender und Ressourcen | Nur ausdrücklich spezifizierter Umfang |
| Erste Ergebnisziele | Quantile, Zielerreichung, Qualitätsstatus, Maßnahmenvergleich |
| Fremdnutzung | Erst nach separater Sicherheits- und Betriebsfreigabe |
| Normenbezug | Gesondertes Mapping vor Konformitätsaussagen |

**Der radikal andere First-Principles-Ansatz liegt damit nicht in einer neuen Simulationsformel, sondern in der Produktstruktur:** Nicht „Risiken eingeben und eine Zahl erhalten“, sondern **entscheidungsrelevante Annahmen begründen, ihre Konsequenzen modellieren und jede Ergebnisänderung bis zur zugrunde liegenden Erkenntnis zurückverfolgen können**.
