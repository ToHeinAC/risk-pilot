# Nuclear Fusion — Deep Dive: Challenge 3
## Tritium Fuel Self-Sufficiency

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — November 2026 update*

***

## Executive Summary

Tritium fuel self-sufficiency is widely regarded as the most underappreciated systemic risk in the fusion development programme. Unlike plasma stability or materials damage — problems that can be tested incrementally in sub-scale experiments — the tritium challenge is deeply systemic: it can only be resolved in an integrated operating fusion power plant, which does not yet exist. The core arithmetic is unforgiving: each DT fusion reaction produces exactly one 14.1 MeV neutron, and that single neutron must simultaneously breed one replacement tritium atom, maintain enough surplus to supply start-up inventory for future reactors, and survive absorption losses to structural materials, coolants, and port penetrations.[^1][^2]

A comprehensive 2021 analysis by Abdou et al. (Nuclear Fusion 61, 013001) — the most authoritative systematic study of this challenge — concluded that **current physics and technology are insufficient to guarantee tritium self-sufficiency or to provide the required start-up inventories** for DEMO and power plants. This is not a fringe finding; it is the consensus of four decades of fusion fuel-cycle analysis, repeatedly confirmed and never resolved. The global civil tritium stockpile is only of order **20–25 kg** (no authoritative figure is published; a 2025 estimate puts it at ~20 kg), the vast majority held in Canada as a by-product of CANDU heavy-water reactors; commercial prices are of order $25,000–$35,000 per gram; tritium decays at 5.47% per year with a 12.3-year half-life; and under ITER's 2024 baseline DT operation will not start before **2039**, by which time a significant share of today's stockpile will have decayed.[^3][^4][^5][^6][^9][^45]

This report provides a deep-dive analysis of six interconnected sub-challenges: (1) the global tritium supply crisis and ITER consumption timeline; (2) the required vs. achievable Tritium Breeding Ratio; (3) the start-up inventory problem; (4) the tritium burn fraction and fuel cycle efficiency; (5) tritium permeation, retention, and accountancy; and (6) breeding blanket technology and ICF-specific complications.

***

## Part I — The Global Tritium Supply Crisis

### 1.1 Where Tritium Comes From Today

Tritium does not occur in nature in meaningful quantities: its 12.3-year half-life means that any primordial tritium has long since decayed. The only current commercial-scale production route is neutron capture on deuterium in CANDU (Canada Deuterium Uranium) heavy-water reactors, in which D\(_2\)O moderator absorbs neutrons via the reaction:[^4]

\[^2\text{D} + n \rightarrow ^3\text{T} + \gamma\]

The accumulated tritium is then extracted from the heavy water in dedicated Tritium Removal Facilities. Canada hosts the majority of operating CANDU reactors and holds the dominant share of the global civil stockpile, giving it a geopolitically significant monopoly on fusion fuel supply. Romania's Nuclearelectrica signed a ~€195 million (~$200–213 million) EPC contract with Korea's KHNP in June 2023 for Europe's first Tritium Removal Facility at Cernavoda; first concrete was poured in June 2025 and completion is targeted for ~2027. South Korea operates the Wolsong detritiation facility, so Canada, Korea and (from ~2027) Romania are the only realistic HWR sellers.[^7][^62]

Current global civil tritium inventory estimates are **~20–25 kg**; higher figures (25–30 kg) circulate in secondary sources but are not supported by a primary inventory statement, and operators do not publish production data.[^9][^7] Heavy-water reactors produce an estimated **210–260 g of tritium per GWe per full-power year**; OPG has historically sold only ~100 g/yr to commercial users at **$25,000–30,000 per gram**.[^7] For context, a single 1 GW (fusion) power plant burns approximately **55.6 kg of tritium per full power year (fpy)** — roughly **2–3 times the entire global civil stockpile consumed in one year of operation**.[^8][^1]

### 1.2 The ITER Consumption Timeline

Under the **2024 ITER baseline**, Start of Research Operation moves to 2034, DD operation to ~2035 and the **start of DT operation from 2035 to 2039**.[^45] At 500 MW fusion power ITER would burn ~28 kg of tritium per *full-power* year, but its low duty factor limits actual consumption: the frequently quoted (unofficial) lifetime estimate is **~12.3 kg**.[^7] The re-baselined first DT phase (DT-1: Q = 10, 500 MW, ≥300 s burns) is planned at only ~1% of the earlier neutron-fluence objective, which lowers near-term consumption, while the high-fluence DT-2 phase follows later.[^46] Since ITER does not breed its own tritium — the test blanket modules produce negligible amounts — this tritium must come from the HWR stockpile.[^7][^5]

The alarming implication, identified by Abdou, is as follows: **By the time ITER completes its DT programme, there may be no external non-fusion tritium supply left to provide start-up inventory for any subsequent major DT fusion facility.** The tritium that existed at the beginning of ITER's design phase has already decayed; what remains from today's stockpile will have further decayed by the 2040s. The Abdou analysis concluded that any DT fusion demonstration device built after ITER must either:[^5]
1. Operate at very low fusion power (<150 MW) to minimize tritium consumption and keep start-up requirements small enough to be obtainable, or[^11][^5]
2. Include a preceding Fusion Nuclear Science Facility (FNSF) device that produces excess tritium over time to supply DEMO's start-up inventory[^5]

