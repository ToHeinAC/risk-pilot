# Nuclear Fusion — Deep Dive: Challenge 4
## Power Exhaust & Divertor Heat Loads

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — November 2026 update*

***

## Executive Summary

The power exhaust problem is arguably the most immediate engineering-physics challenge separating ITER from DEMO and from commercial fusion. The fundamental mismatch is stark: the **unmitigated perpendicular heat flux on the divertor target** of an EU-DEMO-class tokamak is estimated at **~150 MW m\(^{-2}\)** or more (corresponding to a *parallel* heat flux along the field lines of several GW m\(^{-2}\); for the compact high-field SPARC, empirical scalings give an unmitigated parallel heat flux of **>10 GW m\(^{-2}\)**), while the steady-state engineering limit of tungsten armour on water-cooled divertor components is approximately **5–10 MW m\(^{-2}\)** (and lower for neutron-irradiated components). Bridging this gap by a factor of 15–30× — every pulse, every day, for the 20+ year life of the reactor — without degrading core plasma performance is the central power exhaust challenge.[^1][^2][^3][^34]

The difficulty has three compounding layers. The first is the **geometric problem**: the scrape-off layer (SOL) power channel is only **~1 mm wide** at the outboard midplane (empirical Eich scaling extrapolated to ITER/DEMO), concentrating 100–300 MW of exhaust power onto a wetted divertor area of ~1–4 m². The second is the **materials problem**: the only viable armour material — tungsten — on a copper-alloy heat sink is qualified to ~10 MW m\(^{-2}\) steady state (ITER), but the design margin shrinks to ~5 MW m\(^{-2}\) once neutron irradiation degrades the CuCrZr heat sink and the W armour in DEMO. The third is the **compatibility problem**: the techniques used to reduce divertor heat load (impurity seeding, detachment, high density operation) all have the potential to degrade the core plasma confinement whose maintenance is the reason for having the reactor at all.[^4][^2][^5][^1][^11]

Unlike the tritium or materials challenges — which require entirely new facilities to solve — the power exhaust challenge is actively being worked on experimentally on operating machines today. MAST Upgrade (UK) showed (Communications Physics, May 2025) that the Super-X divertor with strong neutral baffling reduces the peak target heat flux **~18.5×** versus a conventional divertor, and a companion *Nature Energy* paper (September 2025) demonstrated feedback control of detachment and passive buffering of transients with near-independent upper/lower divertors. These are, however, **L-mode experiments at ~1 MW SOL power**, i.e. two orders of magnitude below DEMO. In 2025 WEST (France) and EAST (China) set plasma-duration records of 1337 s and 1066 s (H-mode), and Wendelstein 7-X reached a 360 s, 1.8 GJ energy-turnover discharge — long-pulse demonstrations, but at heat-exhaust power densities far below reactor level. No device has yet combined reactor-relevant P\(_{sep}\)/R, long pulse, a burning core and a component-lifetime demonstration; the first facilities that can approach parts of this combination (SPARC ~2027, Italian DTT early 2030s, ITER DT 2039) are still under construction.[^3][^17][^38][^40][^41][^42]

***

## Part I — The Fundamental Power Exhaust Problem

### 1.1 From SOL to Target: The Heat Concentration Geometry

In a tokamak or stellarator, the power that crosses the last closed flux surface from the hot plasma core enters the **Scrape-Off Layer (SOL)**. In this region, open magnetic field lines guide the power along essentially parallel paths to the divertor targets. The key problem is that the heat channel in the SOL is extremely narrow.

The empirical **Eich scaling** for H-mode SOL heat flux width \(\lambda_q\) gives, for ITER-class devices:[^6][^7]

\[\lambda_q \propto B_p^{-1.19}\]

where \(B_p\) is the poloidal magnetic field at the outboard midplane (full regression: \(\lambda_q \approx 0.63\,B_{p}^{-1.19}\) mm). For ITER (\(B_p \approx 0.7\) T) this gives \(\lambda_q \approx 1\) mm at the outboard midplane. For DEMO with similar or higher poloidal field, \(\lambda_q\) is likewise expected to be **~1 mm**. An important caveat: gyrokinetic XGC1 simulations (Chang et al. 2017) reproduce the present-machine data but project **λ\(_q\) ≈ 5.9 mm for ITER**, because turbulent electron transport rather than ion magnetic drift dominates at ITER scale — if correct, this would relax the problem several-fold; it has not been confirmed experimentally. When the heat channel maps to the divertor target (poloidal flux expansion ~3–5× in a conventional divertor, plus divertor broadening S of ~1–2 mm), the footprint on the target is still only a **~1–3 cm wide strike zone**.[^2][^1][^6][^35]

The peak perpendicular power density on this strike zone can be estimated (neglecting volumetric dissipation) as:

\[q_{\perp,target} \approx \frac{f_{out} \cdot P_{sep}}{2\pi R_t \cdot \lambda_{int} \cdot f_x}, \qquad \lambda_{int} \approx \lambda_q + 1.64\,S\]

where \(P_{sep}\) is the power crossing the separatrix, \(f_{out}\) is the fraction going to the outer target (~2/3), \(R_t\) is the major radius of the strike point, \(f_x\) the poloidal flux expansion, and \(\lambda_{int}\) the integral width including divertor broadening. For DEMO with \(P_{sep} \approx 150\) MW, \(R_t \approx 8\) m, \(\lambda_{int} \approx 3\) mm, and \(f_x \approx 4\), the unmitigated target heat flux evaluates to approximately **150–170 MW m\(^{-2}\)** — consistent with independently computed estimates — versus a material limit of ~5–10 MW m\(^{-2}\). The corresponding *parallel* heat flux upstream, \(q_\parallel \approx f_{out} P_{sep}/(2\pi R_u \lambda_q B_p/B)\), is of order **5 GW m\(^{-2}\)** for DEMO; parallel and perpendicular values differ by the field-line incidence and flux expansion and must not be compared directly with material limits.[^8][^3][^34]
*(Corrected Nov 2026: the earlier version of this formula used \(4\pi R\) and a \(\sin\theta\) divisor, which with the quoted inputs gives ~6 GW m\(^{-2}\), not 150 MW m\(^{-2}\).)*

### 1.2 The P/R Scaling Problem

A key insight from multi-machine experimental studies is that the divertor heat flux does not scale with machine size — the loaded divertor area scales approximately linearly with machine major radius \(R\), while the exhaust power \(P_{heat}\) scales as \(R^3\) for fixed geometry. The relevant dimensionless parameter is therefore:[^2]

\[\text{Exhaust power per unit major radius:} \quad P_{sep}/R\]

For ITER (Q = 10): \(P_{sep}/R \approx 100/6.2 \approx 16\) MW m\(^{-1}\).[^4][^2]
For DEMO: \(P_{sep}/R \approx 150/9 \approx 17\) MW m\(^{-1}\) — similar to ITER — but with a tighter material constraint (irradiated components, ~5 vs. 10 MW m\(^{-2}\) design value) and far longer pulse duration (hours instead of 400 s) and cumulative fluence, which removes any reliance on thermal inertia. Metrics that include the field and geometry, such as \(P_{sep}B_t/(q_{95}AR)\), are increasingly used because they track the parallel heat flux more closely; on that metric compact high-field devices (SPARC, ARC) are *more* demanding than DEMO.[^2][^34]

