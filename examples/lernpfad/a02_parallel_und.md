## Parallel-UND: Wenn alles fertig sein muss

**Muster:** Ein Ergebnis braucht mehrere Vorleistungen gleichzeitig – eine Demonstrationsanlage
wartet auf Magnete **und** Plasmaeinschluss, ein Projekt auf alle parallelen Pfade.

**Ausdruck:** `ende = max(p1, p2, …)`

**Was passiert:** Das Maximum liegt im Mittel später als jeder einzelne Pfad, obwohl jeder Pfad
im Mittel nach 10 Jahren fertig ist (*Merge-Bias*). Jeder weitere Pfad verschiebt das Ergebnis
weiter nach hinten, mit abnehmendem Zuwachs. Ein Plan, der nur die Mittelwerte der Pfade
betrachtet, ist systematisch zu optimistisch.

**Analytisch:** Für unabhängige Pfade gilt F(t) = Π Fᵢ(t), bei gleichen Pfaden Φ(t)ᵏ.

**Quellen:** Clark (1961) für den Mittelwert des Maximums; MacCrimmon & Ryavec (1964) für den
Merge-Bias in PERT-Netzplänen.
