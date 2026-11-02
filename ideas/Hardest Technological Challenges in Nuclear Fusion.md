# Nuclear Fusion: The 5 Hardest Technological Challenges
### A Deep-Dive Analysis Across Tokamak, Stellarator, and Laser-Driven Inertial Confinement Fusion

*Objective research report — November 2026 update*

***

## Executive Summary

Fusion has accumulated more proof-points in 2021–2026 than in any earlier period. NIF reached ignition in December 2022 (3.15 MJ from 2.05 MJ of laser energy) and set its yield record of 8.6 MJ from 2.08 MJ (target gain 4.13) on 7 April 2025, with ten ignition shots by October 2025. Commonwealth Fusion Systems' Toroidal Field Model Coil reached 20 T in September 2021, and a full-scale SPARC TF magnet was validated under DOE's milestone programme in September 2025. In 2025 EAST (1,066 s H-mode), WEST (1,337 s) and Wendelstein 7-X (tokamak-class triple product held for 43 s; a 360 s, 1.8 GJ discharge) set long-pulse records.[^2][^3][^52][^54][^55][^56][^57][^58][^64][^65] Even so, commercial fusion energy still faces five systemic technological challenges. They are intertwined, unresolved, and arguably harder than achieving ignition itself. No magnetic-confinement device has yet produced Q > 1, and the first MCF burning-plasma tests have slipped: ITER's 2024 baseline puts DT operation in 2039, and SPARC's first plasma is now expected in 2027.[^60][^62][^63] This report identifies, decomposes and cross-maps the five challenges across the three leading realization pathways: **Tokamak** (T), **Stellarator** (S) and **Laser-Driven Inertial Confinement Fusion** (ICF).[^1][^4]

The five challenges are:

1. **Plasma Stability, Confinement & Turbulent Transport** — keeping the fuel hot and dense long enough
2. **Plasma-Facing Materials & Neutron Damage** — building a wall that survives the fusion environment
3. **Tritium Fuel Self-Sufficiency** — closing the fuel cycle with a net-positive breeding ratio
4. **Power Exhaust & Heat Removal** — handling gigawatt-scale heat fluxes without destroying the device
5. **Driver/Magnet Engineering & Steady-State Operation** — scaling the energy system to power-plant requirements

