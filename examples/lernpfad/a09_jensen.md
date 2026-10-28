## Nichtlineare Wirkung: Der Mittelwert lügt

**Muster:** Eine unsichere Größe wirkt über eine gekrümmte Kennlinie – Kosten steigen
überproportional mit dem Verzug, eine Förderkennlinie sättigt.

**Ausdruck:** `kostenfaktor = exp(verzug)`

**Was passiert:** Der Kostenfaktor beim mittleren Verzug (e¹ ≈ 2,72) ist nicht der mittlere
Kostenfaktor. Bei einer konvex gekrümmten Kennlinie liegt der Mittelwert der Wirkung darüber, und
zwar umso mehr, je größer die Unsicherheit ist. Bei Sättigung (konkav) ist es umgekehrt.

**Analytisch:** Jensen-Ungleichung f(E[X]) ≤ E[f(X)] für konvexes f; hier exakt
E[e^X] = e^(μ + σ²/2).