On ASDEX Upgrade, at \(P_{sep}/R \approx 10\) MW m\(^{-1}\) (approximately 2/3 of ITER's value), the unmitigated divertor heat flux would be of order 40 MW m\(^{-2}\); it was reduced to <5 MW m\(^{-2}\) by feedback-controlled nitrogen (N\(_2\)) seeding. **Extrapolation to DEMO suggests that without advanced divertor solutions, approximately 95–97% of the total power crossing the separatrix must be dissipated before reaching the target** to keep heat flux below 5 MW m\(^{-2}\). ASDEX Upgrade reached 85 ± 10% with double-radiation feedback control, and later, using a controlled **X-point radiator (XPR)**, achieved full detachment at a dissipated power fraction of **~95%** with ELM suppression and only minor confinement loss (Bernert et al. 2021). In 2025 XPR control was also demonstrated in JET D and DT plasmas (with argon; neon did not allow control). These results close the *fraction* gap, but at absolute P\(_{sep}\)/R, pulse length and wall conditions well short of DEMO; no device has yet shown ≥95% dissipation at DEMO-relevant P\(_{sep}\)/R with H\(_{98}\) ≈ 1 for long pulses.[^9][^10][^4][^36][^37]

### 1.3 The DEMO Constraint Table

| Parameter | ITER | EU DEMO | Material Limit | Gap Factor |
|---|---|---|---|---|
| P\(_{sep}\) (power to SOL) | ~100 MW | ~150 MW[^9] | — | — |
| P\(_{sep}\)/R [MW m\(^{-1}\)] | ~16 | ~17[^2] | — | — |
| Unmitigated q\(_{\perp,target}\) [MW m\(^{-2}\)] | tens (order 40)[^4] | ~150[^3] | — | — |
| Unmitigated q\(_\parallel\) [GW m\(^{-2}\)] | ~1–3 | ~5 (est.) | — | SPARC: >10[^34] |
| W armour heat flux limit [MW m\(^{-2}\)] | ~10 (unirrad.)[^11] | ~5 (irrad. design value)[^1] | 5–10 | 15–30× needed |
| Required dissipated fraction | ~70–80% | ~95–97%[^9][^10] | — | AUG: 85% (double radiator), ~95% (XPR)[^36] |
| Natural Type-I ELM energy (DEMO) | — | ~100 MJ[^10] | target energy density ~0.5 MJ m\(^{-2}\) | ≥10× (up to ~200×) reduction needed[^10] |
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

MAST Upgrade is a spherical tokamak at UKAEA Culham specifically designed to test ADCs with combined long-legged geometry, high total flux expansion, and strong neutral baffling. Two papers published in 2025 — Verhaegh et al., *Communications Physics* 8, 215 (May 2025) on the steady-state physics, and Kool et al., *Nature Energy* 10, 1116–1131 (September 2025) on exhaust control and transients — provide the strongest experimental evidence to date for ADC benefits:[^17][^3][^38]

**Important scope caveat**: the main shape comparison was made in **NBI-heated L-mode at P\(_{SOL}\) ≈ 1.2 MW** (NBI 1.5–1.7 MW); H-mode comparisons were reported earlier only qualitatively (outer divertor attached in conventional, detached in Super-X, no pedestal impact). The quantitative factors below therefore come from a regime ~100× below DEMO SOL power.[^3]

**Steady-state heat flux reduction** (Communications Physics 2025):
- Super-X divertor vs. conventional divertor: **~18.5× reduction** in peak target heat flux, substantially exceeding the ~5.8× expected from geometry alone[^3]
- Elongated divertor: ~7× reduction vs. conventional (~2.1× expected from geometry)[^3]
- The additional factor of ~3.2× beyond geometric expectation is attributed to additional volumetric/cross-field power dissipation (hydrogenic losses alone reduced target power ~4× in SXD), with molecular processes (MAR, MAD) and EIR in the extended, baffled leg — confirming that the long-leg volume is an active power sink, not merely a geometric expansion. Total flux expansion explains roughly 80% of the improved detachment access[^3]

**Detachment access and stability**:
- Super-X and Elongated divertors were fully detached at all tested core densities; the Conventional divertor only detached at \(f_{GW} \approx 40\%\), near the Greenwald limit[^3]
- The SXD detachment front sensitivity to changes in core density is **5× lower** than the conventional divertor — a critical stability improvement for reactor control[^3]
- These detachment stability benefits extend to **dynamic transients** (fast gas valve perturbations): the SXD passively absorbs fuelling transients that would move the conventional divertor detachment front beyond the operational window into MARFE or re-attachment[^17]

**Core-edge compatibility**:
- **No adverse core impact** was observed when the outer target was detached in the SXD or ED, in contrast to the conventional divertor which required high Greenwald fraction for detachment[^3]
- Core electron temperatures, densities, and total SOL power remained unchanged as divertor shape was varied[^3]

**Control demonstration (experiments 2023–2024, published *Nature Energy* September 2025)**:
- First demonstration of **active feedback exhaust control** in an alternative divertor configuration, using a new diagnostic method for the neutral gas buffer that shields the target[^17]
- Same PI controller (tuned once) successfully controlled detachment in both ED and SXD configurations
- Upper and lower divertors showed **near-independent controllability** (decoupled from each other and from the core by strong neutral baffling), a prerequisite for double-null reactor designs[^17][^38]

These results represent a step-change in confidence for ADC solutions. The finding that detachment benefits persist at "more moderate divertor shaping" (lower flux expansion than the maximum SXD) is particularly important for reactor engineering — it suggests that DEMO need not implement the most extreme divertor geometry to capture most of the exhaust benefit.[^3]

**2025–2026 campaign and next steps**: UKAEA completed the **fifth MAST-U campaign** (>1,100 discharges across 2025–2026; reported August 2026). Exhaust-relevant results include the first detailed study of nitrogen-seeded radiative exhaust in a tightly baffled Super-X double-null on a spherical tokamak (a large share of exhaust power radiated), access to the ELM-free/small-ELM **QH-mode and I-mode** regimes, negative-triangularity studies, and record plasma pressure for the device. Peer-reviewed quantitative results from this campaign were not yet available at the time of writing. The enhancement programme (two additional NBI injectors doubling NBI power, plus a 1.6 MW EBW system relevant to STEP) runs through 2027; the **sixth campaign is planned for 2028** — so the earlier expectation of >10 MW high-power ADC tests "from 2026" has slipped to 2028 or later.[^39]

### 3.3 Other ADC Concepts

**Snowflake Divertor (SFD)**: A second X-point is placed near the primary X-point, forking the SOL power into two strike points and significantly enhancing cross-field transport in the null region. TCV experiments show an order-of-magnitude reduction in peak heat flux in the XPT variant. MAST-U H-mode experiments showed strong radiative exhaust in the region of low poloidal field around the X-points, with power sinks redistributed among multiple divertor legs downstream of the secondary X-point. However, the Snowflake geometry has a narrow magnetic configuration window and is sensitive to plasma current profile changes.[^18][^16][^15]

**X-point Target (XPT)**: A second X-point is placed inside or at the divertor target, producing extremely large poloidal flux expansion and locally enlarged connection length and SOL volume — an order-of-magnitude reduction in peak heat flux even at intermediate density. The challenge is the very shallow field-line angle at the target, which creates issues with leading edges and component alignment tolerances.[^15]

**X-point radiator (XPR)**: rather than a new magnetic geometry, a strongly radiating impurity "cloud" is held inside the confined region just above the X-point by feedback on seeding (N, Ar). AUG achieved ~95% dissipated power with full detachment and ELM suppression; JET extended XPR control to D and DT plasmas in 2025 (argon only). The XPR works in a conventional divertor, which makes it attractive for ITER/DEMO-like machines, but the radiator sits close to the confined plasma and loss of control can lead to a radiative collapse/disruption.[^36][^37]

**Negative triangularity (NT)**: NT plasmas on DIII-D and TCV are intrinsically ELM-free at powers well above the L-H threshold while reaching H\(_{98}\) ≳ 1 at high density, removing the ELM problem by plasma shape. The drawback for exhaust is a **narrower SOL and harder detachment** observed on TCV; integrated detached high-performance NT scenarios have only been shown partially (TCV, 2025–2026 abstracts).[^48]

### 3.4 Liquid-Metal Divertors

Liquid-metal plasma-facing components (Li, Sn, Li-Sn), either as capillary-porous systems or fast-flowing free surfaces, offer a self-healing surface without a fatigue/erosion lifetime limit and potentially higher heat-flux tolerance via evaporation and vapour shielding. Status in 2026:
- Modelling for COMPASS-U and DEMO/DTT finds both Li and Sn feasible under suitable divertor conditions, but Sn may need backside cooling beyond ITER-like water cooling, and Li retention of tritium and evaporation into the core remain major concerns.
- **Tokamak Energy** has built a flowing-lithium loop with a replaceable open-surface divertor module installed on the HIDRA device (University of Illinois), targeting the ~5 mm thick, ~1 m s\(^{-1}\) flowing layer estimated necessary for a ~1 m divertor; a free-surface fast-flow (>1 m s\(^{-1}\)) Li divertor is being explored for its ST-E1 pilot plant. No plasma-exposed operation at reactor heat flux had been reported by November 2026.[^49]
- DTT's magnetic and divertor design explicitly allows liquid-metal-based divertor solutions, to be tested in its later full-performance phase.[^45]

Liquid metals therefore remain a **TRL 3–4 option**: a potential breakthrough that would relax both the heat-flux and the component-lifetime constraint, but with open tritium-inventory, MHD-flow and core-contamination risks.

### 3.5 Dedicated Exhaust Facilities: Italian DTT and SPARC

**Divertor Tokamak Test (DTT, Frascati)**: a 6 T superconducting tokamak (R = 2.19 m, I\(_p\) = 5.5 MA, ~45 MW installed heating at full performance) with tungsten divertor and wall, designed so that P\(_{SOL}\)/R approaches ITER/DEMO values (~15 MW m\(^{-1}\)) and with a flexible poloidal field system for single-null, double-null and alternative divertors, explicitly including liquid-metal solutions. The 2022 plan was staged: ~20 MW at first plasma, ~45 MW about four years later, advanced divertors tested only in a third phase at full performance. Its first-plasma date has slipped repeatedly: ~2022 (2016 proposal) → spring 2028 (2022 plan) → end-2030 → the 2025 IAEA FEC overview poster gives **July 2032**. The first superconducting TF coil was completed in May 2025. With the staged heating plan, DEMO-relevant P\(_{sep}\)/R exhaust results from DTT are unlikely before **~2036–2040**.[^43][^44][^45]

**SPARC (Commonwealth Fusion Systems)**: high-field (12.2 T) compact tokamak, all-tungsten PFCs. Empirical scalings give an **unmitigated peak parallel heat flux >10 GW m\(^{-2}\)** (roughly an order of magnitude above anything demonstrated) and parallel ELM energy fluences of ~11–34 MJ m\(^{-2}\), comparable to ITER. Because pulses are ~10 s, the baseline uses a **~1 Hz strike-point sweep** onto inertially cooled tungsten tiles rather than an actively cooled steady-state divertor, plus impurity seeding. SPARC assembly progressed through 2026 (TF magnet installation began in January 2026; vacuum vessel delivered); first plasma is targeted for 2027. SPARC will be the first test of exhaust at reactor-class q\(_\parallel\), but **not** a long-pulse or lifetime demonstration; ARC must solve the steady-state problem separately.[^34][^51]

### 3.6 Long-Pulse Tokamaks: WEST and EAST (2025)

- **EAST** (Hefei) sustained a **1066 s H-mode** plasma on 20 January 2025.[^40][^52]
- **WEST** (CEA Cadarache, all-tungsten, actively cooled ITER-grade W monoblock divertor) sustained plasma #61299 for **1337 s** on 12 February 2025 with ~2 MW of lower-hybrid heating and 2.6 GJ injected and extracted energy; CEA aims to raise power to ~10 MW at ~1000 s durations.[^40]

These pulses validate actively cooled tungsten components, wall-conditioning and control over 1000 s timescales — essential for the "long-pulse" part of the gate — but at P\(_{sep}\)/R of order 1 MW m\(^{-1}\), an order of magnitude below ITER/DEMO. Combining 1000-s duration with reactor power density remains undemonstrated.

***

## Part IV — Transient Heat Loads: ELMs and Disruptions

### 4.1 ELMs in DEMO: The Critical Constraint

**Edge Localized Modes (ELMs)** are periodic MHD instabilities at the H-mode pedestal that transiently expel energy from the plasma in intense bursts impacting the divertor. In DEMO, the total thermal energy is \(W_{th} \approx 2\) GJ. A "natural" ELM releasing 5% of \(W_{th}\) corresponds to:

\[\Delta W_{ELM} = 0.05 \times 2 \text{ GJ} = 100 \text{ MJ}\]

The energy impact factor limit for tungsten is approximately \(\eta = \Delta W / (A\sqrt{\tau}) \approx 50\) MJ m\(^{-2}\) s\(^{-0.5}\). For a typical ELM duration of ~1 ms, the area \(A\) that receives 100 MJ without exceeding the melt limit must satisfy:[^12]

\[A > \frac{100 \text{ MJ}}{50 \text{ MJ m}^{-2} \text{ s}^{-0.5} \times \sqrt{10^{-3} \text{ s}}} \approx 63 \text{ m}^2\]

The actual ELM-wetted divertor target area in DEMO is ~2–4 m². This means that uncontrolled natural ELMs in DEMO exceed the tungsten melt limit by a factor of **~15–30×**. JET results on ELM broadening suggest that even accounting for ELM-induced broadening in DEMO, the energy density limit of **~0.5 MJ m\(^{-2}\)** (target energy density per ELM, not total ELM energy) is exceeded by a factor of approximately **8× for a wide range of relative ELM sizes**.[^10]

**ITER reference values**: for ITER the limits are even tighter than the simple surface-melt criterion. Ion-orbit modelling of ELM loads on the ITER W monoblocks (Gunn et al. 2017) finds that avoiding *edge* melting of the monoblocks altogether requires the ELM surface energy density to stay below **~0.15 MJ m\(^{-2}\)**; other analyses use parallel energy-fluence limits of order several MJ m\(^{-2}\) at the leading edge. Uncontrolled Type-I ELMs in ITER Q = 10 operation are expected to melt the top surface of several poloidal rows of monoblocks. For SPARC, scalings give parallel ELM energy fluences of ~11–34 MJ m\(^{-2}\), comparable to ITER. (The different numbers in the literature refer to different quantities — perpendicular vs. parallel, surface vs. leading edge — and should not be mixed.)[^46][^34]

Therefore, ITER and DEMO require an ELM control technique — or an intrinsically ELM-free regime — capable of **reducing individual ELM energy releases by more than an order of magnitude** without degrading H-mode confinement.[^12][^10]

**ELM mitigation approaches** under development:[^19][^12]
- **Resonant Magnetic Perturbations (RMPs)**: external coil sets apply small non-axisymmetric fields that suppress or significantly reduce ELM frequency and amplitude. ITER has a dedicated 27-coil RMP system. RMP ELM suppression has been demonstrated on DIII-D, AUG, KSTAR, and EAST — but performance at ITER pedestal parameters (high electron collisionality) is not yet established
- **High-frequency small ELMs via pellet injection**: injecting small cryogenic hydrogen pellets at high frequency (>10 Hz) triggers small ELMs synchronously, depleting the pedestal energy before it can accumulate to large-ELM levels. Pellet ELM pace-making requires pellet injection rates in the range 50–100 Hz for DEMO, which is at the edge of current pellet injector technology[^19]
- **Naturally ELM-free regimes**: I-mode (high confinement without ELMs), QH-mode (Quiescent H-mode with edge harmonic oscillation instead of ELMs), the quasi-continuous-exhaust (QCE) small-ELM regime, the XPR-induced ELM-suppressed regime, and negative-triangularity plasmas (ELM-free by shape). The challenge is accessing these regimes at DEMO-relevant density and pedestal pressure, simultaneously with a detached divertor. MAST-U accessed QH-mode and I-mode in its 2025–2026 campaign.[^36][^39][^48]

### 4.2 Disruptions in DEMO

A disruption — the sudden termination of plasma current — in DEMO releases on the order of 1–2 GJ of thermal energy within ~1 ms (thermal quench) and a poloidal magnetic energy of the order of a few GJ over tens of ms (current quench). (Corrected: earlier versions quoted 50–100 GJ magnetic energy, which is the order of the *toroidal-field coil* stored energy and is not released in a plasma disruption.) The unmitigated thermal-quench load on the first wall and divertor far exceeds the tungsten melt threshold (heat-flux factor ~50 MJ m\(^{-2}\) s\(^{-0.5}\)) locally. Runaway electron (RE) beams generated during the current quench can carry up to ~10 MA in ITER/DEMO-class devices at typical energies of tens of MeV, with beam kinetic plus magnetic energy of tens to hundreds of MJ that can melt local wall structures if not mitigated.

**Disruption mitigation systems (DMS)** inject massive quantities of frozen gas or shattered pellets of noble gases (Ne, Ar) to:
1. Radiate the thermal energy uniformly before it reaches the wall (thermal quench mitigation)
2. Suppress runaway electron avalanche growth by increasing plasma density
3. Force the current quench to be resistive rather than sudden, reducing induced eddy currents in the vacuum vessel

ITER's baseline Disruption Mitigation System is based on Shattered Pellet Injection (SPI) of H/D and Ne pellets; its design is being finalised on the basis of a multi-machine (JET, DIII-D, KSTAR, AUG) task force, with ITER's new 2024 baseline (tungsten first wall, Start of Research Operation 2034) making early mitigation of disruptions on a W wall even more important. For DEMO, the challenge is more severe:[^20][^12][^42]
- Higher stored energy (~1–2 GJ thermal, a few GJ poloidal magnetic) than ITER (~0.35 GJ thermal, ~0.4 GJ magnetic in-vessel)
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

- **2025 long-pulse records (OP2.3, actively water-cooled divertor)**: a **360 s discharge with 1.8 GJ energy turnover** (previous record 1.3 GJ, 2023), and on 22 May 2025 a world-best triple product for long plasmas sustained for **43 s** with pellet fuelling and ECRH. These show steady-state compatibility of the island divertor with high core performance, but at heating powers of a few MW, i.e. P\(_{sep}\)/R far below reactor level.[^41]

These W7-X results are highly significant because optimised stellarators operated so far in their standard island-divertor regimes show no type-I ELMs and have no current-driven disruptions (ELM-like edge events have been observed in some stellarators, e.g. W7-AS and LHD, but at much smaller amplitude). This is a **fundamental exhaust advantage** of stellarators over tokamaks: the most dangerous transient heat-load mechanisms (large ELMs and disruptions) are largely absent.

### 5.3 Stellarator Divertor Heat Flux Challenges

Despite these advantages, several challenges specific to the stellarator island divertor remain:[^25][^26][^24][^21]

- **3D SOL heat transport complexity**: the island divertor SOL is inherently three-dimensional. Heat flux patterns on W7-X divertor targets show multiple lobes from the five-island chain; leading edges between tiles receive enhanced local heat loads that are difficult to predict and mitigate. The EMC3-EIRENE 3D SOL code has qualitative agreement with experiments but requires further validation[^26][^24]
- **Impurity screening**: the island divertor shows good impurity screening (experiments with overloaded leading edges showed that the island SOL retains good impurity confinement), but this must be confirmed at higher plasma density and heating power relevant to a reactor[^24]
- **Scaling to reactor conditions**: W7-X operates at up to 10 MW of absorbed power in OP2 (with the actively cooled divertor). A HELIAS reactor would exhaust ~350 MW. The SOL heat flux width scaling in the island geometry (\(\Lambda_W\) framework developed at W7-X) is only at early empirical stage — extrapolation to reactor conditions carries large uncertainties[^26]
- **Reactor divertor engineering**: as discussed in Challenge 2, the 3D geometry of a stellarator blanket leaves very limited space for divertor structures. A HELIAS power plant divertor must fit within the complex 3D coil geometry, compatible with neutron shielding requirements and remote maintenance access[^27]
- **Island sensitivity to plasma current and beta**: the island chain position depends on bootstrap current and plasma beta; strike lines can move onto unprotected components during long-pulse evolution, which in W7-X requires current compensation or configuration control. Private stellarator projects (e.g. Type One Energy, Proxima Fusion, Thea Energy) aim at pilot plants in the 2030s, but none has published an experimentally validated reactor-scale divertor solution; their divertor designs rest on W7-X extrapolations.

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

No integrated IFE chamber concept has been demonstrated at rep-rate in any experiment as of November 2026. The German BMBF (now BMFTR) Laser IFE memorandum (2023) identifies the reaction-chamber first wall among the key IFE-specific engineering challenges, alongside driver efficiency/repetition rate and target supply.[^29]

### 6.3 2025–2026 Context: Rising Yields Raise the Bar

NIF produced a record **8.6 ± 0.45 MJ** on 7 April 2025 from 2.08 MJ of laser energy (target gain 4.13), and has achieved ignition repeatedly since December 2022. Each increase in yield per shot raises the per-pulse X-ray, debris and neutron load that a power-plant chamber must absorb: commercial concepts assume yields of ~50–1,000 MJ per shot at 1–10 Hz, i.e. one to two orders of magnitude above NIF, repeated ~10\(^8\)–10\(^9\) times per year. The private IFE developers (e.g. Xcimer, Focused Energy, Marvel Fusion, Inertia Enterprises) have so far concentrated on drivers and targets; published chamber designs largely re-use 1990s–2000s thick-liquid-wall (HYLIFE-II type, FLiBe jets) or dry-wall (HAPL) concepts. There is still no rep-rated high-yield source capable of testing chamber walls, so the IFE wall problem can only be tested in a pilot plant or with surrogate (X-ray, ion-beam, laser) load tests.[^50][^28]

***

## Part VII — Helium-Cooled vs. Water-Cooled Divertor: DEMO Trade-off

The choice between helium-cooled and water-cooled divertor targets in DEMO has significant implications for achievable heat flux limits and system integration:[^32][^33][^2]

**Water-cooled divertor (ITER heritage)**:
- ITER technology: CuCrZr alloy coolant tube with W armour, water at 3.3 MPa, 100°C, 10 m/s with swirl tube insert
- Achievable steady-state heat flux: up to **10 MW m\(^{-2}\)** demonstrated with 5,000 cycles; up to 20 MW m\(^{-2}\) for 300 cycles[^32]
- **DEMO limitation**: CuCrZr loses ductility and fracture toughness under neutron irradiation, particularly at low irradiation temperature (embrittlement), while at higher temperatures it softens; the expected end-of-life damage in the DEMO divertor heat sink (several dpa) leaves only a narrow operating window. The EU DEMO baseline therefore keeps **water-cooled W/CuCrZr monoblock targets**, but with "hot" water at **~130–150 °C and ~5 MPa** (vs. ~70–120 °C in ITER), which reduces critical-heat-flux margin. EU DEMO target mock-ups survived up to 500 cycles at 20 MW m\(^{-2}\) with 130 °C water in high-heat-flux tests; the design steady-state value is ~10 MW m\(^{-2}\) unirradiated, with irradiated margin assumed to be lower.[^11][^47]

**Helium-cooled divertor**:
- Operates at ~10 MPa and ~600–700°C; avoids corrosion and tritium permeation into water; compatible with Brayton cycle thermodynamic efficiency
- **Heat-flux capability**: He-cooled finger/jet concepts (e.g. the KIT HEMJ design) were developed for ~10 MW m\(^{-2}\) and tested at that level, but with small margins, large pumping power and complex manufacturing; the EU therefore dropped them from the DEMO baseline in favour of water cooling.[^32]
- *(Correction, Nov 2026: earlier versions stated a He-cooled divertor limit of ~1 MW m\(^{-2}\). The ~1 MW m\(^{-2}\) "factor 3–4 below ITER" figure in [^9] refers to the **He-cooled DEMO first wall** (vs. 1–4.7 MW m\(^{-2}\) ITER first-wall panels), not to the divertor.)*

The relevant consequence is that a He-cooled **first wall** cannot tolerate the plasma-wall contact and transient loads that the ITER first wall can; this reinforces the need for robust disruption avoidance/mitigation, ELM control and dedicated limiters in DEMO.[^9][^2]

***

## Part VIII — Technology Readiness and Cross-Pathway Comparison

### 8.1 Technology Readiness by Sub-Challenge

| Sub-challenge | Status (2026) | TRL | Key Bottleneck |
|---|---|---|---|
| SOL heat flux width physics (ITER) | Well characterized empirically (~1 mm); gyrokinetics predicts ~6 mm | 5–6 (extrapolation) | Which extrapolation holds for ITER/DEMO? |
| Plasma detachment (tokamak) | Demonstrated at up to ~2/3 ITER P\(_{sep}\)/R (AUG) | 5–6 | Compatibility with high-confinement core at full P\(_{sep}\)/R |
| X-point radiator | ~95% dissipation (AUG); JET DT control 2025 | 4–5 | Robust control at reactor power; disruption risk |
| Alternative divertor config (ADC) | MAST-U: L-mode results 2025; higher-power campaign 2028 | 4 | Engineering integration in reactor; high-power H-mode validation |
| Liquid-metal divertor | Loops and small devices; no reactor-heat-flux plasma test | 3 | Tritium retention, MHD flow, core contamination |
| ELM suppression via RMP | Demonstrated in non-burning plasmas | 5 | ITER pedestal conditions untested |
| ELM pacing via pellets | Demonstrated in present devices | 4–5 | DEMO-relevant frequency and reliability |
| ELM-free regimes (QCE, QH, I-mode, NT) | Demonstrated on several machines; MAST-U QH/I-mode 2025–26 | 4 | Combination with detachment and reactor pedestal |
| Disruption mitigation (SPI) | ITER design maturing | 5 | DEMO energy scale undemonstrated |
| W7-X island divertor detachment | Detached ~28 s; 360 s / 1.8 GJ long pulse (2025) | 5 | Scaling to ~350 MW reactor power |
| Water-cooled DEMO target | HHF mock-ups 500 × 20 MW m\(^{-2}\) at 130 °C | 4–5 | CuCrZr embrittlement at DEMO neutron dose |
| He-cooled DEMO divertor target | HEMJ prototypes ~10 MW m\(^{-2}\); dropped from EU baseline | 3–4 | Small margin, pumping power |
| IFE first wall at 1–10 Hz | No rep-rate test | 1–2 | Cyclic fatigue; ~10\(^{9}\)–10\(^{10}\) shot lifetime |

### 8.2 Pathway Comparison

| Challenge Element | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| Unmitigated q\(_{\perp,target}\) | ~150 MW m\(^{-2}\) (DEMO); q\(_\parallel\) >10 GW m\(^{-2}\) (SPARC)[^3][^8][^34] | Lower (island geometry spreads load), but poorly constrained | Pulsed: per-shot surface energy deposition, not a steady flux |
| ELM problem | Critical — ~100 MJ natural ELMs in DEMO[^10]; need ≥10× reduction or ELM-free regime | Largely absent in optimised stellarators | Absent (no plasma pedestal) |
| Disruption risk | Severe — GJ-class thermal + runaway electrons[^12] | No current-driven disruptions; radiative collapse possible | Absent |
| Detachment approach | Impurity seeding, XPR, ADC | Island divertor; impurity seeding at W7-X[^13] | N/A — gas/liquid protection, chamber radius |
| Wall material limit | W at ~5–10 MW m\(^{-2}\)[^1][^11] | Same W limit; 3D distribution more complex | Ablation/fatigue dominates — no steady-state limit |
| Long-pulse evidence (2025) | WEST 1337 s, EAST 1066 s (low power)[^40] | W7-X 360 s / 1.8 GJ[^41] | None at rep-rate |
| Progress maturity | MAST-U ADC results 2025 (L-mode); SPARC ~2027; DTT ~2032; ITER DT 2039 | W7-X detachment demonstrated[^23]; physics gap to reactor remains | IFE first wall unsolved at rep-rate |

***

## Part IX — Open Research Questions and Analysis Entry Points

### Plasma Detachment and Impurity Seeding

- **Q1.1**: Can simultaneous ≥96% radiated power fraction and H-mode confinement quality factor \(H_{98} \geq 1.0\) be maintained in DEMO-like conditions (\(P_{sep}/R > 15\) MW m\(^{-1}\)) without unacceptable core impurity accumulation? What is the minimum attainable impurity concentration at the plasma core for the Ne/Ar seeding levels required?
- **Q1.2**: What detachment control system (sensor type, actuator bandwidth, predictive control algorithm) is required to maintain stable detachment in a DEMO plasma with ~150 MW SOL power, where a loss of detachment event can heat the divertor from 5 MW m\(^{-2}\) to >30 MW m\(^{-2}\) in <1 second?[^10]
- **Q1.3**: How do the power dissipation mechanisms observed in MAST-U ADCs (MAR, MAD, EIR) scale from MAST-U conditions (~1.2 MW SOL power) to DEMO (~150 MW SOL power), particularly in terms of the neutral pressure required in the divertor volume and the associated pumping requirements?

### Advanced Divertor Configurations

- **Q2.1**: Can the Super-X or Elongated divertor geometry demonstrated in MAST-U (spherical tokamak, aspect ratio ~1.8) be integrated into a conventional tokamak with aspect ratio ~3–4 (DEMO, ITER-like) while retaining >\(F_R = 1.5\) total flux expansion and sufficiently long divertor legs? What is the plasma volume penalty?
- **Q2.2**: What is the maximum P\(_{SOL}\) at which MAST-U ADC detachment benefits persist in H-mode plasmas with DEMO-relevant pedestal pressures? Does the factor of ~18.5× heat flux reduction observed in L-mode at 1.2 MW SOL power hold in H-mode at the higher powers available after the MAST-U enhancement programme (sixth campaign, planned 2028)?[^3][^39]
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

Of all five fusion challenges, power exhaust has seen some of the most rapid experimental progress in 2024–2026. The MAST Upgrade Super-X divertor results — an 18.5× heat flux reduction with improved detachment stability and core-edge compatibility (L-mode, ~1 MW SOL power), combined with the first demonstration of active exhaust control in an ADC — together with ~95% dissipation via the X-point radiator on AUG and its 2025 extension to JET DT plasmas, demonstrate that the physics community has identified several credible solution pathways. W7-X's stable detachment and its 2025 360 s / 1.8 GJ discharge, and the 1000-s-class WEST and EAST pulses, show that long-pulse operation with actively cooled tungsten components is achievable at modest power.[^23][^17][^3][^36][^37][^40][^41]

However, three major uncertainties remain that could reverse this optimism: First, ADC and XPR benefits must be validated at full DEMO-relevant SOL power (~150 MW) and P\(_{sep}\)/R rather than the ~1–15 MW range studied to date — and the next facilities able to do this (DTT, ITER) slipped to the early-to-late 2030s. Second, ELM suppression and disruption avoidance must be demonstrated to work in a burning plasma environment (where the alpha-particle drive, pedestal characteristics, and real-time diagnostic access differ fundamentally from current experiments) — and the consequences of failure are irreversible material damage rather than a plasma collapse requiring reflattening. Third, the reactor divertor must survive neutron irradiation: the water-cooled W/CuCrZr target retained for EU DEMO has a narrow temperature window and reduced margin once irradiated, so the plasma must keep the target heat flux well below the unirradiated qualification level with high reliability, pushing against the boundary of demonstrated core-edge compatibility. For IFE, the chamber-wall problem is essentially untested at rep-rate.[^2][^11][^47]

The power exhaust challenge therefore occupies a unique position among fusion's barriers: its physics has been largely understood and promising solutions have been experimentally demonstrated, but its engineering realization at reactor scale remains the frontier — and the consequences of insufficient progress are directly machine-limiting.

***

## Risk Assessment (November 2026)

### Risk register

| ID | Risk | Pathway(s) | Likelihood | Impact on schedule (years) / on feasibility | Early indicator | Mitigation |
|---|---|---|---|---|---|---|
| EX-1 | SOL power width at ITER/DEMO scale follows the empirical ~1 mm Eich scaling rather than the wider gyrokinetic (~6 mm) prediction, keeping required dissipation at ≥95% | Tokamak | high | +0–3 yr if ADC/XPR work; raises DEMO P\(_{sep}\)/R design risk | ITER early-operation and high-B\(_p\) λ\(_q\) measurements (2034+); SPARC λ\(_q\) at ~12 T (2027–2029) | Design for ~1 mm; ADC/XPR; higher core radiation; flux expansion margin |
| EX-2 | ≥95% dissipation (detachment/XPR) is incompatible with H\(_{98}\) ≈ 1 burning core at DEMO P\(_{sep}\)/R (confinement loss, dilution, radiative collapse) | Tokamak, Stellarator | med | +5–10 yr (redesign to larger R / lower power density); worst case reduces economic feasibility | AUG/JET/DTT integrated scenarios; ITER Q = 10 with seeding (2039+) | Alternative divertors widening the window; Ar/Ne mixes; ELM-free regimes; larger machine |
| EX-3 | Super-X/ADC benefits measured in MAST-U L-mode at ~1 MW do not survive at high-power H-mode or cannot be integrated in a conventional-aspect-ratio reactor (coil, volume, maintenance) | Tokamak | med | +3–5 yr for ADC-dependent designs (STEP, compact pilots) | MAST-U 6th campaign (2028); DTT phase 3 (late 2030s) | Keep conventional+XPR fall-back; double-null designs; moderate shaping |
| EX-4 | Facility slippage: DTT (first plasma slipped 2028→2032), ITER DT (2039), MAST-U high power (2028) delay reactor-relevant exhaust evidence | Tokamak | high | +2–5 yr on gate evidence | Official baseline updates; DTT TF-coil delivery; ITER assembly milestones | Use SPARC, JT-60SA, EAST/BEST, KSTAR in parallel; modelling validation |
| EX-5 | Irradiated W/CuCrZr divertor targets have too short a life (embrittlement, cracking, recrystallisation, erosion) → frequent cassette exchange and low availability | Tokamak, Stellarator | med | +3–8 yr (needs fusion-neutron qualification, e.g. IFMIF-DONES); availability penalty | IFMIF-DONES/fission irradiation data; HHF testing of irradiated mock-ups | W-composite/Cu-composite heat sinks; low design heat flux; fast remote handling; liquid metals |
| EX-6 | Unmitigated ELMs or ELM-control failure in ITER/DEMO-class pedestal (RMP/pellets ineffective at low collisionality, q\(_{95}\) = 3) | Tokamak | med | +2–5 yr (scenario change, ITER research plan) | ITER RMP/pellet results (2034+); multi-machine ELM-free regime data | ELM-free regimes (QCE, QH, I-mode, NT, XPR); design margins |
| EX-7 | Disruptions/runaway electrons damage tungsten first wall and divertor in burning-plasma tokamaks; required disruption rate not achieved | Tokamak | med | +2–6 yr; component replacement campaigns; licensing/availability impact | ITER SPI performance; disruption predictor transfer between machines | SPI; ML-based avoidance; RE mitigation; sacrificial limiters |
| EX-8 | Stellarator island divertor does not scale to ~300+ MW: 3D heat-flux hot spots, island movement with beta/bootstrap current, insufficient space for divertor and blanket | Stellarator | med | +5–10 yr; may force larger device | W7-X high-power OP2.x results; private pilot divertor designs and tests | Configuration optimisation for divertor robustness; current control; larger aspect ratio |
| EX-9 | Liquid-metal divertor fails (tritium retention, Li/Sn core contamination, MHD flow instabilities) — removing the main "lifetime-unlimited" option | Tokamak, Stellarator | med | 0 yr on baseline (option loss only); removes upside of ~3–5 yr | Tokamak Energy/HIDRA flowing-Li tests; DTT liquid-metal phase | Keep solid-W baseline; vapour-box / capillary systems |
| EX-10 | IFE dry first wall fails cyclic fatigue/ablation at 10\(^9\)–10\(^{10}\) shots; liquid/thick-liquid walls incompatible with beam propagation, rep-rate or chamber clearing | Laser ICF | high | +5–15 yr; may block laser IFE power plants | Surrogate X-ray/ion load tests; first rep-rated pilot chamber data | Large chamber radius; gas protection; thick-liquid FLiBe walls; replaceable wall modules |
| EX-11 | No rep-rated high-yield source to test IFE chambers before a pilot plant (integration risk; first test = pilot) | Laser ICF | high | +5–10 yr (iteration loops at pilot scale) | Driver rep-rate milestones (≥1 Hz at ≥ MJ class) | Staged pilots; surrogate test stands; conservative first-of-kind chamber |
| EX-12 | Compact high-field tokamaks (SPARC/ARC, q\(_\parallel\) > 10 GW m\(^{-2}\)) cannot transfer SPARC's inertially cooled sweep solution to steady state | Tokamak (compact) | med | +3–7 yr for compact-tokamak FPPs | SPARC divertor tile damage and seeding results (2027–2030) | Long-leg/X-point target divertors; liquid metals; lower field/power density |

### Gate definition

**Gate (power exhaust, used for the model parameters below):** the gate year is the first calendar year in which, in at least one device of the given pathway, a power-exhaust solution — a divertor for magnetic confinement, or a chamber first wall/protection system for laser IFE — is **demonstrated experimentally** with all of the following at once:

1. **Reactor-relevant power density**: tokamak P\(_{sep}\)/R ≥ ~15 MW m\(^{-1}\) (or equivalent parallel heat flux q\(_\parallel\) ≥ ~1–5 GW m\(^{-2}\) upstream); stellarator separatrix power per unit divertor-target length/area equivalent to ≥ ~50% of a reactor (HELIAS-class) design value; laser IFE ≥ ~50 MJ-class yields at ≥ 1 Hz with chamber radius and per-shot wall fluence of a power-plant design.
2. **Long-pulse operation**: steady target heat flux ≤ ~5–10 MW m\(^{-2}\) (or IFE wall temperature/ablation within design) maintained for ≥ 1000 s (MCF) or ≥ 10\(^6\) consecutive shots (IFE), with active cooling and controlled transients (no unmitigated ELMs; disruption/RE mitigation demonstrated).
3. **Compatibility with a burning core**: achieved simultaneously with a core meeting the pathway's burning-plasma requirements (Q ≥ ~5 or alpha-heating-dominated, H\(_{98}\) ≈ 1 or stellarator equivalent; IFE target gain of the power-plant design), without unacceptable fuel dilution or impurity accumulation.
4. **Acceptable lifetime**: evidence (in-situ fluence plus irradiated-component data) that the exhaust components reach a replacement cycle compatible with ≥ ~70% plant availability (order ≥ 2 full-power years for divertor cassettes or wall modules).

Partial demonstrations (e.g. SPARC at high q\(_\parallel\) for ~10 s, WEST/EAST 1000 s at low power, W7-X at a few MW) count as indicators, not as the gate. In practice the gate is most likely passed in a DEMO-class or pilot-plant device (or in ITER Q = 10 long-pulse operation plus irradiation data).

### Model parameters

These are **calibrated expert judgments** by the report author, grounded in the evidence collected in this report (facility schedules as of Nov 2026, demonstrated exhaust performance, TRLs). They are not outputs of a formal model. Years are calendar years of the gate defined above, conditional on the gate being reached at all; the last column gives the separate probability that the pathway never reaches the gate by 2100 because power exhaust is a show-stopper for it.

| Pathway | P0 | P10 | P50 | P90 | P100 | P(never by 2100, show-stopper) | Rationale |
|---|---|---|---|---|---|---|---|
| Tokamak | 2033 | 2039 | 2047 | 2062 | 2090 | 0.07 | Physics solutions (detachment, XPR, ADC) exist at reduced power; ITER Q = 10 with W divertor (DT 2039+), DTT (2032+) and Chinese/private pilots (BEST, ARC-class) could combine power density and burning core in the 2040s; component lifetime under neutrons is the long pole. Earliest case needs a private compact pilot to succeed in the early 2030s. |
| Stellarator | 2036 | 2042 | 2052 | 2070 | 2100 | 0.12 | No ELMs/disruptions and good W7-X detachment, but no burning stellarator exists; reactor island-divertor scaling and space are unvalidated; depends on private pilots (2030s) or a European DEMO-type stellarator (2050s). |
| Laser ICF | 2038 | 2045 | 2056 | 2078 | 2110 | 0.22 | Gate requires a rep-rated high-yield chamber, which cannot be tested before a pilot plant; first-wall fatigue at 10\(^9\)–10\(^{10}\) shots is untested; liquid/gas-protected walls plausible but immature. |

**Coupling to other challenges** (suggested Spearman rank correlation of this challenge's gate year with the other gate years):
- **Plasma burning performance: ρ ≈ +0.55.** The gate requires a burning core; the same devices (ITER, pilots) deliver both, and core-edge integration is a joint problem. Stellarator +0.5, Laser ICF +0.6 (yield and chamber loads are coupled).
- **Materials qualification: ρ ≈ +0.6.** The lifetime criterion depends on irradiated W/CuCrZr (or IFE wall) data from IFMIF-DONES and pilot plants; slow materials qualification delays this gate almost one-to-one.
- **Tritium/breeding: ρ ≈ +0.3.** Weaker coupling via shared blanket/divertor space, tritium retention in PFCs and liquid-metal options; stronger for laser IFE (+0.4) where liquid-wall and breeder are often the same FLiBe/Li system.
- **Driver/magnets/steady-state: ρ ≈ +0.45.** The long-pulse criterion requires steady-state magnets, current drive (tokamak) or rep-rated drivers (IFE, ρ ≈ +0.6); high-field magnets also raise q\(_\parallel\) (compact tokamaks).
- **Discrete events**: (i) liquid-metal divertor success in a high-power tokamak/stellarator test by 2035: p ≈ 0.12, effect −3 to −5 yr on tokamak/stellarator gate and lifetime risk largely removed; (ii) ITER/SPARC measure λ\(_q\) significantly wider than Eich (gyrokinetic branch): p ≈ 0.2, effect −2 to −4 yr (tokamak); (iii) setback — reactor-level dissipation proves incompatible with H-mode confinement in ITER/DTT integrated scenarios: p ≈ 0.15, effect +6 to +10 yr (tokamak) and push towards larger devices; (iv) setback — irradiated divertor target lifetime < 1 full-power year: p ≈ 0.2, effect +4 to +8 yr (tokamak, stellarator); (v) IFE dry-wall fatigue failure in first pilot chamber: p ≈ 0.35, effect +6 to +12 yr (Laser ICF).

***

## Changelog (2026-11)

- Header date changed to "November 2026 update".
- **Parallel vs. perpendicular heat flux**: clarified that ~150 MW m\(^{-2}\) is the unmitigated *perpendicular target* heat flux for EU DEMO; the parallel heat flux is several GW m\(^{-2}\) (DEMO) and >10 GW m\(^{-2}\) (SPARC, Kuang et al. 2020). Corrected the target heat-flux formula in §1.1 (the old version gave ~6 GW m\(^{-2}\) with its own inputs).
- **λ\(_q\)**: Eich scaling gives ~1 mm (not 2 mm) for ITER; added the gyrokinetic ~5.9 mm prediction (Chang et al. 2017) as a key uncertainty.
- **P\(_{sep}\)/R for ITER**: corrected 150/6.2 ≈ 24 to ~100/6.2 ≈ 16 MW m\(^{-1}\), consistent with the table.
- **Dissipation record**: added AUG X-point radiator ~95% dissipation (Bernert 2021) and JET DT XPR control (Bosman 2025); the "best 85%" statement was outdated.
- **MAST-U**: the 18.5× result is from Verhaegh et al., *Communications Physics* (May 2025), obtained in **L-mode at ~1.2 MW SOL power**; the *Nature Energy* paper (Kool et al., Sep 2025) covers control and transients. Added fifth campaign (2025–26) and that the high-power sixth campaign is planned for 2028 (previous text implied >10 MW from 2026).
- **ELM fluence**: the "0.5 MJ limit" is an energy *density* (MJ m\(^{-2}\)), not an energy; added ITER edge-melt limit ~0.15 MJ m\(^{-2}\) (Gunn et al. 2017) and SPARC parallel ELM fluence 11–34 MJ m\(^{-2}\).
- **Disruption energies**: DEMO poloidal magnetic energy corrected from "50–100 GJ" to a few GJ; RE energies softened.
- **He-cooled divertor**: the ~1 MW m\(^{-2}\) limit in Maviglia 2021 applies to the He-cooled first wall, not the divertor; He-cooled divertor concepts were designed for ~10 MW m\(^{-2}\) and dropped from the EU baseline; EU DEMO targets use ~130–150 °C, ~5 MPa water (not 250–300 °C).
- **New content**: Italian DTT (first plasma slipped to July 2032 per 2025 IAEA poster; first TF coil May 2025), SPARC exhaust strategy and status, WEST 1337 s and EAST 1066 s (2025), W7-X 360 s / 1.8 GJ and 43 s triple-product record (2025), ITER 2024 baseline (W wall, DT 2039), negative triangularity, XPR, liquid-metal divertors (Tokamak Energy/HIDRA), NIF 8.6 MJ (2025) and IFE chamber context. Stellarator "no ELMs" statement softened.
- Not verifiable and therefore not used: specific chamber designs of private IFE companies; quantitative MAST-U fifth-campaign results (not yet peer-reviewed).

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

34. [Divertor heat flux challenge and mitigation in SPARC (Kuang et al., J. Plasma Phys. 2020)](https://eprints.whiterose.ac.uk/166979/1/divertor_heat_flux_challenge_and_mitigation_in_sparc.pdf) - Unmitigated peak parallel heat flux >10 GW/m²; parallel ELM fluence ~11–34 MJ/m²; ~1 Hz strike-point sweep.

35. [Gyrokinetic projection of the divertor heat-flux width from present tokamaks to ITER (Chang et al., Nucl. Fusion 57, 116023, 2017; arXiv)](https://arxiv.org/abs/1701.05507) - XGC1 projects λq ≈ 5.9 mm for ITER vs ≤1 mm from empirical scaling.

36. [X-point radiation, its control and an ELM suppressed radiating regime at the ASDEX Upgrade tokamak (Bernert et al., Nucl. Fusion 2021)](https://infoscience.epfl.ch/record/284513) - Full detachment at ~95% dissipated power fraction; ELM suppression.

37. [X-point radiator control and its dynamics in ASDEX Upgrade and JET deuterium–tritium discharges (Bosman et al., Nucl. Fusion 65, 016057, 2025)](https://research.tue.nl/en/publications/x-point-radiator-control-and-its-dynamics-in-asdex-upgrade-and-je/)

38. [Novel 'Super-X' design shows major advantages in handling hot exhaust of fusion energy (DIFFER / EUROfusion news, 2025)](https://euro-fusion.org/member-news/differ/novel-super-x-design-shows-major-advantages-in-handling-hot-exhaust-of-fusion-energy/)

39. [UK's MAST Upgrade achieves record fusion plasma pressure (Innovation News Network, 10 Aug 2026)](https://www.innovationnewsnetwork.com/uks-mast-upgrade-achieves-record-fusion-plasma-pressure/72496/) - Fifth campaign (>1,100 discharges, 2025–2026); N-seeded Super-X double-null; QH-/I-mode; enhancement programme to 2027; sixth campaign 2028.

40. [WEST sets a new plasma duration record (CEA-IRFM, Feb 2025)](https://irfm.cea.fr/en/2025/02/west-sets-a-new-plasma-duration-record/) - 1337 s, 2.6 GJ, ~2 MW; surpasses EAST's 1066 s of 20 Jan 2025.

41. [Wendelstein 7-X sets new performance records in fusion research (IPP, 2025)](https://www.ipp.mpg.de/5532945/w7x) - 43 s triple-product record; 360 s plasma with 1.8 GJ energy turnover.

42. [ITER Baseline 2024 press conference summary (ITER Organization, July 2024)](https://iter.org/sites/default/files/media/2024-07/baseline_press_conference_summary_july-2024_b.pdf) - Start of Research Operation 2034; DT 2039; tungsten first wall.

43. [DTT reaches milestone with first toroidal magnet completed (EUROfusion / ENEA, 2025)](https://euro-fusion.org/member-news/enea/dtt-reaches-milestone-with-first-toroidal-magnet-completed/)

44. [DTT overview poster, 30th IAEA Fusion Energy Conference (2025)](https://conferences.iaea.org/event/392/contributions/35648/attachments/19722/36216/POSTER%20OV.pdf) - First plasma July 2032 (as indexed; page access restricted at time of writing).

45. [The role of the Divertor Tokamak Test facility in the Italian and European magnetic fusion programs (Zonca and DTT Team, ICPP 2022 abstract)](https://www.afs.enea.it/zonca/CNPS/Activities/meetings/seminars/ICPP2022_Abstract_Zonca+DTT_Team.pdf) - 6 T, R = 2.19 m, 5.5 MA, ~45 MW; staged heating; liquid-metal divertor options.

46. [Ion orbit modelling of ELM heat loads on ITER divertor vertical targets (Gunn et al., Nucl. Mater. Energy 12, 75–83, 2017)](https://doaj.org/article/e51037080ae24d069974e80cfb8be682) - Edge-melt avoidance requires ELM surface energy density < 0.15 MJ/m².

47. [Target concepts for DEMO: results (IAEA Technical Meeting on Divertor Concepts, 2019)](https://conferences.iaea.org/event/192/contributions/15224/attachments/8341/11009/18-Target_concepts_for_DEMO_results_visca.pdf) - EU DEMO targets: water at 130–140 °C, 50 bar; HHF test results.

48. [Characterization of the ELM-free Negative Triangularity Edge on DIII-D (Nelson et al., 2024, arXiv)](https://arxiv.org/html/2405.11082v1)

49. [Advanced Exhaust Solutions and Liquid Metal PFCs for Tokamak Energy's Fusion Pilot Plant (APS DPP 2025)](https://meetings-archive.aps.org/dpp/2025/gm12/12)

50. [National Ignition Facility – FY2025 (LLNL annual report)](https://annual.llnl.gov/fy-2025/national-ignition-facility-2025) - 8.6 ± 0.45 MJ on 7 April 2025 from 2.08 MJ laser energy (gain 4.13).

51. [SPARC (tokamak) — Wikipedia (secondary source for 2026 assembly status)](https://en.wikipedia.org/wiki/SPARC_(tokamak))

52. [World record for WEST (DIFFER news, 2025)](https://www.differ.nl/news/world-record-WEST) - WEST 1337 s, 25% above EAST's record set weeks earlier.
