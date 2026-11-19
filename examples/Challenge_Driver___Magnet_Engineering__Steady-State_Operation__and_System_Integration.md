# Nuclear Fusion — Deep Dive: Challenge 5
## Driver & Magnet Engineering, Steady-State Operation, and System Integration

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — June 2026; reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps gate DR and the deployment, licensing and funding branches to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

Challenge 5 is the integration challenge: having solved (or sufficiently mitigated) plasma stability, materials damage, tritium self-sufficiency, and power exhaust, the fusion reactor must still function as a continuously operating engineering system. This requires three interdependent capabilities that are individually demanding and collectively undemonstrated at reactor scale: (1) **steady-state or quasi-continuous high-performance plasma operation** maintained for weeks to months without disruptions or performance degradation; (2) **magnet engineering** — superconducting coil systems that reliably sustain multi-tesla fields for 30-year plant lifetimes in a neutron-activated environment; and (3) for ICF, a **high-efficiency high-repetition-rate driver** capable of delivering reactor-grade laser energy at 10 Hz continuously for decades, plus a target factory producing half a million precision targets per day.

These challenges are distinct from the plasma physics challenges covered in prior reports. They are not primarily about understanding how fusion works — the physics is largely established. They are about whether the engineering systems that enable fusion to work continuously and economically can be built and operated at reactor scale. The convergence of recent milestones — DIII-D and EAST demonstrating simultaneously high density (\(f_{Gr} > 1\)) and high confinement (\(H_{98y2} \approx 1.5\)), EAST holding a 1,066-second H-mode plasma (2025; "fully non-inductive" **[unconfirmed 2026-11]**), W7-X reaching a new stellarator triple-product record over 43 seconds, CFS's SPARC TF magnets validated by DOE, and NIF achieving ignition 10 times with a record yield of 8.6 MJ — provides the strongest set of proof-points this challenge has ever seen. Nevertheless, the gap between what has been demonstrated and what a power plant requires remains large and should not be understated.[^1][^2][^3][^4][^5][^6][^7]

***

## Part I — Steady-State Tokamak Operation

### 1.1 Why Steady-State Matters

A pulsed tokamak — one that operates inductively, driving its plasma current via a central solenoid transformer — faces a fundamental limitation: the volt-second capacity of the solenoid is finite. ITER's central solenoid provides approximately 277 V·s, sustaining a plasma current of 15 MA for roughly 400–600 seconds per pulse. A commercial tokamak running on 20-minute pulses would require mechanical cycling of the entire thermal and structural system every 20 minutes — inducing fatigue in all in-vessel components and blanket modules, preventing steady tritium breeding and recovery, and making constant availability virtually impossible.[^8]

A fully **steady-state tokamak** drives 100% of its plasma current by non-inductive means: a combination of the self-generated **bootstrap current** (arising from the pressure gradient in the plasma) and externally driven currents from neutral beam injection (NBI) and radio-frequency (RF) heating systems. This eliminates the solenoid constraint but requires:[^9][^10]
- Plasma pressure (normalized beta \(\beta_N\)) high enough to generate a large bootstrap current fraction (\(f_{bs} \geq 50\%\))
- Efficient current drive systems (lower hybrid LHCD, electron cyclotron ECCD, neutral beams) to supply the remaining 50% of current non-inductively
- Simultaneous achievement of high confinement (\(H_{98y2} \geq 1\)), high density (\(f_{Gr} \approx 1\)), and high bootstrap fraction — all requirements that act against each other in standard H-mode plasmas

### 1.2 The High-\(\beta_p\) Reactor Scenario: 2024 Breakthroughs

The most critical unresolved question in tokamak plasma physics for reactor design was whether simultaneous \(f_{Gr} > 1\) (density above the Greenwald limit) and \(H_{98y2} > 1\) (above-standard H-mode confinement) could be achieved. Most compact reactor designs (SPARC ARC, K-DEMO, EU DEMO high-\(\beta_N\) scenario) require both simultaneously — an operating point that had never been experimentally verified.[^11]

In 2024, a landmark Nature paper reported that DIII-D achieved **stable plasmas with \(f_{Gr} \approx 1.2\) simultaneously with \(H_{98y2} \approx 1.5\)** in the high-\(\beta_p\) (high poloidal beta) scenario. The underlying physics mechanism — density-gradient amplification of turbulence suppression at high \(\beta_p\) through formation of a large-radius internal transport barrier (ITB) — was confirmed by predict-first simulations on both DIII-D and EAST. This is a seminal result: it demonstrates that the "uncharted area" of reactor-relevant operation is physically accessible, resolving a decade-long controversy over whether simultaneous high density and high confinement was achievable or fundamentally self-contradictory.[^6][^7]

In parallel, the **EAST tokamak** in China — operating with a full tungsten lower divertor since 2022 — has pushed long-pulse fully non-inductive H-mode operation to new milestones:[^5]
- 2025: repeatable long-pulse operation (LPO) with H-mode edge in fully non-inductive conditions, sustained for **1,066 seconds** (17.8 minutes) — the longest fully non-inductive H-mode ever achieved
- 2024 KSTAR: **102 seconds** of high-performance LPO in its newly installed W-shaped tungsten divertor — demonstrating tungsten wall compatibility with long-pulse high-performance operation[^5]

These records, while far below the continuous operation needed by a power plant, represent genuine physics demonstrations that each individually would have been considered near-impossible a decade ago. The critical remaining step is extending these plasmas from minutes to hours, then days, then continuous — a challenge that shifts from plasma physics to engineering systems (superconducting magnet performance, tritium fuel cycle, wall conditioning, remote maintenance).

In April 2026, the EAST team reported the **DTP (Detached divertor and Turbulence-dominated Pedestal) regime** — the first demonstration of simultaneous partial divertor detachment, ELM-free H-mode, and high pedestal performance sustained on a minute timescale in a metal-wall environment. This is directly relevant to the DEMO integrated operating scenario, where steady-state operation must combine core performance, exhaust management, and ELM suppression simultaneously.[^12]

### 1.3 Current Drive Systems for DEMO: Efficiency Requirements

Sustaining the non-inductive current in a DEMO reactor (~15–20 MA) requires current drive systems whose power consumption must be minimized. The wall-plug-to-plasma current drive efficiency is characterized by \(\gamma_{CD} = n_e I_{CD} R / P_{CD}\) (units: 10\(^{20}\) A W\(^{-1}\) m\(^{-2}\)). DEMO-scale physics calculations require:[^13][^14]

