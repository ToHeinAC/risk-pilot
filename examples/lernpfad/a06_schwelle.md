## Schwelle: Kleine Ursache, großer Sprung

**Muster:** Eine stetige Größe kippt an einer Schwelle in ein ganz anderes Ergebnis – Anschluss
erreicht oder verpasst, Grenzwert eingehalten oder nicht, Budget reicht oder nicht.

**Ausdruck:** `anschluss = verspaetung <= puffer`

**Was passiert:** Nahe der Schwelle entscheiden Minuten über eine Stunde Verspätung am Ziel. Die
Wirkung des Puffers ist stark nichtlinear: Die ersten Minuten Puffer bringen viel, weitere immer
weniger. Wer nur mit der mittleren Verspätung rechnet, sieht das nicht („Flaw of Averages“).

**Analytisch:** P(Anschluss) = p₀ + (1 − p₀)(1 − e^(−b/m)) bei Pünktlichkeit p₀, Puffer b und
mittlerer Verspätung m im unpünktlichen Fall (die mittlere Verspätung insgesamt ist (1 − p₀)·m).