Canada's commitment to refurbishing its CANDU fleet through the 2070s provides some relief — those reactors will continue producing tritium — but at rates insufficient to simultaneously supply multiple DEMO-class devices in parallel. A UKAEA analysis (Coleman & Kovari, IAEA FEC 2018) estimated that Ontario's production can cover ITER's demand but, after ITER's schedule slips, may leave only **~7.4 kg for a DEMO in 2055**; across scenarios, commercially available HWR tritium in 2055 ranges from **0 to ~28 kg**, and a single additional 5 kg purchase (e.g. by CFETR) or a further ITER delay removes several kilograms from that figure. Since DEMO start-up estimates range from ~1 to 20 kg, several DEMO-class devices in parallel in the 2050s would create a severe supply crunch.[^7][^10] Two partial mitigations emerged in 2024–2025: the UKAEA–Canadian Nuclear Laboratories tritium partnership (February 2024) and an Ontario Power Generation–UKAEA memorandum of understanding (September 2025) on a dependable tritium supply for UK fusion facilities.[^49][^50]

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
- Breed one new tritium atom (\(^6\)Li capture alone yields at most one triton per source neutron, so TBR > 1 relies on neutron multiplication via \(^9\)Be(n,2n), Pb(n,2n) and the \(^7\)Li(n,n'α)t reaction, which returns a neutron)
- Overcome structural and coolant parasitic absorption
- Compensate for geometric coverage losses from port penetrations

**Neutron parasitic losses** are the primary TBR killer. Every structural material in the neutron path — steel, tungsten, beryllium — has a finite absorption cross-section. Neutron transport calculations for realistic DEMO blanket designs with EUROFER structural steel, beryllium neutron multiplier, and Li\(_6\)SiO\(_4\) solid breeder pebble beds (HCPB concept) yield TBR values in the range **1.10–1.18** in idealized 1D calculations, dropping to **1.03–1.08** in full 3D calculations that correctly account for:[^17][^18]
- Port penetrations for heating systems, diagnostics, fueling, and vacuum pumping
- Structural ribs, cooling channels, manifolds, and weld reinforcements
- First-wall armor layer absorption
- Neutron streaming through gaps between blanket modules

**Geometric coverage** is a particularly severe constraint. In ITER-scale tokamaks, the first wall surface area is roughly 700–800 m², but ports (equatorial, upper, lower), supporting structures, and the divertor account for 20–30% of the total area. Every uncovered area is a neutron leak. Analysis of EU DEMO finds that the TBR drops by **~0.04–0.06 per 1% decrease in blanket coverage**, meaning that recovering the 15–20% port coverage fraction requires achieving TBR > 1.2 in the blanketed regions just to maintain net TBR > 1.05 overall.[^18]

**Neutron multipliers** are the primary strategy to overcome the one-neutron-per-reaction ceiling. Beryllium (via \(^9\)Be(n,2n), threshold ~1.9 MeV) and lead (via \(^{208}\)Pb(n,2n), threshold ~7.4 MeV) each release **two neutrons per (n,2n) reaction**; because only a fraction of source neutrons undergo (n,2n), the effective multiplication of a practical blanket is well below 2 per source neutron. (The earlier statement that each multiplier produces "1.5–2.0 neutrons per fast neutron above ~5 MeV" conflated the per-reaction yield with the blanket-level gain and misstated the Be threshold.) However:[^13][^2]
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
- Compact pilot-plant studies give sub-kilogram values: for an ARC-like tokamak at ~480 MW fusion power, Parisi et al. compute a minimum start-up inventory of **~0.69 kg** with conventional fuel (falling to ~0.03 kg with fully spin-polarised fuel, an undemonstrated technique); Type One Energy's Infinity Two stellarator study estimates an operational inventory of **~675 g**.[^61][^59] (An earlier version of this report quoted a "90 g" ARC figure from an online forum; it could not be verified and has been removed.)

The dramatic spread — from well under 1 kg to tens of kilograms — reflects genuine design choices and assumptions about tritium burn fraction, inventory turnover time, and acceptable reserve margins. The low-end estimates from compact pilot plants rely on aggressive assumptions (tritium burn efficiency of ~0.5–1% or more, i.e. above ITER's ~0.36%, short processing times, low retention) that have not been experimentally validated; adding realistic tritium trapping in blanket and wall materials raises the ARC-class start-up inventory by ~30%, the doubling time by ~50% and the required TBR by 2–5%.[^60][^65] The high-end estimates correspond to conventional large-scale DEMO-class designs with conservative engineering margins.

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

In a DT plasma, the fraction of injected tritium that actually undergoes fusion in a single pass through the plasma — the **burn fraction** — is determined by the ratio of the fusion reaction rate to the particle confinement time. In ITER, the effective burn fraction is estimated at only **~1%** (the tritium burn efficiency including fuelling efficiency is lower still, ~0.36%).[^60] This means that for every 100 T atoms injected into the plasma, 99 are pumped out through the divertor as unburned exhaust.[^23]

The implication for the fuel cycle is dramatic: a 3 GW fusion plant burns ~450 g T/day. At a burn efficiency of 1% the tritium plant must process ~**45 kg of T per day**; even at an optimistic 5% it is ~**9 kg/day** — 40–45% of the entire global civil stockpile flowing through the plant **every single day**. (The earlier version paired the 9 kg/day figure with a 1% burn fraction, which is inconsistent by a factor of five.) The isotope separation system, tritium accounting, and storage systems must process this at:[^24]
- Isotopic purity requirements of >99.9% D:T ratio for injection
- Tritium recovery efficiency from exhaust of >99.9% (losses at even 0.1% per pass would accumulate to unacceptable inventory losses and environmental releases)
- Cryogenic distillation at 21–26 K for hydrogen isotopologue separation[^25]

No facility has yet demonstrated this full closed-loop cycle at power-plant-relevant throughput. The UKAEA-Eni H3AT Tritium Loop Facility at Culham, announced in 2025, due for completion in 2028 and full operation by 2030, is designed to demonstrate a closed loop continuous flow system at **1/20th pilot plant scale with a 100 g tritium inventory**. It will be the first facility of its kind in the world — a landmark but still far below reactor scale.[^26][^25]

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

A critical sensitivity, following Abdou: losses scale with **throughput**, not with stored inventory. If 0.1% of a ~9 kg/day processing throughput is lost per pass (permeation, leaks, unrecovered exhaust), the loss is ~9 g/day, i.e. **~3.3 kg/year** — of the same order as the *entire* annual tritium output of the world's heavy-water reactors and larger than the full breeding surplus of a 1 GW plant at net TBR 1.05 (~2.8 kg/yr). Manageable losses therefore require per-pass loss fractions of order **10⁻⁵ (0.001%)**, a standard that has not been demonstrated in any integrated facility.[^6][^2][^7]

### 5.2 Tritium Retention in the First Wall and Plasma-Facing Components

As analyzed in Challenge 2, tritium implanted in the plasma-facing first wall creates an inventory that grows over time due to neutron-irradiation-induced trap sites. For a DEMO-class machine with a tungsten first wall:[^32][^33]
- Steady-state tritium inventory in plasma-facing tungsten is dominated by deep-layer retention in the large temperature gradient region near the back of the monoblocks[^32]
- Retention can be reduced by maintaining wall temperatures above ~700 K (thermal detrapping), but this requires operating at baking temperatures that may be incompatible with simultaneous plasma operation
- ITER's in-vessel tritium **safety limit is 1 kg**; after deducting ~120 g assumed in the cryopumps and ~180 g for accounting uncertainty, the **administrative limit is ~700 g** (historically 330–640 g as uncertainty estimates evolved). Reaching it forces operation to stop for tritium removal. DEMO-class machines with much higher fluence will face similar or stricter limits[^63][^34]

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
- **ITER TBM**: the EU HCPB has been merged with Korea's HCCR into the jointly developed **HCCP** (helium-cooled ceramic pebbles) TBM, which with the EU WCLL passed its preliminary design review in 2026[^46][^47]

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
- LIB is at TRL 2–3; no reactor-scale engineering data exist. MIT's BABY experiments (precursor to LIBRA) made the first measurements of tritium breeding in a molten salt under 14 MeV neutrons: TBR ≈ 3.6×10⁻⁴ in 100 mL (surrogate LiCl–LiF salt) and ≈ 2×10⁻³ in 1 L, in good agreement with OpenMC predictions — tiny absolute values by design, but the first validation of molten-salt breeding neutronics and tritium recovery. LIBRA itself aims at TBR ≥ 1 in ~500 L of FLiBe; an ARC-class blanket needs ~250,000 L[^51][^52]

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

ITER's Test Blanket Module (TBM) programme is the main internationally planned test of breeding blanket concepts in a tokamak environment. Under the 2024 baseline, **two equatorial ports (#16 and #18)** host **four Test Blanket Systems** simultaneously during DT-1, two per port: the EU **WCLL**, the EU–Korea **HCCP**, Japan's **WCCB** (water-cooled ceramic breeder) and China's **HCCB** (helium-cooled ceramic breeder). Design is to be completed by 2029, installation starts ~2035 and operation with DT from **2039 for about ten years**; DT-2 could host other concepts (e.g. DCLL). The EU WCLL and HCCP preliminary design reviews were held in 2026, with closure targeted for end-2026.[^46][^47][^41]

However, the TBM programme faces a fundamental limitation: ITER is not a DT breeding reactor. The TBMs occupy only a few percent of the first-wall area, and with DT-1 planned at ~1% of the original fluence objective they will accumulate very little neutron fluence before the 2040s; tritium production is negligible (grams) compared with the tens of kilograms per year a power plant must breed. Their primary value is in demonstrating tritium extraction system integration, activation analysis, and materials performance under fusion neutron bombardment, not in validating full-scale TBR under realistic conditions.[^41][^18]

### 6.4 ICF-Specific Tritium Challenges

Laser ICF imposes a uniquely severe version of the tritium challenge, for several interconnected reasons:[^19][^42][^43]

**Target filling**: Each ICF target contains a **cryogenic DT ice layer** approximately 70–90 µm thick on the inner surface of the 1–2 mm diameter capsule. Filling the capsule requires diffusing DT gas through the capsule wall at high pressure (several hundred bar), then slowly cooling to ~18 K to form a uniform DT ice layer — a process that takes **several days per target**. A power plant needing 500,000 targets per day requires a factory that can fill, layer, and characterize targets in **parallel across thousands of stations** running continuously.

**In-plant tritium inventory**: The US National Academies' IFE assessment warns that long fill and layering times "may result in large (up to ~10 kg) tritium inventories"; older plant studies range from ~4 kg (HYLIFE-II) down to ~0.3 kg for injection-filled foam targets, so target design (fill method, layering time) is the dominant lever. Even the upper value is roughly half the global civil stockpile, and a containment failure in the target factory would be a major radiological event.[^19] (The earlier "10–20 kg" figure overstated the cited source.) On the positive side, ICF burns ~20–30% of the fuel in each capsule, so the burn efficiency per processed gram is far higher than in magnetic confinement; the ICF problem is inventory *residence time*, not throughput.[^19]

**Blanket geometry**: ICF chamber geometry requires laser beam ports (typically 48–96 ports for direct drive, or 2 holes plus laser-entry ports for indirect drive) to penetrate the lithium blanket. These ports reduce the effective blanket coverage area, directly reducing TBR. Published studies indicate an ICF blanket penalty of order **0.05–0.15 in TBR** relative to an equivalent closed geometry (indicative range; it depends strongly on port count and on thick-liquid-wall vs. dry-wall designs — the NAS report notes, for example, that a 24 cm FLiBe wall gives a TBR of only about unity) — potentially placing net ICF TBR below 1.0 in some designs.[^19]

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

No dedicated FNSF in Abdou's sense exists or is funded. The closest is China's **BEST** (Burning plasma Experimental Superconducting Tokamak) in Hefei: under assembly since 2025, with more than half of the main-machine tasks reported complete by October 2026, first plasma targeted for 2027 and DT operation with demonstration of fusion power around 2030; its stated goals include tritium production, extraction and recycling and blanket-module testing, but no blanket design or TBR figures have been published and its DT plans are still under review.[^58] The EU's proposed FTQP (Fusion Technology Qualifying Platform) remains a concept. The absence of the FNSF represents what Abdou calls a "missing step" that makes the entire development pathway to DEMO uncertain at a fundamental level.[^5]

### 7.2 H3AT and Other Near-Term Facilities

The UKAEA-Eni **H3AT Tritium Loop Facility** at Culham is the most significant near-term tritium technology development investment. Announced in 2025 and scheduled for completion by 2028–2030:[^25][^26]
- **Scale**: 100 g tritium inventory — 1/20th pilot plant scale
- **Scope**: demonstrates closed-loop continuous flow fuel cycle; tests palladium membrane reactors for tritium recovery from exhaust; demonstrates cryogenic isotope separation at 21–26 K; validates fuel cycle models
- **Partners**: Eni (industrial engineering and commissioning); AtkinsRéalis (detailed design of the isotope separation system, since May 2024); **Kinectrics** (BWXT) selected in March 2026 as design and fabrication partner for gloveboxes and tritium-handling equipment[^25][^48]
- **Limitation**: operates without a fusion neutron source — cannot test tritium breeding, only the non-breeding fuel cycle subsystems

At ITER itself, the tritium plant includes a closed-loop system capable of processing the ~1% ITER burn fraction exhaust. ITER will be the first integrated test of a multi-kg tritium fuel cycle in a tokamak, but again without blanket breeding. Lessons from ITER's tritium plant operation (DT from 2039, likely into the 2050s) will be invaluable but arrive too late to inform DEMO design, which must be frozen years earlier.[^6][^5][^45]

### 7.3 Developments 2025–2026

- **LIBRTI (UK)**: UKAEA's ~£200 million Lithium Breeding Tritium Innovation programme (2022–2028) is converting a former JET building at Culham into a shielded blockhouse with a 14 MeV DT neutron source (supplier SHINE Technologies, delivery expected ~2027) to test large breeder-blanket mock-ups. In July 2026 **Commonwealth Fusion Systems** became its first international partner and will build the first test articles, explicitly to demonstrate net tritium production for its ARC FLiBe blanket.[^53][^54] This is a non-fusion-plasma neutron source: it validates neutronics and tritium extraction, not the integrated plasma-blanket environment of the gate below.
- **LIBRA / BABY (US)**: first measured molten-salt breeding under 14 MeV neutrons (100 mL, 2025; 1 L campaign 2025, TBR ≈ 2×10⁻³, matching OpenMC); scale-up to FLiBe and ~500 L is the next step.[^51][^52]
- **UNITY-2 (Canada)**: Fusion Fuel Cycles Inc., a Kyoto Fusioneering–Canadian Nuclear Laboratories joint venture, began construction at Chalk River in November 2025 of an integrated fuel-cycle loop circulating up to 30 g of tritium per 24 h (expandable to 100 g); General Atomics invested $20 million. Commissioning was reported for late 2026; operation is not yet confirmed.[^55]
- **United States**: DOE's FIRE Collaboratives (launched 2024) include an SRNL-led fuel-cycle team building a continuous integrated tritium recycle/purify/account system and an INL-led Blanket Nuclear Testing centre, plus ORNL's HASTE blanket flow loop; DOE's Fusion S&T Roadmap (October 2025) names fuel cycle and blankets among six focus areas but makes milestones contingent on public–private partnerships.[^56][^57]
- **UK–Canada supply axis**: UKAEA–CNL tritium framework (2024), OPG–UKAEA supply MoU (September 2025), Canadian participation in H3AT (AtkinsRéalis, Kinectrics).[^49][^50][^48]
- **Private designs**: Type One Energy's Infinity Two stellarator (HCPB blanket) reports a homogenised 3D TBR of 1.30 versus a required TBR < 1.05 and ~675 g operational inventory — a physics-basis result at low engineering fidelity.[^59] A June 2026 UKAEA conference abstract reports that STEP has selected a solid Li\(_2\)O ceramic breeder with Be-based multiplier and CO\(_2\) coolant, moving away from liquid lithium (single source, not yet confirmed in a peer-reviewed design paper).[^64]
- **Romania**: Cernavoda Tritium Removal Facility under construction since June 2025, completion ~2027, adding a third HWR tritium seller.[^62]

Net assessment: 2025–2026 brought a step change in *non-nuclear and neutron-source* fuel-cycle infrastructure (H3AT, UNITY-2, LIBRTI, FIRE), but no change to the central gap: there is still no funded programme to test a breeding blanket with net tritium production in a fusion plasma environment before BEST (~2030+, scope unclear), ARC (2030s, if built and operated in DT) and the ITER TBMs (2039+).

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
| Closed fuel cycle (non-breeding) | UNITY-2 commissioning ~2026–27; H3AT 2028–2030; ITER DT 2039 | 4–5 | Scale, closed-loop integration |
| Permeation barriers (structural) | Proof-of-concept only | 3 | Irradiation stability under neutrons |
| Tritium accountancy at reactor scale | Unresolved | 2–3 | Measurement precision at high throughput |
| ICF target filling at rep-rate | Nonexistent | 1–2 | Factory concept undemonstrated |
| Blanket test with 14 MeV neutron source (no plasma) | LIBRTI ~2027+, LIBRA scale-up | 3–4 | Source strength, mock-up scale |
| In-fusion-environment blanket test | Nonexistent (BEST ~2030+, ITER TBMs 2039+) | — | FNSF does not exist |

### 8.2 Pathway Comparison

| Challenge Element | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Blanket geometry | Axisymmetric; good coverage[^18] | 3D; ~20–30% area penalty from coils; harder to meet TBR[^44] | 20–40% coverage loss from beam ports; may be below TBR = 1 in some designs[^19] |
| Blanket T extraction | Standard purge or flow; continuous option available | Same physics, harder geometry | Requires mass batch process; days-long cycle time[^43] |
| In-plant T inventory risk | Moderate (~kg scale) | Moderate | High (0.3 to ~10 kg in target factory, design-dependent)[^19] |
| T start-up inventory need | ~0.7–20 kg depending on design[^20][^8][^61] | Similar to tokamak (~0.7 kg operational for Infinity Two)[^59] | Large; add target-factory pre-fill inventory |
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

The tritium supply geopolitics also deserve serious strategic attention: Canada's CANDU fleet is currently the dominant source of tritium at meaningful scale (with Korea, and Romania from ~2027), and its availability for fusion is not guaranteed. A global fusion programme that reaches 10+ simultaneous DT facilities in the 2050s — with each needing kilograms of tritium for start-up — will face a supply crunch that no amount of improved blanket physics can resolve if the infrastructure for breeding and fuel cycling is not demonstrated well in advance.[^3]

## Risk Assessment (November 2026)

### Risk register

| ID | Risk | Pathway(s) | Likelihood | Impact on schedule (years) / on feasibility | Early indicator | Mitigation |
|---|---|---|---|---|---|---|
| TR-1 | Achieved 3D/as-built TBR falls below required TBR (≈1.05) once ports, manifolds, diagnostics and trapping are included | All (worst ICF, then stellarator) | med | +5–15 yr (redesign, Be/⁶Li enrichment, coverage changes); can make a design non-self-sufficient | Engineering-fidelity neutronics of ARC, STEP, Infinity Two, EU DEMO trending below 1.10; LIBRTI/LIBRA mock-up results below prediction | Design for local TBR ≥ 1.15–1.2; ⁶Li enrichment; liquid breeders with high coverage; validated neutronics (BABY/LIBRA/LIBRTI benchmarks) |
| TR-2 | No fusion-environment blanket test before DEMO/FPP design freeze (FNSF "missing step") | Tokamak, Stellarator (ICF has no equivalent plan) | high | +5–10 yr, or FOAK built on unvalidated blanket with high first-of-kind failure risk | No FNSF/VNS funding decision by ~2028; BEST blanket/DT scope stays undefined | Use BEST, ARC and ITER DT-1 TBMs as partial FNSF; fund a volumetric neutron source; international blanket-test consortium |
| TR-3 | Start-up tritium not available in time for the first demo plant (HWR stock depleted by ITER, decay, competing buyers, CANDU retirements) | All (DEMO-class designs most exposed) | med | +2–12 yr for the affected plant; caps the number of parallel DT demos | Stockpile/price signals; OPG sales policy; further ITER slip; number of DT programmes requesting > 1 kg | Low-inventory designs (< 1 kg); long-term supply contracts (OPG, KHNP, Cernavoda from ~2027); DD start-up / tritium-lean operation; dedicated fission production (TPBAR-type) as backstop |
| TR-4 | Tritium burn efficiency stays near ITER level (~0.3–1%), forcing large processing throughput, inventories and required TBR | Tokamak, Stellarator | med | +3–8 yr; raises required TBR and start-up inventory | ITER/JT-60SA/BEST fuelling-efficiency data; DIR (direct internal recycling) demonstrations | Pellet fuelling optimisation, DIR, metal-foil pumps, asymmetric/tritium-lean fuelling, spin-polarised fuel R&D |
| TR-5 | Permeation and unaccounted losses exceed ~10⁻⁵ per pass at power-plant throughput | All | med | +3–10 yr; can erase the breeding surplus and block licensing | H3AT/UNITY-2 loop loss data; barrier performance under irradiation | Permeation barriers, low-temperature heat exchangers, double-walled components, protium swamping |
| TR-6 | Tritium accountancy (MUF) cannot meet regulator limits at kg/day throughput | All | med | +2–5 yr licensing delay | Regulators' fusion-specific tritium rules (UK, US NRC Part 30, Canada); H3AT/SRNL demonstration of real-time accountancy | Inline calorimetry/Raman; small, segmented inventories; early regulator engagement |
| TR-7 | Retention in PFCs/blanket (incl. neutron-induced traps) drives in-vessel inventory to administrative limits | Tokamak, Stellarator | med | +1–4 yr; reduced availability | ITER/JET/WEST retention data; ITER DT-1 inventory evolution against 700 g administrative limit | Hot walls, W-based PFCs, periodic detritiation; liquid-metal PFCs |
| TR-8 | Liquid breeder (LiPb, FLiBe) engineering: MHD, corrosion, Be/FLiBe chemistry, tritium extraction efficiency | Tokamak (ARC, DCLL/WCLL), ICF (thick liquid walls) | med | +3–8 yr; may force blanket change | LIBRA/LIBRTI FLiBe extraction efficiency; HASTE loop results; FCI irradiation data | Parallel solid-breeder option; flow-channel insert qualification; staged blanket in ARC |
| TR-9 | IFE target-factory inventory and fill/layer throughput incompatible with < few kg in-plant inventory | Laser ICF | high | +10–20 yr, possibly pathway-limiting | No rep-rate fill/layer demonstration by ~2032 | Injection-filled foam targets, fast layering, tritium-lean targets |
| TR-10 | ITER DT further delayed or descoped, removing TBM data and pushing more tritium demand into the 2040s–2050s | Tokamak (indirectly Stellarator) | med | +2–5 yr for blanket validation | ITER Council schedule updates; TBM PDR/FDR slippage | Rely more on BEST/ARC/LIBRTI; retain TBM programme budget |
| TR-11 | Safety/regulatory event (tritium release) at a fuel-cycle or DT facility triggers stricter limits | All | low | +2–5 yr sector-wide | Incident reports; regulator rule-making | Conservative inventories, confinement design, transparent reporting |
| TR-12 | Beryllium supply/toxicity constraints for HCPB/HCCP and FLiBe at fleet scale | Tokamak, Stellarator (Be multiplier), ICF (FLiBe) | low | +0–3 yr for first demo; fleet-level constraint | Be price, supplier capacity, STEP/ARC Be procurement | Pb-based multipliers, Be recycling, enriched ⁶Li to reduce Be mass |

### Gate definition

**Gate (Tritium self-sufficiency):** *Breeding blanket and closed fuel cycle demonstrated in a fusion nuclear environment with net TBR margin sufficient for self-sufficiency, and start-up inventory for a first demonstration power plant secured.*

As used in the model, the gate year is the first year in which **all** of the following hold for a given pathway:

1. **Fusion nuclear environment**: a breeding blanket (full blanket or blanket sectors covering a representative fraction of the first wall) has operated in a DT fusion device of that pathway (tokamak, stellarator, or IFE chamber) — not only under an accelerator- or generator-based 14 MeV source — at a neutron wall load ≥ ~0.5 MW m⁻² for cumulative operation of at least several months.
2. **Measured breeding**: tritium production has been measured (not only computed), and an as-built, validated neutronics model extrapolated to the pathway's demo-plant design gives a **net TBR ≥ the required TBR plus ≥ 0.05 margin** (in practice net TBR ≳ 1.05–1.10), with recovery, retention and losses measured in that operation.
3. **Closed fuel cycle**: tritium from exhaust and blanket has been recovered, purified, isotopically separated and re-injected continuously, with per-pass losses ≲ 10⁻⁴ and an accountancy closure accepted by a regulator.
4. **Start-up inventory**: a contract, allocation or in-house production plan covering the full start-up inventory of the pathway's first demonstration power plant exists and is deliverable by its planned start.

The gate is *not* met by ITER TBM operation alone (no net breeding) nor by LIBRTI/LIBRA (no plasma environment); it could be met by a breeding-capable BEST, by ARC operating its FLiBe blanket in DT, by an FNSF/VNS, or by a demo plant's own first operating phase.

### Model parameters

These are **calibrated expert judgments** by the author of this report, grounded in the evidence above (2024 ITER baseline, BEST and ARC schedules, LIBRTI/H3AT/UNITY-2 timelines, published TBR margins, HWR stockpile projections). They are not outputs of a formal elicitation. Percentiles are calendar years for the gate defined above, **conditional on the gate being reached** in that pathway; the show-stopper column is the separate probability that the pathway never reaches the gate by 2100 for reasons tied to this challenge.

| Pathway | P0 | P10 | P50 | P90 | P100 | P(never by 2100, show-stopper) | Rationale |
|---|---|---|---|---|---|---|---|
| Tokamak | 2033 | 2038 | 2048 | 2065 | 2095 | 0.10 | Earliest candidates BEST (DT ~2030+, blanket scope unclear) and ARC FLiBe blanket (2030s); ITER TBMs from 2039 add data but not net breeding; EU DEMO/CFETR-class proof likely 2050s; good coverage geometry, most mature blankets |
| Stellarator | 2038 | 2045 | 2058 | 2080 | 2105 | 0.20 | No DT stellarator before late 2030s; Infinity Two (TBR 1.30 at low fidelity, ~675 g inventory) is the main candidate but schedule is aspirational; 3D blanket geometry and maintenance harder; relies heavily on tokamak blanket/fuel-cycle results |
| Laser ICF | 2042 | 2050 | 2065 | 2088 | 2115 | 0.30 | No IFE chamber with breeding blanket planned; needs rep-rated driver and target factory first; beam-port coverage penalty and target-factory inventory (0.3–10 kg) unresolved; favourable burn-up per target |

**Start-up inventory risk:** probability that the start-up tritium for the *first* demonstration power plant (any pathway) is **not** available when needed: **0.30**. If it is not available, the delay is **P10 = 2 years, P50 = 5 years, P90 = 12 years** (time to accumulate from HWR purchases, DD/tritium-lean start-up, or a breeding predecessor). The probability is lower (~0.15) for sub-kilogram pilot designs (ARC-, Infinity Two-class) and higher (~0.45) for 5–10 kg DEMO-class designs started after ITER DT in the 2040s–2050s.

**Coupling to other challenges** (suggested Spearman rank correlation with the gate year of this challenge):

- **Plasma burning performance: ρ ≈ +0.50** — burn fraction/fuelling efficiency set required TBR and start-up inventory, and a breeding demonstration needs a sustained DT burning plasma (ARC, BEST, DEMO) in the first place.
- **Materials qualification: ρ ≈ +0.60** — blanket structures, permeation barriers and breeders need irradiation qualification; the same missing fusion-neutron facility (FNSF/VNS, IFMIF-DONES) gates both.
- **Power exhaust / divertor: ρ ≈ +0.35** — divertor and port area reduce blanket coverage; PFC retention drives in-vessel inventory; divertor pumping sets fuel-cycle throughput.
- **Driver / magnets / steady-state: ρ ≈ +0.45** — duty factor and availability determine breeding surplus, doubling time and whether months of cumulative operation are reached; for ICF, driver rep-rate and target delivery are prerequisites.

**Discrete breakthrough/setback events:**

- *Breakthrough*: LIBRTI or LIBRA measures local TBR ≥ 1 in a full-thickness mock-up consistent with prediction by 2030 — p = 0.35; effect −2 years (all pathways, via design confidence).
- *Breakthrough*: ARC (or BEST) demonstrates net tritium production from its blanket in DT operation before 2038 — p = 0.20; effect −5 years for Tokamak, −3 years for Stellarator.
- *Breakthrough*: spin-polarised or tritium-lean fuelling demonstrated with ≥ 2× burn efficiency — p = 0.10 by 2040; effect −2 years and start-up inventory risk halved.
- *Setback*: further ITER DT slip beyond 2042 or TBM descoping — p = 0.40; effect +2 years (Tokamak, Stellarator).
- *Setback*: tritium release incident or regulatory tightening at a DT/fuel-cycle facility — p = 0.10; effect +3 years (all pathways).
- *Setback*: HWR supply shock (Canadian export/allocation policy, accelerated CANDU retirements, non-fusion demand e.g. He-3) — p = 0.15; effect +4 years on the start-up inventory component.

## Changelog (2026-11)

- Header date changed to "November 2026 update".
- Global civil stockpile corrected from 25–30 kg to ~20–25 kg (2025 estimate ~20 kg); price range corrected to ~$25–35k/g; "twice the stockpile per GW-year" corrected to 2–3×.
- ITER DT start updated to 2039 (2024 baseline, previously "2035–2036"); ITER lifetime consumption corrected from "5–10 kg" to the ~12.3 kg unofficial estimate; erroneous "0.9 kg per full-power year" removed (≈28 kg/fpy at 500 MW).
- "A 2025 UKAEA analysis" corrected to Coleman & Kovari (IAEA FEC 2018), with its 7.4 kg (0–28 kg) DEMO availability in 2055.
- Romania contract corrected (June 2023, KHNP EPC, ~€195 M; construction since June 2025).
- "TBR ceiling 1.0 from ⁶Li" clarified; Be/Pb multiplication corrected (2 neutrons per (n,2n) reaction, Be threshold ~1.9 MeV, Pb ~7.4 MeV; blanket-level gain well below 2).
- Fuel-cycle throughput arithmetic fixed (1% burn efficiency → ~45 kg/day; 9 kg/day corresponds to ~5%); permeation example reformulated as per-pass loss on throughput.
- ITER in-vessel limit clarified: 1 kg safety limit, ~700 g administrative limit.
- ITER TBM programme updated: two ports (#16, #18), four TBS (EU WCLL, EU–KO HCCP, JA WCCB, CN HCCB), DT-1 from 2039, EU PDRs 2026.
- Reddit source (ref. 9) replaced; unverifiable "90 g ARC inventory" removed and replaced with published ARC-like (~0.69 kg) and Infinity Two (~675 g) figures.
- ICF target-factory inventory corrected from "10–20 kg" to "up to ~10 kg" (NAS 2013), with lower-bound designs; ICF TBR penalty marked as indicative.
- BEST description corrected (Burning plasma Experimental Superconducting Tokamak; under construction, first plasma target 2027).
- Added section 7.3 (LIBRTI + CFS, BABY/LIBRA, UNITY-2, FIRE/DOE roadmap, UK–Canada, Infinity Two, STEP breeder choice, Cernavoda), TRL table rows, and the Risk Assessment section.

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

9. [Unlocking Tritium for Fusion Energy (RSIS Commentary CO25215, 29 October 2025)](https://rsis.edu.sg/rsis-publication/rsis/unlocking-tritium-for-fusion-energy/) - Estimates the current global tritium stockpile at about 20 kg and ~14 kg by 2055 under moderate assumptions. (Replaces a Reddit thread cited in the June 2026 version.)

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

45. [ITER baseline press conference summary, July 2024](https://iter.org/sites/default/files/media/2024-07/baseline_press_conference_summary_july-2024_b.pdf) - Start of Research Operation 2034; start of DT operation moved from 2035 to 2039.

46. [L. Giancarli, ITER TBM Program overview (IAEA technical meeting, 2025)](https://conferences.iaea.org/event/406/contributions/37064/attachments/20785/35166/Luciano%20Giancarli%20-%20ITER.pdf) - DT-1/DT-2 phases; four TBS in equatorial ports #16 and #18; design by 2029, installation from 2035, operation from 2039.

47. [Fusion for Energy: ITER Test Blanket Modules move forward (6 August 2026)](https://fusionforenergy.europa.eu/news/iter-test-blanket-modules-preliminary-design-review/) - Preliminary design reviews of the EU WCLL and HCCP TBMs.

48. [Kinectrics selected as design & fabrication partner for UKAEA-Eni Tritium Loop Facility (16 March 2026)](https://www.bnnbloomberg.ca/press-releases/2026/03/16/kinectrics-selected-as-design-fabrication-partner-for-ukaea-eni-tritium-loop-facility/)

49. [UKAEA and Canadian Nuclear Laboratories partner to accelerate fusion energy development (February 2024)](https://www.ukaea.org/news/united-kingdom-atomic-energy-authority-and-canadian-nuclear-laboratories-partner-to-accelerate-fusion-energy-development/)

50. [Isotopes from OPG's nuclear fleet advancing fusion energy research (OPG, November 2025)](https://interactive.opg.com/2025-november/watts-new/isotopes-from-opgs-nuclear-fleet-advancing-fusion-energy-research) - Context of the OPG–UKAEA tritium supply MoU of 22 September 2025.

51. [Delaporte-Mathurin et al., Advancing Tritium Self-Sufficiency in Fusion Power Plants: Insights from the BABY Experiment, Nucl. Fusion 65 (2025) 026037](https://arxiv.org/abs/2412.02721)

52. [BABY 1L: First Tritium Breeding Campaign Results (arXiv:2509.26174, 2025)](https://arxiv.org/abs/2509.26174)

53. [UKAEA: LIBRTI — The Lithium Breeding Tritium Innovation Programme](https://www.ukaea.org/work/librti/)

54. [CFS named first international partner in UKAEA's LIBRTI program (July 2026)](https://cfs.energy/news-and-media/cfs-named-first-international-partner-in-ukaeas-librti-program/)

55. [General Atomics invests $20 million in Canadian fusion venture to advance tritium fuel cycle technologies (UNITY-2)](https://www.ga.com/ga-invests-20-million-in-canadian-nuclear-fusion-venture-to-advance-tritium-fuel-cycle-technologies); [Kyoto Fusioneering: UNITY-2 construction start (November 2025)](https://kyotofusioneering.com/en/news/2025/11/04/3556)

56. [INL: Fusion for the future — nuclear lab plays key role in testing a crucial technology (FIRE Collaboratives)](https://inl.gov/feature-story/fusion-for-the-future-nuclear-lab-plays-key-role-in-testing-a-crucial-technology)

57. [ANS Nuclear Newswire: DOE's latest fusion energy road map aims to bridge known gaps (17 October 2025)](https://www.ans.org/news/2025-10-17/article-7466/does-latest-fusion-energy-road-map-aims-to-bridge-known-gaps)

58. [EUROfusion and ASIPP have released the BEST Research Plan](https://euro-fusion.org/eurofusion-news/eurofusion-asipp-best-research-plan/); [CGTN: China's artificial sun project enters key construction phase (1 October 2026)](https://news.cgtn.com/news/2026-10-01/China-s-artificial-sun-project-enters-key-construction-phase-1QSYBsXj0d2/p.html)

59. [Clark et al., Breeder blanket and tritium fuel cycle feasibility of the Infinity Two fusion pilot plant, J. Plasma Phys. (2025)](https://www.cambridge.org/core/product/248C49CCA0B7ABEA2F7BF7031290EDC4)

60. [S. Meschini, Tritium fuel cycle modelling for ARC- and STEP-class plants (PPPL NSTX seminar, September 2024)](https://nstx.pppl.gov/DragNDrop/NSTX_Meetings/Monday_Physics_Meetings/2024/2024_09_09/Meschini_NSTX_seminar.pdf) - TBE as figure of merit (Whyte et al. 2023; Meschini et al. 2023, Nucl. Fusion 63 126005); ITER TBE ≈ 0.36%.

61. [Parisi, Diallo, Schwartz, Simultaneous enhancement of tritium burn efficiency and fusion power with low-tritium spin-polarized fuel, Nucl. Fusion (2024), arXiv:2406.05970](https://arxiv.org/abs/2406.05970)

62. [WNN: First concrete poured for Europe's first tritium removal facility (June 2025)](https://wnn.world-nuclear.org/articles/first-concrete-poured-for-europes-first-tritium-removal-facility); [WNN: Contract for Cernavoda tritium removal facility (June 2023)](https://world-nuclear-news.org/articles/contract-for-cernavoda-tritium-removal-facility)

63. [J. Roth et al., Tritium inventory in ITER plasma-facing materials and tritium removal procedures (review)](https://pure.mpg.de/pubman/item/item_2142377_1/component/file_2142376/Roth_Tritium.pdf) - 1 kg in-vessel safety limit; administrative limit evolution (330 g → ~700 g).

64. [STEP breeding blanket selection abstract, 2nd Fusion Neutronics Meeting, KIT, June 2026](https://indico.kit.edu/event/5433/contributions/22944/) - Conference abstract only; Li₂O ceramic breeder, Be-based multiplier, CO₂ coolant.

65. [Meschini et al., Nucl. Fusion 65 (2025) 036010 — impact of tritium trapping on fuel-cycle performance](https://iris.polito.it/bitstream/11583/3002926/2/Meschini_2025_Nucl._Fusion_65_036010.pdf) - Trapping raises ARC-class start-up inventory ~30%, doubling time ~50%, required TBR 2–5%.