- **ECCD (Electron Cyclotron Current Drive)**: peak efficiencies of \(\gamma_{CD} \approx 0.4 \times 10^{20}\) A W\(^{-1}\) m\(^{-2}\) achievable at frequencies ~230–290 GHz by exploiting top-launch geometry for absorption by high-energy electrons. Gyrotron sources at DEMO frequencies are at TRL 4–5; development of multi-MW units at 240+ GHz is ongoing[^14][^13]
- **LHCD (Lower Hybrid Current Drive)**: highest demonstrated non-inductive efficiency in existing tokamaks (\(\gamma_{CD} \approx 0.5–0.8\)); however, at ITER and DEMO plasma densities, lower hybrid waves are strongly absorbed at the plasma periphery, limiting penetration to the core. This "density limit" for LHCD has been partially overcome in advanced scenarios but remains a fundamental constraint at \(n_e > 5 \times 10^{19}\) m\(^{-3}\)[^15][^16]
- **Neutral Beam Current Drive (NBCD)**: most versatile and demonstrated current drive method; ITER uses 1 MeV negative ion beams at 33 MW; for DEMO, beam energies of 500–1000 keV and powers of 30–50 MW are needed for current profile control; ion source development for 1 MeV beams is at TRL 5, with ITER prototype sources approaching specifications[^17]

For a fully non-inductive DEMO with \(f_{bs} = 60\%\) and 40% of current supplied by ECCD/LHCD/NBI, the total current drive power recirculated internally is approximately **50–80 MW** — representing 10–15% of total fusion power, a non-negligible recirculation fraction that directly impacts plant electricity output.

### 1.4 SPARC and ARC: The Compact High-Field Approach

Commonwealth Fusion Systems (CFS) has pursued a distinct strategy: rather than optimizing for steady-state at moderate field (as ITER/DEMO), use **very high magnetic field** (20 T at coil, 12.2 T on axis) made possible by HTS magnets to achieve high fusion power density in a compact machine. Higher field raises both plasma pressure and bootstrap current at smaller device size, potentially enabling near-full bootstrap operation at lower plasma current:[^18][^1]

- SPARC was approximately **75% complete** in April 2026; first plasma is now targeted for **2027**, with Q > 1 to follow as soon as possible **[corr. 2026-11]** (was: first plasma late 2026, net energy early 2027)[^19][^20][^18]
- First of 18 superconducting TF magnets was installed in SPARC in January 2026; the plan to install all 18 by the end of summer 2026 slipped **[corr. 2026-11]** (secondary reporting)[^18]
- ARC, the 400 MW commercial pilot plant targeting grid connection in the early 2030s, is planned for Chesterfield County, Virginia[^18]
- CFS has raised approximately **$3 billion** in private capital since 2018[^1]

If SPARC achieves its Q > 1 goal in 2027, it will be the first fusion device to demonstrate net energy gain from a magnetically confined plasma — and the first concrete proof-point for the compact high-field approach. The ARC concept proposes a novel **demountable magnet** design: the HTS coils can be disassembled and reassembled, allowing remote replacement of the first wall and blanket without the months-long in-vessel robotics operations needed for permanently wound coils in ITER/DEMO. This demountable design is specifically aimed at solving the maintenance availability challenge identified above.[^8]

***

## Part II — Superconducting Magnet Engineering

### 2.1 Why Magnets Are the Engineering Linchpin

Magnetic confinement fusion requires sustaining magnetic fields of 5–13 T (on-axis in the plasma) continuously over the reactor lifetime. This is only economically feasible with superconducting electromagnets; resistive copper coils at DEMO scale would consume more electrical power than the plant produces. The two candidate technologies are:

- **Low Temperature Superconductors (LTS)**: Nb\(_3\)Sn and NbTi, operating at 4 K; ITER's 18 TF coils use Nb\(_3\)Sn Cable-In-Conduit Conductors (CICC) reaching 11.8 T at the conductor; well-established manufacturing[^8]
- **High Temperature Superconductors (HTS)**: REBCO (Rare Earth Barium Copper Oxide) tapes operating at 20–50 K; can achieve fields well above 20 T; significantly higher critical current density at high field than LTS; developed primarily for the compact tokamak approach[^21][^1]

### 2.2 CFS SPARC HTS Magnet Milestones

The CFS/MIT SPARC magnet programme has produced the most important magnet engineering milestones in fusion since ITER conductor qualification:

**2021 — TFMC (Toroidal Field Model Coil)**:[^22]
- Demonstrated a sustained magnetic field of **>20 tesla** — setting a world record for HTS fusion-grade magnets
- Proved that the SPARC TF coil design can reach and sustain the field required for net energy fusion in a compact tokamak
- The result was described as providing "a clear path to fusion power for the first time"[^22]

**2024 — CSMC (Central Solenoid Model Coil)**:[^23]
- Successfully built and tested the CSMC, proving REBCO HTS performance under pulsed (ramping) current conditions, directly replicating the operating mode of the SPARC central solenoid
- Key test results: ramp rates, stored energy, quench performance, and structural integrity all met SPARC requirements[^23]
- CSMC complements the TFMC by validating both steady DC (TF coils) and pulsed (CS coil) HTS magnet technologies

**2025 — DOE Milestone Validation**:[^1]
- DOE's Milestone-Based Fusion Development Program independently validated CFS's full-scale production TF magnets against acceptance tests
- CFS received $8 million — the largest single milestone payment in the DOE programme to date[^1]
- Production magnets are in serial manufacturing; the same design will be used in the ARC power plant[^1]
- CFS has also completed **Paschen testing** of SPARC's insulated HTS magnets at 21 kV under fusion-relevant vacuum conditions, qualifying the insulation system for SPARC operations[^24][^25]

The comprehensive HTS magnet qualification programme — spanning from individual REBCO tape testing through pancake/layer testing through full coil acceptance testing — represents the most rigorous fusion magnet qualification campaign ever executed outside ITER.[^25]

### 2.3 HTS Magnet Challenges for Commercial Fusion

Despite these milestones, several engineering challenges for long-duration commercial operation remain:[^26][^21][^1]

**Quench protection**: An HTS magnet quench (sudden loss of superconductivity) in a 20 T coil at SPARC stores ~3–6 GJ of magnetic energy. Unlike LTS magnets (where propagation of normal zones is fast, enabling dump into resistors), HTS quenches propagate extremely slowly — a "silent quench" can develop in a local region and burn through the coil before detection unless the protection system fires. SPARC uses a novel detection scheme based on voltage monitoring and coil current sharing, validated in the CSMC campaign. At ARC scale, quench protection design for demountable joints under repeated thermal cycling remains an open engineering challenge[^1]

