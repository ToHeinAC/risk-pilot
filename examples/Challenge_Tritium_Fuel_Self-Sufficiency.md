# Nuclear Fusion — Deep Dive: Challenge 3
## Tritium Fuel Self-Sufficiency

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — June 2026; reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps gate TR to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

Tritium fuel self-sufficiency is widely regarded as the most underappreciated systemic risk in the fusion development programme. Unlike plasma stability or materials damage — problems that can be tested incrementally in sub-scale experiments — the tritium challenge is deeply systemic: it can only be resolved in an integrated operating fusion power plant, which does not yet exist. The core arithmetic is unforgiving: each DT fusion reaction produces exactly one 14.1 MeV neutron, and that single neutron must simultaneously breed one replacement tritium atom, maintain enough surplus to supply start-up inventory for future reactors, and survive absorption losses to structural materials, coolants, and port penetrations.[^1][^2]

A comprehensive 2021 analysis by Abdou et al. (Nuclear Fusion 61, 013001) — the most authoritative systematic study of this challenge — concluded that **current physics and technology are insufficient to guarantee tritium self-sufficiency or to provide the required start-up inventories** for DEMO and power plants. This is not a fringe finding; it is the consensus of four decades of fusion fuel-cycle analysis, repeatedly confirmed and never resolved. The global civil tritium stockpile is approximately 25–30 kg, the vast majority held in Canada as a fission by-product; prices range from $30,000–$40,000 per gram; tritium decays at 5.47% per year with a 12.3-year half-life; and by the time ITER begins DT operations in 2039 (Baseline 2024), roughly half of today's stockpile will have decayed at 5.47 % per year **[corr. 2026-11]** (was: "mid-2030s", "decayed below usable concentrations" — decay reduces the quantity, not the usability of the remaining tritium).[^3][^4][^5][^6]

This report provides a deep-dive analysis of six interconnected sub-challenges: (1) the global tritium supply crisis and ITER consumption timeline; (2) the required vs. achievable Tritium Breeding Ratio; (3) the start-up inventory problem; (4) the tritium burn fraction and fuel cycle efficiency; (5) tritium permeation, retention, and accountancy; and (6) breeding blanket technology and ICF-specific complications.

***

## Part I — The Global Tritium Supply Crisis

### 1.1 Where Tritium Comes From Today

Tritium does not occur in nature in meaningful quantities: its 12.3-year half-life means that any primordial tritium has long since decayed. The only current commercial-scale production route is neutron capture on deuterium in CANDU (Canada Deuterium Uranium) heavy-water reactors, in which D\(_2\)O moderator absorbs neutrons via the reaction:[^4]

\[^2\text{D} + n \rightarrow ^3\text{T} + \gamma\]

The accumulated tritium is then extracted from the heavy water in dedicated Tritium Removal Facilities. Canada hosts the majority of operating CANDU reactors and holds the dominant share of the global civil stockpile, giving it a geopolitically significant monopoly on fusion fuel supply. Romania signed a $200 million contract in 2024 to build the first European tritium extraction facility for its own CANDU plant.[^7][^3]

Current global civil tritium inventory estimates range from **25–30 kg**. The price has stabilized at approximately **$30,000–$40,000 per gram**, a direct consequence of limited supply and growing fusion R&D demand. For context, a single 1 GW fusion power plant burns approximately **55.6 kg of tritium per full power year (fpy)**, which is roughly **twice the entire global civil stockpile — consumed in one year of operation**.[^8][^9][^3]

### 1.2 The ITER Consumption Timeline

ITER will begin DT plasma operations in 2039 under Baseline 2024 **[corr. 2026-11]** (was: "approximately 2035–2036"). During its DT phase, ITER will burn approximately **0.9 kg of tritium per full power year**. Over its operational lifetime (roughly 16 years of mixed D and DT operation), ITER will consume on the order of **5–10 kg of tritium**. Since ITER does not breed its own tritium — its design does not include a tritium breeding blanket capable of net production — this tritium must come from the global stockpile.[^10][^5]

The alarming implication, identified by Abdou, is as follows: **By the time ITER completes its DT programme, there may be no external non-fusion tritium supply left to provide start-up inventory for any subsequent major DT fusion facility.** The tritium that existed at the beginning of ITER's design phase has already decayed; what remains from today's stockpile will have further decayed by the 2040s. The Abdou analysis concluded that any DT fusion demonstration device built after ITER must either:[^5]
1. Operate at very low fusion power (<150 MW) to minimize tritium consumption and keep start-up requirements small enough to be obtainable, or[^11][^5]
2. Include a preceding Fusion Nuclear Science Facility (FNSF) device that produces excess tritium over time to supply DEMO's start-up inventory[^5]

Canada's commitment to refurbishing its CANDU fleet through the 2070s provides some relief — those reactors will continue producing tritium — but at rates insufficient to simultaneously supply multiple DEMO-class devices in parallel. A 2025 analysis from UKAEA confirmed that if multiple DEMO-class devices (EU DEMO, CFETR, etc.) are built in parallel in the 2050s, they could collectively require **several kilograms of tritium each**, creating a severe supply crunch.[^3][^10]

***

## Part II — The Tritium Breeding Ratio: Required vs. Achievable

### 2.1 Fundamental Physics of Tritium Breeding

All near-term fusion power plant designs will rely on breeding tritium in a **lithium-containing blanket** that surrounds the plasma. Fusion neutrons are absorbed by lithium via two reactions:[^2][^12]

