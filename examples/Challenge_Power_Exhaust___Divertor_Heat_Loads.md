# Nuclear Fusion — Deep Dive: Challenge 4
## Power Exhaust & Divertor Heat Loads

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — June 2026; reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps gate EX to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

The power exhaust problem is arguably the most immediate engineering-physics challenge separating ITER from DEMO and from commercial fusion. The fundamental mismatch is stark: unmitigated plasma heat loads **perpendicular to the DEMO divertor target** reach **~150 MW m\(^{-2}\)** (the parallel heat flux in the scrape-off layer is of order GW m\(^{-2}\)) **[corr. 2026-11]**, while the thermomechanical limit of tungsten armour on water-cooled divertor components is approximately **5–10 MW m\(^{-2}\)**. Bridging this gap by a factor of 15–30× — every pulse, every day, for the 20+ year life of the reactor — without degrading core plasma performance is the central power exhaust challenge.[^1][^2][^3]

The difficulty has three compounding layers. The first is the **geometric problem**: the scrape-off layer (SOL) in which heat is transported to the divertor is only a few millimetres wide at the outboard midplane, concentrating 100–300 MW of exhaust power onto a divertor target area of ~2–4 m². The second is the **materials problem**: the only viable armour material — tungsten — has a maximum safe heat flux that drops from ~10 MW m\(^{-2}\) in ITER to ~3–5 MW m\(^{-2}\) in DEMO due to neutron irradiation embrittlement. The third is the **compatibility problem**: the techniques used to reduce divertor heat load (impurity seeding, detachment, high density operation) all have the potential to degrade the core plasma confinement whose maintenance is the reason for having the reactor at all.[^4][^2][^5][^1]

