## Bedingte Verteilung: Eine Ursache verschiebt die Unsicherheit

**Muster:** Der Parameter einer Verteilung hängt von einer anderen Größe ab – ein Durchbruch bei
den Magneten verkürzt die erwartete Entwicklungszeit des Plasmaeinschlusses, gutes Wetter senkt
die mittlere Verspätung.

**Ausdruck:** `plasma ~ Normal(mean = basis − effekt · durchbruch, sd = 3)`

**Was passiert:** Das Ergebnis ist eine Mischung über die Ursache. Seine Streuung ist größer als
die Streuung innerhalb jedes Zweigs, weil die Unsicherheit über die Ursache hinzukommt.

**Analytisch:** Gesetz der totalen Erwartung und Varianz:
E[Y] = E[E[Y | X]] und Var[Y] = E[Var(Y | X)] + Var(E[Y | X]) = 3² + 5²·p(1 − p).
