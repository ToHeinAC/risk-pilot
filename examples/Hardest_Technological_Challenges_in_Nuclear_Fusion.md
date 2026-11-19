# Nuclear Fusion: The 5 Hardest Technological Challenges
### A Deep-Dive Analysis Across Tokamak, Stellarator, and Laser-Driven Inertial Confinement Fusion

*Reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps this overview to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

Despite record-breaking milestones — NIF's laser ignition in December 2022 producing 3.15 MJ from 2.05 MJ laser input, Wendelstein 7-X sustaining plasma for 8 minutes in 2023, and the ~20 T HTS Toroidal Field Model Coil test by CFS/MIT in 2021 **[corr. 2026-11]** — commercial fusion energy faces five systemic technological challenges that are intertwined, unresolved, and arguably harder than achieving ignition itself. This report identifies, decomposes, and cross-maps these challenges across the three leading realization pathways: **Tokamak** (T), **Stellarator** (S), and **Laser-Driven Inertial Confinement Fusion** (ICF).[^1][^2][^3][^4]

The five challenges are:

1. **Plasma Stability, Confinement & Turbulent Transport** — keeping the fuel hot and dense long enough
2. **Plasma-Facing Materials & Neutron Damage** — building a wall that survives the fusion environment
3. **Tritium Fuel Self-Sufficiency** — closing the fuel cycle with a net-positive breeding ratio
4. **Power Exhaust & Heat Removal** — handling gigawatt-scale heat fluxes without destroying the device
5. **Driver/Magnet Engineering & Steady-State Operation** — scaling the energy system to power-plant requirements

Each challenge is rated by technology readiness and cross-mapped to the three pathways.

***

## Challenge Overview Matrix

| Challenge | Tokamak | Stellarator | Laser ICF | TRL (2025; pathway system TRLs for 2026 see review section) |
|---|---|---|---|---|
| Plasma stability & turbulent transport | Critical (disruptions, ELMs) | Moderate (no disruptions, turbulence remains) | Critical (RT instability, symmetry) | 4–5 |
| Plasma-facing materials & neutron damage | Critical | Critical | Critical (first wall + optics) | 3–4 |
| Tritium self-sufficiency | Critical | Critical | Critical | 2–3 |
| Power exhaust & heat removal | Critical (divertor) | Moderate (island divertor) | Severe (cyclic shock loading) | 3–4 |
| Driver/magnet engineering & steady-state | High (pulsed vs. steady-state) | Moderate (coil complexity) | Severe (laser efficiency, rep-rate) | 2–4 |

***

## Challenge 1: Plasma Stability, Confinement & Turbulent Transport

### Core Problem Statement

The fusion triple product \(n \cdot T \cdot \tau_E\) — where \(n\) is plasma density, \(T\) is temperature, and \(\tau_E\) is the energy confinement time — must exceed a critical threshold (\(\sim 3 \times 10^{21}\) keV·s·m\(^{-3}\)) for ignition. Achieving this requires simultaneously sustaining temperatures exceeding 100 million °C and confining the plasma for long durations. Both objectives are undermined by instabilities and turbulence that bleed energy from the core far faster than classical theory predicts.[^5]

### Tokamak: Disruptions and ELMs

Tokamaks maintain plasma through a combination of external toroidal coils and an induced plasma current. This self-organized state is inherently fragile. When current or pressure profiles deviate from acceptable limits, the plasma can undergo a **disruption** — a sudden, total loss of confinement releasing stored thermal and magnetic energy in milliseconds. In ITER, disruptions could generate runaway electron beams of up to 12 MA, carrying energies of 20–200 MJ capable of melting reactor walls. Modeling shows that collisional suppression of runaway electron avalanche requires electron density increases of 300–700×, beyond ITER's pumping capability **[unconfirmed 2026-11]** (the factor could not be traced in the cited sources).[^6][^7][^8]

At the edge, **Edge-Localized Modes (ELMs)** — periodic eruptions of magnetohydrodynamic instability — eject bursts of plasma energy that erode plasma-facing components like miniature solar flares. ELM energy fluence projections for SPARC and ITER are 11–34 MJ m\(^{-2}\), far exceeding material endurance limits.[^9][^1]

Even without disruptions, **anomalous (turbulent) transport** remains the dominant energy loss mechanism in all operating regimes. Plasma microturbulence driven by ion-temperature-gradient (ITG) and trapped-electron-mode (TEM) instabilities creates a "sea of eddies" that transports heat from the hot core to the cool edge. Critically, interactions between long- and short-wavelength turbulent eddies can increase heat losses tenfold above standard models, and the mechanism in the pedestal region remains an open scientific problem.[^10][^11][^12][^13]

### Stellarator: Neoclassical Transport vs. Turbulence

Stellarators avoid disruptions entirely by eliminating the large plasma current. This is their central advantage. The Wendelstein 7-X (W7-X) experiment has confirmed that **neoclassical transport** — the dominant loss mechanism in un-optimized stellarators — can be engineered away through precision magnetic field shaping: W7-X demonstrated plasma profiles that would have been impossible in a less optimized device.[^14][^15][^1]

However, once neoclassical transport is suppressed, **turbulent transport takes its place** as the primary loss channel. Power balance analyses at W7-X show that the remaining neoclassical loss is insufficient to explain observed energy losses, implying large anomalous transport contributions. A further subtlety is that magnetic field optimization in 3D stellarator geometry creates a strong temperature dependence in neoclassical transport, meaning losses scale unfavorably at the extreme temperatures needed for a burning plasma.[^16][^15][^17]

### Laser ICF: Rayleigh–Taylor Instability and Implosion Symmetry

In inertial confinement fusion, a millimeter-scale fuel capsule is imploded at implosion velocities of ~350 km/s. Any non-uniformity in the drive or target surface is exponentially amplified by the **Rayleigh–Taylor instability (RTI)**: the heavier, accelerating shell interpenetrates the lighter fuel, breaking up the implosion and preventing hot-spot formation. Even in NIF's 2022 breakeven experiment, high-Z contaminants from the capsule liner were injected into the fuel hot spot.[^18][^19]

RTI operates in two phases:
- **Acceleration phase**: laser-nonuniformity seeds are imprinted on the ablation front and amplified
- **Deceleration phase**: the decelerating shell is unstable, mixing cold ablator material into the hot spot

The requirement for implosion symmetry is extreme: typical tolerances are at the 10 µm level for surface finish and sub-percent uniformity for shell thickness. At indirect drive (NIF), an intermediate hohlraum converts laser light to X-rays, smoothing the drive at the cost of ~80% energy loss in the conversion step. Direct drive achieves higher laser-to-target coupling efficiency but requires laser beam uniformity that current systems cannot deliver.[^20][^21][^22]

### Key Open Questions for Further Analysis

- Can plasma control systems detect pre-disruption signatures fast enough to intervene in ITER/DEMO-scale machines?
- What is the quantitative scaling of turbulent transport to burning-plasma temperatures in stellarators?
- Can laser beam smoothing techniques (e.g., spatiotemporal partially coherent sources) reduce RTI seeds to acceptable levels?[^23]
- Does magnetic field assistance in ICF implosions meaningfully suppress RTI growth?[^24]

***

## Challenge 2: Plasma-Facing Materials (PFMs) and Neutron Damage

### Core Problem Statement