**Radiation tolerance**: REBCO tape is significantly more sensitive to radiation than Nb\(_3\)Sn. At neutron fluences above ~10\(^{22}\) n m\(^{-2}\), critical current degradation begins in REBCO; at 10\(^{23}\) n m\(^{-2}\), the material approaches end-of-life. The magnet shielding design (first wall + breeding blanket + vacuum vessel + coil case) must reduce the fluence at the coil below these limits for the plant lifetime. For SPARC, the shielding requirement drives the minimum blanket thickness and reduces the achievable TBR (as discussed in Challenge 3). For DEMO with LTS ITER-style coils, radiation tolerance is less critical but long-term helium accumulation in the Nb\(_3\)Sn conductor from residual fast neutron flux remains unvalidated over 30-year plant lifetimes[^27]

**Joint engineering (demountable HTS)**: ARC's demountable magnet design requires electrical joints between HTS REBCO tapes at the coil assembly plane that must carry ~50–80 kA with joint resistance below ~1 n\(\Omega\) (to limit resistive heating during operation) while surviving thousands of thermal cycles from 300 K (room temperature disassembly) to 20 K (operating temperature). The joint resistance requirement and thermal cycling tolerance have been demonstrated in laboratory settings but not at production scale or at the operational cycle count expected over a plant lifetime[^8]

**Stellarator coil complexity**: The non-planar, three-dimensionally shaped HTS coils required for a stellarator reactor (W7-X type HELIAS) present a geometric winding challenge qualitatively beyond SPARC's D-shaped coils. The possibility of winding REBCO tape around tight 3D curvatures without exceeding the critical bend radius of the tape is a significant manufacturing challenge. A 2022–2024 study exploring REBCO-based precise-geometry high-field stellarators demonstrated that the concept is physically feasible, but no reactor-grade 3D HTS coil has been manufactured[^26]

***

## Part III — IFE: Driver Efficiency and the Target Factory

### 3.1 The Laser Driver Efficiency Problem

The NIF laser uses flashlamp-pumped Nd:glass amplifiers — a technology derived from the pulsed high-energy laser tradition. At NIF's laser-to-target energy conversion efficiency, the overall **wall-plug-to-laser efficiency is <1%**. This is catastrophically low for an energy plant:[^28]

The basic IFE power balance requires:

\[\eta_{driver} \cdot G \geq \frac{1}{\eta_{therm}} + \epsilon\]

where \(\eta_{driver}\) is wall-plug driver efficiency, \(G\) is target energy gain, \(\eta_{therm}\) is thermal-to-electric conversion efficiency (~0.40 for a Brayton cycle), and \(\epsilon\) is the net electricity margin that makes the plant economical. For \(\eta_{therm} = 0.40\) and a minimum margin of \(\epsilon = 0.1\), the equation gives:

\[\eta_{driver} \cdot G \geq \frac{1}{0.40} + 0.1 = 2.6\]

NIF's current best result achieves target gain \(G = 4.13\) (8.6 MJ from 2.08 MJ laser input), but with wall-plug efficiency ~0.006 (0.6%), giving \(\eta_{driver} \cdot G \approx 0.025\) — a factor of **100× below the minimum economical threshold**. Even the NIF Enhanced Yield Capability (EYC) upgrade, targeting >30 MJ from a 2.6 MJ laser, would give \(G \approx 12\) — still \(\eta_{driver} \cdot G \approx 0.072\), still 35× below threshold.[^2][^3]

The resolution to this deficit requires a **completely different laser architecture**: diode-pumped solid-state lasers (DPSSL) in which semiconductor diode pump sources replace flashlamps. DPSSLs can achieve wall-plug efficiencies of **10–18%** with the right gain media:[^29][^30]

- The LLNL Mercury laser programme (completed ~2010) demonstrated a DPSSL operating at **10 Hz, >50 J, for >300,000 shots** — proving out average-power DPSSL operation at all core subsystems (gas-cooled slabs, diode pump arrays, thermal management)[^30]
- The LIFE (Laser Inertial Fusion Energy) conceptual design proposed a 384-beamline DPSSL system delivering 2.2 MJ at 16 Hz with **18% wall-plug efficiency**, using Yb:S-FAP or Yb:YAG gain medium — achieving \(\eta_{driver} \cdot G \approx 18\% \times 76 = 13.7\), just above economic threshold at assumed target gain of 76 (at 3.7 MJ laser energy)[^31][^32][^30]

**Current challenges for DPSSL drivers**:[^33][^34][^29]
- Laser diode costs must fall from current ~$0.50/Watt to **$0.05–0.07/Watt** for a LIFE-class plant to be economically viable — a 7–10× cost reduction requiring industrial diode manufacturing at unprecedented scale
- Yb-based gain media must operate under ~6 kW/cm\(^2\) of pump fluence with thermal distortion managed by gas cooling; the Mercury laser validated this, but only at 1/200 the power level of a LIFE plant
- Average power of ~1–10 MW per beamline must be sustained for plant lifetime (30 years, ~10\(^{10}\) shots) — comparable to industrial laser requirements but at higher peak power than any current laser product
- Alternative driver concepts: **GaN-based blue diode lasers** with target efficiencies >20% are in early development; krypton fluoride (KrF) gas lasers offer potentially better beam smoothing for direct drive; heavy-ion accelerator drivers (for indirect drive) remain theoretically attractive but are at TRL 1–2[^28]

### 3.2 NIF's Record Progress and the Gap to IFE

NIF has achieved ignition 10 times as of mid-2026, with target gains improving substantially:[^35][^2]
- December 2022: Q = 1.54 (3.15 MJ from 2.05 MJ)[^36]
- April 2025: **Q = 4.13 (8.6 MJ from 2.08 MJ)** — current record[^3][^2]
- The key enabling innovation was **continuous gradient doping** of the high-density carbon capsule, eliminating the hard density interface between doped and undoped ablator layers that seeded hydrodynamic instabilities[^2]
- NIF's Enhanced Yield Capability (EYC) project, which received CD-0 approval in September 2024 and completed its conceptual design review in June 2025, will boost NIF's maximum energy from 2.2 MJ to 2.6 MJ, enabling predicted fusion yields >30 MJ (Q > 12); LLNL's May 2026 overview shows ~40 MJ for EYC **[update 2026-11]**[^3]

Even so, the gap between NIF (single shot, ~6 hours between shots, <1% wall-plug efficiency) and a commercial IFE plant (10 Hz, 18% efficiency) spans a factor of **~60,000** in shot rate. NIF's FY2025 refurbishment effort — replacing 192 integrated optical modules whose precision optics suffered accumulated damage — illustrates the fundamental optics challenge: sustaining the precision optical surfaces at IFE rep-rate over a plant lifetime.[^3]

### 3.3 Target Factory: 500,000 Targets Per Day

An IFE power plant operating at 10 Hz requires **~500,000–864,000 targets per day**. Each target is a cryogenic precision component with a ~2 mm diameter spherical capsule, a DT ice layer uniformly distributed to within ±1 µm surface roughness, and a hohlraum (for indirect drive) machined to tolerances of ~5–10 µm:[^37][^38]

