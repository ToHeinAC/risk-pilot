## T3 – Bahnreise mit Anschluss

Zug 1 ist in 60 % der Fälle pünktlich, sonst verspätet er sich um eine exponentialverteilte Zeit
mit Mittel 6 Minuten. Zum Umsteigen bleiben 7 Minuten, mindestens 2 braucht man: Bis zu
5 Minuten Verspätung (Puffer) ist der Anschluss sicher. Wird er verpasst, gilt das Frühere von
nächstem Zug (+60 min) und Bus (33 bis 40 min).

**Analytisch:** P(Anschluss) = 0,6 + 0,4 · (1 − e^(−5/6)) ≈ 82,6 %.

**Lesart:** Die Ankunftszeit hat zwei Gipfel – knapp nach Plan (Anschluss erreicht) und gut eine
halbe Stunde später (Bus). Median und häufigster Wert fallen auseinander; der Mittelwert
beschreibt keinen typischen Fall. Die Ergebnisseite weist darauf hin.

**Szenario:** „früherer Zug“ verlängert den Puffer auf 20 Minuten. Der Sweep (Seite Analyse) über
den Puffer zeigt, ab wann sich der frühere Zug lohnt.

Alle Zahlen sind illustrativ.