\[^6\text{Li} + n \rightarrow ^3\text{T} + ^4\text{He} + 4.8 \text{ MeV}\]
\[^7\text{Li} + n \rightarrow ^3\text{T} + ^4\text{He} + n' - 2.5 \text{ MeV}\]

The \(^6\)Li reaction is exothermic and has a high cross-section for thermal neutrons; natural lithium is only 7.5% \(^6\)Li, so enrichment to 30–90% is used in most blanket designs to raise the breeding rate. The \(^7\)Li reaction is endothermic and requires a fast neutron above ~3 MeV, but it produces an additional fast neutron, contributing to the **neutron economy**. The key figure of merit is the **Tritium Breeding Ratio (TBR)** — the number of tritium atoms produced per tritium atom burned.[^13][^12]

The minimum required net TBR for a self-sufficient fusion power plant is mathematically:

\[\text{TBR}_{required} = 1 + \frac{\eta_T}{\eta_{burn}} + \frac{\eta_P}{\eta_{burn}} + \frac{Q_T^{decay}}{T_{burn}}\]

where \(\eta_T\) is the fractional T retention in materials, \(\eta_P\) is process loss, and the decay term accounts for radioactive losses during storage and processing. Engineering studies consistently find that the minimum viable net TBR is approximately **1.05–1.15** to account for realistic permeation, retention, and reserve requirements.[^14][^15][^16][^1]

A net TBR below 1.0 means the reactor burns more tritium than it produces — a terminal condition for sustained operation.

### 2.2 Why TBR > 1 Is Structurally Difficult

The irreducible constraint is that each DT fusion event produces exactly **one neutron**. The blanket must use this neutron to:
- Breed one new tritium atom (TBR contribution = 1.0 is the absolute ceiling from direct \(^6\)Li capture)
- Overcome structural and coolant parasitic absorption
- Compensate for geometric coverage losses from port penetrations

**Neutron parasitic losses** are the primary TBR killer. Every structural material in the neutron path — steel, tungsten, beryllium — has a finite absorption cross-section. Neutron transport calculations for realistic DEMO blanket designs with EUROFER structural steel, beryllium neutron multiplier, and Li\(_6\)SiO\(_4\) solid breeder pebble beds (HCPB concept) yield TBR values in the range **1.10–1.18** in idealized 1D calculations, dropping to **1.03–1.08** in full 3D calculations that correctly account for:[^17][^18]
- Port penetrations for heating systems, diagnostics, fueling, and vacuum pumping
- Structural ribs, cooling channels, manifolds, and weld reinforcements
- First-wall armor layer absorption
- Neutron streaming through gaps between blanket modules

**Geometric coverage** is a particularly severe constraint. In ITER-scale tokamaks, the first wall surface area is roughly 700–800 m², but ports (equatorial, upper, lower), supporting structures, and the divertor account for 20–30% of the total area. Every uncovered area is a neutron leak. Analysis of EU DEMO finds that the TBR drops by **~0.04–0.06 per 1% decrease in blanket coverage**, meaning that recovering the 15–20% port coverage fraction requires achieving TBR > 1.2 in the blanketed regions just to maintain net TBR > 1.05 overall.[^18]

**Neutron multipliers** are the primary strategy to overcome the one-neutron-per-reaction ceiling. Beryllium (via \(^9\)Be(n,2n)) and lead (via \(^{208}\)Pb(n,2n)) can each produce 1.5–2.0 neutrons per fast neutron above ~5 MeV, effectively amplifying the neutron flux available for breeding. However:[^13][^2]
- Beryllium is expensive (~$900/kg), globally scarce, and highly toxic; its supply chain for reactor-scale use is unconfirmed
- Lead has a lower multiplication cross-section than Be, generates radioactive \(^{210}\)Pb and \(^{210}\)Bi in the blanket, and in liquid form (LiPb) creates magnetohydrodynamic (MHD) flow challenges
- At the 14 MeV neutron energies from fusion, **both Be and Pb have (n,2n) thresholds** well below the peak neutron energy, but there is a reduction in the available multiplication factor at high neutron fluences due to transmutation[^18]

### 2.3 Achievable TBR: The 3D Reality

The gap between 1D and full-3D TBR estimates is systematically large and consistently unfavorable:

| Blanket Concept | 1D TBR (ideal) | 3D TBR (realistic) | Key Degradation Source |
|---|---|---|---|
| HCPB (He-cooled pebble bed) | ~1.18–1.22[^18] | ~1.06–1.10[^18] | Port area, radial ribs |
| WCLL (water-cooled lithium lead) | ~1.14–1.18[^18] | ~1.03–1.08[^18] | Be elimination, port area |
| DCLL (dual-coolant lithium lead) | ~1.16–1.20[^18] | ~1.05–1.09[^18] | MHD flow channel inserts |
| ICF spherical blanket | ~1.10–1.15[^19] | ~0.95–1.05[^19] | Laser beam ports dominate |

The consistently narrow margin between achievable 3D TBR and required net TBR implies that any unforeseen design change — adding a diagnostic port, increasing a structural rib thickness, changing a coolant manifold geometry — can push the TBR below the self-sufficiency threshold. This fragility is not an artifact of crude calculations; it reflects the fundamental one-neutron constraint of DT fusion physics.

***

## Part III — The Start-Up Inventory Problem

### 3.1 How Much Tritium Does a New Plant Need?

Before a fusion power plant can begin DT operation, it must be loaded with a **start-up inventory** of tritium sufficient to:
1. Fill the fueling system, storage beds, and isotope separation plant with operating tritium reserves
2. Maintain a minimum burn inventory in the plasma for the ignition phase
3. Cover losses during initial operation and commissioning while the breeding blanket is not yet at full performance
4. Provide a **reserve inventory** (safety stock for unexpected shutdowns, maintenance periods, and tritium decay during outages)

Estimates of the required start-up inventory in the literature span a wide range:
- A baseline 500 MW fusion reactor start-up calculation: **~327 grams** for basic operation, **~642 grams** including 24-hour reserve inventory[^20]
- EU DEMO operating at ~2 GW fusion power: **3–10 kg**, with the range driven by assumptions about burn fraction, blanket TBR, and commissioning duration[^10][^11][^8]
- The Abdou comprehensive analysis finds that for large DT plants, start-up inventory of **tens of kilograms** may be required when reserve tritium (for long maintenance outages) is included, nearly equal to the entire global stockpile[^15][^5]
- Commonwealth Fusion Systems' ARC pilot plant, by contrast, claims a maximum in-plant tritium inventory of only **90 grams** by using compact design and minimizing in-vessel retention[^9]

The dramatic spread — from 90 grams to tens of kilograms — reflects genuine design choices and assumptions about tritium burn fraction, inventory turnover time, and acceptable reserve margins. The low-end estimates from compact pilot plants rely on aggressive assumptions (high burn fraction >5%, low retention) that have not been experimentally validated. The high-end estimates correspond to conventional large-scale DEMO-class designs with conservative engineering margins.

### 3.2 The Tritium Doubling Time

A self-sufficient fusion power plant that produces excess tritium (TBR > 1 + margins) can supply start-up inventory for future plants. The **tritium doubling time** \(\tau_d\) is the time for the plant's tritium inventory to double through breeding, accounting for decay and internal consumption:

\[\tau_d = \frac{I_0 \ln 2}{\dot{T}_{excess} - \lambda I_0}\]

where \(I_0\) is the operating inventory, \(\dot{T}_{excess}\) is the excess breeding rate, and \(\lambda = \ln 2 / 12.3\) yr\(^{-1}\) is the decay constant.[^21][^2]

For a 1 GW fusion power plant with TBR = 1.10 and a tritium start-up inventory of 5 kg, a typical doubling time is **10–25 years** — depending on burn fraction, availability factor, and reserve margins. This is deeply problematic for fleet deployment: if the first plant takes 15 years to accumulate enough tritium to start the second plant, a fleet of 100 reactors could not be deployed within a human generation from the first-of-kind plant, even if all engineering challenges were resolved simultaneously.[^22][^2][^21][^5]

The Wisconsin ARIES studies quantified this explicitly: achieving a tritium doubling time short enough to enable rapid fleet deployment requires simultaneously achieving:[^2][^22]
- TBR > 1.10 (at the high end of what 3D calculations suggest is achievable)
- Tritium burn fraction > 3–5% (undemonstrated at reactor scale)
- Overall availability factor > 50% (well above current best estimates for DEMO RAMI)
- Start-up inventory < 5 kg (requires compact designs with aggressive tritium management)

The probability of achieving all four simultaneously by first-of-kind operation is essentially unknown and has never been empirically bounded.

***

## Part IV — Tritium Burn Fraction and the Fuel Cycle

### 4.1 The 1% Burn Fraction Problem

In a DT plasma, the fraction of injected tritium that actually undergoes fusion in a single pass through the plasma — the **burn fraction** — is determined by the ratio of the fusion reaction rate to the particle confinement time. In ITER, the effective burn fraction is estimated at only **~1%**. This means that for every 100 T atoms injected into the plasma, 99 are pumped out through the divertor as unburned exhaust.[^23]

The implication for the fuel cycle is dramatic: in a 3 GW thermal fusion plant burning ~450 g T/day, the main fuel processing loop must handle at least **9 kg of DT per day** (exhaust + burn fraction) — more than 30% of the global tritium stockpile flowing through the plant **every single day**. The isotope separation system, tritium accounting, and storage systems must process this at:[^24]
- Isotopic purity requirements of >99.9% D:T ratio for injection
- Tritium recovery efficiency from exhaust of >99.9% (losses at even 0.1% per pass would accumulate to unacceptable inventory losses and environmental releases)
- Cryogenic distillation at 21–26 K for hydrogen isotopologue separation[^25]

No facility capable of demonstrating this full closed-loop cycle at any scale exists today. The UKAEA-Eni H3AT Tritium Loop Facility at Culham, announced in 2025 and due for completion in 2028–2030, is designed to demonstrate a closed loop continuous flow system at **1/20th pilot plant scale with a 100 g tritium inventory**. It will be the first facility of its kind in the world — a landmark but still far below reactor scale.[^26][^25]

### 4.2 Burn Fraction Physics and Tritium Confinement Time

The tritium burn fraction is related to the tritium confinement time \(\tau_T\) and energy confinement time \(\tau_E\) by:[^27]

\[f_{tb} \propto \frac{\tau_T}{\tau_E}\]

In tokamaks and stellarators, \(\tau_T / \tau_E\) is not well characterized and can vary significantly based on fueling location, recycling, and turbulent transport. If \(\tau_T \gg \tau_E\), tritium accumulates in the plasma (problematic for helium ash buildup and fuel dilution); if \(\tau_T \ll \tau_E\), burn fraction is low (high fuel cycle throughput).[^27]

Raising the burn fraction from 1% to, say, 5% would reduce fuel cycle throughput by 5×, dramatically easing isotope separation requirements and reducing tritium inventory. However, the confinement time ratio \(\tau_T / \tau_E\) is determined by plasma transport physics that is not independently controllable — it is a consequence of the same turbulence that determines energy confinement. There is no demonstrated mechanism to specifically increase tritium confinement time without also increasing helium ash retention, which would lead to plasma dilution. The 1% burn fraction constraint is, for current designs, essentially inescapable.[^23][^27]

Alternative approaches — **asymmetric DT pumping** (preferentially pumping T over D in the scrape-off layer) and **tritium-lean plasma operation** (deuterium-rich mixtures) — have been proposed to reduce tritium throughput, but these approaches require either reduced DT fusion rate (lowering power) or fundamental changes to divertor geometry that have not been demonstrated at reactor scale.[^28]

***

## Part V — Tritium Permeation, Retention, and Accountancy

### 5.1 Tritium Permeation Through Structural Materials

Tritium generated in the breeding blanket exists initially as dissolved atoms in the breeder material (Li ceramic or LiPb alloy) at temperatures of 300–700 °C. It must migrate to extraction points without permeating through the structural steel walls into the coolant. Tritium permeation through steel is a significant challenge because:[^29][^30][^31]
- Hydrogen isotopes are highly permeable through steel at elevated temperatures, following an Arrhenius dependence: permeation flux \(J \propto \exp(-E_a / k_B T)\) with activation energies of ~0.5–0.7 eV
- Even small temperature non-uniformities create permeation hotspots
- Tritiated water in the coolant (HTO, DTO) creates a safety issue (secondary containment contamination) and a tritium accountancy problem

Strategies to limit permeation include:[^30]
- **Al\(_2\)O\(_3\) or Cr\(_2\)O\(_3\) permeation barriers**: oxide coatings that reduce hydrogen permeability by factors of 10\(^2\)–10\(^4\); however, they crack under thermal cycling and neutron irradiation, and their long-term effectiveness in fusion conditions is unvalidated
- **Hydrogen (protium) addition to the purge gas**: raising the H partial pressure reduces the net T permeation driving force via isotopic dilution; the tradeoff is increased isotope separation burden
- **Conversion to tritiated water** (catalytic oxidation + adsorption) as a trapping mechanism in the breeder coolant loop, with subsequent CECE (Combined Electrolysis and Catalytic Exchange) recovery

A critical sensitivity analysis from Abdou: if tritium permeation losses are **0.1% per day** of the circulating inventory, and the circulating inventory is ~9 kg/day, then permeation losses of ~9 g/day accumulate to **3.3 kg/year** — comparable to the entire annual CANDU production capacity. The system requires permeation losses below ~**0.001% per pass** to be manageable, a standard that has not been demonstrated in any integrated facility.[^6][^2]

### 5.2 Tritium Retention in the First Wall and Plasma-Facing Components

As analyzed in Challenge 2, tritium implanted in the plasma-facing first wall creates an inventory that grows over time due to neutron-irradiation-induced trap sites. For a DEMO-class machine with a tungsten first wall:[^32][^33]
- Steady-state tritium inventory in plasma-facing tungsten is dominated by deep-layer retention in the large temperature gradient region near the back of the monoblocks[^32]
- Retention can be reduced by maintaining wall temperatures above ~700 K (thermal detrapping), but this requires operating at baking temperatures that may be incompatible with simultaneous plasma operation
- The regulatory limit for in-vessel tritium inventory in ITER is **700 g**; exceeding this threshold triggers mandatory operational restrictions. For DEMO at 10× higher neutron flux, similar constraints will exist with potentially stricter limits[^34]

### 5.3 Tritium Accountancy: The Measurement Problem

A fusion power plant with a 9 kg/day tritium throughput must track its inventory to within **~1 gram accuracy** to:[^35][^24]
- Satisfy regulatory requirements (material control and accountancy for nuclear material)
- Optimize fuel injection (D:T ratio control in the plasma for optimal fusion performance)
- Detect abnormal leaks or retention before safety limits are breached
- Verify breeding blanket performance against the design TBR

Current tritium accountancy techniques — ionization chambers, calorimetry, mass spectrometry, beta-ray detection — have measurement uncertainties of ~**0.1–1%** on bulk quantities. For a 9 kg/day throughput, a 0.1% uncertainty corresponds to ~9 g/day accumulation in the "unaccounted for" category. Over a year, this sums to ~3 kg — comparable to the start-up inventory of a small fusion pilot plant.[^34][^35]

This is not a hypothetical concern. Nuclear regulatory bodies require that **tritium material unaccounted for (MUF)** does not exceed specific limits; if the natural measurement uncertainty alone exceeds these limits, the plant cannot legally operate. Building tritium accountancy systems with the required sub-gram accuracy at throughputs of thousands of grams per day represents a measurement technology challenge that has received insufficient attention in the fusion community.[^24][^6]

***

## Part VI — Breeding Blanket Technology and ICF Complications

### 6.1 Major Blanket Concept Classes

Four main breeding blanket concepts are being developed for tokamak/stellarator fusion:[^36][^18]

**Helium-Cooled Pebble Bed (HCPB)**:
- Solid Li\(_4\)SiO\(_4\) or Li\(_2\)TiO\(_3\) ceramic pebbles as breeder, beryllium pebbles as neutron multiplier
- Helium gas coolant at 8 MPa and 300–500 °C
- Tritium extracted by purge-gas sweeping (He + 0.1% H\(_2\)) of the pebble bed
- Tritium release kinetics from ceramics is strongly temperature-dependent: below 400 °C, T release rates drop precipitously, creating inventory retention problems[^37][^38]
- **ITER TBM**: EU HCPB and WCLL Test Blanket Modules are scheduled for ITER integration[^17]

**Water-Cooled Lithium Lead (WCLL)**:
- Liquid Pb-15.7Li alloy as both breeder and neutron multiplier (no separate Be multiplier needed)
- Water coolant at 15.5 MPa and 285–325 °C — familiar technology from fission, but creates tritium permeation into water stream
- Continuous tritium extraction from flowing LiPb using vacuum permeator or cold-trap methods
- MHD pressure drop from LiPb flow in magnetic field requires non-conducting flow channel inserts (FCIs)[^39]

**Dual-Coolant Lithium Lead (DCLL)**:
- LiPb as both breeder and self-cooled primary coolant; He for cooling of FCI and first wall
- Higher operating temperatures (up to 700 °C for LiPb) enables higher Carnot efficiency
- Requires advanced FCI materials (SiC/SiC) that are still at TRL 3–4[^39]

**Liquid Immersion Blanket (LIB) / FLiBe**:
- Fluoride salt (FLiBe: LiF-BeF\(_2\)) as both breeder and neutron moderator, surrounding the plasma chamber
- Online tritium extraction via sparging or vacuum degassing
- Very low in-vessel T inventory possible; actively pursued by some private fusion companies (CFS ARC)[^40]
- LIB is at TRL 2–3; no reactor-scale engineering data exist

### 6.2 Solid vs. Liquid Breeder Trade-offs

| Parameter | Solid Breeder (HCPB) | Liquid Breeder (WCLL/DCLL) | Liquid Immersion (FLiBe) |
|---|---|---|---|
| T extraction | Slow (pebble-bed purge) | Continuous (flow extraction) | Continuous (online) |
| In-vessel T inventory | Moderate (kg-scale, pebbles) | Low (extracted continuously) | Very low (mg to g scale)[^40] |
| Structural complexity | Moderate | High (MHD, FCI) | Moderate |
| Neutron multiplier | Required (Be) | Not needed (Pb in LiPb) | Not needed (Be in FLiBe) |
| T permeation risk | Moderate (purge gas capture) | High (into water coolant) | Moderate (into salt coolant) |
| Temperature window | 350–600 °C | 285–700 °C (wide) | 450–700 °C |
| Maturity | TRL 4–5 | TRL 4–5 | TRL 2–3 |

A fundamental limitation of all solid breeder concepts is the **slow tritium release kinetics at low temperatures**. Tritium diffuses through Li\(_4\)SiO\(_4\) or Li\(_2\)TiO\(_3\) crystals via an interstitial mechanism whose rate falls exponentially below 500 °C. If the purge-gas extraction temperature is too low, tritium accumulates in the pebble bed for weeks or months before being swept out — a safety concern (inventory at risk) and an accountability problem. Experimental T release data at ITER-relevant conditions remain sparse.[^38][^37]

### 6.3 ITER Test Blanket Module Programme

ITER's Test Blanket Module (TBM) programme is the only planned near-term test of breeding blanket concepts in a tokamak environment. EU, China, Japan, South Korea, India, and Russia have all developed TBM concepts. The EU HCPB and WCLL TBMs will be integrated into equatorial port 18 of ITER, occupying a total first-wall area of ~2.8 m² each.[^41][^17]

However, the TBM programme faces a fundamental limitation: ITER is not a DT breeding reactor. The TBM test area (~1–3% of total first-wall area) will produce only a tiny fraction of the neutron flux needed for meaningful breeding data. The TBMs will generate at most ~0.01–0.05 kg of tritium per year — five orders of magnitude less than a power reactor. Their primary value is in demonstrating tritium extraction system integration, activation analysis, and materials performance under fusion neutron bombardment, not in validating full-scale TBR under realistic conditions.[^41][^18]

### 6.4 ICF-Specific Tritium Challenges

Laser ICF imposes a uniquely severe version of the tritium challenge, for several interconnected reasons:[^19][^42][^43]

**Target filling**: Each ICF target contains a **cryogenic DT ice layer** approximately 70–90 µm thick on the inner surface of the 1–2 mm diameter capsule. Filling the capsule requires diffusing DT gas through the capsule wall at high pressure (several hundred bar), then slowly cooling to ~18 K to form a uniform DT ice layer — a process that takes **several days per target**. A power plant needing 500,000 targets per day requires a factory that can fill, layer, and characterize targets in **parallel across thousands of stations** running continuously.

**In-plant tritium inventory**: Even at optimistic fill rates, the total tritium at risk in the target factory and associated storage at any given moment is estimated at **10–20 kg** — more than half the entire global civil stockpile. A tritium containment failure in the target factory would be a major radiological event.[^19]

**Blanket geometry**: ICF chamber geometry requires laser beam ports (typically 48–96 ports for direct drive, or 2 holes plus laser-entry ports for indirect drive) to penetrate the lithium blanket. These ports reduce the effective blanket coverage area, directly reducing TBR. Analysis consistently shows that ICF blanket TBR is **0.05–0.15 lower** than for the equivalent MCF blanket geometry — potentially placing net ICF TBR below 1.0 even in favorable designs.[^19]

**Fuel processing cycle time**: ICF targets cannot be refueled like MCF plasmas. A target is destroyed in a microexplosion and the DT exhaust from the target and chamber must be recaptured, processed through the tritium plant, and incorporated into new target fills. The fuel cycle has a minimum time constant set by target fabrication — potentially days to weeks per cycle — introducing a large tritium inventory buffer requirement that makes ICF even more sensitive to the start-up inventory problem.[^43]

***

## Part VII — The Missing Facility: FNSF and the Pathway to Self-Sufficiency

### 7.1 The Argument for a Fusion Nuclear Science Facility (FNSF)

Mohamed Abdou's 2021–2022 comprehensive analysis argues, supported by four decades of consistent technical studies, that no amount of non-fusion laboratory testing can substitute for testing breeding blankets in an actual fusion nuclear environment. The reason is the **synergistic and integrated nature** of the tritium challenge: tritium release kinetics, permeation, retention, accountancy, and MHD effects all interact in ways that cannot be predicted from separate-effect experiments. The behavior of a breeding blanket at steady state under simultaneous fusion neutron flux, plasma thermal loads, and cyclic thermal stress is qualitatively different from any lab simulation.[^6][^5]

Abdou's proposed pathway:[^5]
1. Build a **Fusion Nuclear Science Facility** (FNSF) — a small tokamak or stellarator with 0.5–1 MW m\(^{-2}\) neutron wall loading on 10–20 m² of test area, Q ≈ 1–3, operating at low fusion power (<150 MW) to limit tritium consumption
2. FNSF Stage I (5–10 years): demonstrate scientific feasibility of blanket functions under real fusion environment; discover synergistic phenomena
3. FNSF Stage II (5–10 years): demonstrate engineering feasibility (blanket module reliability, tritium extraction at continuous operation)
4. FNSF Stage III: produce excess tritium to accumulate start-up inventory for DEMO; demonstrate availability approaching 30%
5. Only then build DEMO with confidence in TBR achievement and RAMI performance

No such facility exists today, and none is formally funded for construction in any country as of 2026. China's BEST (Blanket/first-wall Engineering and Science Testing) facility and EU's proposed FTQP (Fusion Technology Qualifying Platform) are conceptually advanced but not yet approved. The absence of the FNSF represents what Abdou calls a "missing step" that makes the entire development pathway to DEMO uncertain at a fundamental level.[^5]

### 7.2 H3AT and Other Near-Term Facilities

The UKAEA-Eni **H3AT Tritium Loop Facility** at Culham is the most significant near-term tritium technology development investment. Announced in 2025 and scheduled for completion by 2028–2030:[^25][^26]
- **Scale**: 100 g tritium inventory — 1/20th pilot plant scale
- **Scope**: demonstrates closed-loop continuous flow fuel cycle; tests palladium membrane reactors for tritium recovery from exhaust; demonstrates cryogenic isotope separation at 21–26 K; validates fuel cycle models
- **Partners**: Eni (private sector), ITER Organization, Atkins/Raelis[^25]
- **Limitation**: operates without a fusion neutron source — cannot test tritium breeding, only the non-breeding fuel cycle subsystems

At ITER itself, the tritium plant includes a closed-loop system capable of processing the ~1% ITER burn fraction exhaust. ITER will be the first integrated test of a multi-kg tritium fuel cycle in a tokamak, but again without blanket breeding. Lessons from ITER's tritium plant operation (likely 2035–2050) will be invaluable but arrive too late to inform DEMO design, which must be frozen years earlier.[^6][^5]

***

## Part VIII — Technology Readiness and Cross-Pathway Comparison

### 8.1 Technology Readiness by Sub-Challenge

| Sub-challenge | Status (2026) | TRL | Key Bottleneck |
|---|---|---|---|
| Lithium breeding reaction (physics) | Proven | 9 | None — physics is settled |
| TBR in 1D/2D blanket design | Well-characterized | 6 | Gap to 3D realistic TBR |
| TBR in 3D integrated design | Partially characterized | 4 | Port coverage, streaming |
| Solid breeder T release kinetics | Lab-scale data only | 4 | No fusion-flux irradiation data |
| Liquid breeder T extraction | Concept tested, no fusion demo | 3–4 | MHD flows, permeation |
| Closed fuel cycle (non-breeding) | ITER plant ~2039 (DT start) **[corr. 2026-11]**; H3AT ~2030 | 4–5 | Scale, closed-loop integration |
| Permeation barriers (structural) | Proof-of-concept only | 3 | Irradiation stability under neutrons |
| Tritium accountancy at reactor scale | Unresolved | 2–3 | Measurement precision at high throughput |
| ICF target filling at rep-rate | Nonexistent | 1–2 | Factory concept undemonstrated |
| In-fusion-environment blanket test | Nonexistent | — | FNSF does not exist |

### 8.2 Pathway Comparison

| Challenge Element | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Blanket geometry | Axisymmetric; good coverage[^18] | 3D; ~20–30% area penalty from coils; harder to meet TBR[^44] | 20–40% coverage loss from beam ports; may be below TBR = 1 in some designs[^19] |
| Blanket T extraction | Standard purge or flow; continuous option available | Same physics, harder geometry | Requires mass batch process; days-long cycle time[^43] |
| In-plant T inventory risk | Moderate (~kg scale) | Moderate | Very high (~10–20 kg in target factory)[^19] |
| T start-up inventory need | 0.3–20 kg depending on design[^20][^8] | Similar to tokamak | Large; add target-factory pre-fill inventory |
| Supply gap severity | Severe; ITER consumes bulk of stockpile | Same | Severe + geometry penalty |

***

## Part IX — Open Research Questions and Analysis Entry Points

### TBR and Blanket Physics

- **Q1.1**: What is the statistically bounded range of achievable 3D TBR in a realistic EU DEMO HCPB or WCLL design, accounting for all port penetrations, manifolds, and structural elements? What is the probability that TBR > 1.05 at the 90% confidence level?
- **Q1.2**: Can compact tokamak designs (smaller aspect ratio, higher field) achieve better blanket coverage fractions than conventional designs, and does this translate into meaningfully higher TBR margins?
- **Q1.3**: What beryllium supply chain and production capacity would be required for a fleet of 100 HCPB-blanket fusion power plants, and is this compatible with known global Be reserves?

### Tritium Extraction and Processing

- **Q2.1**: What is the temperature-dependent tritium release rate from Li\(_4\)SiO\(_4\) and Li\(_2\)TiO\(_3\) pebbles under simultaneous fusion neutron irradiation (with He cogeneration) and tritium implantation? Does neutron damage increase or decrease T release kinetics?
- **Q2.2**: Can online tritium extraction from LiPb at fusion-relevant flow rates and magnetic fields achieve permeation losses below 0.001% per pass through a steel heat exchanger, even with degraded Al\(_2\)O\(_3\) permeation barriers?
- **Q2.3**: What closed-loop fuel cycle architecture minimizes in-plant tritium inventory for a DEMO-class plant, and what is the achievable minimum start-up inventory under optimistic but physically consistent assumptions?

### Accountancy and Regulatory Framework

- **Q3.1**: What tritium accountancy measurement techniques can achieve sub-gram precision at throughputs of >1,000 g/day? Is this compatible with online non-destructive measurement, or does it require periodic destructive sampling (which introduces safety and scheduling constraints)?
- **Q3.2**: What regulatory framework will govern tritium material unaccounted for (MUF) limits for fusion power plants, and are existing nuclear material control standards (e.g., IAEA safeguards) applicable to fusion's DT fuel cycle?

### Supply and Fleet Deployment

- **Q4.1**: What is the minimum tritium start-up inventory for the first-of-kind commercial fusion power plant under the most optimistic credible assumptions (compact design, high burn fraction, low retention), and is it obtainable from CANDU production after ITER consumption?
- **Q4.2**: Is a dedicated fission reactor purpose-built for tritium production (e.g., a tritium-producing burnable absorber rod (TPBAR) light water reactor) economically justified as a bridge technology for fusion fleet deployment?
- **Q4.3**: What is the minimum TBR excess above 1.0 needed to achieve a tritium doubling time short enough (<10 years) to enable fleet deployment on a commercially relevant timeline?

### ICF-Specific Questions

- **Q5.1**: Can a continuous-flow IFE target filling and layering system be demonstrated at 1–10 Hz rep-rate with DT ice uniformity within ±1 µm RMS, and what in-plant tritium inventory does this system require?
- **Q5.2**: What first-wall geometry for an IFE chamber (spherical vs. cylindrical, dry vs. wetted wall) maximizes blanket coverage fraction while accommodating laser beam propagation requirements, and what is the maximum achievable TBR for the optimal geometry?

***

## Conclusion

The tritium self-sufficiency challenge is unique among fusion's technical obstacles in that it cannot be partially solved or incrementally demonstrated — it requires an integrated operating fusion power plant producing, circulating, breeding, and accounting for tritium in real time. Every other challenge in the list allows at least partial experimental validation in sub-scale or non-burning experiments; tritium self-sufficiency does not.

The most alarming finding from four decades of systematic analysis — confirmed by the most comprehensive recent study — is that current physics and technology are insufficient to guarantee self-sufficiency or to provide the required start-up inventories at DEMO scale. This is not a problem that more research alone can resolve; it requires the construction of a Fusion Nuclear Science Facility in which blankets can be tested in the real fusion environment at sustained neutron wall loadings. Without this missing step, the path from ITER to DEMO to power plant is built on extrapolation of uncertain models across the most operationally critical subsystem in the entire fusion energy concept.[^6][^5]

The tritium supply geopolitics also deserve serious strategic attention: Canada's CANDU fleet is currently the only viable source of tritium at meaningful scale, and its availability for fusion is not guaranteed. A global fusion programme that reaches 10+ simultaneous DT facilities in the 2050s — with each needing kilograms of tritium for start-up — will face a supply crunch that no amount of improved blanket physics can resolve if the infrastructure for breeding and fuel cycling is not demonstrated well in advance.[^3]

---

## Review & Model Update (November 2026)

Scope and model architecture are described in the overview report. This section covers gate **TR** (tritium
self-sufficiency) and the common tritium show-stopper.

### R.1 Currency and claim check

| ID | Location | Statement | Finding | Status |
|---|---|---|---|---|
| C3-01 | Executive summary, Part I | ITER DT "mid-2030s" / "2035–2036" | Baseline 2024: DT from 2039 [R1] | corrected |
| C3-02 | Executive summary | Stockpile "decayed below usable concentrations" | Overstated. About half of today's inventory remains by 2039 (5.47 %/y) | corrected |
| C3-03 | Part I | Stockpile 25–30 kg | Inconsistent with the overview (22 kg); both are estimates. The overview now cites 20–30 kg | harmonised |
| C3-04 | Part I | 1 GW burns 55.6 kg/fpy | Correct (≈ 150 g/day) | confirmed |
| C3-05 | Part VIII table | "ITER plant ~2035" | Follows C3-01 | corrected |
| C3-06 | Parts VI–VII | Facility timelines (H3AT, UNITY-2, LIBRTI, Cernavoda) | Not re-verified on 3 November 2026 | not re-verified |
| C3-07 | Part V 5.3 | Accountancy as a regulatory issue | Confirmed: the NRC proposal requires tritium and activation-product accounting in applications [R5][R32] | confirmed |

### R.2 Direct vs. indirect drive for this challenge

Both ICF variants share the coverage problem of a spherical chamber with beam ports, and the target-factory
inventory. The differences:
- **Indirect drive** needs hohlraum assembly around each capsule, which means a longer and more complex
  fill/layer/assembly chain and a larger in-process inventory. Model: TR P50 2066, show-stopper 0.30.
- **Direct drive** uses bare capsules, so the inventory is somewhat smaller. Model: TR P50 2064, show-stopper
  0.28.
- Both are clearly later than MCF, because no IFE blanket has been tested at any scale.

### R.3 TRL / licensing / funding view of Challenge 3

| Pathway | TRL | Licensing / permit | Funding |
|---|---|---|---|
| All pathways | Breeding blankets: TRL 2–4. There is no blanket test in a fusion environment; ITER's TBMs come with DT from 2039 [R1]. | The kg-scale tritium inventory is the largest single licensing object: accountancy, release limits, emergency planning (NRC trigger at 1 rem offsite) [R5][R32]. A fission-like regime after an incident is modelled as `g_regime` (p = 0.10). | Start-up inventories must be bought from finite supply. Dedicated breeding facilities need public funding. |
| Tokamak / stellarator | Blanket coverage is better in tokamaks; 3D geometry penalises the stellarator. | Same framework. | — |
| Direct / indirect drive | No IFE blanket design has been tested. | Target-factory inventory adds to the plant inventory. | No dedicated IFE tritium programme was identified. |

### R.4 Mapping to the risk model (gate TR)

- **TR** — Breeding blanket operated in a DT device of the pathway; measured net TBR ≥ requirement + 0.05; closed fuel cycle; start-up inventory secured.

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | TR – Tritium | 2032 / 2038 / 2048 / 2065 / 2090 | 0.10 | `tok_tr`, `tok_f_tr` |
| Stellarator | TR – Tritium | 2038 / 2045 / 2058 / 2080 / 2098 | 0.20 | `stl_tr`, `stl_f_tr` |
| Direct Drive | TR – Tritium | 2044 / 2049 / 2064 / 2086 / 2099 | 0.28 | `dir_tr`, `dir_f_tr` |
| Indirect Drive | TR – Tritium | 2045 / 2050 / 2066 / 2088 / 2099 | 0.30 | `ind_tr`, `ind_f_tr` |

Common show-stopper `g_f_tritium` = 0.03 (fuel cycle cannot be closed at acceptable losses for any DT
pathway). The tritium gates of different pathways are coupled at ρ = 0.6 (MCF), 0.7 (ICF) and 0.5 (across the
pillars). Scenario `tritium_engpass`: all TR gates +4 years and `g_f_tritium` = 0.08.

### Sources for this review

Accessed 3 November 2026. Secondary sources are marked as such; claims resting only on them are flagged in the tables above.

- **[R1]** ITER Organization via ANS Nuclear News, 'ITER begins operations at its magnet cold test facility' (1 Jun 2026) — Baseline 2024: SRO 2034, full magnetic energy 2036, DT 2039. <https://www.ans.org/news/article-8081/iter-begins-operations-at-its-magnet-cold-test-facility/>
- **[R5]** US NRC, proposed rule 'Regulatory Framework for Fusion Machines', Federal Register 26 Feb 2026 (10 CFR Part 30). <https://www.federalregister.gov/documents/2026/02/26/2026-03865/regulatory-framework-for-fusion-machines>
- **[R32]** Orrick, 'NRC proposed fusion rule further clarifies path for commercial deployment' (Mar 2026) — tritium/activation reporting, Part 51 environmental review. <https://www.orrick.com/en/Insights/2026/03/NRC-Proposed-Fusion-Rule-Further-Clarifies-Path-for-Commercial-Deployment>

---

## References

1. [[PDF] Tritium Breeding Ratio Requirements [presented at the ARIES-TNS ...](https://fti.neep.wisc.edu/fti.neep.wisc.edu/aries/TALKS/lae_tbr0607.pdf) - Fusion power plants must breed their own tritium (55.6 kg/FPY per 1 GW P f ). Net TBR must be close ...

2. [UWFDM-1330  Toward the Ultimate Goal of Tritium Self-Sufficiency: Technical Issues and Requirements Imposed on ARIES Fusion Power Plants](https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm1330.pdf)

3. [UK and Canada team up to solve nuclear fusion fuel ...](https://sciencebusiness.net/news/uk-and-canada-team-solve-nuclear-fusion-fuel-shortage) - The UK and Canada have agreed on a joint research programme to tackle one of the toughest problems f...

4. [[PDF] Tritium Fuel Cycle Overview Daniel Clark Sr. Materials Scientist](https://www.agreementstates.org/uploads/1/1/8/4/118443122/t_0155_tritium_fuel_cycle_overview_v3-d._clark.pdf) - • Tritium decays with a 12.3 year half-life (Decay rate of 5.47% per year) o ... oOnly intrinsic rad...

5. [[PDF] Tritium Breeding Blanket Technology, Tritium Fuel Cycle, and ...](https://www.fusion.ucla.edu/files/2022/12/FINAL-Abdou_Pilot-Plant-Session-FPA-12-7-2022.pdf) - Fusion, if it works, will be the ultimate energy source for mankind. • But the Pace of fusion develo...

6. [Physics and technology considerations for the deuterium-tritium fuel ...](https://publikationen.bibliothek.kit.edu/1000128200)

7. [[PDF] GLOBAL SUPPLY OF TRITIUM FOR FUSION R&D FROM HEAVY ...](https://scientific-publications.ukaea.uk/wp-content/uploads/3B76859550CE98DC127082F1E5B5381C8B96.PDF)

8. [Insights into fuel start‐up and self‐sufficiency for fusion energy: The ...](https://scijournals.onlinelibrary.wiley.com/doi/10.1002/ese3.291) - For a fusion reactor with 1 GW fusion power, about 37.1 kg deuterium and 55.6 kg tritium would be bu...

9. [With the current supply of tritium, how many functioning tokamaks ...](https://www.reddit.com/r/fusion/comments/1fnb83m/with_the_current_supply_of_tritium_how_many/) - Assuming tritium breeding works, you still need startup fuel. There is only about 20 kg of usable tr...

10. [Global supply of tritium for fusion R&D](https://scientific-publications.ukaea.uk/papers/global-supply-of-tritium-for-fusion-rd/)

11. [Fusion reactor start-up without an external tritium source](https://www.sciencedirect.com/science/article/abs/pii/S0920379615303598) - It is also recognised that the initial start-up of a fusion reactor will require several kilograms o...

12. [[PDF] Tritium Breeding Blanket Technology, Tritium Fuel Cycle, and ...](https://bpb-us-w2.wpmucdn.com/research.seas.ucla.edu/dist/d/39/files/2022/10/M-Abdou-DT-Cycle-KIT-MaPLE-U-Colloquium-10-14-2022-FINAL.pdf)

13. [ANS / Publications / Journals / Fusion Science and Technology](https://www.ans.org/pubs/journals/fst/article-39804/)

14. [The ways to evaluate the required value for the tritium](https://www.nifs.ac.jp/report/annrep12/pdf/256.pdf)

15. [Assessment of Startup Inventory and Required Tritium Breeding Ratio for Fusion Reactor Based on Integrated Analytical Scheme – DOAJ](https://doaj.org/article/b6a5083d087d46ab8a5a71941686ca81) - The development of Tokamak fusion reactors encompasses hybrid and pure fusion reactor designs. In th...

16. [[PDF] Tritium Breeding Ratio Evaluation of Solid Breeder Concepts for the ...](https://www.osti.gov/servlets/purl/2448047) - Therefore, at a minimum, the TBR must be greater than 1.0 for self-sufficiency. a minimum required T...

17. [Predictive modelling of tritium breeding ratio (TBR) in EU DEMO ...](https://www.sciencedirect.com/science/article/abs/pii/S0920379625007124) - Up to 2020, two of them are being developed for integration as Test Blanket Module in ITER, the WCLL...

18. [[PDF] Neutronic Performance Issues of the Breeding Blanket Options for ...](https://scipub.euro-fusion.org/wp-content/uploads/2015/12/EFCP150632.pdf) - This paper presents nuclear performance issues of the HCPB, HCLL, DCLL and WCLL breeder blankets, wh...

19. [An Assessment of the Prospects for Inertial Fusion Energy (2013)](https://www.nationalacademies.org/read/18289/chapter/5) - Targets for ICF experiments are filled by permeation, Tritium breeding is accomplished in the blanke...

20. [Approach to Startup Inventory for Viable Commercial Fusion](https://www.osti.gov/servlets/purl/2403075)

21. [[PDF] Introduction to fusion power plant fuel cycles and tritium breeding ...](https://suli.pppl.gov/2023/course/SULI%202023%20presentation.pdf) - TBR required and I startup. ○ At low TBE, I startup and TBR req become unmanageably high. ○ Longer d...

22. [[PDF] Technical Issues and Requirements Imposed on Fusion Power Plants](https://fti.neep.wisc.edu/fti.neep.wisc.edu/presentations/lae_tofe08.pdf) - T required to provide start-up inventory for new fusion power plant: a. T build-up in power core mat...

23. [Fuelling - ITER](https://www.iter.org/machine/supporting-systems/fuelling) - ... tritium (D-T) reaction has been identified as the most efficient for fusion devices. Only a few ...

24. [Fusion reactor technology, focused on tritium safety ...](https://www.jspf.or.jp/PLASMA2011/PLACON2011/pdf/23T2.pdf)

25. [UKAEA-Eni H3AT Tritium Loop Facility](https://www.ukaea.org/work/ukaea-eni-h3at-tritium-loop-facility/) - UK Atomic Energy Authority and Eni have a ground-breaking collaboration to develop skills and techno...

26. [Ninth DEMO and Fusion Plants Workshop](https://conferences.iaea.org/event/385/contributions/35505/contribution.pdf)

27. [The tritium burn-fraction in DT fusion](https://arxiv.org/abs/2106.01304) - The fraction of the tritium that is burned during one pass through a DT fusion system, $f_{tb}$, is ...

28. [Tritium-Lean Fusion Power Plants with Asymmetric Deuterium-Tritium Transport and Pumping](https://arxiv.org/html/2410.05238v1)

29. [Modeling and experiments on tritium permeation in fusion ...](https://www.osti.gov/biblio/5918551) - Issues are discussed that are critical in determining tritium loss from helium-cooled fusion breedin...

30. [Tritium permeation barriers for fusion technology](https://www.osti.gov/biblio/196852) - An important issue concerning the safety, feasibility and fueling (i.e., tritium breeding ratio and ...

31. [International Journal of Hydrogen Energy](https://repository.kulib.kyoto-u.ac.jp/dspace/bitstream/2433/267732/1/j.ijhydene.2021.11.225.pdf)

32. [Steady-state tritium inventory in plasma-facing tungsten for fusion reactors: An effective calculation method and implications of calculation results](https://www.sciencedirect.com/science/article/abs/pii/S0022311523000648) - The tritium inventory in plasma-facing components needs to be evaluated with sufficient accuracy sin...

33. [Tritium inventory and recovery in next-step fusion devices](https://www.sciencedirect.com/science/article/abs/pii/S092037960200248X) - There are three materials that are strong candidates for plasma-facing-material use in next-step fus...

34. [[PDF] robert.sindelar@srnl.doe.gov, corresponding author](https://resources.inmm.org/sites/default/files/2023-07/finalpaper_642_0512095320.pdf)

35. [Microsoft Word - SRNL-STI-2013-00384_TAT_0i.docx](https://sti.srs.gov/fulltext/SRNL-STI-2013-00384.pdf)

36. [Breeding Blanket concepts for the EU-DEMO Fusion Power ...](https://www.eventi.enea.it/images/presentazioni2024/2024_12_11_funfi_it/FUNFI-IT_Damico.pdf)

37. [FT/P2-12 Studies and Developments of Tritium Recovery ...](https://www-pub.iaea.org/mtcd/meetings/fec2008/ft_p2-12.pdf)

38. [Development of tritium breeding blankets for DT-burning fusion reactors](https://www.osti.gov/biblio/6377863) - This study examines the status of understanding of blanket tritium recovery and the performance of p...

39. [DCLL manifolds](https://indico.ukaea.uk/event/639/contributions/1049/attachments/454/765/The%20IFMIF%20DONES%20Test%20Blanket%20Units%20Arranz%20F%20v1_3.pdf)

40. [The LIBRA Experiment: Investigating Robust Tritium Accountancy in Molten FLiBe Exposed to a D-T Fusion Neutron Spectrum](https://www.tandfonline.com/doi/full/10.1080/15361055.2022.2078136) - The Liquid Immersion Blanket: Robust Accountancy (LIBRA) experiment will be a first-of-a-kind experi...

41. [[PDF] Preliminary Design of China ITER Test Blanket Module with Helium ...](https://www-pub.iaea.org/MTCD/Meetings/FEC2006/ft_p5-18.pdf) - The results shown that peak power density, energy deposition and tritium breeding ratio are 5.85MW/m...

42. [1](https://lasers.llnl.gov/sites/lasers/files/2023-11/bott-suzuki-UCSD-IFE-workshop-2022.pdf)

43. [Fuel Cycle for an Inertial Fusion Energy Reactor final](https://lasers.llnl.gov/sites/lasers/files/2023-11/shmayda-rochester-IFE-workshop-2022.pdf)

44. [STELLARATOR FUSION REACTORS –– AN OVERVIEW](https://fire.pppl.gov/itc12_wobig_paper.pdf)