Current target fabrication at NIF produces targets in **multi-day processes** at costs of approximately **$2,500–$10,000 per target**. A power plant requires target delivery at less than **$0.30 per target** (allocating 10% of electricity revenue to fuel). This implies a cost reduction of four orders of magnitude — comparable to the reduction required to make the first semiconductor chips economically viable for consumer electronics, a comparison that implicitly reveals both the potential and the risk.[^39][^37]

Key technical challenges for high-throughput target fabrication:[^38][^37]
- **CVD deposition rate**: high-density carbon capsules are made by plasma-assisted CVD at ~1 µm/hour — a 30-layer capsule takes days; multi-reactor parallel production required at scale
- **DT layering**: cryogenic DT ice layer must form a uniform film on the inner capsule wall; quality is verified by shadowgraphy and X-ray phase contrast imaging; uniform filling requires isothermal conditions to ±0.1 mK and vibration isolation, complicating integration with a continuous production line
- **Injection and tracking**: targets must be accelerated from ~5 m away and arrive at the chamber center at **100–200 m/s** with **<50 µm position accuracy** (to within one beam width for indirect drive, <10 µm for direct drive) — while maintaining cryogenic temperatures of ~18 K during the injection process[^38][^39]
- **Target tracking and beam steering**: at 10 Hz, targets arrive every 100 ms; each must be independently tracked by fast cameras and its position communicated to a beam-steering system that redirects 192 laser beams to the target position in real time, correcting for injection trajectory errors[^39]

General Atomics has demonstrated prototype target injection at relevant velocities and cryogenic temperatures over short distances, and the recent NIF target metrology advances (4Pi integrated metrology system enabling rapid screening) are directly applicable to production-line quality control. But no integrated target factory has been built at any fraction of the required throughput.[^39][^2]

***

## Part IV — Stellarator: The Steady-State Advantage and Engineering Challenge

### 4.1 W7-X Records and the Steady-State Demonstration

The stellarator's primary advantage over the tokamak is its intrinsic steady-state capability: no plasma current means no inductive drive, no current-drive power overhead, no disruption risk from current-driven MHD instabilities. W7-X was designed specifically to demonstrate reactor-relevant stellarator confinement in steady-state.[^40]

**2026 status of W7-X steady-state milestones**:[^41][^4][^42]
- **February 2023**: plasma maintained for >8 minutes with 1.3 GJ of coupled and decoupled energy — then-world record for stellarators[^4]
- **May 2025**: new world record triple product over a **43-second plasma duration**, with triple product (n·T·τ\(_E\)) matching the best values achieved in tokamak experiments — the first time a stellarator has competed with tokamak performance on this metric[^4]
- **OP2.3 campaign 2025**: stable, long-pulse detached plasma at 5 MW heating power sustained for **360 seconds** (6 minutes) — new energy input record of **1.8 GJ** — with feedback-controlled neon seeding maintaining radiation fraction ~85% and no impurity accumulation over the full duration[^41]
- **Goal**: 30-minute plasma pulse to demonstrate stellarator suitability for continuous operation; planned for OP3 campaign beginning September 2026 after one-year maintenance period **[unconfirmed 2026-11]** (conflicts with other reporting of campaigns OP2.4 in 2026 and OP2.5 in 2027)[^40][^4]

The 1.8 GJ energy input over 6 minutes at W7-X demonstrates that the actively cooled island divertor and first wall can sustain continuous reactor-like conditions without catastrophic events. This is qualitatively different from what any tokamak has demonstrated: W7-X plasmas terminate because experimenters choose to stop them, not because of a physics or engineering limit.[^40]

### 4.2 Stellarator-Specific Engineering for a Reactor

The engineering barriers for a stellarator DEMO are qualitatively different from a tokamak DEMO:[^43]
- **Coil manufacturing**: W7-X's 50 non-planar superconducting coils (NbTi/Nb\(_3\)Sn) each have unique 3D shapes requiring computer-controlled winding with sub-millimetre accuracy over a 2–3 m coil perimeter; a HELIAS reactor at 5× scale would need equivalent precision in coils 10× larger
- **Plasma optimization sensitivity**: the W7-X plasma equilibrium depends critically on the 3D coil geometry; coil position errors of >1 mm degrade confinement measurably. At reactor scale, thermal expansion, electromagnetic forces, and neutron-induced materials swelling must all be managed to maintain coil positions within similar tolerances
- **No existing stellarator at burning plasma scale**: W7-X heats plasmas to fusion-relevant temperatures (ion temperature ~3 keV) but at densities ~10× below reactor requirements and with auxiliary heating power only; no stellarator has ever operated in a DT burning plasma
- **Ignition physics**: whether a reactor-scale stellarator can reach ignition and operate stably in a self-heated burning plasma is not established; alpha-particle heating in a stellarator may be affected by alpha loss due to non-axisymmetric ripple transport, though W7-X's optimization was specifically designed to minimize this[^43]

***

## Part V — DEMO RAMI: Reliability, Availability, Maintainability, Inspectability

### 5.1 The Availability Target

A fusion power plant must achieve sufficient **availability factor** — the fraction of calendar time actually generating electricity — to be economically competitive. Estimates for DEMO's minimum required availability to demonstrate economic viability range from **30–60%**. Current fusion experiments have availability factors of ~10–20% (reflecting the research nature of their operation, frequent maintenance, and diagnostic campaigns).[^44]

The primary drivers of fusion plant unavailability:[^45][^44]
- **Planned maintenance outages**: blanket replacement (every ~4 fpy), divertor replacement (every 1–3 fpy), heating system maintenance, remote handling system servicing — all requiring months-long shutdowns
- **Unplanned disruptions and damage events**: any disruption causing first-wall or divertor damage triggers a remote inspection and potentially a repair campaign
- **Tritium plant downtime**: any major tritium system fault shuts down DT operation until resolved; the fuel cycle is on the critical path for all reactor operations
- **Magnet repair**: any quench causing a coil to normal-conducting state requires thermal cycling from 4–20 K to room temperature and back — a weeks-long process for large LTS coils; HTS demountable coils mitigate this for REBCO quenches but introduce joint reliability as a new concern

ITER's own RAMI analysis estimated an **availability target of 14% in the DT phase** — already a significant challenge for a device not optimized for availability. DEMO must achieve 2–4× higher availability in its first iteration.[^44]

### 5.2 DEMO Integrated Engineering: The Systems Integration Gap

No component of DEMO can be designed in isolation. The interconnections create a web of constraints:
- Higher TBR requires thicker blanket → less space for heating/CD systems → lower non-inductive current → more inductive operation → shorter pulses → lower availability
- Better ELM control via impurity seeding → higher impurity concentration → lower core performance → lower Q → more external power needed → higher recirculated fraction → lower net electricity output
- Larger divertor surface area for better heat exhaust → more port penetrations → lower TBR → harder tritium self-sufficiency
- Higher magnetic field for better confinement → stronger EM forces on coils → heavier structure → harder remote maintenance → lower availability

