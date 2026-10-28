## Ereignis-Verzweigung: Zwei Welten in einer Verteilung

**Muster:** Ein Ereignis tritt ein oder nicht und schaltet zwischen zwei Verläufen um –
Nacharbeit, ein Materialtest, der scheitert, ein verpasster Anschluss.

**Ausdruck:** `ende = where(nacharbeit, dauer + zusatz, dauer)`

**Was passiert:** Die Ergebnisverteilung ist eine Mischung aus zwei Gipfeln. Der Mittelwert
steigt um p · d, beschreibt aber keinen typischen Fall: Er liegt zwischen den Gipfeln, wo kaum
eine Iteration landet. Der Median bewegt sich viel weniger.

**Analytisch:** F(t) = (1 − p)·F₀(t) + p·F₀(t − d), Mittelwert μ + p·d.
