## T2 – Mini-Terminplan: Serie und Parallelität

Pfad 1 besteht aus Vorgang A ~ N(10, 2²) und danach B ~ N(15, 3²); parallel läuft Pfad 2 mit
C ~ N(24, 4²). Das Projekt endet, wenn beide Pfade fertig sind: Ende = max(A + B, C).

**Analytisch:** A + B ~ N(25, 13). Für das Maximum unabhängiger Größen multiplizieren sich die
Verteilungsfunktionen: F(t) = Φ₁(t)·Φ₂(t). Der Mittelwert nach Clark (1961) ist 26,69 Tage –
deutlich mehr als der Wert 25 des längeren Pfads (**Merge-Bias**). Pfad 1 ist in 57,4 % der
Iterationen der entscheidende.

**Weiter:** Mit einem Ereignis „Nacharbeit an B“ gibt es keine geschlossene Lösung mehr – ab dann
hilft nur die Simulation (Lektion A5 im Lernpfad).

**Szenarien:** „B −3 Tage“ verkürzt Vorgang B im Mittel auf 12 Tage. Mit demselben Seed endet das
Projekt in keiner Iteration später, in vielen aber gar nicht früher – dort entscheidet Pfad 2.
„mit Nacharbeit“ setzt die Wahrscheinlichkeit der Nacharbeit an B auf 20 % (+5 Tage). Die Seite
Vergleich zeigt beides gegen das Hauptszenario.