Unlike the tritium or materials challenges — which require entirely new facilities to solve — the power exhaust challenge is actively being resolved experimentally on operating machines today. Critically, the MAST Upgrade tokamak in the UK demonstrated in 2024–2025 that alternative divertor configurations (ADCs), specifically the Super-X divertor with strong neutral baffling, provide **~18.5× reduction in target heat flux** compared to a conventional divertor, while maintaining or improving core plasma performance **[unconfirmed 2026-11]** (shown at ~1.2 MW SOL power; the report's own open questions note that H-mode and reactor-power validation are pending) — the strongest experimental evidence to date that this challenge has a tractable engineering solution. Nevertheless, substantial physics and engineering uncertainties remain, particularly for DEMO-scale power and neutron loads.[^3]

***

## Part I — The Fundamental Power Exhaust Problem

### 1.1 From SOL to Target: The Heat Concentration Geometry

In a tokamak or stellarator, the power that crosses the last closed flux surface from the hot plasma core enters the **Scrape-Off Layer (SOL)**. In this region, open magnetic field lines guide the power along essentially parallel paths to the divertor targets. The key problem is that the heat channel in the SOL is extremely narrow.

The empirical **Eich scaling** for H-mode SOL heat flux width \(\lambda_q\) gives, for ITER-class devices:[^6][^7]

\[\lambda_q \propto B_p^{-1.19}\]

where \(B_p\) is the poloidal magnetic field. For ITER (\(B_p \approx 0.7\) T), \(\lambda_q \approx 2\) mm at the outboard midplane. For DEMO with higher current and larger minor radius, \(\lambda_q\) is expected to narrow to **1–2 mm**. When this narrow heat channel maps geometrically to the divertor target (with a poloidal flux expansion factor of ~5–10× in a conventional divertor), the footprint on the target is still only a **5–15 mm wide strike zone**.[^2][^1]

The power deposited on this narrow strike zone can be estimated as:

\[q_{target} = \frac{f_{SOL} \cdot P_{heat}}{4\pi R \cdot \lambda_{q,target} \cdot \sin\theta}\]

where \(P_{heat}\) is the power crossing the separatrix, \(f_{SOL}\) is the fraction going to the outboard target (~2/3), \(R\) is the major radius, and \(\sin\theta\) accounts for the shallow field-line incidence angle at the target. For DEMO with \(P_{heat} \approx 150\) MW (after core radiation), \(R = 9\) m, \(\lambda_{q,target} \approx 3\) mm, and \(\sin\theta \approx 0.05\), the target heat flux evaluates to approximately **150 MW m\(^{-2}\)** — consistent with independently computed estimates — versus a material limit of 5 MW m\(^{-2}\).[^8][^3]

### 1.2 The P/R Scaling Problem

A key insight from multi-machine experimental studies is that the divertor heat flux does not scale with machine size — the loaded divertor area scales approximately linearly with machine major radius \(R\), while the exhaust power \(P_{heat}\) scales as \(R^3\) for fixed geometry. The relevant dimensionless parameter is therefore:[^2]

\[\text{Exhaust power per unit major radius:} \quad P_{sep}/R\]

For ITER: \(P_{sep}/R \approx 150/6.2 \approx 24\) MW m\(^{-1}\).[^4][^2]
For DEMO: \(P_{sep}/R \approx 150/9 \approx 17\) MW m\(^{-1}\) — slightly lower due to DEMO's larger radius — but this is compensated by the tighter constraint on the material limit (5 vs. 10 MW m\(^{-2}\)) and by DEMO's longer pulse duration (hours, not seconds) which prevents any transient material exceedance.

On ASDEX Upgrade, at \(P_{sep}/R \approx 10\) MW m\(^{-1}\) (approximately 2/3 of ITER's value), an unmitigated divertor heat flux of ~40 MW m\(^{-2}\) was measured; this was reduced to <5 MW m\(^{-2}\) only by feedback-controlled nitrogen (N\(_2\)) seeding. **Extrapolation to DEMO suggests that without advanced divertor solutions, approximately 96–97% of the total SOL power must be radiated away before reaching the target** to keep heat flux below 5 MW m\(^{-2}\). No existing device has achieved this radiation fraction while maintaining H-mode confinement compatible with power production. ASDEX Upgrade has reached 85 ± 10% with double-radiation feedback control — a significant gap from the 96–97% required for DEMO.[^9][^10][^4]

### 1.3 The DEMO Constraint Table

| Parameter | ITER | EU DEMO | Material Limit | Gap Factor |
|---|---|---|---|---|
| P\(_{sep}\) (power to SOL) | ~100 MW | ~150 MW[^9] | — | — |
| P\(_{sep}\)/R [MW m\(^{-1}\)] | ~17 | ~17[^2] | — | — |
| Unmitigated q\(_{target}\) [MW m\(^{-2}\)] | ~40[^4] | ~150[^3] | — | — |
| W armour heat flux limit [MW m\(^{-2}\)] | ~10 (unirrad.)[^11] | ~3–5 (irrad.)[^1] | 3–5 | 30–50× needed |
| Required total radiated fraction | ~80–85% | ~96–97%[^9][^10] | — | ASDEX best: 85% |
| ELM energy per event (DEMO) | — | ~100 MJ[^10] | ~0.5 MJ\(_{\text{limit}}\) | ~200× reduction needed[^10] |
| Max pulse length (ITER vs DEMO) | Seconds–minutes | Hours–continuous[^12] | — | No thermal memory |

***

## Part II — Plasma Detachment: The Primary Heat Exhaust Strategy

### 2.1 Physics of Divertor Detachment

**Plasma detachment** is the process by which the hot plasma separating from the divertor target transitions into a cool, partially neutral region that absorbs the incoming power through atomic and molecular processes rather than delivering it as a thermal flux to the material surface. In a detached divertor:[^3]

1. The plasma temperature at the target drops below ~3–5 eV (from ~30–100 eV in attached conditions)
2. At \(T_e < 3\) eV, physical sputtering of W by D and T ions falls below threshold — this synergy is critical, as sputtering and heat flux reduction must occur simultaneously
3. **Molecular Activated Recombination (MAR)** and **Electron-Ion Recombination (EIR)** deplete the ion density near the target, reducing the particle (and hence power) flux
4. The power is dissipated volumetrically by radiation (line emission from fuel atoms and impurity ions) and by charge-exchange/ionization processes in the neutral gas buffer below the ionization front

The condition for detachment onset can be expressed via the two-point model: detachment requires the upstream separatrix electron pressure to reach a critical value proportional to \(T_{e,target}^{7/2}\). Since power increases proportional to \(P_{SOL}\) but the detachment threshold scales more weakly, larger devices with higher \(P_{SOL}\) will require **more aggressive detachment** — i.e., colder divertor plasmas with higher radiation fractions — to stay below material limits.

### 2.2 Impurity Seeding: The Primary Detachment Tool

The simplest approach to achieving detachment is to inject radiating impurity gases into the plasma boundary region. Nitrogen (N\(_2\)), neon (Ne), and argon (Ar) are the primary candidates:[^13][^5][^14]

- **Nitrogen**: highly effective at cooling the SOL at moderate plasma temperatures; creates N\(^{2+,3+}\) ions that radiate efficiently in the 10–100 eV temperature range; seeding N\(_2\) in the ASDEX Upgrade small-angle slot (SAS) divertor achieved simultaneous detachment across all boundary diagnostics with **no core confinement degradation**. However, N\(_2\) causes W sputtering initially (see Challenge 2), is cryopumped efficiently (creating supply/demand dynamics), and transmutes to \(^{15}\)O and \(^{14}\)C under neutron irradiation — adding to plasma impurity burden[^5]
- **Neon**: a noble gas that does not chemically interact with surfaces; Ne seeding at W7-X reduced divertor heat loads globally by **2/3** with radiative fractions ≥80%; Ne shows higher recycling (longer persistence after seeding stops) than N\(_2\), which complicates feedback control[^13]
- **Argon**: heavier than Ne; higher radiation power per atom but less compatible with high-confinement core conditions; tends to penetrate to the plasma core more readily, causing dilution

The critical compatibility problem is that the impurity seeded for divertor cooling must not penetrate to the plasma core, where high-Z ions radiate too intensely and reduce plasma performance. The balance between sufficient seeding for divertor protection and too much seeding for core stability defines a narrow operating window that narrows further as \(P_{SOL}\) increases. ASDEX Upgrade and DIII-D experiments have demonstrated that **impurity seeding in advanced divertor geometries (e.g., slot divertors, ADCs) substantially widens this window** compared to conventional divertor geometries.[^14][^5][^13]

***

## Part III — Alternative Divertor Configurations: MAST-U Results

### 3.1 The Key Physics Insight

The SOL heat flux width \(\lambda_q \approx 1–2\) mm is a consequence of the local cross-field transport, primarily determined by turbulence at the plasma edge. It is not easily broadened — attempts to increase core density beyond the Greenwald limit cause confinement degradation. The alternative strategy is therefore not to broaden \(\lambda_q\) but to:

1. **Geometrically expand** the flux tube footprint on the target surface (poloidal and total flux expansion)
2. **Lengthen** the connection from the X-point to the target, increasing the plasma-neutral interaction volume
3. **Contain neutrals** inside the divertor chamber using physical baffles, augmenting the interaction volume with recycled neutral molecules

These principles underpin all Advanced Divertor Configurations (ADCs): Super-X, Snowflake, X-point Target (XPT), and Elongated Divertor designs.[^15][^16]

### 3.2 MAST Upgrade Super-X and Elongated Divertor: 2024–2025 Results

MAST Upgrade is a spherical tokamak at UKAEA Culham specifically designed to test ADCs with combined long-legged geometry, high total flux expansion, and strong neutral baffling. Results published in 2024–2025 provide the strongest experimental evidence to date for ADC benefits:[^17][^3]

**Steady-state heat flux reduction**:
- Super-X divertor vs. conventional divertor: **~18.5× reduction** in perpendicular target heat flux, substantially exceeding the ~5.8× expected from geometry alone[^3]
- Elongated divertor: ~7× reduction vs. conventional[^3]
- The additional factor of ~3.2× beyond geometric expectation arises from volumetric power dissipation (MAR, MAD, EIR) in the extended divertor leg — confirming that the long-leg volume is an active power sink, not merely a geometric expansion[^3]

**Detachment access and stability**:
- Super-X and Elongated divertors were fully detached at all tested core densities; the Conventional divertor only detached at \(f_{GW} \approx 40\%\), near the Greenwald limit[^3]
- The SXD detachment front sensitivity to changes in core density is **5× lower** than the conventional divertor — a critical stability improvement for reactor control[^3]
- These detachment stability benefits extend to **dynamic transients** (fast gas valve perturbations): the SXD passively absorbs fuelling transients that would move the conventional divertor detachment front beyond the operational window into MARFE or re-attachment[^17]

**Core-edge compatibility**:
- **No adverse core impact** was observed when the outer target was detached in the SXD or ED, in contrast to the conventional divertor which required high Greenwald fraction for detachment[^3]
- Core electron temperatures, densities, and total SOL power remained unchanged as divertor shape was varied[^3]

**Control demonstration (2024)**:
- First demonstration of **active feedback exhaust control** in an alternative divertor configuration[^17]
- Same PI controller (tuned once) successfully controlled detachment in both ED and SXD configurations
- Upper and lower divertors demonstrated **independent controllability** (decoupled by strong neutral baffling), a prerequisite for double-null reactor designs[^17]

These results represent a step-change in confidence for ADC solutions. The finding that detachment benefits persist at "more moderate divertor shaping" (lower flux expansion than the maximum SXD) is particularly important for reactor engineering — it suggests that DEMO need not implement the most extreme divertor geometry to capture most of the exhaust benefit.[^3]

**Planned next steps on MAST-U**: independent simultaneous control of upper and lower divertors (2024–2025 campaign), high-power operation with >10 MW NBI (from 2026), and studies of combined hydrogenic + impurity gas seeding at reactor-relevant power levels.[^17]

### 3.3 Other ADC Concepts

**Snowflake Divertor (SFD)**: A second X-point is placed near the primary X-point, forking the SOL power into two strike points and significantly enhancing cross-field transport in the null region. TCV experiments show an order-of-magnitude reduction in peak heat flux in the XPT variant. MAST-U H-mode experiments showed strong radiative exhaust in the region of low poloidal field around the X-points, with power sinks redistributed among multiple divertor legs downstream of the secondary X-point. However, the Snowflake geometry has a narrow magnetic configuration window and is sensitive to plasma current profile changes.[^18][^16][^15]

**X-point Target (XPT)**: A second X-point is placed inside or at the divertor target, producing extremely large poloidal flux expansion and locally enlarged connection length and SOL volume — an order-of-magnitude reduction in peak heat flux even at intermediate density. The challenge is the very shallow field-line angle at the target, which creates issues with leading edges and component alignment tolerances.[^15]

***

## Part IV — Transient Heat Loads: ELMs and Disruptions

### 4.1 ELMs in DEMO: The Critical Constraint

**Edge Localized Modes (ELMs)** are periodic MHD instabilities at the H-mode pedestal that transiently expel energy from the plasma in intense bursts impacting the divertor. In DEMO, the total thermal energy is \(W_{th} \approx 2\) GJ. A "natural" ELM releasing 5% of \(W_{th}\) corresponds to:

\[\Delta W_{ELM} = 0.05 \times 2 \text{ GJ} = 100 \text{ MJ}\]

The energy impact factor limit for tungsten is approximately \(\eta = \Delta W / (A\sqrt{\tau}) \approx 50\) MJ m\(^{-2}\) s\(^{-0.5}\). For a typical ELM duration of ~1 ms, the area \(A\) that receives 100 MJ without exceeding the melt limit must satisfy:[^12]

\[A > \frac{100 \text{ MJ}}{50 \text{ MJ m}^{-2} \text{ s}^{-0.5} \times \sqrt{10^{-3} \text{ s}}} \approx 63 \text{ m}^2\]

The actual divertor target area in DEMO is ~2–4 m². This means that uncontrolled natural ELMs in DEMO exceed the tungsten melt limit by a factor of **~15–30×**. JET results on ELM broadening suggest that even accounting for ELM-induced broadening in DEMO, the energy density limit of **~0.5 MJ m\(^{-2}\)** per ELM is exceeded by a factor of approximately **8× for a wide range of relative ELM sizes**.[^10]

Therefore, DEMO requires an ELM control technique capable of **reducing individual ELM energy releases by more than an order of magnitude** without degrading H-mode confinement.[^12][^10]

**ELM mitigation approaches** under development:[^19][^12]
- **Resonant Magnetic Perturbations (RMPs)**: external coil sets apply small non-axisymmetric fields that suppress or significantly reduce ELM frequency and amplitude. ITER has a dedicated 27-coil RMP system. RMP ELM suppression has been demonstrated on DIII-D, AUG, KSTAR, and EAST — but performance at ITER pedestal parameters (high electron collisionality) is not yet established
- **High-frequency small ELMs via pellet injection**: injecting small cryogenic hydrogen pellets at high frequency (>10 Hz) triggers small ELMs synchronously, depleting the pedestal energy before it can accumulate to large-ELM levels. Pellet ELM pace-making requires pellet injection rates in the range 50–100 Hz for DEMO, which is at the edge of current pellet injector technology[^19]
- **Naturally ELM-free regimes**: I-mode (high confinement without ELMs), QH-mode (Quiescent H-mode with edge harmonic oscillation instead of ELMs), and various H-mode variants that exhibit only small, benign ELMs. The challenge is accessing these regimes at DEMO-relevant density and pedestal pressure

### 4.2 Disruptions in DEMO

A disruption — the sudden termination of plasma current — in DEMO releases approximately 2 GJ of thermal energy and 50–100 GJ of magnetic energy within milliseconds. The heat load on the first wall and divertor from a thermal quench exceeds \(10^9\) J m\(^{-2}\) s\(^{-0.5}\) locally, an order of magnitude beyond any material limit. Runaway electron (RE) beams generated during the current quench carry up to 10 MA at 50–100 MeV, with total beam energies up to 100 MJ that can ablate or melt local wall structures if not mitigated.

**Disruption mitigation systems (DMS)** inject massive quantities of frozen gas or shattered pellets of noble gases (Ne, Ar) to:
1. Radiate the thermal energy uniformly before it reaches the wall (thermal quench mitigation)
2. Suppress runaway electron avalanche growth by increasing plasma density
3. Force the current quench to be resistive rather than sudden, reducing induced eddy currents in the vacuum vessel

ITER's Shattered Pellet Injector (SPI) system has been designed to inject ~10\(^{24}\) Ne or Ar atoms in ~50 ms. For DEMO, the challenge is more severe:[^20][^12]
- Higher stored energy (~2 GJ thermal, ~50 GJ magnetic) than ITER
- DEMO's first wall and divertor are designed for neutron-irradiated tungsten with lower thermal shock resistance
- DEMO availability targets (~70–80% capacity factor) cannot tolerate frequent disruptions; RE beams that damage wall panels require weeks of remote maintenance

The disruption rate in DEMO must be **essentially zero** during steady-state burning plasma operation — a target that has never been achieved on any existing device without disruption prediction and avoidance algorithms that have not yet been validated at burning plasma conditions.

***

## Part V — Stellarator Island Divertor

### 5.1 The Island Divertor Concept

Stellarators do not have the option of a conventional poloidal divertor because their 3D coil geometry does not produce a simple 2D axisymmetric magnetic null. Instead, W7-X uses the **island divertor** concept: it exploits naturally occurring low-order magnetic islands at the plasma boundary (created by the residual non-axisymmetric field perturbations from the modular coils), which provide extended connection lengths along the island boundary — typically **one order of magnitude longer** than in a medium-sized tokamak — and distribute the heat load over a much larger area.[^21]

### 5.2 W7-X Island Divertor Results

Wendelstein 7-X has demonstrated island divertor operation in multiple experimental campaigns:[^22][^23][^24][^13]

**Key results**:
- **First observation of stable highly dissipative divertor regime** (2019): total plasma radiation approached the absorbed heating power without noticeable stored energy loss; divertor thermography showed **simultaneous strong reduction of heat loads on all divertor targets**, indicating nearly complete power detachment[^22]
- **Full heat flux detachment**: divertor heat loads dropped by **an order of magnitude** from >5 MW m\(^{-2}\) to <0.5 MW m\(^{-2}\) with increasing density, while stored energy remained at \(W_{dia} > 600\) kJ and \(Z_{eff} \approx 1.5\) (no impurity accumulation)[^23]
- **Impurity seeding**: both Ne and N\(_2\) seeding reduced divertor heat loads globally by **~2/3** (radiative fraction ≥80%) with stable plasma operation. N\(_2\) seeding showed slower decay of radiation (high recycling), Ne showed controllable injection behavior[^13]
- **Particle exhaust**: detached scenario achieved neutral pressure compression ratios and sub-divertor neutral pressures extrapolating to steady-state particle exhaust requirements for high-performance OP2 operation with active cooling[^23]
- **Duration**: stably detached for up to **28 seconds** — equivalent to several hundred energy confinement times and longer than current relaxation timescales[^23]

These W7-X results are highly significant because stellarators do not have ELMs (the intrinsic helical field structure and lack of a driven plasma current eliminate the pedestal MHD instability mechanism). This is a **fundamental exhaust advantage** of stellarators over tokamaks: the single most dangerous transient heat load mechanism (ELMs in DEMO) is absent.

### 5.3 Stellarator Divertor Heat Flux Challenges

Despite these advantages, several challenges specific to the stellarator island divertor remain:[^25][^26][^24][^21]

- **3D SOL heat transport complexity**: the island divertor SOL is inherently three-dimensional. Heat flux patterns on W7-X divertor targets show multiple lobes from the five-island chain; leading edges between tiles receive enhanced local heat loads that are difficult to predict and mitigate. The EMC3-EIRENE 3D SOL code has qualitative agreement with experiments but requires further validation[^26][^24]
- **Impurity screening**: the island divertor shows good impurity screening (experiments with overloaded leading edges showed that the island SOL retains good impurity confinement), but this must be confirmed at higher plasma density and heating power relevant to a reactor[^24]
- **Scaling to reactor conditions**: W7-X operates at up to 10 MW of absorbed power in OP2 (with the actively cooled divertor). A HELIAS reactor would exhaust ~350 MW. The SOL heat flux width scaling in the island geometry (\(\Lambda_W\) framework developed at W7-X) is only at early empirical stage — extrapolation to reactor conditions carries large uncertainties[^26]
- **Reactor divertor engineering**: as discussed in Challenge 2, the 3D geometry of a stellarator blanket leaves very limited space for divertor structures. A HELIAS power plant divertor must fit within the complex 3D coil geometry, compatible with neutron shielding requirements and remote maintenance access[^27]

***

## Part VI — ICF First Wall: The Cyclic Shock Problem

### 6.1 Unique ICF Thermal Loads

In Laser ICF, the power exhaust challenge is fundamentally different from MCF. Instead of a steady-state plasma heat flux, the first wall faces a **cyclic pulsed load** at 5–10 Hz repetition rate, with each pulse delivering:[^28][^29][^30]

- A pulse of 14 MeV neutrons and energetic X-rays (arriving within ~100 ns)
- Soft X-rays with photon energies 100 eV–10 keV (absorbed in the first few micrometers of the first-wall surface)
- Plasma debris ions at 100–1,000 eV arriving over ~1 µs
- Fast neutrons (14.1 MeV) penetrating to the breeding blanket and structural materials

For a 1 GW\(_e\) IFE plant at 10 Hz, the time-averaged neutron wall loading is ~1–3 MW m\(^{-2}\) — comparable to DEMO. However, the **peak instantaneous energy deposition** in the first few microseconds after each microexplosion exceeds the surface ablation threshold of any known solid material unless the chamber is designed to absorb this energy differently.

Three first-wall concepts are under development for IFE:[^29][^28]
- **Dry wall** (solid first wall, typically W or SiC): acceptable for neutron and X-ray loads at large chamber radius (>4 m), but vulnerable to plasma debris erosion. Fatigue life modeling of W/Cu functionally graded material first walls shows that increasing chamber size and target frequency reduces temperature oscillations, extending service life, but achievable chamber radii of 4–6 m are barely within the erosion tolerance window[^31][^30]
- **Wetted wall**: a thin film of liquid metal (Li, Sn) or liquid salt continuously renews the inner surface, absorbing the plasma debris and X-ray pulse. The liquid film is replenished between shots by injection or capillary action. This concept provides an inherently renewing surface with no solid-material erosion limit, but creates evaporative contamination of the laser beam path and challenges for lithium breeding compatibility
- **Gas/vapor protection**: a low-density gas (e.g., Xe at ~1 Pa) fills the chamber and is ionized by the soft X-rays, absorbing the X-ray pulse before it reaches the solid first wall. The vapor shield re-expands after each shot. This concept (studied for the HAPL program) absorbs the most damaging X-ray and debris pulse but creates a partially ionized gas layer that the laser must propagate through repeatedly — requiring either grazing-incidence or non-central laser geometry[^28]

**Cyclic fatigue** is the defining constraint for solid first walls in IFE. A 30-year reactor lifetime at 10 Hz corresponds to ~10\(^{10}\) thermal cycles. Metals tested under fusion-relevant cyclic loads (>0.5 MW m\(^{-2}\) per pulse) show fatigue crack nucleation within 10\(^4\)–10\(^6\) cycles for most alloys at elevated temperature — orders of magnitude below the reactor lifetime requirement.[^30][^28]

### 6.2 IFE Chamber Scale and Neutron Wall Loading

IFE chamber design requires trading between:
- **Large radius** (~4–8 m): reduces per-pulse energy density on the first wall; reduces plasma debris sputtering; increases neutron shielding path length — but at the cost of larger, more expensive chamber and larger laser path length increasing beam divergence
- **Small radius** (~2–3 m): favorable for direct-drive ICF optical geometry (beam port angles), reduces blanket cost — but increases per-pulse first-wall loading beyond solid-material tolerance

No integrated IFE chamber concept has been demonstrated at rep-rate in any experiment as of 2026. The German BMF (Bundesministerium für Forschung) IFE memorandum (2023) identifies the first wall as one of the three hardest IFE-specific engineering challenges, alongside driver efficiency and target injection.[^29]

***

## Part VII — Helium-Cooled vs. Water-Cooled Divertor: DEMO Trade-off

The choice between helium-cooled and water-cooled divertor targets in DEMO has significant implications for achievable heat flux limits and system integration:[^32][^33][^2]

**Water-cooled divertor (ITER heritage)**:
- ITER technology: CuCrZr alloy coolant tube with W armour, water at 3.3 MPa, 100°C, 10 m/s with swirl tube insert
- Achievable steady-state heat flux: up to **10 MW m\(^{-2}\)** demonstrated with 5,000 cycles; up to 20 MW m\(^{-2}\) for 300 cycles[^32]
- **DEMO limitation**: CuCrZr alloys are severely embrittled by neutron irradiation at >5 dpa — their end-of-life damage dose at DEMO divertor conditions (~6–13 dpa for the Cu pipe) renders ITER-like copper alloy pipe solutions inadequate. DEMO requires higher coolant temperatures (250–300°C vs. ITER's 100°C) to avoid damage within the property window of available materials, reducing critical heat flux margin by ~30% compared to ITER[^11]

**Helium-cooled divertor**:
- Operates at 8–10 MPa and 600–700°C; avoids corrosion and tritium permeation into water; compatible with Brayton cycle thermodynamic efficiency
- **Limiting heat flux**: substantially lower than water-cooled — approximately **1 MW m\(^{-2}\)** (steady state), i.e., a factor 3–4 below ITER specifications[^9]
- This means He-cooled DEMO divertor **absolutely requires** plasma detachment to a higher degree than water-cooled designs; no margin exists for even brief heat flux excursions above the detachment operating point

The helium-cooled limit of ~1 MW m\(^{-2}\) makes it incompatible with any disruption or large ELM event, reinforcing the absolute necessity of zero-disruption operation and complete ELM suppression in a He-cooled DEMO design.[^9][^2]

***

## Part VIII — Technology Readiness and Cross-Pathway Comparison

### 8.1 Technology Readiness by Sub-Challenge

| Sub-challenge | Status (2026) | TRL | Key Bottleneck |
|---|---|---|---|
| SOL heat flux width physics (ITER) | Well characterized experimentally | 7 | Extrapolation to DEMO validated? |
| Plasma detachment (tokamak) | Demonstrated at ITER-relevant P\(_{sep}\)/R | 6 | Compatibility with high-confinement core |
| Alternative divertor config (ADC) | MAST-U: major results 2024–2025 | 4–5 | Engineering integration in reactor; high-power validation |
| ELM suppression via RMP | Demonstrated in non-burning plasmas | 5 | ITER pedestal conditions untested |
| ELM suppression via pellet | Demonstrated up to 50 Hz on AUG/KSTAR | 5 | DEMO-relevant frequency and reliability |
| Disruption mitigation (SPI) | ITER design complete | 5–6 | DEMO energy scale undemonstrated |
| W7-X island divertor detachment | Stable at 5–6 MW, ~28 s | 5 | Scaling to 350 MW reactor power |
| Water-cooled DEMO target | Component tests to 20 MW m\(^{-2}\) | 4 | CuCrZr embrittlement at DEMO neutron dose |
| He-cooled DEMO target | Prototype at 1 MW m\(^{-2}\) | 3 | Maximum heat flux 3–4× below ITER limit |
| IFE first wall at 10 Hz | No rep-rate test | 1–2 | Cyclic fatigue; 10\(^{10}\) shot lifetime |

### 8.2 Pathway Comparison

| Challenge Element | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Unmitigated q\(_{target}\) | ~150 MW m\(^{-2}\)[^3][^8] | Lower (island geometry spreads load) | Pulsed: peak >> MW m\(^{-2}\) per shot |
| ELM problem | Critical — 100 MJ ELMs[^10]; need >10× suppression | **Absent** — no driven plasma current, no ELM instability | Absent (no plasma pedestal) |
| Disruption risk | Severe — 2 GJ thermal + runaway electrons[^12] | Lower intrinsic disruption rate | Absent |
| Detachment approach | Impurity seeding + ADC | Island divertor; impurity seeding at W7-X[^13] | N/A — different physics |
| Wall material limit | W at 3–5 MW m\(^{-2}\) (irrad.)[^1] | Same W limit; 3D distribution more complex | Ablation/fatigue dominates — no steady-state limit |
| Progress maturity | MAST-U ADC results 2024–2025; RMP ELM suppression ongoing | W7-X detachment demonstrated[^23]; physics gap to reactor remains | IFE first wall design unsolved at rep-rate |

***

## Part IX — Open Research Questions and Analysis Entry Points

### Plasma Detachment and Impurity Seeding

- **Q1.1**: Can simultaneous ≥96% radiated power fraction and H-mode confinement quality factor \(H_{98} \geq 1.0\) be maintained in DEMO-like conditions (\(P_{sep}/R > 15\) MW m\(^{-1}\)) without unacceptable core impurity accumulation? What is the minimum attainable impurity concentration at the plasma core for the Ne/Ar seeding levels required?
- **Q1.2**: What detachment control system (sensor type, actuator bandwidth, predictive control algorithm) is required to maintain stable detachment in a DEMO plasma with ~150 MW SOL power, where a loss of detachment event can heat the divertor from 5 MW m\(^{-2}\) to >30 MW m\(^{-2}\) in <1 second?[^10]
- **Q1.3**: How do the power dissipation mechanisms observed in MAST-U ADCs (MAR, MAD, EIR) scale from MAST-U conditions (~1.2 MW SOL power) to DEMO (~150 MW SOL power), particularly in terms of the neutral pressure required in the divertor volume and the associated pumping requirements?

### Advanced Divertor Configurations

- **Q2.1**: Can the Super-X or Elongated divertor geometry demonstrated in MAST-U (spherical tokamak, aspect ratio ~1.8) be integrated into a conventional tokamak with aspect ratio ~3–4 (DEMO, ITER-like) while retaining >\(F_R = 1.5\) total flux expansion and sufficiently long divertor legs? What is the plasma volume penalty?
- **Q2.2**: What is the maximum P\(_{SOL}\) at which MAST-U ADC detachment benefits persist in H-mode plasmas with DEMO-relevant pedestal pressures? Does the factor of ~18.5× heat flux reduction observed at 1.2 MW SOL power hold at 10–15 MW (MAST-U upgrade power levels planned from 2026)?[^17]
- **Q2.3**: Can a stellarator be designed with a reactor-compatible island divertor geometry that simultaneously satisfies neutron shielding requirements, breeding blanket coverage, and remote maintenance access, without exceeding tungsten heat flux limits under reactor power?

### ELMs and Disruptions

- **Q3.1**: Does RMP ELM suppression in H-mode (demonstrated at \(q_{95} \approx 3.5\) in DIII-D/KSTAR/AUG) remain effective at the ITER baseline scenario (\(q_{95} = 3.0\)), and at the high electron collisionality pedestal conditions expected in ITER during DT operation?
- **Q3.2**: What pellet injection frequency, pellet size, and injection geometry achieve consistent ELM pace-making at DEMO pedestal energy levels (~10 MJ pedestal energy), while maintaining D\(_\infty\)-compatible fuel cycle (avoiding excessive tritium in pellet material)?
- **Q3.3**: What is the maximum tolerable disruption rate (disruptions per full-power-year) in DEMO without exceeding maintenance downtime budgets, and can disruption avoidance algorithms trained on ITER data be shown to generalize to burning plasma operational spaces before DEMO construction?

### ICF First Wall

- **Q4.1**: What W/Cu or W/SiC functionally graded material composition and first-wall chamber radius minimize temperature oscillations per shot to below the fatigue crack nucleation threshold for 10\(^{10}\) cycles at a 10 Hz rep rate? Is this achievable within chamber optical geometry constraints for direct-drive ICF?
- **Q4.2**: Can a liquid-metal wetted wall (Li or Sn/Li) be demonstrated in a rep-rate test stand at 5–10 Hz over 10\(^6\) shots with acceptable evaporation rate, tritium inventory, and plasma-compatibility?

***

## Conclusion

Of all five fusion challenges, power exhaust has seen the most rapid experimental progress in 2024–2025. The MAST Upgrade Super-X divertor results — an 18.5× heat flux reduction with improved detachment stability and core-edge compatibility, combined with the first demonstration of active exhaust control in an ADC — demonstrate that the physics community has identified a credible solution pathway. W7-X's stable detachment at near-full-power dissipation, sustained over hundreds of energy confinement times with no impurity accumulation, provides an encouraging parallel result for the stellarator pathway.[^23][^17][^3]

However, three major uncertainties remain that could reverse this optimism: First, ADC benefits must be validated at full DEMO-relevant SOL power (~150 MW) rather than the 1–15 MW range studied to date. Second, ELM suppression and disruption avoidance must be demonstrated to work in a burning plasma environment (where the alpha-particle drive, pedestal characteristics, and real-time diagnostic access differ fundamentally from current experiments) — and the consequences of failure are irreversible material damage rather than a plasma collapse requiring reflattening. Third, the helium-cooled divertor technology needed for DEMO's higher coolant temperatures has a heat flux limit 3–4× lower than ITER's water-cooled solution, demanding a much deeper level of plasma detachment control that pushes against the boundary of demonstrated core-edge compatibility.[^2][^9]

The power exhaust challenge therefore occupies a unique position among fusion's barriers: its physics has been largely understood and promising solutions have been experimentally demonstrated, but its engineering realization at reactor scale remains the frontier — and the consequences of insufficient progress are directly machine-limiting.

---

## Review & Model Update (November 2026)

Scope and model architecture are described in the overview report. This section covers gate **EX** (power
exhaust demonstrated).

### R.1 Currency and claim check

| ID | Location | Statement | Finding | Status |
|---|---|---|---|---|
| C4-01 | Executive summary | "~150 MW m⁻² in the scrape-off layer" | This is the unmitigated perpendicular target load, consistent with the report's own Part I 1.1 derivation; the SOL parallel flux is GW m⁻² | corrected |
| C4-02 | Executive summary | Super-X "while maintaining or improving core performance" | The result was obtained at ~1.2 MW SOL power. The report itself lists H-mode and DEMO-power validation as open (Part IX) | qualified |
| C4-03 | Throughout | DTT, MAST-U high-power campaigns, W7-X island divertor results | Not re-verified on 3 November 2026 | not re-verified |
| C4-04 | Part VI | Laser ICF chamber as one pathway | Split in R.2 | supplemented |

### R.2 Direct vs. indirect drive for this challenge

For IFE, the "exhaust" problem is the chamber: cyclic X-ray, ion and debris loads at 5–10 Hz, and clearing the
chamber before the next target arrives.
- **Indirect drive** adds hohlraum debris (high-Z vapour and droplets), which complicates clearing, optics
  protection and recovery. Model: EX P50 2057.
- **Direct drive**: EX P50 2056.
- Both have a show-stopper probability of 0.22, because no rep-rated chamber has been tested.

### R.3 TRL / licensing / funding view of Challenge 4

| Pathway | TRL | Licensing / permit | Funding |
|---|---|---|---|
| Tokamak | Detachment control and advanced divertors: TRL 4–5 at reduced power. Reactor-power validation (DTT, ITER) only in the 2030s [R1]. | Limited direct relevance. Divertor replacement drives activated-waste volumes. | Mostly public (DTT, MAST-U, ITER). SPARC tests compact high-flux exhaust. |
| Stellarator | The island divertor has run long pulses at W7-X; scaling to reactor power is open. | As tokamak. | Public (IPP) plus private (Proxima, Type One). |
| Direct / indirect drive | IFE first wall/chamber: TRL 1–2. | Chamber debris and activated-material handling are licence topics. | No dedicated chamber test facility is funded. |

### R.4 Mapping to the risk model (gate EX)

- **EX** — MCF: ≤ 5–10 MW m⁻² for ≥ 1000 s at reactor-relevant P/R. ICF: ≥ 50 MJ yields at ≥ 1 Hz over ≥ 10⁶ shots.

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | EX – Power exhaust | 2033 / 2039 / 2047 / 2062 / 2085 | 0.07 | `tok_ex`, `tok_f_ex` |
| Stellarator | EX – Power exhaust | 2035 / 2042 / 2052 / 2070 / 2095 | 0.12 | `stl_ex`, `stl_f_ex` |
| Direct Drive | EX – Power exhaust | 2040 / 2045 / 2056 / 2078 / 2098 | 0.22 | `dir_ex`, `dir_f_ex` |
| Indirect Drive | EX – Power exhaust | 2040 / 2046 / 2057 / 2080 / 2098 | 0.22 | `ind_ex`, `ind_f_ex` |

EX is coupled within a pathway to PL (MCF 0.60, ICF 0.35) and to MA (0.55). Across pathways it is coupled at
0.4 (tokamak–stellarator) and 0.7 (direct–indirect, same chamber problem). In the model, EX belongs to the
"nuclear" gates (`<p>_nuk`), which gate the first commercial plant rather than the demo decision.

### Sources for this review

Accessed 3 November 2026. Secondary sources are marked as such; claims resting only on them are flagged in the tables above.

- **[R1]** ITER Organization via ANS Nuclear News, 'ITER begins operations at its magnet cold test facility' (1 Jun 2026) — Baseline 2024: SRO 2034, full magnetic energy 2036, DT 2039. <https://www.ans.org/news/article-8081/iter-begins-operations-at-its-magnet-cold-test-facility/>

---

## References

1. [[PDF] Inter-ELM power exhaust in tokamak fusion reactors](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss74.pdf) - ... DEMO. Since material limits require that Qmax t remain below ∼ 10 MW/m2 for ITER, and likely bel...

2. [[PDF] mission for solution on heat-exhaust systems - MPG.PuRe](https://pure.mpg.de/rest/items/item_2218659_5/component/file_2414738/content)

3. [Divertor shaping with neutral baffling as a solution to the tokamak ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC12098118/) - 'Divertor detachment' is a process that reduces the ion target flux, enabling further power dissipat...

4. [[PDF] Physics of divertor power exhaust - ITER](https://www.iter.org/sites/default/files/education/%5B2-3%5D22JAN2019_Zohm.pdf)

5. [Improved core-edge compatibility using impurity seeding in the ...](https://pubs.aip.org/aip/pop/article/27/6/062506/1025327/Improved-core-edge-compatibility-using-impurity) - The challenge for future reactors is the achievement of divertor detachment compatible with high cor...

6. [[PDF] Scaling of the tokamak near scrape-off layer H- mode power width ...](https://conferences.iaea.org/event/10/contributions/73/attachments/15/15/ITR-1-1_Eich_T..pdf)

7. [Microsoft Word - SOL width paper v4.1](https://www.osti.gov/servlets/purl/1167692)

8. [[PDF] Limitations of Transient Power Loads on DEMO and Analysis of ...](https://pure.mpg.de/rest/items/item_2332340_6/component/file_2424443/content)

9. [[PDF] Nuclear Materials and Energy](https://boa.unimib.it/retrieve/d24807d7-bd02-4e37-8c4c-4ba3fd4fbaa7/Maviglia-2021-Nucl%20Mater%20Energy-VoR.pdf) - This solution, however, limits the tolerable steady-state heat flux to ~1 MW/m2, i.e. a factor. 3–4 ...

10. [DEMO divertor limitations during and in between ELMs](https://pure.mpg.de/rest/items/item_2072835/component/file_2072833/content)

11. [High-heat-flux technologies for the European DEMO divertor targets: State-of-the-art and a review of the latest testing campaign](https://pure.mpg.de/rest/items/item_3284207/component/file_3284616/content)

12. [DEMO Exhaust Challenges Beyond ITER](https://pure.mpg.de/rest/items/item_2240145_4/component/file_3319251/content)

13. [First demonstration of radiative power exhaust with impurity ...](https://www.osti.gov/pages/biblio/1802584) - The U.S. Department of Energy's Office of Scientific and Technical Information

14. [Comparison of divertor behavior and plasma confinement between argon and](https://www.osti.gov/servlets/purl/1829010)

15. [[PDF] Advanced divertor research on the TCV tokamak](https://info.fusion.ciemat.es/OCS/EPS2015ABS/pdf/P2.150.pdf)

16. [[PDF] Novel SOLPS-ITER simulations of X-point target and snowflake ...](https://eprints.whiterose.ac.uk/id/eprint/197573/1/Cowley_2023_Plasma_Phys._Control._Fusion_65_035011.pdf)

17. [Demonstration of Super-X divertor exhaust control for transient heat load management in compact fusion reactors](https://www.nature.com/articles/s41560-025-01824-7) - Managing power exhaust in fusion reactors is a key challenge, especially in compact designs for cost...

18. [[PDF] Highlights from the third experiment campaign of MAST Upgrade](https://www.aappsdpp.org/DPP2025/html/3contents/pdf/5736.pdf)

19. [[PDF] OV/1-1 Research Toward Resolving Key Issues for ITER and Steady ...](https://www6.lehigh.edu/~eus204/per/publications/abstracts/iaea12c.pdf)

20. [[PDF] Power Handling and Plasma Protection Aspects that affect the ...](https://conferences.iaea.org/event/98/contributions/11964/attachments/5827/7196/Wenninger_R.pdf) - The divertor protection problem in DEMO is expected to be more challenging than in ITER. The total h...

21. [[PDF] First results from divertor operation in Wendelstein 7-X](https://juser.fz-juelich.de/record/858313/files/Pedersen_2019_Plasma_Phys._Control._Fusion_61_014035.pdf) - The typical Lc in the island divertor in W7-X is about one order of magnitude longer than that in a ...

22. [First Observation of a Stable Highly Dissipative Divertor Plasma Regime on the Wendelstein 7-X Stellarator - PubMed](https://pubmed.ncbi.nlm.nih.gov/31386539/) - For the first time, the optimized stellarator Wendelstein 7-X has operated with an island divertor. ...

23. [Stable heat and particle flux detachment with efficient particle exhaust in the island divertor of Wendelstein 7-X](https://www.osti.gov/biblio/1814444) - The island divertor concept is an innovative and promising idea to handle heat and particle exhaust ...

24. [Overview of the results from divertor experiments with attached and detached plasmas at Wendelstein 7-X and their implications for steady-state operation](https://www.osti.gov/pages/biblio/1835350) - The U.S. Department of Energy's Office of Scientific and Technical Information

25. [[PDF] First results from divertor operation in Wendelstein 7-X](https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPS1PR18_21092_submitted.pdf)

26. [Heat Transport Widths and its Scaling in the W7-X Island ...](https://conferences.iaea.org/event/394/contributions/37584/contribution.pdf)

27. [STELLARATOR FUSION REACTORS –– AN OVERVIEW](https://fire.pppl.gov/itc12_wobig_paper.pdf)

28. [[PDF] Chamber wall response to target implosion in inertial fusion reactors](https://engineering.purdue.edu/CMUXE/Publications/AH/FED02-AH.pdf)

29. [[PDF] Memorandum Laser Inertial Fusion Energy - BMFTR](https://www.bmftr.bund.de/SharedDocs/Downloads/DE/2023/230522-memorandum-laser-inertial-fusion-energy.pdf?__blob=publicationFile&v=3) - first wall in the reaction chamber, fuel cycle or blanket development. As ... A high repetition rate...

30. [Thermal Mechanical Response Analysis of the First Wall in Laser ...](https://www.sciencedirect.com/science/article/pii/S246860502500050X)

31. [1136590358575054874-70252](https://www.bohrium.com/paper-details/thermal-mechanical-response-analysis-of-the-first-wall-in-laser-initial-confinement-fusion-reactors/1136590358575054874-70252)

32. [A review on two previous divertor target concepts for DEMO](https://pure.mpg.de/rest/items/item_2227442/component/file_3154032/content)

33. [[PDF] High heat flux components for a DEMO fusion reactor - CERN Indico](https://indico.cern.ch/event/400452/contributions/1841118/attachments/1182813/1713232/11-EUCARD2_CERN_Workshop_M._Coleman_v5.pdf)