This systems-level coupling means that no single challenge can be "solved" without simultaneously worsening at least one other. DEMO's integrated design has been undergoing a continuous redesign cycle since the EU Pre-Conceptual Design (2014–2020) and conceptual design phase (2021–2026) as each subsystem optimization revealed conflicts with others. As of 2026, the EU DEMO project has not yet converged on a stable reference design that simultaneously satisfies all first-principles physics constraints, engineering requirements, and regulatory boundary conditions.[^46][^44]

***

## Part VI — Technology Readiness: Cross-System Summary

### 6.1 Technology Readiness Table

| Sub-challenge | Tokamak | Stellarator | Laser ICF | TRL Range |
|---|---|---|---|---|
| Steady-state high-performance plasma (\(f_{Gr}>1\), \(H_{98}>1\)) | Demonstrated transiently (DIII-D, EAST)[^6][^7] | Not applicable (no driven current) | N/A | 4–5 |
| Long-pulse non-inductive H-mode (>1000 s) | EAST 1066 s (2025)[^5] | Intrinsic; W7-X 360 s detached at 5 MW[^41] | N/A | 5–6 (stellarator) |
| High-field HTS magnets (>20 T) | CFS SPARC TF coils validated[^1][^22] | W7-X HTS stellarator concept studied[^26] | N/A | 6 (SPARC) |
| Demountable HTS joints at scale | Lab-scale only | Same | N/A | 3 |
| Current drive systems (ECCD, NBCD) | ITER-scale systems being built | Not required for steady-state | N/A | 5–6 |
| DEMO integrated operating scenario | Not demonstrated — design ongoing | HELIAS concept only | N/A | 2–3 |
| DPSSL at 10 Hz, >50 J (rep-rate) | N/A | N/A | Mercury: 300,000 shots at 50 J[^30] | 4–5 |
| DPSSL at 10 Hz, ~2 MJ (plant scale) | N/A | N/A | Concept only (LIFE)[^31][^30] | 2 |
| Target gain (Q > 1) | Never demonstrated in MCF device | Never demonstrated | NIF: Q = 4.13 (April 2025)[^2] | 9 (physics only) |
| Target factory at 500,000/day | N/A | N/A | Nonexistent[^37][^38] | 1–2 |
| DEMO RAMI ≥ 30% availability | Not demonstrated; design ongoing | Not demonstrated | N/A | 2 |

### 6.2 SPARC as the Imminent Decision Point

SPARC's first plasma (now targeted for 2027) and net energy demonstration (2027–2028) **[corr. 2026-11]** represent the most consequential fusion milestones in the near-term programme. A successful SPARC result will:[^19][^18]
- Confirm that compact high-field HTS tokamaks can reach burning plasma conditions
- Validate the REBCO HTS magnet performance in an integrated electromagnetic, thermal, and neutron environment
- Provide the first data on alpha-particle self-heating in a compact geometry
- Establish commercial confidence for private-sector and government investment in the ARC pilot plant

A failure (disruption damage, magnet quench, or missed Q target) would be a significant setback, but the physics basis for net energy at SPARC parameters is well-established by simulation and by the TFMC and CSMC magnet tests — the risk is predominantly engineering, not physics.

***

## Part VII — Open Research Questions and Analysis Entry Points

### Steady-State Plasma

- **Q1.1**: Can the high-\(\beta_p\) scenario (\(f_{Gr} > 1\), \(H_{98y2} > 1.3\), fully detached divertor, zero ELMs) demonstrated transiently at DIII-D and EAST be sustained for >1,000 seconds in a single discharge without performance degradation, wall conditioning issues, or fuel recycling instabilities? What minimum current drive power is required to maintain the current profile?
- **Q1.2**: Does the DTP regime demonstrated at EAST in 2026 extrapolate to DEMO-relevant heating power (150 MW) and plasma current (17 MA)? What transport mechanisms govern pedestal pressure in this turbulence-dominated, partially detached regime, and are they predictable by current gyrokinetic simulation codes?[^12]
- **Q1.3**: Can W7-X achieve the 30-minute plasma goal in OP3 (from September 2026) without exceeding heat loads on the actively cooled first wall or accumulating impurities to a plasma-quenching level? What is the lifetime of the CFC divertor targets under continuous 5 MW operation?[^40]

### Magnet Engineering

- **Q2.1**: What is the minimum demountable HTS joint resistance achievable at 50–80 kA and 20 K over 10,000 assembly-disassembly cycles, and does residual joint heating at this resistance level produce acceptable temperature non-uniformities in the REBCO tape during ARC operation?
- **Q2.2**: What is the cumulative radiation damage (fast neutron fluence, gamma dose) at the HTS coil location in SPARC after full DT operation, and does this agree with pre-experiment REBCO radiation tolerance models? This data — not yet available — is the single most important HTS magnet materials result needed for ARC design validation.
- **Q2.3**: Can REBCO tapes be wound around the tight 3D curvatures required for a reactor-scale HELIAS stellarator without exceeding the conductor's critical bend radius, and can coil positioning tolerances of ±0.5 mm be maintained over a 15 m coil perimeter in a radiation-activated environment?

### IFE Driver and Target Factory

- **Q3.1**: Can a DPSSL driver system achieve 18% wall-plug efficiency simultaneously with 2.2 MJ pulse energy at 16 Hz in a single integrated demonstration system? What is the required laser diode cost trajectory and what scale of diode production is needed to reach $0.07/W?
- **Q3.2**: What is the maximum achievable target gain at NIF following EYC upgrade (2.6 MJ laser energy), and does the continuous gradient doping innovation extrapolate linearly to higher laser energy, or are new target design challenges encountered at >10 MJ yield?
- **Q3.3**: Can an automated target filling, layering, and metrology line produce cryogenic DT targets with <1 µm RMS surface roughness and <50 µm capsule sphericity error at a throughput of 1,000 targets per hour (a prerequisite milestone for eventual 500,000/day factory design)? What is the dominant quality-limiting step — capsule fabrication, DT fill, or ice layer uniformity?

### DEMO Integration

- **Q4.1**: What is the minimum DEMO design that simultaneously satisfies all five challenge constraints (plasma stability + materials + tritium TBR > 1.05 + power exhaust < 5 MW m\(^{-2}\) + availability > 30%)? Does such a design exist within physically consistent constraints, and what is the minimum fusion power required for it to generate net electricity?
- **Q4.2**: What RAMI methodology should govern DEMO component replacement scheduling and how does blanket replacement frequency (currently driven by ~4 fpy dose limit) propagate through the plant availability budget? What availability factor is achievable given current RH technology TRL?

