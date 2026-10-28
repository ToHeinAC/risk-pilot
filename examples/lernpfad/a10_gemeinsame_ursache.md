## Gemeinsame Ursache: Gleichlauf ohne Absprache

**Muster:** Eine Ursache wirkt auf mehrere Größen zugleich – Wetter auf zwei Züge, eine
Lieferkette auf zwei Technologien, ein Zinsschock auf mehrere Anlagen.

**Ausdruck:** `a = 30 + anteil · wetter + ea`, `b = 25 + anteil · wetter + eb`

**Was passiert:** a und b laufen gleich, obwohl nirgends eine Korrelation eingetragen ist. Die
Summe streut stärker als bei unabhängigen Größen, weil die gemeinsame Ursache doppelt eingeht.
Redundanz (Lektion A3) verliert an Wert, wenn beide Alternativen von derselben Ursache abhängen.

**Analytisch:** Var(a + b) = Var(ea) + Var(eb) + 4·anteil²·Var(wetter).

**Quellen:** In der Zuverlässigkeitstechnik heißt das *Common-Cause Failure*; das β-Faktor-Modell
(Fleming 1974) und NUREG/CR-5485 (Mosleh et al. 1998) beschreiben, wie man es berücksichtigt.
Korrelation ohne bekanntes Wirkungsmodell (Copula) folgt mit Meilenstein M5.
