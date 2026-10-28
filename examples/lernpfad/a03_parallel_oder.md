## Parallel-ODER: Der Erste gewinnt

**Muster:** Redundanz – mehrere Wege führen zum Ziel, und es reicht einer: nächster Zug oder Bus,
zwei unabhängige Lieferanten, zwei konkurrierende Technologiepfade.

**Ausdruck:** `wartezeit = min(zug, bus, …)`

**Was passiert:** Das Minimum liegt früher und streut weniger als jede einzelne Alternative.
Jede zusätzliche Alternative hilft, aber mit abnehmendem Grenznutzen.

**Analytisch:** F(t) = 1 − Π(1 − Fᵢ(t)). Für exponentielle Wartezeiten addieren sich die Raten:
min(Exp(λ₁), Exp(λ₂)) = Exp(λ₁ + λ₂).

**Grenze:** Redundanz wirkt nur, solange die Alternativen nicht von derselben Ursache abhängen
(Lektion A10).