***

## Conclusion

Challenge 5 is the ultimate integration test: whether all the partial solutions to Challenges 1–4 can be assembled into a continuously operating, reliable, economically viable energy system. The milestones of 2024–2026 represent the most concentrated set of positive results in fusion's history. The DIII-D/EAST plasma regime breakthrough eliminates the theoretical doubt about whether reactor-relevant operating points exist. W7-X's 360-second fully detached plasma demonstrates stellarator steady-state in a way that cannot be dismissed as a transient. CFS's DOE-validated HTS magnets in serial production mark the first time a fusion engineering component has moved from research prototype to manufactured product. NIF's April 2025 record of Q = 4.13 establishes that ICF ignition is not an edge-case anomaly but a reproducible physics regime.[^7][^6][^2][^41][^1]

Yet the magnitude of the remaining engineering gaps must be equally clearly stated. SPARC must demonstrate net energy to validate the compact high-field approach — and no fusion device has ever done this. A DEMO-class integrated system with the necessary RAMI performance has never been designed to a stable reference, let alone built. The IFE target factory is an entirely new industrial sector that needs to be invented, scaled, and costed. The time between today's milestones and a commercial fusion power plant — even under optimistic assumptions — is measured in decades, not years. The value of these milestones is not that they shorten the timeline dramatically; it is that they progressively close the space of physical unknowns, converting speculative engineering assumptions into validated design inputs.

The next decade — dominated by SPARC net energy results (2027), ITER Start of Research Operation (2034; DT from 2039) **[corr. 2026-11]**, W7-X 30-minute operation (OP3, 2026–2028), and the IFMIF-DONES materials data pipeline — will determine whether the integrated engineering pathway to commercial fusion is achievable within the century's first half.

---

## Review & Model Update (November 2026)

Scope and model architecture are described in the overview report. This section covers gate **DR**
(reactor-grade driver/magnets), the deployment chain (FID → demo → first commercial plant → ≥ 10 GWe) and the
funding and licensing branches, which this report's integration theme touches most.

### R.1 Currency and claim check

| ID | Location | Statement | Finding | Status |
|---|---|---|---|---|
| C5-01 | Part I 1.4, VI 6.2, Conclusion | SPARC first plasma "late 2026", net energy "early 2027" | First plasma now targeted for 2027 [R2] | corrected |
| C5-02 | Part I 1.4 | Remaining 17 TF magnets in H1 2026 | Slipped against the summer-2026 plan [R3] (secondary) | corrected |
| C5-03 | Conclusion | "ITER first plasma (2033)" | Baseline 2024: SRO 2034, DT 2039 [R1] | corrected |
| C5-04 | Part III 3.2 | NIF ten ignitions, 8.6 MJ, EYC 2.6 MJ / > 30 MJ | Confirmed; LLNL 2026 shows EYC at ~40 MJ [R15][R16] | confirmed / updated |
| C5-05 | Part IV 4.1 | W7-X OP3 from September 2026 | Conflicting campaign naming in other reporting; not re-verified | unconfirmed |
| C5-06 | Executive summary | EAST 1,066 s "fully non-inductive" | Not confirmed by the cited source | unconfirmed |
| C5-07 | Part III | IFE drivers: DPSSL, KrF, GaN | Updated: Xcimer's excimer prototype Phoenix has operated since June 2026 [R19] and has DOE milestone funding of USD 39.5 M [R18]. Inertia is building Thunderwall (10 kJ, 10 Hz, 10 %) [R17]. Focused Energy (direct drive, Biblis) raised USD 240 M [R21] | supplemented |
| C5-08 | Part V | Integration risks | Licensing and funding were not covered; added in R.3 | supplemented |

### R.2 Direct vs. indirect drive for this challenge

The driver gate has the largest split.
- **Indirect drive** must compensate for hohlraum coupling losses with higher gain and pays more per target.
  Diode-pumped solid-state lasers (e.g. Thunderwall) must reach ≥ 10 % wall-plug efficiency at 10 Hz [R17].
  Model: DR P50 2055, show-stopper 0.20.
- **Direct drive** can use excimer lasers (shorter wavelength, smoother illumination, gas optics) or DPSSL,
  and simpler, cheaper targets [R19][R21]. Model: DR P50 2050, show-stopper 0.12.
- Xcimer's two-beam "half-hohlraum" concept [R20] is a hybrid and is treated under direct drive.

### R.3 Licensing and funding branches (all pathways)

**Licensing.** All four pathways are licensed under radiation-protection or byproduct-material law, not
reactor law:
- **US:** NRC proposed rule under Part 30 (26 Feb 2026) [R5]; final rule targeted for Oct 2026, deadline
  31 Dec 2027 [R6][R7]; publication not confirmed on 3 November 2026. The rule also widens Part 51 environmental
  review for larger facilities [R32].
- **Tennessee:** first fusion-specific licence (Type One, 31 Aug 2026) [R8][R9].
- **Germany:** amendment of the Radiation Protection Act in the legislative process [R10][R11]; ReFus guidance
  in preparation [R12].
- **Indirect drive** carries an additional classification and export-control burden [R26][R27][R28].

**Funding.** The sector raised USD 4.48 bn in the 12 months to July 2026 (USD 14.24 bn since 2021) [R4].
- **Tokamak:** CFS (~USD 3 bn).
- **Stellarator:** Proxima (EUR 411 M; the EUR 1.2 bn federal share for Alpha is not yet committed [R13]);
  Type One (Series B USD 200 M [R14], secondary).
- **Indirect drive:** Inertia (USD 450 M [R17]).
- **Direct drive:** Focused Energy (USD 240 M [R21]); Xcimer (~USD 200 M + DOE [R18]).

Investor-implied commercialization probabilities are mostly below 20 % [R31].

| Pathway | FOAK licensing duration P0/P10/P50/P90/P100 (y) | P(major licensing delay) | P(licensing blocked at scale) | FOAK capital need P0/P10/P50/P90/P100 (USD bn) | Base P(funding abandoned) |
|---|---|---|---|---|---|
| Tokamak | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.02 | 3 / 5 / 8 / 15 / 30 | 0.05 |
| Stellarator | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.02 | 4 / 6 / 10 / 18 / 35 | 0.10 |
| Direct Drive | 2 / 3 / 4 / 6 / 10 | 0.30 | 0.03 | 3 / 4 / 7 / 14 / 30 | 0.12 |
| Indirect Drive | 2 / 3 / 5 / 7 / 12 | 0.40 | 0.05 | 4 / 6 / 10 / 20 / 40 | 0.12 |

