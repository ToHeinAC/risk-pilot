## k-von-n: Genug muss klappen

**Muster:** Von n Komponenten müssen mindestens k funktionieren – zwei von drei
Materialkandidaten, zwei von drei Pumpen, eine Mehrheit von Gutachtern.

**Ausdruck:** `erfolg = (m1 + m2 + m3) >= k`

**Was passiert:** k = 1 ist Parallel-ODER (Redundanz), k = n ist die Kette (alles muss klappen,
Lektion A8). Dazwischen reagiert das Ergebnis sehr stark auf k: Mit drei Kandidaten zu je 60 %
liegt die Erfolgswahrscheinlichkeit bei 94 %, 65 % oder 22 %, je nachdem, ob einer, zwei oder
alle drei gebraucht werden.

**Analytisch:** Bei gleichen, unabhängigen Wahrscheinlichkeiten p: Binomialverteilung,
P(X ≥ k) = Σ C(n, i) pⁱ (1 − p)ⁿ⁻ⁱ.