Each challenge is rated by technology readiness and cross-mapped to the three pathways. Each has a dedicated deep-dive report in this folder with a November 2026 risk assessment; the section [Integrated Risk Assessment (November 2026)](#integrated-risk-assessment-november-2026) consolidates their risk registers, gate definitions, gate-year distributions and couplings.

***

## Status November 2026

### Key milestones 2025–2026

| Date | Milestone | Challenge(s) |
|---|---|---|
| Jan–Feb 2025 | EAST holds a 1,066 s H-mode plasma (RF-sustained, ~60 % Greenwald); WEST (all-tungsten, actively cooled) holds 1,337 s at ~2 MW with 2.6 GJ injected and extracted.[^57][^58] | 1, 4, 5 |
| 7 Apr 2025 | NIF record: 8.6 MJ from 2.08 MJ, target gain 4.13. Tenth ignition shot on 1 Oct 2025. Optics damage limited laser energy in 2025–2026. Enhanced Yield Capability (2.6 MJ, > 30 MJ yield predicted) passed conceptual design review in June 2025.[^52][^53][^54] | 1, 5 |
| May 2025 | W7-X sets a world-best triple product for long plasmas (43 s) and a 360 s, 1.8 GJ discharge with an actively cooled island divertor.[^55][^56] | 1, 4, 5 |
| May / Sep 2025 | MAST-U Super-X divertor: ~18.5× lower peak target heat flux than a conventional divertor, measured in L-mode at ~1.2 MW SOL power. Feedback control of detachment followed. AUG and JET DT plasmas extend X-point-radiator control (~95 % dissipation on AUG).[^42][^43][^93][^94] | 4 |
| Sep 2025 | DOE milestone panel validates CFS's full-scale SPARC TF magnet. Tokamak Energy's Demo4 HTS magnet set reaches 11.8 T in Nov 2025.[^64][^99] | 5 |
| Nov 2025 | Multilateral International DONES Agreement signed (Spain 55 %, EU 25 %, Italy 8 %, Japan 5.1 %, Croatia 5 %). The building permit followed in Jun 2026 and Main Building site works began in Sep 2026, with the building targeted for 2029.[^70][^71][^72] | 2 |
| 2025–2026 | Tritium infrastructure: Cernavoda tritium removal facility under construction (completion ~2027); UNITY-2 fuel-cycle loop under construction at Chalk River (Nov 2025); H3AT design partner selected (Mar 2026); CFS joins UKAEA's LIBRTI breeding programme (Jul 2026).[^83][^85][^86][^87] | 3 |
| 2025–2026 | SPARC ~75 % complete. TF magnet installation began in Jan 2026, but only 8 of 18 were installed by 22 Sep 2026 (plan: all by end of summer). First plasma now expected in 2027.[^62][^63] | 1, 5 |
| 2025–2026 | Finance and programmes: Google (200 MW) and Eni (> $1 B) offtake from ARC; Proxima Fusion €411 M (Jul 2026); Focused Energy ~$240 M (May 2026); TAE–Trump Media merger (announced Dec 2025); UK £2.5 B over five years; German action plan > €2 B to 2029; China Fusion Energy Co. founded (Jul 2025).[^67][^100][^105][^109][^113][^114][^118][^119] | 5 |
| Feb 2026 | US NRC proposed rule places fusion under the byproduct-material framework (10 CFR Part 30). The final rule was planned for fall 2026, but publication could not be confirmed as of 2 Nov 2026. The UK (Energy Act 2023 s.156) and Germany (Radiation Protection Act) also regulate proportionately.[^110][^111][^112][^114] | 5 (licensing), 3 |
| Jun 2026 | DOE finalizes its Fusion S&T Roadmap. Xcimer's Phoenix excimer laser prototype starts operation. DOE approves Xcimer's pre-conceptual Athena plant design.[^103][^104][^115] | 5 |

### Decision points 2027–2035

| When | Decision point | What it resolves |
|---|---|---|
| 2026–2027 | W7-X campaigns OP2.4 (Aug–Dec 2026) and OP2.5 (Feb–May 2027)[^117] | Stellarator steady-state at higher T\(_i\) and β; turbulence at higher heating (PL-7, EX-8) |
| 2027 | **SPARC first plasma**; Q > 1 attempted 2027–2028 (Google's PPA is contingent on it)[^62][^118] | Compact high-field HTS route, first significant MCF alpha heating, exhaust at q\(_\parallel\) > 10 GW m\(^{-2}\) (DR-1, PL-5, EX-12) |
| End-2027 | **BEST** (Hefei) completion; burning-plasma experiments announced from 2027, power-generation demonstration ~2030[^66][^67] | Second compact burning-plasma tokamak; possible first in-plasma breeding data, though the scope is unclear (TR-2) |
| 2027 | JT-60SA scientific campaigns resume from end-2026; LIBRTI neutron source ~2027; Cernavoda tritium removal facility[^68][^84][^87] | High-β/steady-state scenarios; breeding mock-up neutronics; third HWR tritium seller |
| By 31 Dec 2027 | US NRC final fusion rule (NEIMA deadline)[^111] | First proportionate licensing route exercised (DR-10) |
| 2028 | Xcimer Anvil (~200 kJ); MAST-U high-power sixth campaign; Helion Orion electricity target; H3AT tritium loop (2028–2030)[^82][^95][^103][^107] | Excimer driver efficiency at scale (DR-7); ADC at high power (EX-3); closed non-breeding fuel cycle (TR-5) |
| 2029 | IFMIF-DONES Main Building substantially complete[^71] | First milestone on the materials critical path (MA-1) |
| ~2030 | EU DEMO conceptual design complete; engineering design 2030–2040[^116] | Whether EU DEMO converges on a stable reference design |
| ~2031 | **Proxima Fusion Alpha** demonstration stellarator (Garching). Total cost ~€2 B; the requested €1.2 B federal share was not committed as of mid-2026.[^100][^101] | Reactor-relevant HTS non-planar coils (DR-6); funding of the stellarator route (PL-7) |
| Jul 2032 | **DTT** (Frascati) first plasma per the 2025 IAEA poster. Full heating and advanced-divertor phases are unlikely to produce DEMO-relevant exhaust results before ~2036–2040.[^96][^97] | Exhaust at P\(_{sep}\)/R ≈ 15 MW m\(^{-1}\) (EX-2, EX-3, EX-4) |
| Early 2030s | ARC grid connection (Virginia); STEP construction start; Focused Energy's Biblis plant (mid-2030s)[^105][^106][^113][^118] | First FOAK power plants: availability, licensing, financing (DR-9 – DR-12) |
| ~2033–2035 | **IFMIF-DONES first neutrons** (no official date; ~2034 most cited). ≥ 10 dpa data expected ~2037–2039.[^71][^73] | Fusion-spectrum materials data for licensing (MA-1, MA-2, MA-5) |
| 2034 → 2039 | **ITER** Start of Research Operation 2034, full magnetic energy 2036, DT 2039. First disruption-mitigation-system injection 2034.[^60][^126] | Q = 10 at reactor scale, disruption/RE mitigation, ELM control, TBMs (PL-1, PL-6, TR-10) |

***

## Challenge Overview Matrix

| Challenge | Tokamak | Stellarator | Laser ICF | TRL (2026) |
|---|---|---|---|---|
| Plasma stability & turbulent transport | Critical (disruptions, ELMs) | Moderate (no disruptions, turbulence remains) | Critical (RT instability, symmetry, gain ≈ 4 vs. ~30–50 needed) | 4–5 (alpha-particle physics 2–3) |
| Plasma-facing materials & neutron damage | Critical | Critical | Critical (first wall + optics) | 3–5 (baseline materials MTRL 4–5; no fusion-spectrum data) |
| Tritium self-sufficiency | Critical | Critical | Critical | 2–4 (no blanket test in a fusion environment) |
| Power exhaust & heat removal | Critical (divertor) | Moderate (island divertor) | Severe (cyclic shock loading) | 4–5 MCF; 1–2 IFE first wall |
| Driver/magnet engineering & steady-state | High (pulsed vs. steady-state) | Moderate (coil complexity) | Severe (laser efficiency, rep-rate, target factory) | 2–6 (SPARC HTS 6; target factory 1–2) |

***

## Challenge 1: Plasma Stability, Confinement & Turbulent Transport

*Deep dive: [Challenge Plasma Stability, Confinement & Turbulent Transport.md](Challenge%20Plasma%20Stability,%20Confinement%20&%20Turbulent%20Transport.md)*

### Core Problem Statement

The fusion triple product \(n \cdot T \cdot \tau_E\) must exceed roughly \(3 \times 10^{21}\) keV·s·m\(^{-3}\) for ignition in a magnetically confined plasma. Here \(n\) is the plasma density, \(T\) the temperature and \(\tau_E\) the energy confinement time. Reaching it means sustaining temperatures above 100 million °C while confining the plasma for long durations. Instabilities and turbulence undermine both, bleeding energy from the core far faster than classical theory predicts. The best tokamak values (JT-60U, JET) are ~1–1.5 × 10\(^{21}\) keV·s·m\(^{-3}\) in short pulses. JET's 1997 DT shot remains the fusion-power record (16 MW, Q ≈ 0.62–0.67). Its 2021 and 2023 campaigns set fusion-energy records of 59 MJ and 69 MJ at Q ≈ 0.3.[^5][^69][^124]

### Tokamak: Disruptions and ELMs

A tokamak's plasma current makes the configuration inherently fragile. A **disruption** is a sudden, total loss of confinement that releases the stored thermal and magnetic energy within milliseconds. Present devices disrupt in ~10 % of pulses, whereas ITER at full current needs ≤ 1 %. Unmitigated ITER disruptions could convert ~10–12 MA of the 15 MA plasma current into runaway-electron beams carrying ~20–200 MJ. ITER's disruption mitigation system (27 shattered-pellet injectors, first injection 2034) is designed but not yet validated.[^126] AI-based prediction and control have advanced: reinforcement-learning tearing-mode avoidance was shown on DIII-D, and DeepMind and CFS are applying AI to SPARC scenario design. Predictors trained on today's machines must still work under the distribution shift to ITER conditions.[^6][^8][^123]

At the edge, **Edge-Localized Modes (ELMs)** periodically eject bursts of energy onto plasma-facing components. Projected parallel ELM energy fluences for SPARC and ITER are ~11–34 MJ m\(^{-2}\), far above material limits. RMP coils suppress ELMs in present devices, and ELM-free regimes (QCE, QH-mode, I-mode, negative triangularity, X-point radiator) have been demonstrated, but none yet under reactor pedestal conditions.[^9][^1]

**Anomalous (turbulent) transport** remains the dominant energy-loss channel in every operating regime. Ion-temperature-gradient (ITG) and trapped-electron-mode (TEM) microturbulence carries heat from the core to the edge. Multi-scale interactions with electron-scale turbulence can raise losses well above single-scale predictions, and the pedestal transport mechanism remains an open scientific problem. EAST's 2026 operation at 1.3–1.65× the Greenwald density shows that operating limits are still being revised.[^10][^11][^12][^13][^59]

### Stellarator: Neoclassical Transport vs. Turbulence

Stellarators avoid current-driven disruptions by eliminating the large plasma current. W7-X has confirmed that optimized 3D shaping suppresses **neoclassical transport**. Its peak short-pulse triple product (2018) was ~6 × 10\(^{19}\) keV·s·m\(^{-3}\). In May 2025 it sustained a tokamak-class triple product for 43 s with pellet fuelling, the best value for plasmas longer than 10 s.[^14][^15][^55][^56] Once neoclassical losses are suppressed, **turbulent transport takes their place**. W7-X ion temperatures are clamped at ~3 keV, a factor ~5 below reactor requirements, and no burning-plasma stellarator is funded. Proxima Fusion's Alpha (~2031) is a sub-burning demonstrator.[^16][^17][^100]

### Laser ICF: Rayleigh–Taylor Instability and Implosion Symmetry

A millimetre-scale capsule is imploded at ~350–400 km/s, and any drive or surface non-uniformity is amplified by the **Rayleigh–Taylor instability (RTI)** in both the acceleration and deceleration phases. Required tolerances are at the sub-µm to 10 µm level for surface finish, with sub-percent uniformity in shell thickness. NIF's hohlraum couples only ~10–15 % of the laser energy to the capsule. The April 2025 record (gain 4.13) came from target improvements, notably continuous gradient doping of the ablator. A power plant needs gain of ~30–100 together with ≥ 10 % efficient drivers, which is more than an order of magnitude beyond today. Shot-to-shot variability and the optics-damage constraints of 2025–2026 limit the pace of learning.[^18][^19][^20][^22][^52][^53]

### Burning Plasma: The Untested Regime

Alpha-particle-driven Alfvén eigenmodes have never been observed with fusion-born alpha parameters. SPARC (2027+) and BEST (end-2027+) may reach alpha-relevant conditions before ITER's DT phase (2039), but only ITER is designed to test Q = 10 at reactor scale. Its Q = 10 demonstration is unlikely before the early-to-mid 2040s.[^4][^60][^66]

### Key Open Questions for Further Analysis

- Can disruption predictors trained on existing machines transfer to ITER/DEMO-scale currents and reach ≤ 1 % disruption rates?
- What is the quantitative scaling of turbulent transport to burning-plasma temperatures in stellarators?
- Will alpha-driven Alfvén eigenmodes be benign or cause a self-limiting burn?
- Can laser beam smoothing and magnetized implosions reduce RTI seeds enough to reach gain ≥ 30–50?[^23][^24]

***

## Challenge 2: Plasma-Facing Materials (PFMs) and Neutron Damage

*Deep dive: [Challenge Plasma-Facing Materials & Neutron Damage.md](Challenge%20Plasma-Facing%20Materials%20&%20Neutron%20Damage.md)*

### Core Problem Statement

In a DT reactor, 80 % of the fusion energy is carried by 14.1 MeV neutrons. These displace lattice atoms and transmute nuclei at rates no fission environment reproduces. DEMO front-wall steel (EUROFER97) accumulates ~12–15 dpa per full-power year (fpy), and tungsten armour ~6–9 dpa/fpy. The starter blanket's ~20 dpa design limit therefore corresponds to only ~1.3–1.7 fpy, while 5 fpy gives ~60–75 dpa in steel. EUROfusion rates its baseline materials (EUROFER97, W, CuCrZr) at Materials TRL ~4–5. MTRL 7, the target for DEMO, requires fusion-spectrum irradiation data that do not yet exist.[^25][^26][^76]

### Tungsten: The Leading PFM Candidate

Tungsten is the primary armour candidate thanks to its heat resistance, high sputtering threshold and low tritium retention when unirradiated. Under neutron irradiation it degrades in several ways:[^27][^28][^29]

- **Embrittlement**: the ductile-to-brittle transition temperature rises, possibly above the operating temperature
- **Transmutation** to Re and Os (several at.% Re and ~1–3 at.% Os after 5–10 fpy, position-dependent), with Os particularly embrittling[^27]
- **Thermal conductivity loss**, **void swelling** and increased **tritium trapping** at neutron-induced defects

### The Missing Neutron Source: IFMIF-DONES

No facility today provides 14 MeV-dominated neutron fluxes at reactor-relevant fluence. **IFMIF-DONES** (Granada) is now funded and under construction. Its 40 MeV, 125 mA deuteron beam on a liquid-lithium target is designed for 12–25 dpa/fpy in the high-flux module. Expected timeline: Main Building complete 2029, first neutrons ~2033–2035, ≥ 10 dpa post-irradiation data ~2037–2039, ~20 dpa ~2039–2041. The prototype accelerator LIPAc has reached 125 mA only at 5 MeV in pulsed mode. The US FPNS, Japan's A-FNS and China's CFNS have no construction decision. Private pilot plants targeting the 2030s will therefore have to license **without** fusion-spectrum data at their end-of-life dose.[^70][^71][^72][^73][^77]

### Tokamak and Stellarator: Shared but Geometrically Distinct Challenges

- In tokamaks, the **divertor** sustains the highest heat and particle fluxes; erosion-limited replacement every 1–3 fpy is expected
- In stellarators, the **3D geometry** constrains blanket design, coil shielding and port access, making module replacement and remote maintenance harder[^31]

After shutdown the activated structure is a strong gamma source. ITER's in-vessel remote-handling equipment is specified for ~250 Gy h\(^{-1}\). DEMO blanket components at shutdown are estimated at ~13–17 kGy h\(^{-1}\) and divertor cassettes at ~9–12 kGy h\(^{-1}\), roughly two orders of magnitude above ITER. Reaching ITER-like levels would take about five years of cooling. All in-vessel maintenance must therefore be fully remote, with radiation-hardened tooling. (The earlier figure of ~5 × 10\(^5\) Sv h\(^{-1}\) is not supported by the sources and has been withdrawn.)[^32][^74][^75]

### Laser ICF: First Wall and Optics Damage

The energy of each microexplosion scales with yield: a 40 MJ shot equals ≈ 10 kg TNT, and plant yields of 100–1,000 MJ equal ~25–240 kg TNT. At 5–10 Hz the chamber sees **4.3–8.6 × 10\(^5\) shots per day**, or ~4–8 × 10\(^9\) shots over a 30-year life at ~85 % availability. Dry walls must survive very-high-cycle fatigue, X-ray and debris ablation. Thick liquid walls (HYLIFE-type FLiBe jets) avoid high-dpa structures but must re-form within ~0.1–0.2 s. The laser **final optics** must survive debris, neutron- and gamma-induced absorption at rep-rate. NIF's 2025–2026 optics-damage constraints, at a few shots per day, illustrate the scale of the problem.[^30][^33][^34][^35][^53]

### Key Open Questions for Further Analysis

- Will EUROFER97 and tungsten retain adequate ductility at 10–20 dpa with fusion-relevant He/dpa ratios?
- Will regulators accept lifetime-limited starter blankets licensed on fission/ion data plus early (≤ 5 dpa) DONES data?
- What remote-maintenance change-out time is compatible with economic availability, especially for stellarators?
- How can laser final optics be engineered to survive IFE rep-rate conditions?

***

## Challenge 3: Tritium Fuel Self-Sufficiency

*Deep dive: [Challenge Tritium Fuel Self-Sufficiency.md](Challenge%20Tritium%20Fuel%20Self-Sufficiency.md)*

### Core Problem Statement

All near-term concepts rely on the DT reaction. Tritium does not occur naturally in useful quantities. The global civil stockpile, mostly from Canadian CANDU reactors, is only of order **20–25 kg**; a 2025 estimate puts it at ~20 kg. Tritium decays at 5.47 % per year and sells at ~$25,000–35,000 per gram. A **1 GW (fusion) plant burns ~55.6 kg of tritium per full-power year (~150 g/day)**, so one year of full-power operation would consume 2–3 times the entire civil stockpile. Today's stockpile would last only about four to five full-power months of such a plant.[^78][^79][^80] ITER (DT from 2039) will burn ~28 kg per *full-power* year at 500 MW, but its low duty factor limits consumption to an unofficial lifetime estimate of ~12.3 kg. ITER does not breed tritium. A UKAEA analysis (Coleman & Kovari, 2018) leaves ~7.4 kg (scenario range 0–28 kg) of heavy-water-reactor tritium available for a DEMO in 2055. Partial mitigations are the UKAEA–CNL tritium partnership (2024) and an OPG–UKAEA supply memorandum (September 2025).[^60][^79][^88]

The solution is to breed tritium in a **breeding blanket** that surrounds the plasma, using lithium:

\[^6\text{Li} + n \rightarrow T + ^4\text{He} + 4.8 \text{ MeV}\]
\[^7\text{Li} + n \rightarrow T + ^4\text{He} + n' - 2.5 \text{ MeV}\]

The figure of merit is the **Tritium Breeding Ratio (TBR)**: tritium atoms produced per tritium atom burned. Net TBR must exceed ~1.05–1.15 to cover losses, decay, inventory and doubling time.[^37][^38]

### Why TBR > 1 Is Not Guaranteed

Each DT reaction yields exactly **one neutron**. ⁶Li capture alone gives at most one triton per neutron, so TBR > 1 relies on neutron multiplication via Be(n,2n), Pb(n,2n) and ⁷Li(n,n'α)t, and every port, rib and coolant channel costs margin. Full 3D neutronics give **~1.03–1.10** for the main EU blanket concepts (HCPB, WCLL, DCLL), against ~1.14–1.22 in idealized 1D models. The TBR drops ~0.04–0.06 per percentage point of lost blanket coverage. Losses scale with fuel-cycle **throughput**, not inventory: at 1 % burn efficiency a 3 GW plant processes ~45 kg of tritium per day. Abdou et al. (2021) concluded that current physics and technology cannot guarantee self-sufficiency or the start-up inventories for DEMO and power plants.[^39][^81]

### Blanket Technology and 2025–2026 Developments

HCPB, WCLL and DCLL blankets each trade structural compatibility, extraction kinetics, MHD effects and coverage. Liquid FLiBe blankets (ARC) and solid Li\(_2\)O ceramic breeders (reported for STEP) are also being pursued.[^40] Non-plasma test infrastructure grew markedly in 2025–2026:

- **H3AT** (UKAEA–Eni, Culham, 100 g inventory, 2028–2030) tests the closed non-breeding fuel cycle
- **UNITY-2** (Chalk River) is an integrated loop circulating up to 30 g of tritium per day
- **LIBRTI** (UK, 14 MeV DT neutron source ~2027) tests breeder mock-ups; CFS joined in July 2026
- **BABY/LIBRA** (US) measured molten-salt breeding under 14 MeV neutrons[^82][^83][^84][^85][^86][^89]

No breeding blanket has yet operated in a fusion plasma environment. ITER's four test blanket systems (from DT-1, 2039) will not demonstrate net breeding. The earliest in-plasma tests are BEST (~2030+, scope unclear) and ARC's FLiBe blanket (2030s), and no dedicated Fusion Nuclear Science Facility is funded.[^81][^90]

### Laser ICF: An Especially Severe Problem

Long target fill and layering times can produce in-plant inventories **up to ~10 kg** (US National Academies, 2013). Injection-filled foam targets bring this down to ~0.3 kg, so target design is the dominant lever. Even ~10 kg is about half the civil stockpile. Beam ports penetrate the spherical blanket, an indicative penalty of 0.05–0.15 in TBR, which may push some designs below TBR = 1. On the positive side, ICF burns ~20–30 % of the fuel in each capsule.[^21][^41][^91]

### Key Open Questions for Further Analysis

- Can engineering-fidelity designs keep net TBR ≥ 1.05 after ports, manifolds and trapping, and will LIBRTI/LIBRA mock-ups confirm the neutronics?
- How much start-up tritium will the first demonstration plants need, and can sub-kilogram designs (ARC-class ~0.7 kg; Infinity Two ~675 g) avoid the supply crunch?[^125]
- Can tritium accountancy reach gram-level precision at kg/day throughput?
- Is a dedicated tritium source (FNSF, fission production) needed to bridge to the first fleet?

***

## Challenge 4: Power Exhaust and Plasma Heat Removal

*Deep dive: [Challenge Power Exhaust & Divertor Heat Loads.md](Challenge%20Power%20Exhaust%20&%20Divertor%20Heat%20Loads.md)*

### Core Problem Statement

Power crossing the separatrix (~150 MW in EU DEMO, P\(_{sep}\)/R ≈ 17 MW m\(^{-1}\)) flows in a scrape-off layer only **~1 mm wide** at the outboard midplane (empirical Eich scaling). Gyrokinetic XGC1 simulations predict ~6 mm for ITER, which would relax the problem but has not been confirmed. Two distinct quantities must not be confused:

- The **unmitigated perpendicular heat flux on the divertor target** of EU DEMO is ~150 MW m\(^{-2}\), against a steady-state limit of ~5–10 MW m\(^{-2}\) for tungsten on a water-cooled heat sink (~5 MW m\(^{-2}\) once irradiated). That is a **15–30× gap**.
- The corresponding **parallel** heat flux along the field lines is several GW m\(^{-2}\) for DEMO and **> 10 GW m\(^{-2}\)** for compact high-field SPARC.

Without advanced divertors, ~95–97 % of P\(_{sep}\) must be dissipated before reaching the target.[^9][^92][^98]

### Tokamak: Detachment, Advanced Divertors and ELMs

AUG reached ~95 % dissipation with a controlled **X-point radiator** (ELM-suppressed, minor confinement loss), and XPR control was demonstrated in JET DT plasmas in 2025. On MAST-U, the **Super-X divertor** cut the peak target heat flux ~18.5× compared with a conventional divertor and reduced detachment-front sensitivity 5×. A companion paper (Sep 2025) showed feedback control of detachment and passive buffering of transients. These are **L-mode results at ~1 MW SOL power**, two orders of magnitude below DEMO, and the high-power sixth MAST-U campaign is now planned for 2028.[^42][^43][^93][^94][^95]

Type-I ELMs in DEMO would release ~100 MJ each and must be reduced ≥ 10× (up to ~200×) or avoided by ELM-free regimes. ITER's monoblocks require ELM surface energy densities below ~0.15 MJ m\(^{-2}\) to avoid edge melting. Mitigation strategies:

- **Impurity seeding** (N, Ne, Ar) and XPR to radiate power before it reaches the target
- **ELM control**: RMP suppression, pellet pacing, ELM-free regimes
- **Advanced divertor geometries**: Super-X, X-point target, snowflake, and liquid-metal targets as an upside option[^1][^9][^43]

Dedicated exhaust facilities have slipped. Italy's **DTT** (P\(_{sep}\)/R ≈ 15 MW m\(^{-1}\)) moved from 2028 to a first plasma in July 2032, and ITER DT to 2039. No device has yet combined reactor-relevant P\(_{sep}\)/R, long pulse, a burning core and component lifetime.[^60][^96][^97]

### Stellarator: Island Divertor and Inherent Advantages

W7-X's **island divertor** achieved full heat-flux detachment, with heat loads falling an order of magnitude (> 5 to < 0.5 MW m\(^{-2}\)) and no impurity accumulation, stable for up to 28 s. In 2025 it ran a 360 s, 1.8 GJ discharge with ~85 % radiated fraction on an actively cooled divertor. Optimized stellarators show no type-I ELMs and no current-driven disruptions. Scaling from W7-X's ≤ 10 MW to a ~350 MW HELIAS reactor remains unvalidated, as do 3D hot spots, island movement with β and bootstrap current, and space for divertor and blanket.[^14][^44][^56]

### Laser ICF: Cyclic Thermal Shock

In ICF the first wall takes a periodic impulse from each microexplosion at 5–10 Hz: X-rays and debris within microseconds, and ~10\(^9\)–10\(^{10}\) cycles over the plant life. Metals tested under fusion-relevant cyclic loads nucleate fatigue cracks within 10\(^4\)–10\(^6\) cycles. Commercial concepts assume yields of ~50–1,000 MJ per shot, one to two orders of magnitude above NIF's 8.6 MJ. Dry walls, wetted walls, gas protection and thick liquid walls have all been proposed, but none has been tested at rep-rate. No rep-rated high-yield source exists, so the first integrated test would be a pilot plant.[^30][^52]

### Key Open Questions for Further Analysis

- Does λ\(_q\) follow the ~1 mm empirical or the ~6 mm gyrokinetic extrapolation at ITER scale?
- Can ≥ 95 % dissipation coexist with H\(_{98}\) ≈ 1 in a burning core at DEMO P\(_{sep}\)/R?
- Do Super-X benefits survive in high-power H-mode, and can advanced divertors be integrated at conventional aspect ratio?
- How does the W7-X island divertor scale to reactor power, and what IFE chamber wall survives ~10\(^{9}\)–10\(^{10}\) shots?

***

## Challenge 5: Driver & Magnet Engineering, and Steady-State Operation

*Deep dive: [Challenge Driver & Magnet Engineering, Steady-State Operation, and System Integration.md](Challenge%20Driver%20&%20Magnet%20Engineering,%20Steady-State%20Operation,%20and%20System%20Integration.md)*

### Core Problem Statement

A commercial plant needs a **driver** (magnets for MCF, lasers or other drivers for ICF) that delivers fusion conditions with a manageable recirculating power fraction. The driver must also operate continuously (MCF) or at 5–10 Hz (ICF) for decades in an integrated plant with acceptable availability, licensing and financing. ITER's own DT-phase availability target is ~14 %, and DEMO needs 30–60 %.[^122]

### Tokamak: Steady-State Operation and Superconducting Magnets

Inductive current drive makes conventional tokamaks **pulsed**, with fatigue and energy-storage penalties. Steady state requires a high bootstrap fraction plus efficient NBI/RF current drive without excessive recirculating power. Long-pulse records have advanced, though at low heating power and not at reactor performance:[^45][^46][^57][^58]

- EAST: 1,066 s RF-sustained H-mode at ~60 % Greenwald (Jan 2025)
- WEST: 1,337 s at ~2 MW, not H-mode (Feb 2025)
- DIII-D and EAST: transient operation with f\(_{Gr}\) > 1 and H\(_{98}\) ≈ 1.5

HTS magnets are the most transformative advance. CFS's TFMC reached **20 T** on 5 September 2021, a CS model coil followed in 2024, and DOE validated a full-scale SPARC TF magnet in September 2025. These magnets enable compact high-field devices (SPARC: 12.2 T on axis, Q ≈ 11 design goal). Tokamak Energy's Demo4 reached 11.8 T as a full HTS magnet set. Open issues remain:[^47][^64][^65][^99][^121]

- **REBCO radiation tolerance** at operating temperature
- **Quench protection** and demountable joints over many thermal cycles
- **Tape supply**: > 5,000 km/yr global capacity and ~$100–300/kA·m today, against ~$10–50/kA·m targets
- **FOAK integration**: only 8 of 18 SPARC TF coils were installed by September 2026

### Stellarator: 3D Coil Precision and Reactor-Scale Manufacturing

W7-X uses 50 non-planar and 20 planar **NbTi** superconducting coils (~2.5–3 T on axis), built to millimetre accuracy. A reactor needs comparable relative precision at ~5–6 T and several times the size, which points to Nb\(_3\)Sn or HTS conductors. Private developers bet on 3D HTS coils, which no one has yet manufactured at reactor grade:[^31][^44][^48][^49]

- Proxima Alpha: ~2031, ~€2 B
- Type One Infinity One/Two: prototype start-up ~2029; TVA letter of intent for a ~350 MW(e) plant
- Thea Energy

Steady state is intrinsic to the stellarator (W7-X 360 s, 1.8 GJ); the next goals are W7-X OP2.4/2.5 and, later, 30-minute high-power pulses.[^56][^100][^102][^117]

### Laser ICF: Driver Efficiency, Repetition Rate and Target Factory

NIF's flashlamp-pumped Nd:glass laser has a **wall-plug efficiency of well below 1 %** (~0.5–0.6 %; ~300–400 MJ from the grid per shot). With gain 4.13 this gives \(\eta_{driver} G \approx 0.025\). That is ~100× below engineering breakeven (\(\eta G \approx 2.6\)) and ~400× below an economic plant (\(\eta G \gtrsim 10\)), which needs gain ≳ 50–100 *and* ≥ 10 % efficient drivers at 5–10 Hz.[^35][^52] Legacy rep-rate data remain small-scale: the Mercury DPSSL (10 Hz, ~50 J, > 300,000 shots) and the NRL Electra KrF laser (5 Hz).[^50] Private programmes in 2026:[^103][^104][^105][^106]

- **Xcimer**: KrF excimer with Brillouin compression; Phoenix (2026), Anvil (2028), Vulcan (~2030–2031)
- **Focused Energy**: plant at Biblis by the mid-2030s
- **Marvel Fusion**: ATLAS laser facility
- **Pacific Fusion**: pulsed power, not a laser

None has yet shown ≥ 10 % wall-plug efficiency at MJ-class energy and ≥ 5 Hz. NIF's shot cadence is ~2 × 10\(^5\) times below 10 Hz.

A plant also needs **~500,000–864,000 cryogenic targets per day** at ≲ $0.30 each, against $2,500–10,000 per NIF target today, a ~10\(^4\)× cost reduction. Targets must be injected at 100–200 m/s and tracked at 10 Hz. No pilot target factory exists (TRL 1–2).[^22][^41][^51][^120]

### Integration, Regulation and Financing

The integrated plant problem includes:

- **Availability** (RAMI), with the first FOAK demonstration plants expected to reach < 50 % of design availability
- **FOAK cost and schedule**: ITER's 2024 re-baseline cost ~€5 B extra and brings a ~10-year cumulative slip
- **Licensing**: the NRC Part 30 route, UK s.156 and the German Radiation Protection Act are not yet exercised for a kg-tritium plant
- **Financing**: multi-billion-dollar FOAK equity, with power purchase agreements contingent on milestones. Helion began building its Orion plant in 2025 and targets electricity for Microsoft from 2028; its Polaris prototype reported DT fusion in February 2026, but no electricity recovery has been publicly demonstrated.[^61][^107][^108][^110][^112][^114][^122]

### Key Open Questions for Further Analysis

- Does SPARC reach Q > 1 in 2027–2028 without magnet or disruption damage?
- Can HTS coils survive plant-lifetime fluence with practical shielding, and can REBCO supply and cost scale to a fleet?
- What is the achievable wall-plug efficiency of excimer or DPSSL drivers at MJ class and 5–10 Hz, and can targets reach ≲ $1, ultimately ~$0.30?
- Can stellarator coils be simplified (e.g. tilted circular toroids) without losing the optimization gains?[^49]
- Will FOAK plants reach the availability that financing assumes?

***

## Cross-Cutting Themes and Systemic Risks

### Absence of a Fusion Materials Test Facility

IFMIF-DONES is now funded (Nov 2025) and under construction (site works since Sep 2026), but first neutrons are expected ~2033–2035 and ≥ 10 dpa data ~2037–2039. Until then DEMO and pilot-plant designs rest on extrapolation from fission, ion-beam and separate plasma-exposure data.[^26][^70][^71]

### The Integrated Challenge

None of the five challenges is independent. High-performance plasma (challenge 1) tightens the demands on plasma-facing materials (challenge 2) and raises tritium burn rates (challenge 3). Higher power output worsens heat exhaust (challenge 4) and demands more efficient drivers (challenge 5). Blanket thickness trades against magnet shielding and port space, and divertor space trades against breeding coverage. The deep dives quantify these links as rank correlations between gate years (see the coupling matrix below). The challenges must be solved simultaneously in an integrated system that has never been built.

### Pathway Comparison: Relative Difficulty

| Challenge | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Disruptions / implosion instability | **Hardest** (disruptions + ELMs) | Easiest (no current-driven disruptions) | **Hardest** (RT instability, tight tolerances, gain ≈ 4) |
| Anomalous turbulent transport | Moderate | Moderate (neoclassical solved, turbulence remains) | Less relevant (burn time ~ns) |
| Neutron damage to materials | Moderate | **Harder** (3D geometry limits shielding/maintenance) | Hardest (+ rep-rate shock loading + optics) |
| Tritium breeding | Moderate | **Harder** (geometry-limited blanket coverage) | Hardest (target-factory inventory + beam-port coverage) |
| Power exhaust | Moderate (advanced divertors advancing, at low power) | Moderate (island divertor promising) | Different (cyclic shock, untested at rep-rate) |
| Driver/steady-state | Moderate (HTS progress, steady-state unsolved) | Hard (3D coil complexity, no reactor prototype) | **Hardest** (~100× in ηG needed, target factory nonexistent) |

***

## Research Roadmap Anchors

The following open problems are the highest-leverage research targets, ranked by their potential to unblock commercialization:

1. **Disruption prediction and avoidance in large-current tokamaks**: ML and RL-based avoidance, validation of the ITER SPI system, runaway-electron mitigation (SPARC 2027+, ITER 2034+)
2. **Turbulence modelling and burning-plasma validation**: gyrokinetic validation against SPARC, BEST, JT-60SA and W7-X high-T\(_i\) data; alpha-particle stability
3. **14 MeV neutron materials database**: on-schedule IFMIF-DONES commissioning (first neutrons ~2033–2035); irradiation of EUROFER97, ODS, W alloys and CuCrZr; early design-code cases
4. **Breeding-blanket testing in a fusion environment**: LIBRTI/LIBRA mock-ups, ITER TBMs (2039+), breeding on BEST or ARC, a funded FNSF/VNS; closed fuel-cycle loops (H3AT, UNITY-2)
5. **Advanced divertor validation at reactor-relevant power**: MAST-U high power (2028), DTT (2032+), SPARC and ITER; liquid-metal options
6. **HTS magnet radiation hardness, quench protection and supply chain**: cryogenic irradiation of REBCO, demountable joints, tape cost and capacity
7. **High-efficiency, high-rep-rate drivers**: excimer (Xcimer Anvil 2028) and DPSSL modules at ≥ 10 % wall-plug efficiency and ≥ 5 Hz
8. **IFE target mass production**: automated fill, layer and injection lines at ≥ 10\(^4\) targets/day with a cost path to ≲ $1 per target

***

## Integrated Risk Assessment (November 2026)

This section consolidates the "Risk Assessment (November 2026)" sections of the five deep dives. Their likelihoods, gate-year distributions and correlations are **calibrated expert judgments** grounded in the evidence of each report, not outputs of a formal elicitation. They are treated here as priors.

### Consolidated top-15 risk register

The ranking uses a severity score: likelihood (low = 1, low–med = 1.5, med = 2, med–high = 2.5, high = 3) × midpoint of the schedule impact in years. The score is multiplied by 1.5 for risks that affect all pathways and by 1.25 for two. Risks describing the same mechanism in different deep dives are merged, and the higher likelihood and wider impact are kept.

| # | ID | Risk | Pathways | Likelihood | Impact | Early indicator |
|---|---|---|---|---|---|---|
| 1 | DR-8 / TR-9 | IFE target factory cannot reach ~10\(^5\)–10\(^6\) targets/day at ≲ $0.30–1 each with an in-plant tritium inventory of a few kg or less | Laser ICF | high | +5–20 y; possibly pathway-limiting | Automated-line throughput and cost per target; no rep-rate fill/layer demonstration by ~2032 |
| 2 | DR-7 | IFE driver fails to reach ≥ 10 % wall-plug at ≥ 5–10 Hz with MJ-class energy and adequate optics lifetime | Laser ICF | high | +5–15 y; show-stopper if ηG ≳ 10 unreachable | Xcimer Phoenix/Anvil efficiency and rep-rate data; diode $/W trend |
| 3 | EX-10 / MA-8 / EX-11 | IFE chamber first wall or liquid-jet wall fails very-high-cycle (10\(^9\)–10\(^{10}\)) fatigue or rep-rate jet re-formation; the first integrated test is the pilot plant | Laser ICF | high | +5–15 y; may block laser IFE plants | Surrogate X-ray/ion load tests; jet re-formation data at Hz rates; first rep-rated pilot chamber |
| 4 | TR-1 | As-built 3D TBR falls below required (~1.05) once ports, manifolds, diagnostics and trapping are included | All (worst ICF, then stellarator) | med | +5–15 y; design may be non-self-sufficient | Engineering-fidelity neutronics of ARC, STEP, Infinity Two, EU DEMO trending < 1.10; LIBRTI/LIBRA results below prediction |
| 5 | TR-2 | No blanket test in a fusion environment before DEMO/FPP design freeze (the FNSF "missing step") | Tokamak, Stellarator | high | +5–10 y, or FOAK on an unvalidated blanket | No FNSF/VNS funding decision by ~2028; BEST blanket/DT scope undefined |
| 6 | PL-8 | ICF shot-to-shot variability and RT/mix keep target gain at ~4–10 | Laser ICF | med–high | +5–15 y; may need a new > 2 MJ facility | NIF yields after optics recovery; EYC upgrade; OMEGA direct-drive scaling |
| 7 | DR-12 | FOAK construction time and cost overrun (ITER pattern: ~2× cost, +5–10 y) | All | high | +3–8 y per FOAK plant | Schedule variance on SPARC (8/18 TF coils by Sep 2026), BEST, Alpha, Orion, STEP |
| 8 | TR-3 | Start-up tritium not available in time for the first demonstration plant | All (DEMO-class most exposed) | med | +2–12 y for the affected plant | Stockpile and price signals; OPG sales policy; further ITER slip; number of DT programmes requesting > 1 kg |
| 9 | DR-9 | FOAK demo reaches < 50 % of design availability (remote maintenance, tritium plant, RF/driver reliability) | All | high | +3–6 y to commercial plant | Commissioning durations of SPARC, BEST, Helion Orion; RAMI data from W7-X/JT-60SA/ITER |
| 10 | PL-7 | Stellarator turbulence optimization does not hold at reactor temperature; no burning-plasma stellarator funded before the late 2030s | Stellarator | med | +5–15 y | W7-X OP2.4+ results at higher T\(_i\); Proxima Alpha federal funding and construction start |
| 11 | TR-5 | Permeation and unaccounted tritium losses exceed ~10\(^{-5}\) per pass at power-plant throughput | All | med | +3–10 y; can erase breeding surplus and block licensing | H3AT/UNITY-2 loop loss data; barrier performance under irradiation |
| 12 | PL-5 | Alpha-driven Alfvén eigenmodes cause > 10 % alpha loss or a self-limiting burn | Tokamak, Stellarator | low–med | +5–15 y; possible show-stopper for compact high-β designs | First alpha-heating data from SPARC and BEST (2028+); ITER DT fast-ion loss detectors |
| 13 | EX-2 | ≥ 95 % dissipation incompatible with an H\(_{98}\) ≈ 1 burning core at DEMO P\(_{sep}\)/R | Tokamak, Stellarator | med | +5–10 y; larger, less economic machines | AUG/JET/DTT integrated scenarios; ITER Q = 10 with seeding (2039+) |
| 14 | PL-6 / TR-10 / DR-14 / EX-4 | ITER slips beyond the 2024 baseline (DT 2039) and other public facilities (DTT 2032, MAST-U high power 2028) slip further, delaying reactor-relevant validation data | Tokamak (indirectly all MCF) | med–high | +3–8 y to MCF Q = 10 at reactor scale; +2–5 y on blanket and exhaust evidence | ITER Council progress reports and SRO tracking; DTT TF-coil delivery; TBM design-review slippage |
| 15 | MA-1 / MA-5 | IFMIF-DONES first neutrons slip beyond 2035, and design-code/regulator acceptance of irradiation data lags by > 5 y | All | med / med–high | +3–6 y on all gates | DONES Main Building not complete in 2029; LIPAc fails to show CW high-current operation; code-body acceptance of small-specimen standards |

Next in rank are MA-9 (ICF final-optics lifetime), PL-4 (turbulent transport worse than extrapolated), MA-2 (EUROFER97 unsuitable at 10–20 dpa), DR-2 (HTS degradation under irradiation), MA-6/MA-7 (remote maintenance, stellarator 3D blanket), EX-8 (island-divertor scaling) and DR-5 (current-drive efficiency).

### Gate definitions and gate-year distributions

Each deep dive defines one gate per challenge. Years are calendar years of reaching the gate, **conditional on the gate being reached**. P(never) is the separate probability that a show-stopper in that challenge prevents the gate in that pathway by 2100. Values are copied verbatim from the deep dives' "Model parameters" tables.

| Gate | Definition (short form) | Tokamak P10 / P50 / P90 · P(never) | Stellarator P10 / P50 / P90 · P(never) | Laser ICF P10 / P50 / P90 · P(never) |
|---|---|---|---|---|
| **PL** — burning-plasma performance with reactor-relevant control | MCF: DT Q ≥ 10 (compact: alpha heating ≥ 2/3 and route to Q\(_{eng}\) > 1) sustained ≥ ~3 current-diffusion times or ≥ 300 s, with disruption rate ≤ ~1 %, validated RE mitigation and ELM control. ICF: target gain ≥ ~30–50 with a plant-consistent driver (ηG ≳ 10), shot-to-shot variation < 2× | 2036 / 2044 / 2058 · 0.05 | 2042 / 2055 / 2078 · 0.15 | 2038 / 2050 / 2075 · 0.20 |
| **MA** — materials qualified for licensing | Fusion-spectrum irradiation data to ≥ ~20 dpa for first-wall/blanket structure and armour, accepted by the licensing authority via a design code; remote maintenance validated on full-scale mock-ups and (MCF) in an activated DT device | 2040 / 2046 / 2057 · 0.05 | 2043 / 2050 / 2063 · 0.10 | 2042 / 2050 / 2065 · 0.15 |
| MA milestone — neutron source | IFMIF-DONES (or equivalent) delivers post-irradiation data at ≥ ~10 dpa | 2036 / 2038 / 2043 · 0.03 (all pathways) | (same) | (same) |
| **TR** — tritium self-sufficiency | Breeding blanket operated in a DT device of that pathway (≥ ~0.5 MW m\(^{-2}\), months); measured breeding with validated net TBR ≥ required + 0.05; closed fuel cycle with per-pass losses ≲ 10\(^{-4}\) and regulator-accepted accountancy; start-up inventory for the first demo plant secured | 2038 / 2048 / 2065 · 0.10 | 2045 / 2058 / 2080 · 0.20 | 2050 / 2065 / 2088 · 0.30 |
| **EX** — power exhaust demonstrated | Reactor-relevant power density (tokamak P\(_{sep}\)/R ≥ ~15 MW m\(^{-1}\); IFE ≥ ~50 MJ yields at ≥ 1 Hz); target ≤ ~5–10 MW m\(^{-2}\) for ≥ 1000 s (IFE ≥ 10\(^6\) shots) with controlled transients; compatible with a burning core; component lifetime ≥ ~2 fpy | 2039 / 2047 / 2062 · 0.07 | 2042 / 2052 / 2070 · 0.12 | 2045 / 2056 / 2078 · 0.22 |
| **DR** — reactor-grade driver demonstrated | MCF: plant-scale superconducting magnet system with validated quench protection and lifetime-fluence evidence, plus ≥ ~1 h (tokamak) or ≥ 30 min high-power (stellarator) operation with recirculating power ≤ ~20–25 %. ICF: driver ≥ 10 % wall-plug at ≥ 5–10 Hz (≥ ~10 kJ modules, optics ≥ 10\(^8\) shots) plus a target line ≥ ~10\(^4\)/day with a cost path to ≲ $1 | 2036 / 2045 / 2062 · 0.05 | 2039 / 2050 / 2068 · 0.07 | 2040 / 2052 / 2075 · 0.15 |

The full distributions (P0/P100), the discrete breakthrough/setback events, and the integration and deployment parameters of Challenge 5 are listed in the deep dives:

- FID → first net electricity: P50 of 10 / 11 / 9 years for tokamak / stellarator / ICF
- Demo → first commercial plant: P50 of 10 / 11 / 10 years
- P(demo < 50 % availability): 0.65 / 0.55 / 0.70
- P(major licensing or financing delay): 0.45 / 0.45 / 0.50

### Cross-challenge coupling (Spearman ρ between gate years)

Each pair is covered by two deep dives, one from each side. The table lists both values and a consolidated value: their mean, rounded to the nearest 0.05 (halves up). Where a deep dive gives no pathway-specific value, its general value is used for both pathways.

| Pair | Tokamak: value in A / value in B | Tokamak consolidated | Laser ICF: value in A / value in B | Laser ICF consolidated |
|---|---|---|---|---|
| PL – MA | 0.30 / 0.30 | **0.30** | 0.20 / 0.30 | **0.25** |
| PL – TR | 0.40 / 0.50 | **0.45** | 0.20 / 0.50 | **0.35** |
| PL – EX | 0.60 / 0.55 | **0.60** | 0.10 / 0.60 | **0.35** |
| PL – DR | 0.50 / 0.50 | **0.50** | 0.60 / 0.60 | **0.60** |
| MA – TR | 0.60 / 0.60 | **0.60** | 0.60 / 0.60 | **0.60** |
| MA – EX | 0.50 / 0.60 | **0.55** | 0.50 / 0.60 | **0.55** |
| MA – DR | 0.25 / 0.40 | **0.35** | 0.35 / 0.30 | **0.35** |
| TR – EX | 0.35 / 0.30 | **0.35** | 0.35 / 0.40 | **0.40** |
| TR – DR | 0.45 / 0.30 | **0.40** | 0.45 / 0.30 | **0.40** |
| EX – DR | 0.45 / 0.45 | **0.45** | 0.60 / 0.20 | **0.40** |

"A" is the first-named challenge's deep dive and "B" the second's. The stellarator-specific values in the deep dives are PL–EX 0.50 (exhaust report) and PL–DR 0.40 (driver report); all other stellarator couplings equal the tokamak values.

Consolidated matrix. The upper triangle holds tokamak/MCF values and the lower triangle Laser ICF values. Both matrices are positive definite, so they can be used directly for correlated sampling.

| | PL | MA | TR | EX | DR |
|---|---|---|---|---|---|
| **PL** | 1 | 0.30 | 0.45 | 0.60 | 0.50 |
| **MA** | 0.25 | 1 | 0.60 | 0.55 | 0.35 |
| **TR** | 0.35 | 0.60 | 1 | 0.35 | 0.40 |
| **EX** | 0.35 | 0.55 | 0.40 | 1 | 0.45 |
| **DR** | 0.60 | 0.35 | 0.40 | 0.40 | 1 |

Two ICF pairs disagree strongly between the deep dives:

- **PL–EX**: 0.10 in the plasma report vs. 0.60 in the exhaust report, which couples yield to chamber loads
- **EX–DR**: 0.60 in the exhaust report vs. 0.20 in the driver report

The consolidated values for these pairs (0.35 and 0.40) should be treated as uncertain.

### Quantitative Monte Carlo model

The gate distributions, show-stopper probabilities, couplings and discrete events above were assembled into a Monte Carlo model for the Risk Pilot app: `data/models/kernfusion_risiko.yaml` (German UI labels; main scenario = tokamak, sub-scenarios stellarator, laser IFE and three tokamak variants). All inputs are calibrated expert judgments from the deep dives, not a formal elicitation.

**Structure.**
- Five gate years (plasma, materials = DONES data + qualification time, tritium, power exhaust, driver/magnets), each with its discrete breakthrough/setback events. The base distributions are shifted by the events' expected effect so that each gate matches the deep-dive values on average.
- A show-stopper event per gate (P(never by 2100)), coupled with ρ = 0.3 as a common cause.
- Gate years coupled via a Gaussian copula with the Spearman matrix from the coupling section.
- Demo plant: the investment decision falls `vorlauf` years (P50 8 y) before the last gate. First net electricity follows at max(FID + construction + licensing/financing delay + tritium start-up inventory delay, last gate).
- The first commercial plant follows after another 10 y (P50), plus a delay if the demo's availability is low.

**Results** (N = 50 000, seed 20261102; year quantiles conditional on no show-stopper):

| Scenario | P(show-stopper) | Last gate P50 | Demo net electricity P10/P50/P90 | First commercial plant P10/P50/P90 | P(demo ≤ 2050) | P(commercial ≤ 2060) | P(commercial ≤ 2075) | P(commercial ≤ 2100) |
|---|---|---|---|---|---|---|---|---|
| Tokamak (basis) | 0.24 | 2058 | 2051 / 2065 / 2090 | 2064 / 2080 / 2104 | 0.06 | 0.04 | 0.28 | 0.65 |
| Stellarator | 0.41 | 2069 | 2058 / 2076 / 2101 | 2072 / 2091 / 2116 | 0.01 | 0.01 | 0.09 | 0.40 |
| Laser IFE | 0.57 | 2073 | 2061 / 2080 / 2107 | 2074 / 2095 / 2123 | 0.00 | 0.00 | 0.05 | 0.25 |
| Tokamak, private pilots succeed | 0.24 | 2058 | 2048 / 2062 / 2086 | 2061 / 2076 / 2100 | 0.10 | 0.07 | 0.35 | 0.68 |
| Tokamak, tritium shortage | 0.31 | 2058 | 2053 / 2069 / 2093 | 2066 / 2083 / 2108 | 0.04 | 0.02 | 0.20 | 0.56 |
| Tokamak, DONES delayed ≥ 3 y | 0.24 | 2059 | 2052 / 2066 / 2090 | 2064 / 2080 / 2104 | 0.05 | 0.03 | 0.27 | 0.65 |

**Which gate decides?** Share of successful iterations in which each gate is the last one closed. Tokamak: tritium 28 %, exhaust 23 %, driver/magnets 20 %, materials 18 %, plasma 12 %. Stellarator: tritium 34 %, plasma 25 %. Laser IFE: tritium 51 %.

**Main findings.**
1. **The max-of-five effect dominates.** Each tokamak gate has a median around 2045–2048, but the last of the five correlated gates has a median of 2058. Single-challenge roadmaps therefore systematically understate the integrated schedule.
2. **Show-stopper risk outweighs schedule risk.** Small per-gate probabilities (5–10 % tokamak, 7–30 % ICF) compound to 24 % (tokamak), 41 % (stellarator) and 57 % (laser IFE) even with positive coupling. Tritium self-sufficiency is the largest single contributor in every pathway.
3. **Largest schedule drivers for the tokamak demo** (tornado on demo year; years of swing between P10 and P90 of each input):

   | Input | Swing (years) |
   |---|---|
   | Tritium gate | 7.0 |
   | Driver gate | 5.5 |
   | Exhaust gate | 5.5 |
   | Construction time | 5.4 |
   | FID lead time | −5.3 |
   | Plasma gate | 3.3 |

   Discrete events with the largest conditional delay are a missing tritium start-up inventory (p 0.30, +4.8 y), licensing/financing delays (p 0.45, +3.2 y), dissipation incompatible with H-mode (+2.7 y), alpha-driven losses (+2.5 y) and EUROFER failure at 10–20 dpa (+2.5 y).
4. **DONES delay matters less than expected** (−0.01 on P(commercial ≤ 2075)), because the materials gate is rarely the last one. A tritium shortage costs about 8 points.
5. **"Private pilots succeed" moves the median by only ~4 years.** It does not address tritium breeding, exhaust lifetime or materials, so the gating structure stays the same.

**Limits.** The model treats gates as prerequisites for the demo plant. In reality some gates (breeding, exhaust at full power) are closed in the demo or pilot itself; this is approximated by building in parallel with the last gate. The probabilities come from one structured literature review, not from a panel of experts. The scenarios are not weighted, and there are no costs or LCOE. Results should be read as "in the model …", not as forecasts.

***

## Conclusion

Commercial fusion is not gated by a single breakthrough. It depends on solving five interconnected challenges together, each needing years to decades of further engineering. In the November 2026 deep-dive assessments, the median gate years for the tokamak lie between 2044 and 2048. Stellarator medians run to 2058 and Laser ICF medians to 2065, with the tritium gate latest in every pathway. Across all pathways the slowest gates are therefore tritium self-sufficiency and, for ICF, the driver/target-factory and chamber problems, not plasma physics alone.

Each pathway has a different weak point:

- **Tokamaks** are most mature, but ITER's DT phase has moved to 2039 and the near-term test is now SPARC (first plasma 2027).
- **Stellarators** have intrinsic steady-state and stability advantages (W7-X 2025 records), but face unproven reactor-scale 3D coils and no funded burning-plasma device.
- **Laser ICF** has ignited ten times with gain 4.13, but still needs ~100× in driver efficiency × gain, an entire target-manufacturing industry and a first wall that survives ~10\(^9\)–10\(^{10}\) shots.[^2][^3][^52][^56][^60][^62]

The most consequential gap across all pathways remains the **absence of an integrated fusion nuclear environment**: a facility combining burning-plasma neutron flux, tritium breeding and power extraction in a single machine operating for years. Funding of IFMIF-DONES (2025) and the new tritium test loops narrow the gap, but they do not close it. Several technical risks coincide in the 2027–2035 window:

- SPARC and BEST results
- the DONES schedule
- DTT and ITER start-up
- the first private pilot plants

Financing and regulation improved faster than hardware in 2025–2026. The window will therefore decide whether the integrated engineering pathway can deliver fusion electricity at scale in the first half of the century.

---

## Changelog (2026-11)

- Header and date lines changed to "November 2026 update"; executive summary rewritten for late-2026 status; new section "Status November 2026" (milestones 2025–2026, decision points 2027–2035).
- **Corrected facts** (aligned with the deep dives):
  - NIF record 8.6 MJ from 2.08 MJ, gain 4.13 (7 April 2025), with ten ignitions
  - CFS TFMC 20 T in 2021 (not 20.8 T)
  - W7-X 2023 > 8 min / 1.3 GJ plus the 2025 records (43 s triple product, 360 s / 1.8 GJ)
  - ITER 2024 baseline: SRO 2034, DT 2039
  - JET records clarified (1997 power record; 59/69 MJ energy records at Q ≈ 0.3)
  - Runaway currents ~10–12 MA; the unsupported "300–700× density increase" removed
- **Materials**:
  - "70 dpa over blanket lifetime" replaced by ~12–15 dpa/fpy in front-wall steel, a ~20 dpa starter-blanket limit (~1.3–1.7 fpy) and ~60–75 dpa at 5 fpy
  - IFMIF-DONES status (MIDA Nov 2025, site works Sep 2026, first neutrons ~2033–2035)
  - Dose rates corrected (ITER RH ~250 Gy/h; DEMO ~13–17 kGy/h; "5 × 10\(^5\) Sv/h" withdrawn)
  - ICF shots per day corrected from ~10\(^5\) to 4.3–8.6 × 10\(^5\); TNT equivalence tied to yield
- **Tritium**:
  - Stockpile ~20–25 kg (was 22 kg)
  - 1 GW burns ~55.6 kg T/fpy, ~150 g/day (was "184 g/day")
  - ITER lifetime use ~12.3 kg; Coleman & Kovari 2055 availability
  - 3D TBR ranges from the deep dive replace the "2022 analysis 1.15 / 1.05" statement
  - ICF inventory "up to ~10 kg" (NAS 2013) and no longer "larger than the global stockpile"
- **Exhaust**:
  - DEMO ~150 MW m\(^{-2}\) identified as the *perpendicular* target heat flux (parallel: several GW m\(^{-2}\); SPARC > 10 GW m\(^{-2}\) parallel)
  - λ\(_q\) ~1 mm vs. gyrokinetic ~6 mm
  - AUG XPR ~95 % dissipation; MAST-U results qualified as L-mode at ~1 MW
  - DTT first plasma July 2032
- **Driver**:
  - Wall-plug efficiency definition corrected; NIF ~0.5–0.6 %
  - ηG ≈ 2.6 is engineering breakeven, while an economic plant needs ηG ≳ 10
  - Target cost ≲ $0.30 (was $0.20) against $2,500–10,000 today; 500,000–864,000 targets/day
  - W7-X coils all NbTi
  - Added Demo4, REBCO supply, private IFE drivers, regulation and financing
- Overview matrix column renamed "TRL (2026)" with updated ranges; the five challenge chapters were condensed and each links to its deep-dive file.
- Added "Integrated Risk Assessment (November 2026)": consolidated top-15 risk register, gate table with verbatim P10/P50/P90 and show-stopper probabilities, coupling matrix (tokamak and ICF), and a placeholder for the quantitative Monte Carlo model.
- References 52–126 added, copied from the deep dives' reference lists. References 1–51 kept with their numbering; two are no longer cited in the text (7, 36).

---

## References

1. [Plasma Confinement Physics: Challenges and Innovations in Tokamak and Stellarator Designs](https://www.youtube.com/watch?v=9ZV-RZqmyTw) - Explore the quest for fusion energy, comparing the challenges and recent breakthroughs in the two ma...

2. [National Ignition Facility - 2023 - Annual Report](https://annual.llnl.gov/fy-2023/national-ignition-facility-2023) - Supporting stockpile stewardship through a wide range of experiments including study of fusion ignit...

3. [Ignition | Lawrence Livermore National Laboratory](https://www.llnl.gov/news/ignition) - On Dec. 5, 2022, Lawrence Livermore National Laboratory made history, demonstrating fusion ignition ...

4. [Different approaches around the world - ITER](https://www.iter.org/node/20687/different-approaches-around-world) - Look east, look west ... tokamak projects are underway in different parts of the world. All of them ...

5. [IAEA](https://www-pub.iaea.org/MTCD/publications/PDF/FusionOutlook2023_web.pdf)

6. [arXiv:2507.05456v5 [physics.plasm-ph] 9 Sep 2025](https://arxiv.org/pdf/2507.05456v5.pdf)

7. [IAEA](https://arxiv.org/pdf/2105.04706.pdf)

8. [[PDF] Runaway Electrons in Tokamaks - ITER](https://www.iter.org/sites/default/files/education/IISS2011_Putvinski_L8.pdf) - • Runaway electrons can be produced in a tokamak during plasma disruption. • It is expected that mac...

9. [Divertor heat flux challenge and mitigation in SPARC - OSTI](https://www.osti.gov/biblio/1772637) - Owing to its high magnetic field, high power, and compact size, the SPARC experiment will operate wi...

10. [The long and short of plasma turbulence](https://www.sciencedaily.com/releases/2015/11/151110170936.htm) - One of the world's largest supercomputers reveals the complex interplay between two types of turbule...

11. [[PDF] Instabilities, Turbulence and Transport - ITER](https://www.iter.org/sites/default/files/media/2024-04/dong_instability_transport.pdf)

12. [TCV Core transport + Turbulence ‒ SPC - EPFL](https://www.epfl.ch/research/domains/swiss-plasma-center/tcv-core-transport-and-turbulence/) - Overall, improving transport control remains a key challenge in achieving sustained fusion condition...

13. [doi:10.1016/j.crhy.2006.06.011](https://comptes-rendus.academie-sciences.fr/physique/item/10.1016/j.crhy.2006.06.011.pdf)

14. [Experimental confirmation of efficient island divertor operation and successful neoclassical transport optimization in Wendelstein 7-X](https://arxiv.org/abs/2105.04002v1) - We present recent highlights from the most recent operation phases of Wendelstein 7-X, the most adva...

15. [Demonstration of reduced neoclassical energy transport in ...](https://researchportal.rma.ac.be/de/publications/demonstration-of-reduced-neoclassical-energy-transport-in-wendels-5/) - Such an optimization was undertaken in designing Wendelstein 7-X (W7-X)2, a large helical-axis advan...

16. [arXiv:2311.04342v3  [physics.plasm-ph]  24 Jul 2024](https://arxiv.org/pdf/2311.04342.pdf)

17. [[PDF] Overview of Measurements from the Wendelstein 7-X ... - Cortland](https://facultyweb.cortland.edu/eric.edlund/portfolio/research/presentations/Edlund-APS2020.pdf)

18. [Degradation of performance in ICF implosions due to Rayleigh—Taylor instabilities: a Hamiltonian perspective](https://arxiv.org/html/2411.12933v1)

19. [Instabilities and Mixing in Inertial Confinement Fusion](https://www.annualreviews.org/content/journals/10.1146/annurev-fluid-022824-110008?crawler=true) - The main hydrodynamic instabilities that affect ICF are the Rayleigh–Taylor (RT) instability and the...

20. [Fusion for energy: significant progress, major challenges](https://www.rochester.edu/newscenter/what-challenges-remain-in-achieving-inertial-confinement-fusion-170572/) - In the article, Betti and Hurricane assess the "state of the art" in five key approaches to inertial...

21. [[PDF] Future for Inertial Fusion Energy in Europe - ELI ERIC Indico Page](https://indico.eli-laser.eu/event/35/attachments/131/406/8_Talk%20Batani%20HiPER%20Praga%20LIF%20-2023.pdf) - Technology: Address the engineering issues related to IFE: high repetition rate lasers, target devel...

22. [[PDF] Target mass production for inertial fusion energy](https://lasers.llnl.gov/sites/lasers/files/2023-11/alexander-GA-IFE-workshop-2022-2.pdf) - Targets require high fabrication tolerance (~10 µm level), and large numbers if them are needed. (~5...

23. [New scheme for inertial confinement fusion laser drivers ...](https://www.cambridge.org/core/journals/high-power-laser-science-and-engineering/article/new-scheme-for-inertial-confinement-fusion-laser-drivers-based-on-a-spatiotemporal-partially-coherent-multimode-source-and-its-prospects/30ED75F76835CAF605C59B7FBFF4890C) - New scheme for inertial confinement fusion laser drivers based on a spatiotemporal partially coheren...

24. [A study of the Rayleigh-Taylor Instability during deceleration in ...](https://vtechworks.lib.vt.edu/items/b3c1f320-2bcb-44cb-9706-4c0e509da6dd) - The Rayleigh-Taylor instability (RTI) is one of the primary hydrodynamic instabilities that acts as ...

25. [The-role-of-fusion-report cover_Final_150dpi](https://energy.mit.edu/wp-content/uploads/2024/09/MITEI_FusionReport_091124_final_COMPLETE-REPORT_fordistribution.pdf)

26. [Critical remarks on the current TAB report on nuclear fusion](https://www.ipp.mpg.de/5481806/tab_bericht_2025) - Recycling technologies are needed that allow all activated components of a fusion reactor to be rele...

27. [[PDF] Issues of tungsten as a plasma facing material for ITER and DEMO](http://www.eie.eng.osaka-u.ac.jp/~supraweb/PDF/ITC22_Ueda12R3.pdf)

28. [Please cite this article as: S.Das et al., Jmade (2018) https://doi.org/10.1016/j.matdes.2018.11.001](https://arxiv.org/pdf/1811.05412.pdf)

29. [Recent advances in characterising irradiation damage in ...](https://d-nb.info/1207536903/34)

30. [Nuclear fusion](https://ethz.ch/content/dam/ethz/special-interest/dual/istp-dam/documents/Events/Colloquium/2025/FSOpen/Kernfusion_ETH_5Mrz2025_fin.pdf)

31. [High-temperature superconducting strong-field stellarator with precise ...](https://www.sciencedirect.com/science/article/pii/S2666675823001650)

32. [Remote Handling Systems](https://www.vltfusion.org/areas-of-research/remote-handling-systems/)

33. [[PDF] PROGRESS TOWARDS DEMONSTRATING IFE TARGET ...](https://fusion.gat.com/pubs-ext/MISCONF01/A23832.pdf)

34. [Preparation and Submission of a Manuscript for the Proceedings](https://www-pub.iaea.org/MTCD/Meetings/PDFplus/2010/cn180/cn180_papers/ife_1-4.pdf)

35. [development of innovative repeatable power laser for ...](https://conferences.iaea.org/event/392/papers/35694/files/13602-Manuscript_Template%20FEC%202025_resubmit.pdf)

36. [Tritium breeding control within liquid metal blankets](https://www.sciencedirect.com/science/article/abs/pii/S0920379612004747) - A key requirement for DEMO is the on-site breeding of tritium. In order to do this, a robust control...

37. [Fueling Our Star on Earth: The Tritium Challenge Explained](https://www.proximafusion.com/press-news/fueling-our-star-on-earth-the-tritium-challenge-explained) - The tritium challenge is a technology challenge, not a challenge of access to natural resources.

38. [Advancing Tritium Self-Sufficiency in Fusion Power Plants - arXiv](https://arxiv.org/html/2412.02721v1)

39. [A shortage of tritium fuel may leave fusion energy with an empty tank](https://www.science.org/content/article/fusion-power-may-run-fuel-even-gets-started) - Experts fear giant ITER reactor will worsen looming shortage of tritium

40. [Development of tritium breeding blankets for DT-burning fusion reactors](https://www.osti.gov/biblio/6377863) - This study examines the status of understanding of blanket tritium recovery and the performance of p...

41. [IFE target fabrication and injection—achieving “believability”](https://www.sciencedirect.com/science/article/abs/pii/S016890020100016X)

42. [Divertor shaping with neutral baffling as a solution to the tokamak ...](https://www.nature.com/articles/s42005-025-02121-1) - Exhausting power from the hot fusion core to the plasma-facing components is one fusion energy's big...

43. [Demonstration of Super-X divertor exhaust control for transient heat load management in compact fusion reactors](https://www.nature.com/articles/s41560-025-01824-7) - Managing power exhaust in fusion reactors is a key challenge, especially in compact designs for cost...

44. [Stellarator: The Twisted Path to Fusion - Dan B Gray](https://www.danbgray.com/blog/Science%2FNuclear_%2FStellarator) - Stellarator: The Twisted Path to Fusion While tokamaks dominate fusion research, another magnetic co...

45. [1](https://www.burningplasma.org/activities/uploads_tec/FESAC%20High%20Field.pdf)

46. [Microsoft Word - IAEA-CN-69...](https://www-pub.iaea.org/mtcd/publications/pdf/csp_008c/fec1998/pdf/ov2_3.pdf)

47. [[PDF] COMMONWEALTH FUSION SYSTEMS' HIGH-FIELD PATH TO ...](https://media.superevent.com/documents/20230927/b850523d7f0af4c50710a7b23612f652/brunner.d-pwf-synopsis.pdf) - HTS, in contrast to the low-temperature superconductors (LTS) being used in ITER and other major sup...

48. [[PDF] A Stellarator Reactor based on the Optimization Criteria of ...](https://pure.mpg.de/rest/items/item_2142701_1/component/file_2142700/content)

49. [[PDF] Development of a Simple Stellarator using Tilted Circular Toroidal ...](https://arxiv.org/pdf/2604.06677.pdf)

50. [Challenges of high power diode-pumped lasers for fusion energy](https://www.researching.cn/articles/OJ9eb992af446ddbde) - This paper reviews the different challenges that are encountered in the delivery of high power laser...

51. [[PDF] A Target Fabrication and Injection Facility for Laser-IFE](https://qedfusion.org/LIB/REPORT/CONF/SOFE03/Tillack.pdf) - Elements of the facility include mass production. (in batch mode) of cryogenic targets that meet the...

52. [National Ignition Facility – LLNL Annual Report FY2025](https://annual.llnl.gov/fy-2025/national-ignition-facility-2025) - Record 8.6 MJ yield from 2.08 MJ (7 April 2025), target gain 4.13.

53. [NIF User Forum: Optic Issues and Recovery Plan (LLNL, Aug 2025)](https://lasers.llnl.gov/sites/lasers/files/2025-08/NIF-User-Forum-Optic-Issues-and-Recovery-Plan.pdf)

54. [NIF status presentation, LSO workshop 2026 — LLNL (June 2026)](https://lasers.llnl.gov/sites/lasers/files/2026-06/lso-workshop-2026-wednesday-g-brunton.pdf)

55. [Wendelstein 7-X sets new fusion performance records – World Nuclear News (2025)](https://www.world-nuclear-news.org/Articles/Wendelstein-7-X-sets-new-fusion-performance-records)

56. [Wendelstein 7-X sets new performance records in fusion research (IPP, 2025)](https://www.ipp.mpg.de/5532945/w7x) - 43 s triple-product record; 360 s plasma with 1.8 GJ energy turnover.

57. [WEST sets a new plasma duration record – CEA-IRFM (Feb 2025)](https://irfm.cea.fr/en/2025/02/west-sets-a-new-plasma-duration-record/)

58. [China's EAST smashes fusion confinement record – Physics World (Jan 2025)](https://www.physicsworld.com/a/chinas-experimental-advanced-superconducting-tokamak-smashes-fusion-confinement-record/)

59. [EAST tokamak experiments exceed plasma density limit – PIIM / Aix-Marseille (2026); paper: Science Advances, doi:10.1126/sciadv.adz3040](https://piim.univ-amu.fr/en/actualite/east-tokamak-experiments-exceed-plasma-density-limit-offering-new-approach-to-fusion-ignition/)

60. [ITER baseline press conference summary (July 2024)](https://iter.org/sites/default/files/media/2024-07/baseline_press_conference_summary_july-2024_b.pdf)

61. [ITER fusion reactor hit by massive decade-long delay and €5bn price hike — Physics World](https://physicsworld.com/a/iter-fusion-reactor-hit-by-massive-decade-long-delay-and-e5bn-price-hike/)

62. [Fortune: Commonwealth Fusion SPARC update (Jan 2026)](https://fortune.com/2026/01/07/fusion-power-commonwealth-sparc-nuclear-fusion-pilot-ai-siemens-nvidia/)

63. [Commonwealth Fusion Systems on X: eight of 18 SPARC TF magnets installed (22 September 2026)](https://x.com/CFS_energy/status/2102395361390149897)

64. [US Department of Energy Validates Commonwealth Fusion Systems ...](https://cfs.energy/news-and-media/us-department-of-energy-validates-commonwealth-fusion-systems-completion-of-magnet-tech/)

65. [The SPARC Toroidal Field Model Coil Program — Hartwig et al., arXiv:2308.12301](https://arxiv.org/pdf/2308.12301)

66. [China's artificial sun advances (BEST construction status) – Interesting Engineering (Oct 2026)](https://interestingengineering.com/energy/chinas-artificial-sun-advances)

67. [China launches fusion-focused company — ANS Nuclear Newswire (July 2025)](https://www.ans.org/news/2025-07-30/article-7244/china-launches-fusionfocused-company/); [China sets out fusion progress, collaboration opportunities — World Nuclear News (January 2026)](https://www.world-nuclear-news.org/articles/china-sets-out-fusion-progress-collaboration-opportunities)

68. [JT-60SA upgraded and ready for restart – ANS Nuclear Newswire (May 2026)](https://www.ans.org/news/2026-05-15/article-8036/jt60sa-upgraded-and-ready-for-restart/)

69. [New world record set in JET's final fusion experiments – World Nuclear News (Feb 2024)](https://world-nuclear-news.org/articles/new-world-record-set-in-jet-s-final-fusion-experim)

70. [International agreement signed for fusion materials research facility](https://www.world-nuclear-news.org/articles/international-agreement-signed-for-fusion-materials-research-facility) - Fusion for Energy, representing the European Commission and Member States' contribution, together wi...

71. [IFMIF-DONES construction enters a new phase with the start of site works (17 Sep 2026)](https://ifmif-dones.es/dones-updates/ifmif-dones-construction-enters-a-new-phase-with-the-start-of-site-works/)

72. [Escúzar Town Council grants building permit for IFMIF-DONES](https://ifmif-dones.es/dones-updates/escuzar-town-council-grants-building-permit-for-ifmif-dones-paving-the-way-for-construction-to-begin-this-summer/)

73. [DONES Programme collaboration takes shape (F4E, Apr 2024: "could be operational by 2034")](https://fusionforenergy.europa.eu/news/dones-programme-collaboration-takes-shape/)

74. [DEMO Hot Cell and Ex-Vessel Remote Handling (UKAEA/CCFE)](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss29.pdf) - shutdown dose rates 13.1–17.4 kGy/h (blanket, 60 dpa) and 8.8–11.6 kGy/h (divertor, 30 dpa)

75. [QST repository: DEMO in-vessel component replacement and maintenance-port dose rates](https://repo.qst.go.jp/records/48891) - ITER in-vessel RH limit 250 Gy/h; DEMO surface dose rates two orders higher

76. [Pintsuk et al., EUROfusion material development and qualification roadmap, 4th DONES Users Workshop, Oct 2026](https://indico.ifmif-dones.es/event/92/contributions/1385/)

77. [Lumsdaine, US FPNS risk reduction activity, IAEA presentation 2025](https://conferences.iaea.org/event/425/contributions/37857/attachments/21714/37327/Arnie%20Lumsdaine.pdf)

78. [Unlocking Tritium for Fusion Energy (RSIS Commentary CO25215, 29 October 2025)](https://rsis.edu.sg/rsis-publication/rsis/unlocking-tritium-for-fusion-energy/) - Estimates the current global tritium stockpile at about 20 kg and ~14 kg by 2055 under moderate assumptions. (Replaces a Reddit thread cited in the June 2026 version.)

79. [[PDF] GLOBAL SUPPLY OF TRITIUM FOR FUSION R&D FROM HEAVY ...](https://scientific-publications.ukaea.uk/wp-content/uploads/3B76859550CE98DC127082F1E5B5381C8B96.PDF)

80. [Insights into fuel start‐up and self‐sufficiency for fusion energy: The ...](https://scijournals.onlinelibrary.wiley.com/doi/10.1002/ese3.291) - For a fusion reactor with 1 GW fusion power, about 37.1 kg deuterium and 55.6 kg tritium would be bu...

81. [[PDF] Tritium Breeding Blanket Technology, Tritium Fuel Cycle, and ...](https://www.fusion.ucla.edu/files/2022/12/FINAL-Abdou_Pilot-Plant-Session-FPA-12-7-2022.pdf) - Fusion, if it works, will be the ultimate energy source for mankind. • But the Pace of fusion develo...

82. [UKAEA-Eni H3AT Tritium Loop Facility](https://www.ukaea.org/work/ukaea-eni-h3at-tritium-loop-facility/) - UK Atomic Energy Authority and Eni have a ground-breaking collaboration to develop skills and techno...

83. [Kinectrics selected as design & fabrication partner for UKAEA-Eni Tritium Loop Facility (16 March 2026)](https://www.bnnbloomberg.ca/press-releases/2026/03/16/kinectrics-selected-as-design-fabrication-partner-for-ukaea-eni-tritium-loop-facility/)

84. [UKAEA: LIBRTI — The Lithium Breeding Tritium Innovation Programme](https://www.ukaea.org/work/librti/)

85. [CFS named first international partner in UKAEA's LIBRTI program (July 2026)](https://cfs.energy/news-and-media/cfs-named-first-international-partner-in-ukaeas-librti-program/)

86. [General Atomics invests $20 million in Canadian fusion venture to advance tritium fuel cycle technologies (UNITY-2)](https://www.ga.com/ga-invests-20-million-in-canadian-nuclear-fusion-venture-to-advance-tritium-fuel-cycle-technologies); [Kyoto Fusioneering: UNITY-2 construction start (November 2025)](https://kyotofusioneering.com/en/news/2025/11/04/3556)

87. [WNN: First concrete poured for Europe's first tritium removal facility (June 2025)](https://wnn.world-nuclear.org/articles/first-concrete-poured-for-europes-first-tritium-removal-facility); [WNN: Contract for Cernavoda tritium removal facility (June 2023)](https://world-nuclear-news.org/articles/contract-for-cernavoda-tritium-removal-facility)

88. [Isotopes from OPG's nuclear fleet advancing fusion energy research (OPG, November 2025)](https://interactive.opg.com/2025-november/watts-new/isotopes-from-opgs-nuclear-fleet-advancing-fusion-energy-research) - Context of the OPG–UKAEA tritium supply MoU of 22 September 2025.

89. [BABY 1L: First Tritium Breeding Campaign Results (arXiv:2509.26174, 2025)](https://arxiv.org/abs/2509.26174)

90. [L. Giancarli, ITER TBM Program overview (IAEA technical meeting, 2025)](https://conferences.iaea.org/event/406/contributions/37064/attachments/20785/35166/Luciano%20Giancarli%20-%20ITER.pdf) - DT-1/DT-2 phases; four TBS in equatorial ports #16 and #18; design by 2029, installation from 2035, operation from 2039.

91. [An Assessment of the Prospects for Inertial Fusion Energy (2013)](https://www.nationalacademies.org/read/18289/chapter/5) - Targets for ICF experiments are filled by permeation, Tritium breeding is accomplished in the blanke...

92. [[PDF] Inter-ELM power exhaust in tokamak fusion reactors](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss74.pdf) - ... DEMO. Since material limits require that Qmax t remain below ∼ 10 MW/m2 for ITER, and likely bel...

93. [X-point radiation, its control and an ELM suppressed radiating regime at the ASDEX Upgrade tokamak (Bernert et al., Nucl. Fusion 2021)](https://infoscience.epfl.ch/record/284513) - Full detachment at ~95% dissipated power fraction; ELM suppression.

94. [X-point radiator control and its dynamics in ASDEX Upgrade and JET deuterium–tritium discharges (Bosman et al., Nucl. Fusion 65, 016057, 2025)](https://research.tue.nl/en/publications/x-point-radiator-control-and-its-dynamics-in-asdex-upgrade-and-je/)

95. [UK's MAST Upgrade achieves record fusion plasma pressure (Innovation News Network, 10 Aug 2026)](https://www.innovationnewsnetwork.com/uks-mast-upgrade-achieves-record-fusion-plasma-pressure/72496/) - Fifth campaign (>1,100 discharges, 2025–2026); N-seeded Super-X double-null; QH-/I-mode; enhancement programme to 2027; sixth campaign 2028.

96. [DTT overview poster, 30th IAEA Fusion Energy Conference (2025)](https://conferences.iaea.org/event/392/contributions/35648/attachments/19722/36216/POSTER%20OV.pdf) - First plasma July 2032 (as indexed; page access restricted at time of writing).

97. [DTT reaches milestone with first toroidal magnet completed (EUROfusion / ENEA, 2025)](https://euro-fusion.org/member-news/enea/dtt-reaches-milestone-with-first-toroidal-magnet-completed/)

98. [Gyrokinetic projection of the divertor heat-flux width from present tokamaks to ITER (Chang et al., Nucl. Fusion 57, 116023, 2017; arXiv)](https://arxiv.org/abs/1701.05507) - XGC1 projects λq ≈ 5.9 mm for ITER vs ≤1 mm from empirical scaling.

99. [Tokamak Energy announces fusion power plant magnet technology breakthrough (November 2025)](https://tokamakenergy.com/2025/11/19/tokamak-energy-announces-fusion-power-plant-magnet-technology-breakthrough/)

100. [Proxima Fusion raises 411 million euros — Max Planck Society (July 2026)](https://www.mpg.de/26861952/proxima-fusion-raises-411-million-euros)

101. [Proxima Fusion seeks €2 billion to build a nuclear fusion test facility — The Next Web (February 2026)](https://thenextweb.com/news/proxima-fusion-seeks-e2-billion-to-build-a-nuclear-fusion-test-facility)

102. [TVA and Type One Energy to build 350 MW fusion plant — Neutron Bytes (September 2025)](https://neutronbytes.com/2025/09/20/tva-and-type-one-energy-to-build-350-mw-fusion-plant/)

103. [DOE approves Xcimer's laser fusion power plant design — ANS Nuclear Newswire (June 2026)](https://www.ans.org/news/article-8111/doe-approves-xcimer-laser-fusion-power-plant-design/)

104. [Xcimer activates Phoenix fusion laser — Nuclear Engineering International](https://www.neimagazine.com/news/xcimer-activates-phoenix-fusion-laser/)

105. [Focused Energy: $240 million, the largest Series A financing in the global fusion industry — Focused Energy (May 2026)](https://www.focused-energy.co/news-release/focused-energy-sets-a-new-benchmark-240-million-for-the-largest-series-a-financing-in-the-global-fusion-industry)

106. [Biblis wird zum Laserfusions-Hub — TU Darmstadt (July 2026)](https://www.tu-darmstadt.de/universitaet/aktuelles_meldungen/einzelansicht_572032.de.jsp)

107. [Helion secures land and begins building on the site of world's first fusion power plant — Business Wire (July 2025)](https://www.businesswire.com/news/home/20250730326704/en/Helion-Secures-Land-and-Begins-Building-on-the-Site-of-Worlds-First-Fusion-Power-Plant)

108. [Helion achieves new industry-first fusion energy milestones — Helion (February 2026)](https://helionenergy.com/newsroom/helion-achieves-new-fusion-energy-milestones)

109. [Trump Media to merge with fusion startup TAE Technologies in $6B deal — ANS Nuclear Newswire (December 2025)](https://www.ans.org/news/article-7632/trump-media-to-merge-with-fusion-startup-tae-technologies-in-6b-deal/); [status update: closing targeted Q4 2026 — The Next Web](https://thenextweb.com/news/trump-media-drops-truth-social-spinoff-refocuses-on-6-billion-fusion-merger-with-tae-technologies)

110. [Regulatory Framework for Fusion Machines, proposed rule — Federal Register 91 FR 9476 (26 February 2026)](https://www.govinfo.gov/content/pkg/FR-2026-02-26/html/2026-03865.htm)

111. [Fusion machine rulemaking status — US NRC](https://www.nrc.gov/materials/fusion/rulemaking-status)

112. [Energy Act 2023, section 156: Fusion energy facilities — nuclear site licence not required](https://www.legislation.gov.uk/ukpga/2023/52/section/156)

113. [£2.5 billion for world-first prototype fusion energy plant — GOV.UK (June 2025)](https://www.gov.uk/government/news/25-billion-for-world-first-prototype-fusion-energy-plant)

114. [German government pledges more than €2 bln for nuclear fusion — Clean Energy Wire (October 2025)](https://www.cleanenergywire.org/news/german-government-pledges-more-eu2-bln-nuclear-fusion)

115. [Energy Department releases finalized Fusion Science and Technology Roadmap — US DOE (June 2026)](https://www.energy.gov/node/4858962)

116. [Euratom fusion programme — European Commission presentation at IEA (February 2025)](https://iea.blob.core.windows.net/assets/98a960b8-ec25-4e85-8e88-7beddf6cabd5/ElenaRighi_EURATOM.pdf)

117. [W7-X Task Force goals for OP2.4/OP2.5 — IPP](https://www.ipp.mpg.de/5229513/TFI_goals.pdf)

118. [Google to buy power from Chesterfield fusion plant — Greater Richmond Partnership](https://www.grpva.com/news/google-to-buy-power-from-chesterfield-fusion-plant/)

119. [Google-backed CFS signs PPA with Italian energy company Eni — DatacenterDynamics](https://www.datacenterdynamics.com/en/news/google-backed-fusion-firm-commonwealth-fusion-systems-signs-ppa-with-italian-energy-company-eni/)

120. [A key challenge for inertial fusion energy (Journal Article) | OSTI.GOV](https://www.osti.gov/biblio/20783153) - Developing a commercial production process for 500,000 targets per day: A key challenge for inertial...

121. [Commercial compact fusion triggered REBCO tape industry: pulsed laser deposition technology opportunities and challenges — EurekAlert (2025)](https://www.eurekalert.org/news-releases/1101339)

122. [[PDF] RAMI: the challenge of Fusion Nuclear Technologies](https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/NJOCCPR17_18540_submitted-4.pdf) - This paper summarizes the RAMI statistics in existing fusion machines, the RAMI approaches adopted i...

123. [J. Seo et al., Avoiding fusion plasma tearing instability with deep reinforcement learning, Nature 626, 746 (2024)](https://www.nature.com/articles/s41586-024-07024-9)

124. [S. E. Wurzel and S. C. Hsu, Progress toward fusion energy breakeven and gain as measured against the Lawson criterion (Phys. Plasmas 2022)](https://arxiv.org/abs/2105.10954)

125. [Clark et al., Breeder blanket and tritium fuel cycle feasibility of the Infinity Two fusion pilot plant, J. Plasma Phys. (2025)](https://www.cambridge.org/core/product/248C49CCA0B7ABEA2F7BF7031290EDC4)

126. [S. Jachmich et al., ITER Disruption Mitigation System – IAEA FEC 2025 presentation](https://conferences.iaea.org/event/392/contributions/35757/attachments/19779/36445/3%20S_Jachmich-IAEA-FEC-2025_v2.1.pdf)