Funding mechanics in the model:
- `<p>_fund_fail` has p = base × (need / USD 8 bn) / funding climate × (1 + max(TRL7 year − 2045, 0)/40),
  clipped to [0.01, 0.95].
- `<p>_fin_verz` = clip(2 y × need / 8 / climate, 0, 15).

Licensing in the model:
- `<p>_lic_jahre` = duration + delay (if the delay event occurs; 1/2/4/7/12 y) + fission-like-regime years
  (if `g_regime` occurs).

### R.4 Mapping to the risk model (gate DR and deployment)

- **DR** — MCF: plant-scale magnet system plus ≥ 1 h (stellarator ≥ 30 min) high-power operation. ICF: ≥ 10 % wall-plug at 5–10 Hz plus a target line of ≥ 10⁴ targets per day.

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | DR – Driver/magnets | 2030 / 2036 / 2045 / 2062 / 2085 | 0.05 | `tok_dr`, `tok_f_dr` |
| Stellarator | DR – Driver/magnets | 2032 / 2039 / 2050 / 2068 / 2095 | 0.07 | `stl_dr`, `stl_f_dr` |
| Direct Drive | DR – Driver/magnets | 2034 / 2040 / 2050 / 2072 / 2095 | 0.12 | `dir_dr`, `dir_f_dr` |
| Indirect Drive | DR – Driver/magnets | 2037 / 2042 / 2055 / 2078 / 2098 | 0.20 | `ind_dr`, `ind_f_dr` |

Deployment parameters (all pathways):
- FID lead before TRL 7: 3/5/8/10/12 y.
- Construction: tokamak, direct and indirect drive 4/5/7/10/15 y; stellarator 5/6/8/11/16 y.
- Demo → first commercial plant: 4/6/8/12/18 y, +4 y if the demo's availability is below 50 %
  (p = 0.65 tokamak, 0.55 stellarator, 0.70 ICF).
- Ramp-up to ≥ 10 GWe: 6/8/12/18/30 y × funding-climate factor.

Pathway scenarios touching DR:
- `alpha_finanziert` / `alpha_ohne_bund` (stellarator DR ±4–5 y, funding base 0.06 / 0.16);
- `excimer_bestaetigt` (direct drive DR −4 y, show-stopper 0.08);
- `eyc_erfolg` (indirect drive DR −4 y).

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
- **[R26]** National Research Council, 'An Assessment of the Prospects for Inertial Fusion Energy' (2013). <https://uwnxt.nationalacademies.org/read/18288/chapter/2>
- **[R27]** 'Nonproliferation and fusion power plants', arXiv:2207.14348 — direct-drive ICF largely declassified by 1974; export controls for indirect drive. <https://arxiv.org/pdf/2207.14348>
- **[R28]** Physics Today, 'Inertial fusion energy gets a nod' (2013) — proliferation concern greater for indirect than direct drive. <https://physicstoday.aip.org/news/inertial-fusion-energy-gets-a-nod>
- **[R31]** Spitzer et al., 'Is Fusion Too Late?', MIT CEEPR WP 2025-20 (Oct 2025) — investor-implied commercialization probabilities mostly < 20 %. <https://ceepr.mit.edu/workingpaper/is-fusion-too-late-how-investors-value-its-role-in-a-decarbonized-europe/>
- **[R32]** Orrick, 'NRC proposed fusion rule further clarifies path for commercial deployment' (Mar 2026) — tritium/activation reporting, Part 51 environmental review. <https://www.orrick.com/en/Insights/2026/03/NRC-Proposed-Fusion-Rule-Further-Clarifies-Path-for-Commercial-Deployment>

---

## References

