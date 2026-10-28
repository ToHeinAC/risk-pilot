## T1 – Faltung: Summe zweier Unsicherheiten

Zwei unabhängige Größen X₁, X₂ sind gleichverteilt auf [0, 1]; gesucht ist die Verteilung ihrer
Summe S = X₁ + X₂.

**Analytisch:** Die Dichte der Summe ist die Faltung der Einzeldichten – hier ein Dreieck auf
[0, 2] mit Spitze bei 1. Es gilt E[S] = 1 und Var[S] = 1/6.

**Numerische Faltung:** Dieselbe Rechnung auf einem feinen Gitter funktioniert auch für Summen
ohne geschlossene Formel; die App zeigt sie als dritte Kurve.

**Prüfung der Simulation:** Der größte Abstand zwischen simulierter und analytischer CDF
(Kolmogorov-Abstand) muss unter der DKW-Schranke ε = √(ln(2/α)/(2N)) liegen; bei N = 100 000 und
α = 0,001 ist ε ≈ 0,0062.