In a DT fusion reactor, 80% of the fusion energy is carried by 14.1 MeV neutrons. Unlike fission reactors, which operate at ~2 MeV neutron energies, fusion neutrons have sufficient energy to displace lattice atoms in structural materials at unprecedented rates, creating damage measured in **displacements per atom (dpa)**. DEMO first-wall materials are expected to accumulate 70 dpa over blanket lifetime, a material environment for which no validated data exists at scale.[^25][^26]

### Tungsten: The Leading PFM Candidate

Tungsten (W) is the primary candidate for plasma-facing armor due to its exceptional heat resistance and low tritium retention. However, neutron bombardment causes several compounding problems:[^27][^28][^29]

- **Lattice damage and embrittlement**: Increases in the ductile-to-brittle transition temperature (DBTT) mean tungsten becomes brittle at the temperatures encountered in operation
- **Transmutation**: 14 MeV neutrons convert W to Rhenium (Re) and then Osmium (Os) via neutron capture reactions (specifically \(^{184}\text{W}(n,\gamma)\) and \(^{186}\text{W}(n,\gamma)\)); Os is particularly embrittling[^27]
- **Reduced thermal conductivity**: Lattice defects degrade the thermal conductivity by which W dissipates plasma heat loads
- **Void swelling**: Vacancy clusters coalesce into voids, causing dimensional instability
- **Tritium trapping**: Neutron-induced defects increase T retention in W, posing radiological concerns

A fundamental research limitation is the absence of a high-flux 14 MeV neutron source for materials qualification testing at reactor-relevant fluences. IFMIF itself was never built; its successor IFMIF-DONES in Granada is now under construction (international agreement November 2025, building permit June 2026, Main Building targeted for ~2029; first neutrons not officially dated) **[corr. 2026-11]**.[^30]

### Tokamak and Stellarator: Shared but Geometrically Distinct Challenges

Both tokamaks and stellarators face the same neutron damage problem, but geometry matters:
- In tokamaks, the **divertor** region — where heat and particles are exhausted — sustains the highest heat and particle fluxes, driving extremely rapid erosion
- In stellarators, the **complex 3D geometry** makes blanket design, shielding, and remote maintenance far more difficult. Recessed coils with complex shapes limit port access and make blanket module replacement a profound engineering problem[^31]

Neutron activation of the entire reactor structure creates **radiological environments** where dose rates near the first wall immediately after shutdown are ~5 × 10\(^5\) Sv/hr, approximately 10\(^{10}\) times human occupational limits **[unconfirmed 2026-11]** (the value is not supported by the cited source and is likely overstated; the conclusion that maintenance must be fully remote is unaffected). All maintenance must therefore be fully robotic, using manipulators that must themselves survive high radiation doses.[^32]

### Laser ICF: First Wall and Optics Damage

In laser ICF, each fusion shot is equivalent to exploding ~10 kg of TNT in the target chamber. The first wall must:[^30]
- Withstand ~10\(^5\) shots per day at a repetition rate of ~5–10 Hz[^33]
- Survive cyclic thermal shock, energetic X-ray and neutron bombardment, and debris from each microexplosion
- Maintain chamber pressure conditions compatible with injecting the next target within ~0.1–0.2 seconds

Simultaneously, the laser **final optics** — located inside or adjacent to the chamber — must survive debris and neutron bombardment. This was a central problem at NIF even at single-shot operation rates; scaling to 10 Hz rep-rate amplifies the problem by ~5 orders of magnitude.[^34][^35]

### Key Open Questions for Further Analysis

- Can reduced-activation ferritic/martensitic steels (RAFM), tungsten alloys, or oxide-dispersion-strengthened (ODS) materials meet combined heat flux, dpa, and transmutation requirements?
- What is the minimum wall replacement cycle compatible with economic power plant operation?
- How can laser final optics be engineered to survive IFE rep-rate conditions?
- Is a dedicated fusion neutron source (IFMIF-DONES) an indispensable prerequisite to DEMO licensing?

***

## Challenge 3: Tritium Fuel Self-Sufficiency

### Core Problem Statement

All near-term fusion concepts rely on the deuterium-tritium (DT) reaction because it has the highest cross-section at achievable temperatures. Deuterium is abundant, but **tritium** does not exist naturally on Earth in useful quantities: the global civil stockpile is estimated at roughly 20–30 kg (estimates differ; the tritium deep dive uses 25–30 kg), enough to operate a single 1 GW fusion reactor for about four to six months. A plant with 1 GW of fusion power burns about **150 g of tritium per day** (~55.6 kg per full-power year) **[corr. 2026-11]** (was: "22 kg", "less than four months", "184 g/day").[^36]

The solution is to breed tritium in a **Tritium Breeding Blanket (TBB)** that surrounds the reactor. Lithium in the blanket absorbs fusion neutrons via two reactions:

