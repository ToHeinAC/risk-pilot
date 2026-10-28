## T4 – Portfolio aus drei Anlagen

Aktien, Anleihen und Gold werden einmal gekauft und zehn Jahre gehalten (Buy-and-Hold). Die
Log-Rendite über die Laufzeit ist je Anlage normalverteilt: Lᵢ ~ N(T·μᵢ, T·σᵢ²). Die drei
hängen über die Korrelationsgruppe „markt“ zusammen; eingegeben wird die Rangkorrelation
(Spearman), die Copula rechnet sie in die Korrelation der Normalvariablen um
(2·sin(π·ρ/6)).

**Analytisch:** E[W] = W₀ Σ wᵢ exp(T μᵢ + T σᵢ²/2); die Standardabweichung folgt aus
Cov(e^Lᵢ, e^Lⱼ) = E[e^Lᵢ] E[e^Lⱼ] (e^(T ρᵢⱼ σᵢ σⱼ) − 1) mit der umgerechneten Korrelation.

**Lesart:** Neben Mittelwert und Quantilen zeigt die Ergebnisseite P(Verlust), Value at Risk und
Expected Shortfall (95 %) gegenüber dem Startvermögen, und die erreichten Rangkorrelationen.

**Szenarien:** „defensiv“ (andere Gewichte), „Krisenkorrelation“ (alle ρ = 0,8), „hohe
Volatilität“ (Aktien). Die Seite Vergleich zeigt sie gegen das Hauptszenario.

Alle Zahlen sind illustrativ, keine Anlageberatung.