1. [US Department of Energy Validates Commonwealth Fusion Systems ...](https://cfs.energy/news-and-media/us-department-of-energy-validates-commonwealth-fusion-systems-completion-of-magnet-tech/)

2. [Target Breakthrough Enabled Fusion Record at NIF](https://lasers.llnl.gov/news/target-breakthrough-enabled-fusion-record-nif) - A major innovation in target design, a process known as continuous gradient doping, has contributed ...

3. [National Ignition Facility - 2025 - Annual Report](https://annual.llnl.gov/fy-2025/national-ignition-facility-2025) - Lawrence Livermore National Laboratory supports stockpile stewardship through a wide range of experi...

4. [10 years of Wendelstein 7-X | Max-Planck-Institut für ...](https://www.ipp.mpg.de/5585948/10jahre_w7x)

5. [PowerPoint Presentation](https://conferences.iaea.org/event/392/contributions/36141/attachments/20114/36116/Litaudon-IAEA-Poster%20vf.pdf)

6. [Turbulence suppression at extreme plasma densities on DIII-D and ...](https://www.osti.gov/biblio/2567805) - Recent high-poloidal-beta (high-βP) experiments on DIII-D and EAST have made coordinated breakthroug...

7. [A high-density and high-confinement tokamak plasma regime for fusion energy](https://www.nature.com/articles/s41586-024-07313-3.pdf)

8. [1](https://www.burningplasma.org/activities/uploads_tec/FESAC%20High%20Field.pdf)

9. [Microsoft Word - Luce.doc](https://fusion.gat.com/pubs-ext/APS09/Luce.pdf)

10. [FT/1-1](https://www-pub.iaea.org/MTCD/Meetings/FEC2006/ft_1-1.pdf)

11. [A high-density and high-confinement tokamak plasma regime for fusion energy](https://www.nature.com/articles/s41586-024-07313-3) - A stable tokamak plasma has been demonstrated with a high plasma density and a high energy confineme...

12. [Tokamak regime sustains stable fusion plasma for one minute while ...](https://phys.org/news/2026-04-tokamak-regime-sustains-stable-fusion.html) - For the first time, a research team has demonstrated, in a metal-wall environment, a plasma regime t...

13. [Electron-Cyclotron-Current-Drive Efficiency in DEMO ...](https://pure.mpg.de/rest/items/item_2144786/component/file_2144785/content)

14. [[PDF] Technological and Physics Assessments on Heating and Current ...](https://pure.mpg.de/rest/items/item_2148823/component/file_2148822/content)

15. [Study of Lower Hybrid Current Drive for the Demonstration Reactor](https://www.sciencedirect.com/science/article/pii/S1738573316000632)

16. [[PDF] Simulation of Lower Hybrid Current Drive for DEMO](https://pdfs.semanticscholar.org/c5b5/d3bf69f1cf66dce7573752f09e89cc1289b8.pdf)

17. [Neutral beams for a demonstration fusion reactor (DEMO ...](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/RSIvol85p02B319.pdf)

18. [Commonwealth Fusion Systems Advances SPARC Tokamak and ...](https://energynews.pro/en/commonwealth-fusion-systems-advances-sparc-tokamak-and-plans-400-mw-arc-plant) - Commonwealth Fusion Systems advances its SPARC demonstration tokamak and plans the 400 MW ARC commer...

19. [SPARC Fusion Reactor Nears First Plasma as 2026 Assembly ...](https://www.linos.ai/science/sparc-fusion-reactor-2026-net-energy-milestone/) - Explore CFS SPARC Fusion's timeline to 2026 plasma and 2027 net energy. Understand key hurdles, prog...

20. [SPARC Fusion at 75% Complete — Why Hyperscalers Care](https://porrittinc.com/sparc-just-hit-75-complete-now-the-hyperscalers-are-watching/) - Commonwealth Fusion’s SPARC tokamak is 75% built. Why hyperscale data center operators are watching ...

21. [Tests show high-temperature superconducting magnets ... - MIT News](https://news.mit.edu/2024/tests-show-high-temperature-superconducting-magnets-fusion-ready-0304) - A comprehensive study of high-temperature superconducting magnets built by MIT and Commonwealth Fusi...

22. [Groups Announce Successful Test to Advance Fusion Energy](https://www.powermag.com/groups-announce-successful-test-to-advance-fusion-energy/) - A company working to bring fusion energy technology to market joined with a group from the Massachus...

23. [Commonwealth Fusion Systems Magnet Success ... - PR Newswire](https://www.prnewswire.com/news-releases/commonwealth-fusion-systems-magnet-success-propels-fusion-energy-toward-the-grid-302308013.html) - /PRNewswire/ -- Commonwealth Fusion Systems (CFS) announced today it successfully built and tested a...

24. [Fri-Af-Po.11-06: Paschenization and testing of the SPARC ...](https://indico.cern.ch/event/1431972/contributions/6420219/contribution.pdf)

25. [[PDF] [Plenary] Qualification of the HTS Magnets for SPARC - CERN Indico](https://indico.cern.ch/event/1431972/contributions/6420856/contribution.pdf)

26. [High-temperature superconducting strong-field stellarator with precise ...](https://www.sciencedirect.com/science/article/pii/S2666675823001650)

27. [[PDF] Materials for DEMO and Reactor Applications - Boundary Conditions ...](https://pure.mpg.de/rest/items/item_2242719_4/component/file_2461513/content)

28. [Blue Laser Fusion Tech Profile | Fusion Energy News](https://www.fusionenergynews.com/directory/north-america/blue-laser-fusion) - Read the full engineering profile, confinement mechanics, and fuel cycle analysis for Blue Laser Fus...

29. [[PDF] Diode-Pumped Solid State Lasers for Inertial Fusion Energy - OSTI](https://www.osti.gov/servlets/purl/15013230) - Increase the efficiency of the DPSSL IFE driver to between 10 to 20%. • Reduce the cost of laser dio...

30. [Development of high energy and high average power diode pumped laser drivers for inertial fusion energy systems (Invited Paper)](https://spie.org/photonics-west/presentation/Development-of-high-energy-and-high-average-power-diode-pumped/13358-23) - View presentations details for Development of high energy and high average power diode pumped laser ...

31. [Compact, Efficient Laser Systems Required for Laser Inertial Fusion ...](https://www.ans.org/pubs/journals/fst/article-12325/)

32. [System study of a diode-pumped solid-state-laser driver for inertial fusion energy](https://www.osti.gov/biblio/102290) - The present a conceptual design of a diode-pumped solid-state-laser (DPSSL) driver for an inertial f...

33. [[PDF] Long-Wavelength Diode-Pumped Solid-State Lasers as Inertial ...](https://lasers.llnl.gov/sites/lasers/files/2023-11/payne-LLNL-IFE-workshop-2022.pdf) - The overall efficiency of the laser driver depends on both intrinsic spectroscopic properties of the...

34. [[PDF] Diode-pumped, solid-state laser (DPSSL) drivers for Inertial Fusion ...](https://arpa-e.energy.gov/sites/default/files/migrated/A05-Zuegel-FusionWorkshop_03-07-23.pdf) - Top-level requirements for IFE solid-state laser drivers. Page 5. 5. The Laser Inertial Fusion Energ...

35. [Achieving Fusion Ignition | National Ignition Facility & Photon ...](https://lasers.llnl.gov/science/achieving-fusion-ignition) - 4" data-caption="One of NIF’s key goals was to create self-sustaining thermonuclear fusion reactions...

36. [Igniting the future: Breakthroughs in inertial confinement Fusion](https://www.ifpilm.pl/en/media/gallery/18-news/swiatowe/2484-igniting-the-future-breakthroughs-in-inertial-confinement-fusion) - In December 2022, the National Ignition Facility (NIF) at Lawrence Livermore National Laboratory (US...

37. [A key challenge for inertial fusion energy (Journal Article) | OSTI.GOV](https://www.osti.gov/biblio/20783153) - Developing a commercial production process for 500,000 targets per day: A key challenge for inertial...

38. [[PDF] Target mass production for inertial fusion energy](https://lasers.llnl.gov/sites/lasers/files/2023-11/alexander-GA-IFE-workshop-2022-2.pdf) - Targets require high fabrication tolerance (~10 µm level), and large numbers if them are needed. (~5...

39. [[PDF] IFE TARGET FABRICATION AND INJECTION — ACHIEVING ...](https://fusion.gat.com/pubs-ext/MISCONF00/A23379.pdf)

40. [Wendelstein 7-X - Max-Planck-Institut für Plasmaphysik](https://www.ipp.mpg.de/w7x) - Wendelstein 7-X is the world's largest fusion device of the stellarator type. Its objective is to in...

41. [Development of long-pulse detached plasmas in the ...](https://www.aappsdpp.org/DPP2025/html/3contents/pdf/5715.pdf)

42. [[PDF] 2024 Updates and 2025 Objectives - Indico - EUROfusion](https://indico.euro-fusion.org/event/3130/contributions/12339/attachments/5855/10267/AWP2025_WPW7X_final.pdf) - Wendelstein 7-X is on the path to provide input for the decision on the next step stellarator and th...

43. [STELLARATOR FUSION REACTORS –– AN OVERVIEW](https://fire.pppl.gov/itc12_wobig_paper.pdf)

44. [[PDF] RAMI: the challenge of Fusion Nuclear Technologies](https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/NJOCCPR17_18540_submitted-4.pdf) - This paper summarizes the RAMI statistics in existing fusion machines, the RAMI approaches adopted i...

45. [Preliminary RAMI analysis of WCLL blanket and breeder systems](https://www.sciencedirect.com/science/article/abs/pii/S0920379615001660) - The main objective of these studies is to be able to evaluate the influence of different parameters ...

46. [Breeding Blanket concepts for the EU-DEMO Fusion Power ...](https://www.eventi.enea.it/images/presentazioni2024/2024_12_11_funfi_it/FUNFI-IT_Damico.pdf)