\[^6\text{Li} + n \rightarrow T + ^4\text{He} + 4.8 \text{ MeV}\]
\[^7\text{Li} + n \rightarrow T + ^4\text{He} + n' - 2.5 \text{ MeV}\]

The key figure of merit is the **Tritium Breeding Ratio (TBR)** — the number of tritium atoms produced per tritium atom consumed. A TBR > 1.0, with sufficient margin for losses, is mandatory for tritium self-sufficiency.[^37][^38]

### Why TBR > 1 Is Not Guaranteed

The fundamental constraint is that each DT reaction produces exactly **one neutron**. After accounting for:[^39]
- Neutron parasitic absorption in structural materials, coolants, and magnets
- Geometric coverage losses (port penetrations for heating systems, diagnostics, maintenance access)
- Tritium permeation through blanket structures
- Incomplete tritium extraction efficiency from breeding materials

…achieving a net TBR > 1 with sufficient margin for start-up inventories becomes extremely difficult. A 2022 analysis found that with current technology, the best achievable TBR is approximately **1.15 (15% margin)**, with a more likely central estimate of only ~1.05. A tritium permeation loss rate of just 0.1% — small by engineering standards — was assumed in this analysis, but tritium is notoriously aggressive in permeating metal walls.[^39]

### Blanket Technology Challenges

Several tritium breeding blanket concepts are under development (Helium-Cooled Pebble Bed HCPB, Water-Cooled Lithium Lead WCLL, Dual-Coolant Lead-Lithium DCLL), each with distinct trade-offs in:
- **Structural compatibility**: temperature limits of Li-Pb liquids vs. solid Li ceramics impose different constraints on blanket design[^40]
- **Tritium extraction kinetics**: solid breeders release tritium slowly, requiring elevated temperatures; liquid metal breeders enable continuous tritium extraction but introduce magnetohydrodynamic (MHD) effects in liquid metal flows
- **Blanket coverage**: any fusion device must reserve large fractions of the wall area for heating ports, diagnostics, and maintenance access, directly reducing neutron capture efficiency

No tritium breeding blanket has yet been tested at fusion-relevant neutron fluxes. The first integrated TBB test module is planned for ITER, but ITER itself does not breed tritium — it depends on external supply.

### Laser ICF: An Especially Severe Problem

For ICF power plants, the **tritium inventory challenge** is amplified because target filling requires multi-day diffusion processes under high pressure. A filling inventory of up to ~10 kg of tritium (an upper-end estimate from older IFE plant studies) — a large share of, but not larger than, the global civil stockpile **[corr. 2026-11]** — would be at risk as high-pressure gas if containment failed. Furthermore, ICF needs its blanket to cover a spherical cavity that is punctured by multiple laser beam ports, beam lines, target injection systems, and exhaust diagnostics, making geometric coverage — and hence TBR — even harder to achieve.[^21][^41]

### Key Open Questions for Further Analysis

- Can neutron multiplier materials (Be, Pb) compensate for geometric coverage losses enough to ensure TBR > 1.05 in a realistic power plant?
- What is the minimum tritium inventory needed to "start up" the first generation of fusion power plants, given finite stockpile?
- Can rapid tritium extraction (real-time online processing) enable operation with lower blanket TBR margins?
- Is a dedicated tritium-producing fission reactor needed to bridge the tritium gap between now and first-of-kind fusion power plants?

***

## Challenge 4: Power Exhaust and Plasma Heat Removal

### Core Problem Statement

A 1–2 GW fusion reactor must exhaust ~hundreds of MW of plasma power that is not radiated from the core. This power is channeled by magnetic topology into a narrow **scrape-off layer (SOL)**, typically only millimeters wide, and strikes the **divertor** target plates over a small wetted area. The resulting unmitigated heat flux **perpendicular to the divertor target** can reach ~150 MW m\(^{-2}\) for DEMO (the parallel heat flux along the field lines is of order GW m\(^{-2}\)) **[corr. 2026-11]**, while the material engineering limit is 5–10 MW m\(^{-2}\). This represents a factor of **15–30× gap** between what the plasma produces and what materials can survive continuously.[^42]

For SPARC's compact high-field design, unmitigated peak **parallel** heat fluxes are projected to exceed **10 GW m\(^{-2}\)** **[corr. 2026-11]** — nearly an order of magnitude beyond any demonstrated value.[^9]

### Tokamak: ELM Heat Pulses and Divertor Design

Standard tokamaks in H-mode (high-confinement mode) generate periodic ELMs that deposit intense heat pulses on the divertor. For ITER, each ELM can deposit ~10 MJ m\(^{-2}\) on divertor tiles in less than 1 ms — analogous to a powerful welder moving across the surface. Sustained operation at this level will erode divertor material on timescales of weeks to months.[^1][^9]

Mitigation strategies include:
- **Impurity seeding** (Ne, Ar, N injection) to radiate power uniformly before it reaches the divertor
- **ELM suppression/pacing** using resonant magnetic perturbations (RMPs) or pellet injection
- **Advanced divertor geometries**: Super-X, X-point target, Snowflake configurations that extend the magnetic flux tube and increase the wetted area[^43][^42]

The MAST-Upgrade tokamak has demonstrated Super-X divertor operation with substantially improved exhaust control, showing that divertor shaping combined with neutral baffling can significantly reduce surface heat fluxes. However, these configurations have not been validated at ITER- or DEMO-scale power densities.[^42]

### Stellarator: Island Divertor and Inherent Advantages

W7-X uses an **island divertor** that exploits naturally occurring magnetic islands at the plasma boundary for particle and heat exhaust. W7-X has demonstrated stable plasma detachment with good particle exhaust and low impurity content sustained for tens of seconds. The absence of ELMs is a significant stellarator advantage for divertor loading.[^14]

However, the complex 3D magnetic geometry of a stellarator makes the heat exhaust problem geometrically harder to engineer than in the axisymmetric tokamak: island divertor geometry is non-trivial, and pumping access for particles is constrained by the same 3D coil structure that complicates blanket design.[^44]

### Laser ICF: Cyclic Thermal Shock

In ICF, the power exhaust problem is fundamentally different: instead of a continuous heat load, the **first wall experiences a periodic impulse** from each microexplosion (~10 kg TNT equivalent) at 5–10 Hz repetition rate. The first wall must:[^30]
- Survive X-ray and ion deposition from each shot without ablation exceeding replacement tolerances
- Cope with cyclic thermal stress fatigue over the reactor lifetime (~10\(^{10}\) shots)
- Maintain geometric precision for the target chamber and optical alignment

Several approaches (dry walls, wet walls, magnetic diversion, grazing-incidence protection) have been proposed but none demonstrated at IFE rep-rate conditions. This is an essentially unsolved problem for commercial ICF.

### Key Open Questions for Further Analysis

- Can advanced divertor geometries (Super-X, X-point target) be practically integrated into DEMO-scale tokamaks?
- What is the maximum power that can be radiated as impurity seeding without destabilizing the core plasma?
- Can liquid metal divertor targets (Li, Sn) replace solid tungsten at reactor scale?
- How does the island divertor of W7-X scale to reactor-relevant power densities?
- What first-wall concepts are viable for ICF at 5–10 Hz rep-rates?

***

## Challenge 5: Driver & Magnet Engineering, and Steady-State Operation

### Core Problem Statement

Even if all physics challenges are resolved, a commercial fusion power plant must operate economically and reliably. This requires the **energy driver** (magnets for MCF, lasers for ICF) to: (a) deliver fusion conditions efficiently enough that the recirculating power fraction is manageable, and (b) operate continuously (MCF) or at very high repetition rates (ICF) for decades. Neither condition is close to being demonstrated.

### Tokamak: Steady-State Operation and Superconducting Magnets

Conventional tokamaks drive plasma current inductively via a central solenoid — an inherently **pulsed** configuration. A commercial power plant operating in pulses faces severe engineering penalties: thermal cycling fatigue on structural components, duty-cycle power averaging, and the need for large flywheels or energy storage to smooth pulsed output.[^45][^1]

Achieving **steady-state** requires replacing 100% of the inductive current drive with:
- **Bootstrap current**: self-generated from pressure gradients (~50–80% in advanced scenarios)
- **Neutral Beam Injection (NBI)** and **Radio-Frequency (RF) current drive** for the remainder

As of 2025, steady-state operation with high confinement (\(nT \sim 10^{20}\) keV m\(^{-3}\), T > 5 keV) has never been demonstrated. The current drive efficiency required (~0.2–0.3 × 10\(^{20}\) A W\(^{-1}\) m\(^{-2}\)) must be achieved without consuming an unacceptably large fraction of the fusion power as recirculating current-drive power.[^46][^45]

High-Temperature Superconductor (HTS) magnets represent the most transformative magnet advance: Commonwealth Fusion Systems and MIT demonstrated a **~20 T HTS model coil (TFMC)** in 2021 **[corr. 2026-11]**; a full-scale SPARC TF magnet passed the DOE milestone review in 2025, enabling compact high-field tokamaks (SPARC, ARC) that could achieve Q = 11 at much smaller scale than ITER. The higher field reduces the size — and thus cost — of the device as confinement scales approximately as \(B^2 R^3\). However, challenges remain in:[^4][^47]
- **Radiation hardness** of HTS tape (REBCO) under neutron irradiation
- **Joint design** for high-current HTS cables that can be rewound after damage
- **Manufacturing scalability** for kilometers of high-performance tape needed per reactor

### Stellarator: 3D Coil Precision and Reactor-Scale Manufacturing

Stellarators require **complex, non-planar superconducting coils** whose 3D shapes must be maintained to millimeter precision. W7-X used 50 non-planar and 20 planar superconducting coils; average deviations from the designed coil shape were kept below 3 mm, a remarkable manufacturing achievement — but this took years of precision engineering at high cost.[^48][^31]

Scaling to a reactor:
- Reactor-scale coils will be physically larger, making mm-level relative tolerances harder to achieve
- Field errors from coil misalignment create **magnetic islands** that degrade confinement[^44]
- The complex geometry severely restricts port access, making blanket maintenance and remote handling a multiplied challenge[^31]
- **HTS application to 3D coils** has been demonstrated computationally but not experimentally at scale[^31]

Reactor-scale stellarators remain entirely unproven. There is genuine uncertainty about whether the coil complexity and cost will prove manageable at commercial scale.[^49][^44]

### Laser ICF: Driver Efficiency and Repetition Rate

For ICF, the laser wall-plug efficiency — the ratio of laser energy delivered to the electrical energy drawn by the laser **[corr. 2026-11]** — is currently **less than 1%** at NIF. Engineering breakeven needs a driver-efficiency × target-gain product of ηG ≈ 2.6, an economic plant ηG ≳ 10, i.e. target gains of roughly 50–100 **[corr. 2026-11]** (was: "gain Q ~ 100–200"); the laser system must therefore achieve **~10–20% wall-plug efficiency** at repetition rates of **~5–10 Hz**.[^35][^34][^30]

NIF's flashlamp-pumped Nd:glass architecture cannot achieve this: the laser glass has a ~350 μs excited-state lifetime, generating enormous heat in the gain medium at high rep-rate, causing thermal lensing, wavefront distortion, and birefringence that destroy beam quality. The required advances require a complete **paradigm shift in laser architecture**:[^35]

- **Diode-pumped solid-state lasers (DPSSL)** with ceramic or crystal gain media offer higher efficiency and thermal conductivity but face challenges in scaling to MJ-class energies at 10 Hz[^50]
- **Krypton fluoride (KrF) gas lasers** offer short wavelength (248 nm, improving coupling efficiency) and natural high-rep-rate capability but lower energy per pulse
- **Fiber laser architectures** with coherent beam combination are being explored[^23]

Simultaneously, approximately **500,000 cryogenic DT targets per day** must be manufactured, filled, layered, and injected with 10 µm-level surface tolerances. Current NIF targets cost thousands of dollars each; an IFE target must cost ≲ $0.30 **[corr. 2026-11]** (the Challenge 5 deep dive's figure; "$0.20" was inconsistent with it). No pilot-scale target factory exists. Targets must survive injection into the hot chamber without the DT ice layer deforming — a temperature management problem at the micro-Kelvin level for a cryogenic object moving at ~100–200 m/s.[^51][^22][^41]

### Key Open Questions for Further Analysis

- What is the minimum recirculating power fraction consistent with economically viable fusion electricity at Q ~ 10 (ITER-baseline) vs. Q ~ 50 (commercial target)?
- Can HTS magnets in tokamaks survive a decade of 14 MeV neutron bombardment without replacement?
- What is the achievable efficiency of DPSSL or KrF laser drivers at 10 Hz and MJ-class pulse energies?
- Can stellarator coil geometry be simplified (e.g., tilted circular toroid) without sacrificing optimization gains?[^49]
- Is the ICF target cost target of ~$0.30/target **[corr. 2026-11]** economically achievable with mass production?

***

## Cross-Cutting Themes and Systemic Risks

### Absence of a Fusion Materials Test Facility

No existing facility can test materials under the simultaneous conditions of 14 MeV fusion neutrons at reactor-relevant fluence rates. The planned IFMIF-DONES (International Fusion Materials Irradiation Facility – DEMO-Oriented NEutron Source) would address this but is not yet operational. This is arguably the single most important missing experimental infrastructure: without validated materials data, DEMO designs rest on extrapolation.[^26][^30]

### The Integrated Challenge

None of the five challenges is independent. High-performance plasma (challenge 1) requires tighter engineering tolerances on plasma-facing materials (challenge 2) and increases tritium burning rates (challenge 3). Higher power output exacerbates heat exhaust (challenge 4) and demands more efficient energy drivers (challenge 5). Solving each challenge individually is insufficient; the challenges must be solved simultaneously in an integrated system that has never before been built.

### Pathway Comparison: Relative Difficulty

| Challenge | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Disruptions / implosion instability | **Hardest** (disruptions + ELMs) | Easiest (no disruptions) | **Hardest** (RT instability, nm tolerances) |
| Anomalous turbulent transport | Moderate | Moderate (neoclassical solved, turbulence remains) | Less relevant (burn time ~ns) |
| Neutron damage to materials | Moderate | **Harder** (3D geometry limits shielding/maintenance) | Hardest (+ rep-rate shock loading + optics) |
| Tritium breeding | Moderate | **Harder** (geometry-limited blanket coverage) | Hardest (large inventory + geometry) |
| Power exhaust | Moderate (advanced divertors advancing) | Moderate (island divertor promising) | Different (cyclic shock, unsolved) |
| Driver/steady-state | Moderate (HTS progress, steady-state unsolved) | Hard (coil complexity, no reactor prototype) | **Hardest** (efficiency ×100 improvement needed, target factory nonexistent) |

***

## Research Roadmap Anchors

The following open problems represent the highest-leverage research targets, ranked by their potential to unblock the commercialization pathway:

1. **Disruption prediction and avoidance in large-current tokamaks** — machine learning-based precursor detection, massive gas injection validation, runaway electron mitigation in ITER-scale experiments
2. **Turbulence modeling and suppression** — validation of gyrokinetic codes against burning-plasma experiments; identification of turbulence suppression mechanisms (E×B shear, Shafranov shift) at reactor-relevant \(q^*\) values
3. **14 MeV neutron materials database** — construction and operation of IFMIF-DONES; irradiation campaigns on W alloys, RAFM steels, ODS materials at dpa rates of 20+ dpa/year
4. **Tritium breeding blanket integrated testing** — full-scale mock-up testing of TBB modules in ITER's Test Blanket Module program; modeling of tritium permeation and extraction kinetics
5. **Advanced divertor validation at reactor-relevant power densities** — Super-X and X-point target configurations in MAST-U, DTT, and ultimately SPARC/ITER; liquid metal divertor development
6. **HTS magnet radiation hardness and joint technology** — neutron irradiation testing of REBCO tapes and joint designs; scalable manufacturing processes for reactor-grade magnet systems
7. **High-efficiency, high-rep-rate laser driver** — DPSSL or KrF architecture demonstration at 1–10 kJ and 1–10 Hz; wall-plug efficiency target of 10%+
8. **IFE target mass-production pilot facility** — demonstration of cryogenic target fabrication at 10–100 Hz; development of fluidized-bed layering and automated injection systems

***

## Conclusion

The path to commercial fusion energy is not gated by a single technological breakthrough but by the simultaneous resolution of five interconnected challenges, each representing decades of additional engineering work. Tokamaks are most mature (ITER under construction) but face unresolved disruption and steady-state problems. Stellarators have unique stability advantages but face unproven reactor-scale coil engineering and no burning-plasma demonstration. Laser ICF has achieved scientific breakeven but requires ~100× improvement in laser efficiency, the creation of an entire target manufacturing industry, and solutions to first-wall survival under cyclic impulse loading that do not currently exist.[^2][^3][^35][^30]

The most consequential gap across all pathways is the **absence of an integrated fusion nuclear environment** — a facility that combines burning-plasma neutron flux, tritium breeding, and power extraction in a single machine operating for years. Until such a facility operates, critical systems integration questions will remain unanswered. This is precisely what DEMO is designed to be — and the challenge of building it is the meta-challenge that encompasses all five identified above.

---

## Review & Model Update (November 2026)

This section records the review of 3 November 2026 and the extension of the report to the question of whether fusion
will become usable for **large-scale energy generation**. It is the entry point for the five deep dives, whose
own review sections cover each challenge in detail. An earlier, unversioned November update of these reports
exists in the repository history (commit `439bd79`, 2 Nov 2026). Its gate-year distributions were used as
priors and are labelled "not re-verified" wherever they were not checked again.

### R.1 Research question and scope

| Field | Definition |
|---|---|
| Central question | What is the probability that fusion becomes usable for energy generation at large scale? |
| Operational target | **≥ 10 GWe** of fusion capacity installed worldwide by one pathway (`jahr_gross`). Intermediate milestones: first demonstration/pilot plant delivering net electricity (TRL 8, `jahr_demo`) and first commercial plant (TRL 9, `jahr_kom`). |
| Horizon / cut-off | 2100 / evidence as of 3 November 2026 |
| Pillars and pathways | Pillar 1 **magnetic confinement**: tokamak, stellarator. Pillar 2 **inertial confinement** (laser-driven): **direct drive**, **indirect drive**. |
| Questions per pathway | (1) Technology readiness (TRL), (2) licensing/permit, (3) funding |
| Excluded | Other concepts (FRC/Helion, Z-pinch, pulser-driven or magneto-inertial fusion, heavy-ion drivers), advanced fuels. The modelled probability is therefore a **lower bound** for "fusion at large scale" in general. |

### R.2 Currency and claim check of this overview

| ID | Location | Original statement | Finding | Status |
|---|---|---|---|---|
| OV-01 | Executive summary, Ch. 5 | SPARC "20.8 T HTS magnet" | The 2021 model-coil test reached ~20 T; not re-researched, consistent with the C5 deep dive | corrected |
| OV-02 | Overview matrix | "TRL (2025)" per challenge | Challenge-level only. Pathway system TRLs for 2026 are in R.3 | supplemented |
| OV-03 | Ch. 1 | "300–700×" density increase for RE suppression | Not traceable in the cited sources | unconfirmed |
| OV-04 | Ch. 2 | "IFMIF … not yet operated at full specification" | IFMIF was never built. IFMIF-DONES has a building permit (16 Jun 2026) [R29], and Main Building preparatory works began Sep 2026 with completion around 2029 [R30] | corrected |
| OV-05 | Ch. 2 | Dose rate "~5 × 10⁵ Sv/h" | Not supported by the cited source (VLT web page) and likely overstated | unconfirmed |
| OV-06 | Ch. 3 | "22 kg … less than four months … 184 g/day" | 1 GW fusion power burns ~150 g/day (55.6 kg/fpy, simple calculation). The stockpile estimate is inconsistent with the tritium deep dive (25–30 kg) | corrected |
| OV-07 | Ch. 3 | ICF "~10 kg … larger than the global stockpile" | False comparison: 10 kg is less than the 20–30 kg stockpile. It is also an upper-end estimate from older plant studies | corrected |
| OV-08 | Ch. 4 | "parallel heat flux … 150 MW m⁻²" | 150 MW m⁻² is the unmitigated **perpendicular** target load; the parallel flux is GW m⁻² | corrected |
| OV-09 | Ch. 5 | Wall-plug definition; "Q ~ 100–200" | The definition was wrong. The requirement is better expressed as ηG ≳ 10 (economic) or ≈ 2.6 (engineering breakeven) | corrected |
| OV-10 | Ch. 5 | Target cost "< $0.20" | Inconsistent with the deep dive (≲ $0.30) | corrected |
| OV-11 | Whole report | "Laser ICF" as one pathway | Direct and indirect drive differ in physics maturity, driver, target, licensing and funding (R.4) | split |
| OV-12 | Whole report | Only technology challenges | Licensing/permit and funding are not covered, although they gate deployment (R.3) | supplemented |
| OV-13 | References | Mixed source quality | Several references are a YouTube video [^1], a personal blog [^44] or tertiary pages. Central claims should rest on primary sources | flagged |
| OV-14 | Ch. 5 conclusion | "ITER under construction" and timeline implicit | ITER Baseline 2024: SRO 2034, full magnetic energy 2036, DT 2039 [R1] | confirmed |

### R.3 Status November 2026 by pathway and question

| Pathway | (1) TRL — system level, Nov 2026 | (2) Licensing / permit | (3) Funding |
|---|---|---|---|
| **Tokamak** | **TRL 4–5** (model constant 5). No MCF device has produced Q > 1. SPARC was ~75 % built in April 2026; first plasma is now targeted for 2027 [R2], and TF-magnet installation slipped against the summer-2026 plan [R3] (secondary). ITER: SRO 2034, DT 2039 [R1]. Components are higher: HTS TF magnet ~6, ITER LTS magnets 6–7. | US: NRC proposed rule under the byproduct-material framework (Part 30), published 26 Feb 2026 [R5]. The final rule was targeted for Oct 2026, and the legal deadline is 31 Dec 2027 [R6][R7]. Publication of the final rule could **not** be confirmed on 3 November 2026. UK: Energy Act 2023. DE: amendment of the Radiation Protection Act in consultation [R10][R11]. No plant with a kg-scale tritium inventory has yet been licensed. | Broadest base: ITER, EU-DEMO and Chinese public programmes, plus CFS (~USD 3 bn private; offtake agreements with Google and Eni). Industry-wide: USD 4.48 bn raised in the 12 months to July 2026 and USD 14.24 bn since 2021 [R4]. |
| **Stellarator** | **TRL 3–4** (model 4). W7-X shows optimised confinement and long pulses, but there is no DT operation and no reactor-grade 3D HTS coil set. Proxima's Stellarator Model Coil is planned for 2027 and Alpha for the early 2030s [R13]. | Same frameworks as the tokamak. Precedent: Tennessee issued the first fusion-specific byproduct-material licence in the US to Type One Energy on 31 Aug 2026 [R8][R9]. | Proxima raised EUR 411 M in Jul 2026; Alpha also needs EUR 1.2 bn of federal funds, which were not yet committed [R13]. Type One closed a Series B of USD 200 M [R14] (secondary). Public: IPP/W7-X and the German action plan (> EUR 2 bn to 2029) [R10]. |
| **Direct drive** | **TRL 3** (model 3). No direct-drive ignition. OMEGA (~30 kJ) implosions are hydrodynamically equivalent to a burning plasma if scaled to ≥ ~1.7 MJ [R24], with hot-spot gain > 1 [R23] and record scaled Lawson parameters > 0.9 [R25]. No MJ-class direct-drive facility exists. Drivers: Xcimer's excimer prototype Phoenix has operated since June 2026 [R19]; diode-pumped solid-state lasers. | Direct-drive ICF has been largely declassified since the 1970s [R27]. Licensing follows the byproduct-material or radiation-protection route; tritium in the target factory and the chamber is the main licensing object. | Focused Energy raised USD 240 M in May 2026 (Biblis site) [R21], with company milestones of first implosion 2033 and first grid MWh 2037 [R22] (secondary). Xcimer has ~USD 200 M private funding plus up to USD 39.5 M in DOE milestones [R18]. |
| **Indirect drive** | **Physics TRL high, system TRL 3–4** (model 4). NIF: ten ignitions, record 8.6 MJ from 2.08 MJ (gain 4.13) [R15][R16]. The Enhanced Yield Capability upgrade (~40 MJ) is planned [R16]. Shots are single, wall-plug efficiency is < 1 %, and there is no rep-rated driver or target factory. | Parts of hohlraum physics are classified in the US. The NAS (2013) rated the proliferation concern higher for indirect than for direct drive, but considered it manageable [R26][R28]. Export controls apply [R27]. This lengthens licensing and export, but is not a categorical block. | Inertia Enterprises raised USD 450 M in Feb 2026 (Thunderwall: 10 kJ, 10 Hz, 10 % wall-plug) [R17]. NIF and LMJ are funded by weapons programmes, not as energy programmes. |

Counter-evidence and calibration: an MIT CEEPR working paper derives investor-implied commercialization
probabilities that are mostly below 20 % [R31]. Company roadmaps (grid power in the 2030s) lie at the
optimistic end. The model covers this range with an explicit "industry roadmap" scenario instead of building it
into the base case.

### R.4 Why laser ICF is split into direct and indirect drive

| Challenge | Direct drive | Indirect drive |
|---|---|---|
| Plasma / implosion | Higher hydrodynamic coupling, but no ignition yet. Laser imprint, cross-beam energy transfer and laser-plasma instabilities are the main risks. Ignition needs a new MJ-class facility [R24]. | Ignition repeatedly demonstrated [R16]. Gain is limited by hohlraum coupling (only part of the laser energy reaches the capsule), so higher gains are needed for the same plant balance. |
| Materials / chamber | Neutron and X-ray loads as for indirect drive. More symmetric beam ports mean more final optics exposed. | Additional high-Z hohlraum debris (e.g. gold or lead) in the chamber; material recovery is needed. |
| Tritium | Simpler capsule, smaller in-process inventory. | More complex target assembly; longer fill and layering chain; larger in-process inventory. |
| Driver / targets | Excimer (KrF/ArF) or DPSSL drivers. Cheaper targets. | DPSSL drivers (e.g. Thunderwall). Costlier targets (hohlraum + capsule) against a ≲ $0.30 target. |
| Licensing | Largely declassified [R27]. | Classification and export-control issues [R26][R27]. |
| Hybrid cases | Xcimer is testing externally driven half-hohlraums for its two-beam concept [R20] (secondary). Such concepts sit between the two branches and are modelled with direct-drive driver parameters. | — |

### R.5 Model structure (risk-pilot, schema version 1)

Files: `kernfusion_gesamt.yaml` (main model, all four pathways), and the sub-models `kernfusion_tokamak.yaml`,
`kernfusion_stellarator.yaml`, `kernfusion_direct_drive.yaml` and `kernfusion_indirect_drive.yaml`. All five are
generated from one parameter set, so a node has the same ID, numbers and source notes in the main model and in
its sub-model. Node prefixes: `tok_`, `stl_`, `dir_`, `ind_`; shared nodes `g_`.

```
Large-scale fusion (jahr_gross = min of the pillars; outputs for 2050/2060/2075/2100)
├── Pillar 1 magnetic confinement (mcf_jahr = min)
│   ├── Tokamak ──┐
│   └── Stellarator ┤   each pathway <p>:
├── Pillar 2 inertial confinement (ife_jahr = min)
│   ├── Direct drive ─┤   (1) TRL:       gates PL, MA, TR, EX, DR (year + show-stopper)
│   └── Indirect drive┘                  <p>_trl7 = max(PL, DR) + tempo   (demo-ready)
│                                        <p>_nuk  = max(MA, TR, EX) + tempo (validated in demo operation)
│                         (2) Licensing:  <p>_lic_jahre = duration + delay + fission-like regime; <p>_lic_block
│                         (3) Funding:    <p>_bedarf, <p>_fund_fail (p depends on need, climate, TRL timing),
│                                         <p>_fin_verz
│                         deployment:    FID → demo (TRL 8) → first commercial plant (TRL 9) → ≥ 10 GWe
└── shared: g_klima (funding climate), g_tempo, g_rahmen (framework in force), g_regime (fission-like
    regulation), g_dones (+ g_qual), g_f_tritium, g_f_material (common show-stoppers), g_rollout_f
```

Key relations:
- `<p>_fid = max(<p>_trl7 − <p>_vorlauf, g_rahmen, 2027) + <p>_fin_verz`
- `<p>_demo = max(<p>_fid + max(<p>_bau, <p>_lic_jahre), <p>_trl7)`
- `<p>_kom = max(<p>_demo + <p>_demo_kom + 4·<p>_verf_low, <p>_nuk + 2)`
- `<p>_gross = <p>_kom + <p>_rollout · g_rollout_f`
- A pathway fails if a TRL show-stopper occurs, if licensing at scale is blocked, or if funding is abandoned.

Design decisions:
- **Demo gating.** The materials, tritium and exhaust gates are normally closed only *in* a pilot or demo
  plant. They therefore gate the commercial plant, not the demo decision. Requiring all five gates before the
  demo would double-count them.
- **Funding.** The probability of abandonment rises with capital need, with a weak funding climate and with
  late TRL maturity, because investors withdraw.
- **Correlations.** Gate years are coupled in one 20 × 20 Spearman matrix:
  - within a pathway: the consolidated deep-dive matrices;
  - same challenge across pathways: strong for materials and tritium, weak for plasma and driver.
  Show-stoppers within a pathway are coupled with ρ = 0.3.

Scenarios in the main model:
- funding climate weak or strong;
- fission-like regulation;
- tritium bottleneck;
- "only <pathway>", "only MCF", "only IFE";
- one or two pathway-specific scenarios each (SPARC Q > 1 by 2028, further ITER slip, Alpha with or without
  federal funds, MJ direct-drive facility, excimer efficiency confirmed, EYC/Thunderwall success, stricter
  classification);
- an "industry roadmap" upper bracket (all gates 8 years earlier, show-stoppers halved).

Each sub-model carries its pathway-specific scenarios and the shared ones.

### R.6 Parameter set (calibrated expert judgement)

Gate definitions:

- **PL** — MCF: DT Q ≥ 10 (compact devices: alpha heating ≥ 2/3) sustained ≥ 300 s with disruption, runaway-electron and ELM control. ICF: target gain ≥ 30–50 with a plant-consistent driver.
- **MA** — Fusion-spectrum irradiation data to ≥ ~20 dpa accepted by the regulator; remote maintenance validated (ICF: chamber wall and final optics).
- **TR** — Breeding blanket operated in a DT device of the pathway; measured net TBR ≥ requirement + 0.05; closed fuel cycle; start-up inventory secured.
- **EX** — MCF: ≤ 5–10 MW m⁻² for ≥ 1000 s at reactor-relevant P/R. ICF: ≥ 50 MJ yields at ≥ 1 Hz over ≥ 10⁶ shots.
- **DR** — MCF: plant-scale magnet system plus ≥ 1 h (stellarator ≥ 30 min) high-power operation. ICF: ≥ 10 % wall-plug at 5–10 Hz plus a target line of ≥ 10⁴ targets per day.

Materials gate in the model: `<p>_ma = max(<p>_ma_eigen, g_dones + g_qual)`, with DONES ≥ 10 dpa data
P0/P10/P50/P90/P100 = 2033/2035/2038/2043/2055 and a qualification lag of 5 years.

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | PL – Plasma/implosion | 2031 / 2036 / 2044 / 2058 / 2080 | 0.05 | `tok_pl`, `tok_f_pl` |
| Tokamak | MA – Materials (pathway-specific) | 2034 / 2040 / 2046 / 2057 / 2080 | 0.05 | `tok_ma_eigen`, `tok_f_ma` |
| Tokamak | TR – Tritium | 2032 / 2038 / 2048 / 2065 / 2090 | 0.10 | `tok_tr`, `tok_f_tr` |
| Tokamak | EX – Power exhaust | 2033 / 2039 / 2047 / 2062 / 2085 | 0.07 | `tok_ex`, `tok_f_ex` |
| Tokamak | DR – Driver/magnets | 2030 / 2036 / 2045 / 2062 / 2085 | 0.05 | `tok_dr`, `tok_f_dr` |
| Stellarator | PL – Plasma/implosion | 2035 / 2042 / 2055 / 2078 / 2095 | 0.15 | `stl_pl`, `stl_f_pl` |
| Stellarator | MA – Materials (pathway-specific) | 2036 / 2043 / 2050 / 2063 / 2090 | 0.10 | `stl_ma_eigen`, `stl_f_ma` |
| Stellarator | TR – Tritium | 2038 / 2045 / 2058 / 2080 / 2098 | 0.20 | `stl_tr`, `stl_f_tr` |
| Stellarator | EX – Power exhaust | 2035 / 2042 / 2052 / 2070 / 2095 | 0.12 | `stl_ex`, `stl_f_ex` |
| Stellarator | DR – Driver/magnets | 2032 / 2039 / 2050 / 2068 / 2095 | 0.07 | `stl_dr`, `stl_f_dr` |
| Direct Drive | PL – Plasma/implosion | 2036 / 2042 / 2055 / 2080 / 2098 | 0.25 | `dir_pl`, `dir_f_pl` |
| Direct Drive | MA – Materials (pathway-specific) | 2036 / 2042 / 2050 / 2065 / 2090 | 0.15 | `dir_ma_eigen`, `dir_f_ma` |
| Direct Drive | TR – Tritium | 2044 / 2049 / 2064 / 2086 / 2099 | 0.28 | `dir_tr`, `dir_f_tr` |
| Direct Drive | EX – Power exhaust | 2040 / 2045 / 2056 / 2078 / 2098 | 0.22 | `dir_ex`, `dir_f_ex` |
| Direct Drive | DR – Driver/magnets | 2034 / 2040 / 2050 / 2072 / 2095 | 0.12 | `dir_dr`, `dir_f_dr` |
| Indirect Drive | PL – Plasma/implosion | 2033 / 2037 / 2048 / 2072 / 2095 | 0.15 | `ind_pl`, `ind_f_pl` |
| Indirect Drive | MA – Materials (pathway-specific) | 2036 / 2042 / 2050 / 2065 / 2090 | 0.15 | `ind_ma_eigen`, `ind_f_ma` |
| Indirect Drive | TR – Tritium | 2045 / 2050 / 2066 / 2088 / 2099 | 0.30 | `ind_tr`, `ind_f_tr` |
| Indirect Drive | EX – Power exhaust | 2040 / 2046 / 2057 / 2080 / 2098 | 0.22 | `ind_ex`, `ind_f_ex` |
| Indirect Drive | DR – Driver/magnets | 2037 / 2042 / 2055 / 2078 / 2098 | 0.20 | `ind_dr`, `ind_f_dr` |

Licensing and funding branches:

| Pathway | FOAK licensing duration P0/P10/P50/P90/P100 (y) | P(major licensing delay) | P(licensing blocked at scale) | FOAK capital need P0/P10/P50/P90/P100 (USD bn) | Base P(funding abandoned) |
|---|---|---|---|---|---|
| Tokamak | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.02 | 3 / 5 / 8 / 15 / 30 | 0.05 |
| Stellarator | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.02 | 4 / 6 / 10 / 18 / 35 | 0.10 |
| Direct Drive | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.03 | 3 / 4 / 7 / 14 / 30 | 0.12 |
| Indirect Drive | 2 / 3 / 5 / 7 / 12 | 0.40 | 0.05 | 4 / 6 / 10 / 20 / 40 | 0.12 |

Shared parameters:

| Parameter | Value | Basis |
|---|---|---|
| Funding climate (relative to the 2026 level) | P0/P10/P50/P90/P100 = 0.3/0.55/1.0/1.6/2.5 | FIA 2026 level [R4]; assumption |
| Tempo effect on TRL years | +8 y at climate 0.3, 0 at 1, −3 y at 2.5 (asymmetric) | Assumption |
| Framework in force | 2026.9/2027.0/2027.6/2029/2035 | [R5]–[R8], [R10]–[R12] |
| Fission-like regulation | p = 0.10; adds 3/5/8/12/20 years | Assumption; NGO critique of the German approach as an indicator [R34] |
| Common show-stoppers | Tritium fuel cycle 0.03; materials 0.02 | Assumption |
| FID lead before TRL 7 | 3/5/8/10/12 y | Deep dives |
| Demo → first commercial plant | 4/6/8/12/18 y (+4 y if demo availability < 50 %, p = 0.55–0.70) | Deep dives (RAMI) |
| First commercial plant → ≥ 10 GWe | 6/8/12/18/30 y × climate factor (1.5 at 0.3 … 0.75 at 2.5) | Fission analogue (assumption, not re-researched) |

The gate values for tokamak and stellarator, and the averaged laser-ICF values, come from the deep dives'
"Model parameters" tables of the earlier November update and were **not re-elicited**. The split into direct
and indirect drive (R.4) is new. All values are priors for discussion, not a formal expert elicitation.

### R.7 Limitations and open verification items

- **Not re-verified on 3 November 2026:** the W7-X campaign schedule (the C5 deep dive says "OP3 from September 2026";
  the earlier November update says OP2.4/OP2.5, which conflicts); EAST's 1,066 s being "fully non-inductive";
  most numbers in the deep dives' physics sections.
- **Pending:** the NRC final rule had not been confirmed as published by 3 November 2026 [R7]. The German Radiation
  Protection Act amendment is still in the legislative process [R11]. Both should be checked first at the next
  update.
- **Concept scope:** the model excludes concepts outside the four pathways (see R.1) and does not model costs
  or LCOE, so it gives no economic-competitiveness check.
- **Scenarios** are not weighted against each other.

### Sources for this review

Accessed 3 November 2026. Secondary sources are marked as such; claims resting only on them are flagged in the tables above.

- **[R1]** ITER Organization via ANS Nuclear News, 'ITER begins operations at its magnet cold test facility' (1 Jun 2026) — Baseline 2024: SRO 2034, full magnetic energy 2036, DT 2039. <https://www.ans.org/news/article-8081/iter-begins-operations-at-its-magnet-cold-test-facility/>
- **[R2]** Nuclear News Network, SPARC project tracker (verified 11 Oct 2026) — ~75 % built by April 2026, first plasma target 2027 (secondary, cites CFS). <https://www.nuclearnewsnetwork.com/industry-trackers/fusion-energy-companies/cfs-sparc>
- **[R3]** Venture Atlas, 'Nuclear Fusion' (Sep 2026) — TF-magnet installation target slipped (secondary). <https://www.ventureatlas.org/industry/nuclear-fusion>
- **[R4]** World Nuclear News on FIA 'The Global Fusion Industry in 2026' (Jul 2026) — USD 4.48 bn in 12 months, USD 14.24 bn since 2021. <https://world-nuclear-news.org/articles/fusion-industry-raised-usd45-billion-over-past-year-report-says>
- **[R5]** US NRC, proposed rule 'Regulatory Framework for Fusion Machines', Federal Register 26 Feb 2026 (10 CFR Part 30). <https://www.federalregister.gov/documents/2026/02/26/2026-03865/regulatory-framework-for-fusion-machines>
- **[R6]** US NRC, report to Congress on fusion rulemaking (Mar 2026) — final rule to be completed by Dec 2027. <https://www.nrc.gov/docs/ML2605/ML26055A335.pdf>
- **[R7]** Foley Hoag, 'NRC publishes proposed regulatory framework for fusion machines' (Mar 2026) — agenda target for final rule Oct 2026, NEIMA deadline 31 Dec 2027. <https://foleyhoag.com/news-and-insights/blogs/energy-and-climate-counsel/2026/march/fusion-update-nrc-publishes-proposed-regulatory-framework-for-fusion-machines/>
- **[R8]** Tennessee Department of Environment and Conservation, press release (31 Aug 2026) — first fusion-specific byproduct material licence (Type One Energy). <https://www.tn.gov/environment/news/2026/8/31/first-license-commercial-fusion.html>
- **[R9]** ANS Nuclear News, 'Tennessee issues commercial fusion license to Type One Energy' (2 Sep 2026). <https://www.ans.org/news/article-8360/tennessee-issues-commercial-fusion-license-to-type-one-energy-for-bull-run-site/>
- **[R10]** BMFTR, 'Aktionsplan Fusion' (Oct 2025) — > EUR 2 bn, regulation via Radiation Protection Act, legislation targeted for 2026. <https://www.bmftr.bund.de/SharedDocs/Kurzmeldungen/DE/2025/10/011025-aktionsplan-fusion.html>
- **[R11]** ingenieur.de / VDI nachrichten, interview with Federal Research Minister Bär (2026) — draft amendment of the Radiation Protection Act in consultation. <https://www.ingenieur.de/technik/fachbereiche/energie/wir-wollen-das-erste-kommerzielle-fusionskraftwerk-der-welt-in-deutschland-errichten/>
- **[R12]** GRS, ReFus status report (draft for comment, status June 2026; published Aug 2026). <https://www.grs.de/de/aktuelles/refus-statusbericht>
- **[R13]** Max Planck Society, 'Proxima Fusion raises 411 million euros' (8 Jul 2026) — federal share of EUR 1.2 bn for Alpha not yet committed. <https://www.mpg.de/26861952/proxima-fusion-raises-411-million-euros>
- **[R14]** StockAnalysis company profile Type One Energy (Oct 2026) — Series B USD 200 M (secondary, cites ENR). <https://stockanalysis.com/private/type-one-energy/>
- **[R15]** LLNL, 'Target breakthrough enabled fusion record at NIF' (15 Apr 2026) — 8.6 MJ from 2.08 MJ. <https://lasers.llnl.gov/news/target-breakthrough-enabled-fusion-record-nif>
- **[R16]** LLNL, NIF overview, DOE Laser Safety Officer Workshop (20 May 2026) — ten ignitions, EYC ~40 MJ. <https://lasers.llnl.gov/sites/lasers/files/2026-06/lso-workshop-2026-wednesday-g-brunton.pdf>
- **[R17]** Nuclear Engineering International, 'Inertia secures Series A fusion funding' (Feb 2026) — USD 450 M, Thunderwall 10 kJ / 10 Hz / 10 % wall-plug. <https://www.neimagazine.com/news/inertia-secures-series-a-fusion-funding/>
- **[R18]** Xcimer Energy, 'Additional USD 30.5 million award from DOE Milestone Program' (Oct 2026) — ~USD 200 M private, USD 39.5 M DOE milestones. <https://xcimer.energy/news/xcimer-energy-receives-additional-30-5-million-award-from-doe-milestone-program/>
- **[R19]** Xcimer Energy, start of operations of the Phoenix excimer prototype (3 Jun 2026). <https://xcimer.energy/news/xcimer-energy-announces-the-start-of-operations-for-phoenix-a-prototype-system-for-industrial-scale-laser-fusion-architecture/>
- **[R20]** CB Insights excerpt of a Xcimer/GA release (Mar 2026) — OMEGA experiment on externally driven half-hohlraums for Xcimer's two-beam concept (secondary). <https://www.cbinsights.com/company/general-atomics>
- **[R21]** Nuclear Engineering International on Focused Energy's USD 240 M Series A (May/Jun 2026) — direct drive, Biblis. <https://www.neimagazine.com/?p=104942>
- **[R22]** Runtime Wire, 'Focused Energy raises USD 240M Series A' (2026) — milestones 2028 laser, 2033 implosion, 2035 pilot, 2037 first grid MWh (secondary). <https://runtimewire.com/article/focused-energy-240m-series-a-laser-fusion>
- **[R23]** Williams et al., hot-spot fuel gain > 1 in direct-drive implosions, Nature Physics (2024). <https://www.nature.com/articles/s41567-023-02363-2>
- **[R24]** Gopalaswamy et al., hydrodynamically equivalent burning plasma in direct drive, Nature Physics (2024) — requires ≥ ~1.7 MJ laser energy. <https://doi.org/10.1038/s41567-023-02361-4>
- **[R25]** APS DPP 2025 invited talk, 'Optimization of laser direct-drive implosions … record performance on OMEGA' — scaled Lawson parameter > 0.9. <https://archive.aps.org/dpp/2025/bi02/4>
- **[R26]** National Research Council, 'An Assessment of the Prospects for Inertial Fusion Energy' (2013). <https://uwnxt.nationalacademies.org/read/18288/chapter/2>
- **[R27]** 'Nonproliferation and fusion power plants', arXiv:2207.14348 — direct-drive ICF largely declassified by 1974; export controls for indirect drive. <https://arxiv.org/pdf/2207.14348>
- **[R28]** Physics Today, 'Inertial fusion energy gets a nod' (2013) — proliferation concern greater for indirect than direct drive. <https://physicstoday.aip.org/news/inertial-fusion-energy-gets-a-nod>
- **[R29]** IFMIF-DONES España, building permit granted 16 Jun 2026. <https://ifmif-dones.es/?p=23730>
- **[R30]** Lovguiden summary of F4E news (21 Oct 2026) — first EU procurement arrangements; Main Building preparatory works since Sep 2026, completion ~2029 (secondary). <https://www.lovguiden.dk/en/det-offentlige/fusion-for-energy/2026-10-21-f4e-underskriver-de-foerste-to-indkoebsaftaler-for-ifmif-dones>
- **[R31]** Spitzer et al., 'Is Fusion Too Late?', MIT CEEPR WP 2025-20 (Oct 2025) — investor-implied commercialization probabilities mostly < 20 %. <https://ceepr.mit.edu/workingpaper/is-fusion-too-late-how-investors-value-its-role-in-a-decarbonized-europe/>
- **[R34]** .ausgestrahlt, 'Kernfusion im Strahlenschutzgesetz – reicht das?' (15 Jul 2026) — NGO critique: waste and decommissioning gaps (position source). <https://www.ausgestrahlt.de/blog/2026/07/15/kernfusion-im-strahlenschutzgesetz-reicht-das/>

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
