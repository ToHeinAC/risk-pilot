# Nuclear Fusion — Deep Dive: Challenge 5
## Driver & Magnet Engineering, Steady-State Operation, and System Integration

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — November 2026 update*

***

## Executive Summary

Challenge 5 is the integration challenge: having solved (or sufficiently mitigated) plasma stability, materials damage, tritium self-sufficiency, and power exhaust, the fusion reactor must still function as a continuously operating engineering system. This requires three interdependent capabilities that are individually demanding and collectively undemonstrated at reactor scale: (1) **steady-state or quasi-continuous high-performance plasma operation** maintained for weeks to months without disruptions or performance degradation; (2) **magnet engineering** — superconducting coil systems that reliably sustain multi-tesla fields for 30-year plant lifetimes in a neutron-activated environment; and (3) for ICF, a **high-efficiency high-repetition-rate driver** capable of delivering reactor-grade laser energy at 10 Hz continuously for decades, plus a target factory producing half a million precision targets per day.

These challenges are distinct from the plasma physics challenges covered in prior reports. They are not primarily about understanding how fusion works — the physics is largely established. They are about whether the engineering systems that enable fusion to work continuously and economically can be built and operated at reactor scale. The convergence of recent milestones — DIII-D and EAST demonstrating simultaneously high density (\(f_{Gr} > 1\)) and high confinement (\(H_{98y2} \approx 1.5\)), EAST sustaining an RF-driven H-mode plasma for 1066 seconds (January 2025) and WEST a 1337-second plasma (February 2025), W7-X reaching a new stellarator triple-product record over 43 seconds, CFS's full-scale SPARC TF magnet validated under the DOE milestone programme, Tokamak Energy's Demo4 HTS magnet set reaching 11.8 T, and NIF achieving ignition 10 times with a record yield of 8.6 MJ — provides the strongest set of proof-points this challenge has ever seen. Nevertheless, the gap between what has been demonstrated and what a power plant requires remains large and should not be understated.[^1][^2][^3][^4][^5][^6][^7][^49][^50][^54]

**November 2026 status in brief.** The decisive near-term test has slipped by roughly a year: SPARC first plasma is now expected in 2027 rather than 2026, and by late September 2026 CFS reported 8 of 18 TF magnets installed (the company had said in January it expected all 18 by end of summer).[^51] ITER's 2024 re-baseline moved Start of Research Operation to 2034 and DT operation to 2039, at roughly €5 billion extra cost.[^47][^48] Capital is flowing at unprecedented scale (Proxima Fusion €411 M Series A2 in July 2026; Focused Energy ~$240 M Series A in May 2026; the planned $6 B TAE–Trump Media merger; UK £2.5 B over five years; German federal pledge of >€2 B to 2029), and offtake contracts now exist for plants that have not been built (Google 200 MW and Eni >$1 B from CFS's ARC; Microsoft from Helion's Orion).[^52][^53][^57][^62][^65][^67][^71][^72] Regulation has moved decisively towards proportionate, byproduct-material-style frameworks (US NRC proposed rule, February 2026; UK Energy Act 2023 s.156; German Radiation Protection Act route).[^68][^70][^72] None of these developments demonstrates a reactor-grade driver; they reduce regulatory and financing risk for first-of-a-kind (FOAK) plants while concentrating technical risk on a few imminent integrated tests.

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
- 20 January 2025: a steady-state H-mode plasma sustained for **1,066 seconds** (17.8 minutes) with ~3.05 GJ of injected heating energy, the plasma current being sustained essentially non-inductively by RF current drive — the longest H-mode ever achieved (the earlier 1,056 s EAST discharge of 2021 was not in H-mode). Reported operating parameters were modest relative to a reactor (density ≈ 60 % of the Greenwald limit)[^50][^5]
- 12 February 2025, **WEST** (CEA, France): a hydrogen plasma sustained for **1,337 seconds** (~22 minutes) with 2 MW of lower-hybrid power from a single antenna and ~2.6 GJ of injected and extracted energy — a duration record for tokamaks, though not in H-mode and at low power. CEA's stated next goal is ~10 MW for ~1,000 s.[^49] These records are primarily tests of actively cooled plasma-facing components, RF systems and control over long durations, not of reactor-grade performance
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

- SPARC was reported **~75% complete** in May 2026 (second vacuum-vessel half delivered). The original 2018 plan targeted operation in 2025; first plasma is now expected in **2027**, with Q > 1 attempted shortly afterwards[^19][^20][^18]
- The first of 18 TF magnets was installed in January 2026, when CFS expected all 18 by the end of summer 2026; by 22 September 2026 CFS reported **8 of 18** installed — a visible schedule-pressure indicator for FOAK magnet integration[^18][^51]
- ARC, a ~400 MW(e) plant targeting grid connection in the **early 2030s**, is planned in Chesterfield County, Virginia, with Dominion Energy providing site leasing and grid-connection support. Google agreed (June 2025) to buy 200 MW of ARC output, contingent on SPARC achieving Q > 1; Eni signed a second ARC PPA (September 2025) worth more than $1 billion[^18][^52][^53]
- CFS has raised close to **$3 billion** in private capital since 2018[^1]

If SPARC achieves its Q > 1 goal in 2027–2028, it will be the first fusion device to demonstrate net energy gain from a magnetically confined plasma — and the first concrete proof-point for the compact high-field approach. The ARC concept proposes a novel **demountable magnet** design: the HTS coils can be disassembled and reassembled, allowing remote replacement of the first wall and blanket without the months-long in-vessel robotics operations needed for permanently wound coils in ITER/DEMO. This demountable design is specifically aimed at solving the maintenance availability challenge identified above.[^8]

Note that SPARC is a pulsed (~10 s flat-top) inductive device: it will test HTS magnets, burning-plasma physics and Q > 1, but not steady-state current drive or reactor-relevant neutron fluence on the coils. ARC must therefore close the steady-state/long-pulse and magnet-lifetime parts of the gate largely without a dedicated intermediate step.

### 1.5 ITER's 2024 Re-Baseline: What It Means for Integration Risk

In July 2024 ITER presented a new baseline: **Start of Research Operation (SRO) in 2034** (with a more complete machine and ~27 months of research, replacing the former "First Plasma 2025" milestone), full magnetic energy in **2036**, and **DT operation from 2039** — a ~4-year slip of DT versus the 2016 baseline — at an estimated additional cost of about **€5 billion**. Causes cited include COVID-19, component quality problems (vacuum-vessel sector bevel non-conformities, thermal-shield cooling-pipe corrosion), regulator issues and over-optimistic planning for a first-of-a-kind project.[^47][^48] For this challenge, ITER is the reference data point for FOAK integration risk: a ~10-year cumulative slip and roughly a doubling-plus of cost over its history. Its long-pulse (400 s inductive, up to ~1,000 s hybrid, ~3,000 s steady-state goals), Nb\(_3\)Sn magnet and RAMI data now arrive in the late 2030s/2040s — after several private pilot plants plan to have operated.

***

## Part II — Superconducting Magnet Engineering

### 2.1 Why Magnets Are the Engineering Linchpin

Magnetic confinement fusion requires sustaining magnetic fields of 5–13 T (on-axis in the plasma) continuously over the reactor lifetime. This is only economically feasible with superconducting electromagnets; resistive copper coils at DEMO scale would consume more electrical power than the plant produces. The two candidate technologies are:

- **Low Temperature Superconductors (LTS)**: Nb\(_3\)Sn and NbTi, operating at 4 K; ITER's 18 TF coils use Nb\(_3\)Sn Cable-In-Conduit Conductors (CICC) reaching 11.8 T at the conductor; well-established manufacturing[^8]
- **High Temperature Superconductors (HTS)**: REBCO (Rare Earth Barium Copper Oxide) tapes operating at 20–50 K; can achieve fields well above 20 T; significantly higher critical current density at high field than LTS; developed primarily for the compact tokamak approach[^21][^1]

### 2.2 CFS SPARC HTS Magnet Milestones

The CFS/MIT SPARC magnet programme has produced the most important magnet engineering milestones in fusion since ITER conductor qualification:

**2021 — TFMC (Toroidal Field Model Coil)**:[^22][^78]
- On 5 September 2021 the no-insulation TFMC reached a peak field of **20 T** (not "20.8 T" or ">20 T") at ~20 K and ~40 kA, held for several hours — a record for a large-bore HTS fusion magnet. A deliberate open-circuit quench test in a later campaign produced localized damage that matched simulations; this was documented in the 2024 MIT/CFS analysis and informed SPARC quench-protection design[^21]
- Proved that the SPARC TF coil design can reach and sustain the field required for net energy fusion in a compact tokamak
- The result was described as providing "a clear path to fusion power for the first time"[^22]

**2024 — CSMC (Central Solenoid Model Coil)**:[^23]
- Successfully built and tested the CSMC, proving REBCO HTS performance under pulsed (ramping) current conditions, directly replicating the operating mode of the SPARC central solenoid
- Key test results: ramp rates, stored energy, quench performance, and structural integrity all met SPARC requirements[^23]
- CSMC complements the TFMC by validating both steady DC (TF coils) and pulsed (CS coil) HTS magnet technologies

**2025 — DOE Milestone Validation**:[^1]
- On 30 September 2025 CFS announced that an independent review panel under DOE's Milestone-Based Fusion Development Program had validated performance-test results of its **full-scale SPARC TF magnet** (CFS's third milestone in the programme)
- CFS received $8 million — described as the largest amount paid to any company in the programme (CFS is eligible for $15 million in the first budget period; the programme had $46 million appropriated for that period)[^1]
- Production magnets are in serial manufacturing; the same design will be used in the ARC power plant[^1]
- CFS has also completed **Paschen testing** of SPARC's insulated HTS magnets at 21 kV under fusion-relevant vacuum conditions, qualifying the insulation system for SPARC operations[^24][^25]

The comprehensive HTS magnet qualification programme — spanning from individual REBCO tape testing through pancake/layer testing through full coil acceptance testing — represents the most rigorous fusion magnet qualification campaign ever executed outside ITER.[^25]

**Other HTS magnet programmes (2025–2026)**:
- **Tokamak Energy (UK)**: in November 2025 its **Demo4** system — a complete set of HTS magnets in a tokamak configuration (14 TF limbs plus PF coils, ~7 MA-turns through the centre column) — reached **11.8 T at about −243 °C (30 K)**, with higher-field tests planned for 2026 (no published follow-up found as of this update). Demo4 is the first full HTS tokamak magnet set operated as a system, testing inter-coil forces and coupled quench behaviour[^54]
- **Proxima Fusion (Germany)**: raised a €411 M Series A2 in July 2026 (valuation ~€2.4 B), explicitly to scale HTS cable and non-planar magnet production for its **Alpha** demonstration stellarator (operation targeted ~2031 near Garching; total cost ~€2 B, with €400 M Bavarian commitment and a requested €1.2 B federal share not yet committed as of mid-2026)[^57][^79]
- **Type One Energy (US)**: stellarator developer with a TVA letter of intent (September 2025) for **Infinity Two**, a ~350 MW(e) plant at TVA's Bull Run site; the Infinity One prototype schedule has slipped (sources cite groundbreaking moving into 2027 and start-up ~2029)[^58]

**HTS tape supply and cost**: Fusion is now the dominant buyer of REBCO tape. A 2025 peer-reviewed perspective counts ~15 manufacturers worldwide with combined capacity above **~5,000 km/year (12 mm-equivalent)**, the top pulsed-laser-deposition producers supplying over half; SPARC alone needed on the order of **10,000 km of 4 mm tape**.[^55] Faraday Factory Japan reported capacity >1,000 km/yr (12 mm) and had delivered >8,000 km of tape to fusion by 2025.[^56] Price estimates remain wide and poorly documented: roughly **$100–300/kA·m** (at fusion-relevant 20 K, ~20 T conditions) today, against widely cited targets of ~$50/kA·m near-term and ~$10–20/kA·m long-term for economic fusion magnets.[^55] A fleet of ARC-class plants would need tape output roughly an order of magnitude above current global capacity, and supply is concentrated in a few firms in Japan, China, Russia/elsewhere, which is a geopolitical as well as a cost risk. Announced capacity expansions (some projecting tens of thousands of km/yr) are not confirmed output.

### 2.3 HTS Magnet Challenges for Commercial Fusion

Despite these milestones, several engineering challenges for long-duration commercial operation remain:[^26][^21][^1]

**Quench protection**: An HTS magnet quench (sudden loss of superconductivity) involves a TF system whose stored magnetic energy is of order several GJ for SPARC-class devices (a rough estimate from field and volume; no official figure was found). Unlike LTS magnets (where propagation of normal zones is fast, enabling dump into resistors), HTS quenches propagate extremely slowly — a "silent quench" can develop in a local region and burn through the coil before detection unless the protection system fires. SPARC uses a novel detection scheme based on voltage monitoring and coil current sharing, validated in the CSMC campaign. At ARC scale, quench protection design for demountable joints under repeated thermal cycling remains an open engineering challenge[^1]

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

Note that \(\eta_{driver} G \approx 2.6\) is only *engineering breakeven* — at that point ~96 % of the gross electricity is recirculated to the driver. An economically viable plant needs a recirculating fraction of ≲ 25 %, i.e. \(\eta_{driver} G \gtrsim 10\) (most IFE plant studies assume 10–15). NIF's current best result achieves target gain \(G = 4.13\) (8.6 MJ from 2.08 MJ laser input), but with wall-plug efficiency well below 1 % (~0.5–0.6 %; NIF draws ~300–400 MJ from the grid per shot), giving \(\eta_{driver} \cdot G \approx 0.025\) — a factor of **~100× below engineering breakeven and ~400× below an economic plant**. Even the NIF Enhanced Yield Capability (EYC) upgrade, targeting >30 MJ from a 2.6 MJ laser, would give \(G \approx 12\) — still \(\eta_{driver} \cdot G \approx 0.07\). NIF was never designed for efficiency; the relevant conclusion is that an IFE plant needs *both* \(G \gtrsim 50\)–100 and \(\eta_{driver} \gtrsim 10\) %.[^2][^3]

The resolution to this deficit requires a **completely different laser architecture**: diode-pumped solid-state lasers (DPSSL) in which semiconductor diode pump sources replace flashlamps. DPSSLs can achieve wall-plug efficiencies of **10–18%** with the right gain media:[^29][^30]

- The LLNL Mercury laser programme (completed ~2010) demonstrated a DPSSL operating at **10 Hz, >50 J, for >300,000 shots** — proving out average-power DPSSL operation at all core subsystems (gas-cooled slabs, diode pump arrays, thermal management)[^30]
- The LIFE (Laser Inertial Fusion Energy) conceptual design proposed a 384-beamline DPSSL system delivering ~2.2 MJ at ~16 Hz with **~18% wall-plug efficiency**, using Yb:S-FAP or Yb:YAG gain medium — with assumed target gains of order 60–80 this gives \(\eta_{driver} \cdot G \approx 11\)–14, just inside the economic window (the gain figures are design assumptions, not demonstrated values)[^31][^32][^30]

**Current challenges for DPSSL drivers**:[^33][^34][^29]
- Laser diode costs must fall from current ~$0.50/Watt to **$0.05–0.07/Watt** for a LIFE-class plant to be economically viable — a 7–10× cost reduction requiring industrial diode manufacturing at unprecedented scale
- Yb-based gain media must operate under ~6 kW/cm\(^2\) of pump fluence with thermal distortion managed by gas cooling; the Mercury laser validated this, but only at 1/200 the power level of a LIFE plant
- Average power of ~1–10 MW per beamline must be sustained for plant lifetime (30 years, ~10\(^{10}\) shots) — comparable to industrial laser requirements but at higher peak power than any current laser product
- Alternative driver concepts: **GaN-based blue diode lasers** with target efficiencies >20% are in early development; krypton fluoride (KrF) gas lasers offer potentially better beam smoothing for direct drive; heavy-ion accelerator drivers (for indirect drive) remain theoretically attractive but are at TRL 1–2[^28]

**Private driver programmes, status November 2026**:
- **Xcimer Energy (Denver, US)** — krypton-fluoride (KrF) excimer laser amplifiers (an ArF variant could not be confirmed from the sources reviewed) with stimulated-Brillouin-scattering pulse compression, aiming at low-cost, high-rep-rate direct drive. Its **Phoenix** prototype (described as the largest privately owned laser) began operation in June 2026 to demonstrate integrated amplification plus compression; **Anvil** (~200 kJ on target, two-sided) is slated for 2028 and **Vulcan** for ~2030–2031 (engineering-breakeven goal). In June 2026 DOE approved Xcimer's pre-conceptual **Athena** plant design (molten-salt chamber) under the milestone programme.[^60][^61] Excimer lasers have demonstrated rep-rate (Electra, 5 Hz) but wall-plug efficiencies of only a few percent at system level; the claimed ~10 % remains to be shown at scale
- **Focused Energy (Darmstadt/US)** — direct-drive, proton fast ignition; raised ~$240 M Series A (May 2026, RWE among investors) and plans the first laser fusion power plant at RWE's former **Biblis** nuclear site by the mid-2030s; in July 2026 the German research ministry selected Biblis as the national laser-fusion hub under "Fusion 2040"[^62][^77]
- **Marvel Fusion (Munich/US)** — short-pulse, nanostructured-target concept; co-funding the ~$150 M **ATLAS** laser facility at Colorado State University (groundbreaking October 2024; completion reported for late 2026), a science facility rather than a rep-rated driver[^63]
- **Pacific Fusion (US)** — not a laser: a modular pulsed-power (pulser) driver for magnetically driven implosions, >$1 B raised, targeting net facility gain by 2030; in 2026 it reported pulser-module results and joint experiments with Sandia simplifying the approach[^64]

None of these programmes has yet demonstrated a driver combining ≥10 % wall-plug efficiency, MJ-class energy and ≥5 Hz; the closest legacy data remain Mercury (DPSSL, 10 Hz, ~50 J) and NRL Electra (KrF, 5 Hz, ~hundreds of J).

### 3.2 NIF's Record Progress and the Gap to IFE

NIF has achieved ignition 10 times (the tenth on 1 October 2025, 3.5 MJ); a June 2026 LLNL presentation still lists the April 2025 shot as the yield record, with target gains improving substantially:[^35][^2][^76]
- December 2022: Q = 1.54 (3.15 MJ from 2.05 MJ)[^36]
- April 2025: **Q = 4.13 (8.6 MJ from 2.08 MJ)** — current record[^3][^2]
- The key enabling innovation was **continuous gradient doping** of the high-density carbon capsule, eliminating the hard density interface between doped and undoped ablator layers that seeded hydrodynamic instabilities[^2]
- NIF's Enhanced Yield Capability (EYC) project, which received CD-0 approval in September 2024 and completed its conceptual design review in June 2025, will boost NIF's maximum energy from 2.2 MJ to 2.6 MJ, enabling predicted fusion yields >30 MJ (Q > 12)[^3]

Even so, the gap between NIF (single shot, ~6 hours between shots, <1% wall-plug efficiency) and a commercial IFE plant (10 Hz, 18% efficiency) spans a factor of **~2 × 10\(^5\)** in shot rate (10 Hz versus one shot per ~6 hours; versus NIF's actual cadence of high-yield ignition shots — a few per year — the gap exceeds 10\(^7\)). NIF's FY2025 refurbishment effort — replacing 192 integrated optical modules whose precision optics suffered accumulated damage — illustrates the fundamental optics challenge: sustaining the precision optical surfaces at IFE rep-rate over a plant lifetime.[^3]

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
- **Next campaigns**: after a maintenance period (June 2025 to mid/August 2026), the IPP plan foresees **OP2.4 (August–December 2026)** and **OP2.5 (February–May 2027)**, targeting steady-state scenarios with T\(_i\) > 2.5 keV, radiated fraction > 80 % and detachment for > 60 s, and high-β (> 3 %) scenarios. Start of OP2.4 on schedule could not be confirmed as of this update[^59]
- **Long-term goal**: 30-minute plasma pulses at high heating power (up to ~18 GJ energy turnover) to demonstrate stellarator suitability for continuous operation; this is a multi-campaign goal and not a fixed date (the earlier version of this report wrongly placed it in an "OP3 from September 2026")[^40][^4]

The 1.8 GJ energy input over 6 minutes at W7-X demonstrates that the actively cooled island divertor and first wall can sustain continuous reactor-like conditions without catastrophic events. This is qualitatively different from what any tokamak has demonstrated: W7-X plasmas terminate because experimenters choose to stop them, not because of a physics or engineering limit.[^40]

### 4.2 Stellarator-Specific Engineering for a Reactor

The engineering barriers for a stellarator DEMO are qualitatively different from a tokamak DEMO:[^43]
- **Coil manufacturing**: W7-X has **50 non-planar and 20 planar superconducting coils, all NbTi** (operated at ~4 K, ~2.5–3 T on axis); the non-planar coils (five distinct shapes, about 3.5 m tall, ~6 t each) required winding and positioning to millimetre-level accuracy. A HELIAS-class reactor (major radius ~22 m versus 5.5 m) would need comparable relative precision in coils several times larger and at ~5–6 T on axis, which points to Nb\(_3\)Sn or HTS conductors. Private stellarator developers (Proxima, Type One, Thea Energy) are betting on HTS to shrink the machine — making 3D HTS coil manufacturing, quench protection and support structure the critical-path engineering risk for this pathway[^57][^58]
- **Plasma optimization sensitivity**: the W7-X plasma equilibrium depends critically on the 3D coil geometry; coil position errors of >1 mm degrade confinement measurably. At reactor scale, thermal expansion, electromagnetic forces, and neutron-induced materials swelling must all be managed to maintain coil positions within similar tolerances
- **No existing stellarator at burning plasma scale**: W7-X heats plasmas to ion temperatures of ~3 keV (a factor ~5 below reactor-relevant ~15 keV) at densities a few times below reactor requirements and at low β and with auxiliary heating power only; no stellarator has ever operated in a DT burning plasma
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

This systems-level coupling means that no single challenge can be "solved" without simultaneously worsening at least one other. DEMO's integrated design has been undergoing a continuous redesign cycle since the EU Pre-Conceptual Design (2014–2020) and conceptual design phase (2021–2026) as each subsystem optimization revealed conflicts with others. As of 2026, the EU DEMO project has not yet converged on a stable reference design that simultaneously satisfies all first-principles physics constraints, engineering requirements, and regulatory boundary conditions. European Commission planning (2025) places DEMO conceptual design completion by ~2030, engineering design in 2030–2040 and construction after 2040, i.e. EU DEMO electricity not before the 2050s; its schedule is coupled to ITER's DT results (2039+).[^46][^44][^75]

### 5.3 National Programmes, Regulation, Financing and Supply Chain (2025–2026)

**Public programmes**:
- **UK STEP** (spherical tokamak, West Burton, Nottinghamshire): the June 2025 Spending Review committed **£2.5 billion over five years** to UK fusion, of which ~£1.3 billion flows through UK Industrial Fusion Solutions/STEP delivery; engineering and construction partners were shortlisted in January 2025 with contracts to 2029. STEP targets operation around 2040, with construction starting in the early 2030s.[^71]
- **China**: the **BEST** compact superconducting tokamak in Hefei (aimed at Q > 1 in steady-state-oriented DT operation) targets completion by end-2027, with power-generation demonstrations around 2030; the state-owned **China Fusion Energy Co.** (CNNC subsidiary, registered capital ¥15 billion) was founded in July 2025 and in January 2026 announced burning-plasma experiments from 2027 and engineering-test-reactor design capability by 2030. CFETR remains the long-term DEMO-class step, with BEST effectively inserted ahead of it.[^73]
- **Germany**: the federal cabinet adopted a fusion action plan on 1 October 2025 with **more than €2 billion to 2029** (figures between €1.7 B and €2.4 B are cited depending on what is counted), the stated aim that the world's first fusion power plant be built in Germany, and continued regulation under the **Radiation Protection Act** rather than the Atomic Energy Act. Hubs followed in 2026 (laser-fusion hub at Biblis, July 2026).[^72][^77]
- **United States**: DOE issued a Fusion S&T Roadmap (October 2025; finalized June 2026) targeting commercial fusion power in the mid-2030s under a "Build–Innovate–Grow" strategy; the Milestone-Based Fusion Development Program has eight awardees, with milestone payments only on verified achievement (CFS, Xcimer and others have been validated on early milestones).[^74][^1][^60]
- **EU**: DEMO remains in conceptual design (see 5.2); EU-level strategy for private fusion is still being formulated.

**Regulation (licensing)**:
- **US**: the NRC published its proposed rule "Regulatory Framework for Fusion Machines" on 26 February 2026 (91 FR 9476), placing fusion under the **byproduct-material framework (10 CFR Part 30)** rather than the reactor framework (Part 50/52), with Agreement States able to license; comments closed 27 May 2026. NRC planning targeted a final rule in fall/October 2026, well before the NEIMA deadline of 31 December 2027; **publication of the final rule could not be confirmed as of 2 November 2026**.[^68][^69]
- **UK**: Energy Act 2023 s.156 (in force 10 September 2024) exempts fusion energy facilities from nuclear site licensing; regulation lies with the HSE and environmental regulators, and a National Policy Statement (EN-8) covers siting.[^70]
- **Germany**: Radiation Protection Act route (see above).
These frameworks lower the probability of fission-style licensing delays for FOAK fusion plants, but none has yet been exercised for a plant with gram-to-kilogram tritium inventories and full-power neutron activation; first-time application (environmental review, local permits, tritium-release limits) remains a schedule risk.

**Financing and corporate risk**:
- Private fusion financing has shifted from venture rounds to project-scale capital and offtake: Google/Eni PPAs with CFS; Microsoft–Helion PPA (Helion began construction of the **Orion** plant in Malaga, Washington in July 2025, targeting electricity to Microsoft from 2028, ≥50 MW after a one-year ramp; Helion reported measurable DT fusion and 150 million °C in its Polaris prototype in February 2026, but no electricity recovery has been publicly demonstrated)[^65][^66]; TAE's planned all-stock **$6 billion merger with Trump Media & Technology Group** (announced December 2025; closing pushed to Q4 2026), which plans to site and begin a 50 MW plant in 2026 — a merger raising governance and conflict-of-interest concerns and coupling a fusion developer's financing to a volatile public equity.[^67]
- Most PPAs are contingent on technical milestones (e.g. Google's on SPARC Q > 1) and do not finance construction risk; FOAK plants still need several billion dollars of equity or public money each (Proxima Alpha ~€2 B; ITER-class overruns show the downside).[^52][^79]

**Supply chain**: concentrated single-source risks include REBCO tape (see 2.3), large gyrotrons and high-power RF sources, tritium handling equipment, high-power laser diodes (IFE), large cryoplants and specialised forgings. Fusion competes with other sectors (SMRs, defence, semiconductors) for nuclear-grade fabrication capacity and skilled labour.

***

## Part VI — Technology Readiness: Cross-System Summary

### 6.1 Technology Readiness Table

| Sub-challenge | Tokamak | Stellarator | Laser ICF | TRL Range |
|---|---|---|---|---|
| Steady-state high-performance plasma (\(f_{Gr}>1\), \(H_{98}>1\)) | Demonstrated transiently (DIII-D, EAST)[^6][^7] | Not applicable (no driven current) | N/A | 4–5 |
| Long-pulse non-inductive H-mode (>1000 s) | EAST 1066 s H-mode (Jan 2025); WEST 1337 s, L-mode-like, 2 MW (Feb 2025)[^50][^49] | Intrinsic; W7-X 360 s detached at 5 MW[^41] | N/A | 5–6 (stellarator) |
| High-field HTS magnets (>20 T) | CFS SPARC TF magnet validated (20 T TFMC 2021); Tokamak Energy Demo4 11.8 T (2025)[^1][^22][^54] | Non-planar HTS coils in development (Proxima, Type One); none at reactor scale[^26][^57] | N/A | 6 (SPARC) |
| HTS coil lifetime under reactor neutron fluence | Untested in situ | Untested | N/A | 3 |
| Demountable HTS joints at scale | Lab-scale only | Same | N/A | 3 |
| Current drive systems (ECCD, NBCD) | ITER-scale systems being built | Not required for steady-state | N/A | 5–6 |
| DEMO integrated operating scenario | Not demonstrated — design ongoing | HELIAS concept only | N/A | 2–3 |
| DPSSL at 10 Hz, >50 J (rep-rate) | N/A | N/A | Mercury: 300,000 shots at 50 J[^30] | 4–5 |
| DPSSL at 10 Hz, ~2 MJ (plant scale) | N/A | N/A | Concept only (LIFE)[^31][^30] | 2 |
| Excimer (KrF) driver at rep-rate, ≥10 % wall-plug | N/A | N/A | Xcimer Phoenix prototype operating (2026), Anvil 2028 planned[^61] | 3–4 |
| Target gain (Q > 1) | Never demonstrated in MCF device | Never demonstrated | NIF: Q = 4.13 (April 2025)[^2] | 9 (physics only) |
| Target factory at 500,000/day | N/A | N/A | Nonexistent[^37][^38] | 1–2 |
| DEMO RAMI ≥ 30% availability | Not demonstrated; design ongoing | Not demonstrated | N/A | 2 |

### 6.2 SPARC as the Imminent Decision Point

SPARC's first plasma (now expected 2027) and net energy demonstration (2027–2028) represent the most consequential fusion milestones in the near-term programme. A successful SPARC result will:[^19][^18]
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
- **Q1.3**: Can W7-X progress from the OP2.4/OP2.5 targets (> 60 s high-performance detached scenarios, 2026–2027) to its 30-minute plasma goal without exceeding heat loads on the actively cooled first wall or accumulating impurities to a plasma-quenching level? What is the lifetime of the CFC divertor targets under continuous 5 MW operation?[^40]

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

Challenge 5 is the ultimate integration test: whether all the partial solutions to Challenges 1–4 can be assembled into a continuously operating, reliable, economically viable energy system. The milestones of 2024–2026 represent the most concentrated set of positive results in fusion's history. The DIII-D/EAST plasma regime breakthrough eliminates the theoretical doubt about whether reactor-relevant operating points exist. W7-X's 360-second fully detached plasma demonstrates stellarator steady-state in a way that cannot be dismissed as a transient. CFS's DOE-validated full-scale HTS TF magnet, with serial production for SPARC under way, marks the first time a fusion engineering component has moved from research prototype to manufactured product. NIF's April 2025 record of Q = 4.13 establishes that ICF ignition is not an edge-case anomaly but a reproducible physics regime.[^7][^6][^2][^41][^1]

Yet the magnitude of the remaining engineering gaps must be equally clearly stated. SPARC must demonstrate net energy to validate the compact high-field approach — and no fusion device has ever done this. A DEMO-class integrated system with the necessary RAMI performance has never been designed to a stable reference, let alone built. The IFE target factory is an entirely new industrial sector that needs to be invented, scaled, and costed. The time between today's milestones and a commercial fusion power plant — even under optimistic assumptions — is measured in decades, not years. The value of these milestones is not that they shorten the timeline dramatically; it is that they progressively close the space of physical unknowns, converting speculative engineering assumptions into validated design inputs. The 2025–2026 record also shows the characteristic FOAK pattern: SPARC's magnet installation running months behind the company's own January 2026 plan, ITER's decade-scale re-baseline, and Type One's prototype slip — while financing and regulation, historically the feared bottlenecks, improved faster than the hardware.

The next decade — dominated by SPARC first plasma and net energy results (2027–2028), China's BEST (2027+), Helion's Orion claim (2028), ITER Start of Research Operation (2034) and DT (2039), W7-X long-pulse campaigns (OP2.4/2.5 in 2026–2027, 30-minute goal later), excimer/DPSSL driver prototypes (Xcimer Anvil 2028), and the IFMIF-DONES materials data pipeline — will determine whether the integrated engineering pathway to commercial fusion is achievable within the century's first half.

***

## Risk Assessment (November 2026)

All likelihoods, distributions and correlations in this section are **calibrated expert judgments** by the report author, grounded in the evidence above (FOAK schedule history of ITER, W7-X, NIF and SPARC; demonstrated versus required driver parameters; status of regulation and financing as of 2 November 2026). They are not outputs of a formal elicitation and should be treated as priors to be updated as the early indicators resolve.

### Risk register

| ID | Risk | Pathway(s) | Likelihood | Impact on schedule (years) / on feasibility | Early indicator | Mitigation |
|---|---|---|---|---|---|---|
| DR-1 | SPARC first plasma / Q > 1 slips beyond 2028 or Q > 1 not reached (magnet integration, quench, disruption damage) | Tokamak (HTS); indirectly Stellarator (HTS) | med | +3–5 for HTS tokamak gate; feasibility of compact high-field route questioned if Q > 1 fails for physics reasons | TF magnets installed (8/18 by Sept 2026); date of first plasma; quench/fault reports in commissioning | Staged commissioning; spare TF coils; independent review; keep LTS/ITER-class route as fallback |
| DR-2 | HTS coil degradation under neutron/gamma irradiation at operating temperature faster than predicted (shorter coil life, thicker shield, lower TBR) | Tokamak, Stellarator (HTS) | med | +3–8; may force larger machines or coil replacement every few fpy, eroding the compact-HTS economic case | Cryogenic in-situ irradiation results; SPARC DT-phase coil diagnostics; ARC shielding design changes | Irradiation campaigns at operating temperature; conservative shielding; demountable/replaceable coils; LTS fallback |
| DR-3 | Quench in large HTS/no-insulation or demountable-joint coil causes damage and long outage | Tokamak, Stellarator (HTS) | med | +1–3 per event; availability loss | Quench events in SPARC/Demo4/Proxima coils; joint resistance drift over thermal cycles | Redundant detection (fibre optic, voltage, acoustic); partial insulation; joint qualification over ≥10³ cycles |
| DR-4 | REBCO tape supply cannot scale or cost does not fall below ~$50/kA·m; supplier concentration/export controls | Tokamak, Stellarator (HTS) | med | +2–5 for fleet deployment; FOAK less affected | Global capacity (>5,000 km/yr 12 mm-eq. in 2025) versus announced expansions; price disclosures; export-control actions | Multi-sourcing; long-term offtake; vertical integration (Proxima, Tokamak Energy); LTS fallback for large machines |
| DR-5 | Non-inductive current drive too inefficient (recirculating power > 20–25 %) or long-pulse tokamak operation limited by wall/exhaust; pulsed operation imposes fatigue | Tokamak | med | +3–10; pulsed DEMO variants lower availability and economics | Duration × performance records (EAST/WEST/KSTAR, JT-60SA); gyrotron efficiency at 170–240 GHz; ITER hybrid scenarios after 2034 | High-bootstrap scenarios; high-efficiency gyrotrons with energy recovery; accept long-pulse pulsed design with fatigue-rated components |
| DR-6 | 3D (non-planar) HTS or Nb\(_3\)Sn coil manufacturing and alignment tolerances unachievable at reactor scale/cost | Stellarator | med | +3–8; cost increase, possible need for larger, simpler coils | Proxima/Type One model-coil test results; Alpha and Infinity One schedule; coil cost per tonne | Coil-set simplification in optimisation; modular coils; in-situ trim coils; metrology-based correction |
| DR-7 | IFE driver fails to reach ≥ 10 % wall-plug at ≥ 5–10 Hz with MJ-class energy and adequate lifetime (diode cost, excimer efficiency, optics damage) | Laser ICF | high | +5–15; show-stopper for laser IFE if no architecture reaches ηG ≳ 10 | Xcimer Phoenix/Anvil efficiency and rep-rate data; diode $/W trend; DPSSL kJ-class rep-rated beamlines | Parallel architectures (DPSSL, KrF/excimer, pulsed power as non-laser alternative); higher-gain targets to relax efficiency |
| DR-8 | Target factory cannot reach ~10⁵–10⁶ targets/day at ≲ $0.30–1 per target with required precision; injection/tracking at 10 Hz unproven | Laser ICF | high | +5–15; feasibility risk for IFE economics | Automated-line throughput (targets/hour), cost per target in pilot lines, injection-and-engagement demos | Target designs optimised for manufacturability (e.g. direct-drive foam capsules); early pilot lines; shared industry–lab programmes |
| DR-9 | Plant integration failure: FOAK demo reaches < 50 % design availability (remote maintenance, tritium plant, RF/driver reliability, unplanned outages) | All | high | +3–6 to commercial plant; credibility and financing impact | Commissioning durations of SPARC, BEST, Helion Orion; RAMI data from W7-X/JT-60SA/ITER | RAMI-driven design; hot cells and spares; modular, demountable components; extended integrated test facilities |
| DR-10 | Licensing: first application of new fusion frameworks delayed (NRC final rule slip, state/EU permitting, tritium-release limits, local opposition) | All | med (US/UK low–med; EU med) | +1–4 per FOAK plant | NRC final rule publication (planned fall 2026, unconfirmed); first Part 30/Agreement-State fusion licence; UK EN-8 consents; EU-level framework | Early regulator engagement; byproduct-material approach; harmonised international guidance (IAEA) |
| DR-11 | Financing gap or investor retrenchment for FOAK plants (multi-$B capital at risk; PPAs contingent on milestones; hype-cycle reversal after a visible failure) | All (private-led tokamak/stellarator/IFE most exposed) | med | +2–6; company failures can strand pathways | Size/terms of 2026–2028 rounds; conditional PPAs converting to binding; public co-funding (Germany €2 B+, UK £2.5 B, DOE milestones); TAE–TMTG merger outcome | Public–private cost sharing; milestone financing; government offtake/CfD-type schemes; staged capital commitment |
| DR-12 | FOAK construction time and cost overrun (ITER-type pattern: 2× cost, +5–10 years) | All | high | +3–8 per FOAK plant | Schedule variance on SPARC, BEST, Alpha, Orion, STEP; vendor qualification problems | Design maturity before FID; standardised modules; experienced EPC partners; realistic contingencies |
| DR-13 | Specialised supply chain bottlenecks beyond HTS (gyrotrons, cryoplants, tritium systems, laser diodes, nuclear-grade fabrication, skilled workforce) | All | med | +1–3 | Lead times for gyrotrons/cryoplants; vendor count; workforce programmes | Early procurement; supplier development programmes; standardisation across developers |
| DR-14 | ITER/EU DEMO further slips reduce public validation data (long-pulse, Nb\(_3\)Sn, RAMI) before private plants need it | Tokamak (public route), indirectly all | med | +2–5 for public DEMO route; increases uncertainty for private designs | ITER SRO 2034 milestone tracking; EU DEMO conceptual design 2030 | Private and national facilities (JT-60SA, BEST, SPARC) as substitutes; data-sharing agreements |

### Gate definition

**Gate (Challenge 5): "Reactor-grade driver demonstrated."** The gate is reached in a pathway in the calendar year in which all of the following are publicly demonstrated (peer-reviewed or independently verified) on hardware at, or directly extrapolable to, power-plant scale:

- **MCF (Tokamak, Stellarator)** — both:
  1. A **superconducting magnet system** (HTS or LTS) of plant-relevant size and field (≥ ~5 T on axis for stellarators, ≥ ~10 T for compact HTS tokamaks, or ITER-class LTS) has operated in an integrated fusion device with **quench protection and fault tolerance validated**, and there is **experimental evidence (irradiation at operating temperature plus in-device dosimetry) that the coils, with the planned shielding, survive the design lifetime fluence** (≥ ~20 full-power years or a demonstrated, practical coil-replacement scheme); and
  2. **Long-pulse or steady-state operation** at reactor-relevant performance (H-mode-class confinement, density near Greenwald, actively cooled exhaust) for **≥ ~1 hour (tokamak; or a pulsed design with ≥ 2-hour pulses and fatigue-qualified components)** or **≥ 30 minutes at high heating power (stellarator)**, with a credible extrapolation to **recirculating power ≤ ~20–25 % of gross electric output** (for tokamaks including current-drive power at demonstrated wall-plug efficiencies).
- **Laser ICF** — both:
  1. A **driver architecture** demonstrated at **≥ 10 % wall-plug efficiency and ≥ ~5–10 Hz** at, at minimum, a beamline/module scale (≥ ~10 kJ per module) that sums to MJ-class energy without new physics, with optics lifetime demonstrated to ≥ 10⁸ shots per module or a credible replacement scheme; and
  2. **Target supply at cost-relevant scale**: an automated production line producing ignition-quality targets at ≥ ~10⁴ targets/day with a demonstrated cost trajectory to ≲ $1 per target at plant scale, plus injection-and-engagement at ≥ 5 Hz.

The gate does not require net electricity, tritium self-sufficiency, or materials qualification (separate challenges). Gate years are the year of demonstration, not of commercial deployment.

### Model parameters

| Pathway | P0 | P10 | P50 | P90 | P100 | P(never by 2100, show-stopper) | Rationale |
|---|---|---|---|---|---|---|---|
| Tokamak | 2031 | 2036 | 2045 | 2062 | 2095 | 0.05 | HTS magnets advanced (20 T TFMC, SPARC TF validated) and LTS mature (ITER); binding items are HTS lifetime under fluence (no in-device data before SPARC DT/ARC, ~2030s) and hour-scale reactor-grade non-inductive operation (EAST/WEST are low-power; ITER long-pulse data only after 2039). ARC early 2030s is the earliest route; FOAK slips (SPARC ~1 year, ITER ~10 years) widen the right tail. |
| Stellarator | 2033 | 2039 | 2050 | 2068 | 2100 | 0.07 | Steady state intrinsic (W7-X 360 s, 1.8 GJ) and LTS coils proven, but reactor-scale 3D coils (HTS for compact designs) and 30-min high-power operation not yet shown; Alpha (~2031, funding gap €1.2 B) and Infinity One (~2029) are the earliest tests; no burning stellarator planned before late 2030s. |
| Laser ICF | 2032 | 2040 | 2052 | 2075 | 2110 | 0.15 | Target physics proven (NIF G = 4.13) but driver efficiency is two orders of magnitude short in NIF; DPSSL rep-rate demonstrated only at ~50 J (Mercury), KrF at 5 Hz (Electra); Xcimer Phoenix/Anvil (2026/2028) is earliest data. Target factory is TRL 1–2 and needs a ~10⁴× cost reduction; higher show-stopper probability reflects possible failure to reach ηG ≳ 10 with economic targets. |

**Integration and deployment** (P10 / P50 / P90, with plausible min–max in brackets):

| Parameter | Tokamak | Stellarator | Laser ICF |
|---|---|---|---|
| (i) FID → first net electricity of first demonstration power plant (years) | 7 / 10 / 15 [5–22] | 8 / 11 / 16 [6–24] | 6 / 9 / 14 [5–20] |
| (ii) Demo net electricity → first commercial plant on grid (years) | 6 / 10 / 16 [4–25] | 7 / 11 / 18 [5–25] | 6 / 10 / 17 [4–25] |
| (iii) P(demo < 50 % of design availability in first 5 years) and resulting delay (years, P10/P50/P90) | 0.65; 2 / 4 / 8 | 0.55; 2 / 3 / 7 | 0.70; 2 / 5 / 10 |
| (iv) P(major licensing or financing delay) and size (years, P10/P50/P90) | 0.45; 1 / 3 / 7 | 0.45; 1 / 3 / 7 | 0.50; 1 / 3 / 8 |

Basis: (i) ITER, W7-X (~15 years construction) and NIF (~12 years) show FOAK fusion facilities take 10–15 years; private FOAK claims of 4–6 years (Helion Orion 2025→2028; ARC early 2030s) are treated as the optimistic tail. IFE plants are modestly faster to build (no large superconducting vessel) but need a novel driver and target plant. (ii) Includes design freeze from demo lessons, financing and second-site licensing; compressed if the demo is itself an early commercial unit (ARC, Orion, Infinity Two). (iii) Fusion experiments run at 10–20 % availability; ITER's DT-phase target is ~14 %; stellarators gain from no disruptions, IFE suffers from 10⁸–10⁹ shots/year on optics, injectors and targets. (iv) Licensing risk is reduced by byproduct-material frameworks (US, UK, Germany) but financing of multi-$B FOAK plants remains the dominant contributor; the IFE value is slightly higher because offtake commitments and public frameworks are less mature.

**Coupling to other challenges** (suggested Spearman rank correlation with this challenge's gate year; positive = delays move together) and discrete events:

- **Plasma burning performance**: ρ ≈ +0.5 (Tokamak), +0.4 (Stellarator), +0.6 (Laser ICF). Long-pulse reactor-grade operation and driver requirements depend on achieved confinement/gain (higher target gain relaxes driver efficiency; higher bootstrap fraction reduces current-drive power).
- **Materials qualification**: ρ ≈ +0.4 (MCF; HTS shielding and coil-lifetime evidence share the neutron-irradiation infrastructure, e.g. IFMIF-DONES) and +0.3 (Laser ICF; final optics and chamber-wall damage). **Tritium/breeding**: ρ ≈ +0.3 (all; blanket thickness trades against magnet shielding and port space). **Power exhaust/divertor**: ρ ≈ +0.45 (Tokamak, Stellarator; hour-scale operation is exhaust-limited) and +0.2 (Laser ICF).
- **Breakthrough events**: (a) SPARC achieves Q > 1 by end-2028 with no major magnet damage — p ≈ 0.5; effect −2 years (Tokamak), −1 year (Stellarator, via HTS confidence); (b) HTS tape cost falls below ~$20/kA·m with >20,000 km/yr capacity by 2035 — p ≈ 0.3; effect −2 to −3 years (Tokamak, Stellarator); (c) a rep-rated driver module (excimer or DPSSL) demonstrates ≥ 10 % wall-plug at ≥ 5 Hz by 2032 — p ≈ 0.25; effect −5 years (Laser ICF).
- **Setback events**: (d) SPARC Q > 1 not achieved by 2030 or serious magnet/quench damage — p ≈ 0.25; effect +4 years (Tokamak), +1–2 years (Stellarator HTS); (e) cryogenic irradiation data show REBCO lifetime < 1/3 of design fluence — p ≈ 0.2; effect +5 years (HTS routes; LTS fallback limits the damage); (f) target-factory cost study shows no credible path below ~$1/target — p ≈ 0.3; effect +8 years and raises Laser ICF show-stopper probability to ~0.3; (g) high-profile FOAK failure or bankruptcy of a leading developer triggering a financing downturn — p ≈ 0.3 by 2032; effect +2–3 years (all pathways).

***

## Changelog (2026-11)

- Header updated to "November 2026 update"; executive summary given a status-in-brief paragraph.
- **Corrected**: CFS TFMC peak field is 20 T (September 2021), not ">20 T"/20.8 T; DOE milestone validation (30 Sept 2025, $8 M) concerned performance tests of a full-scale TF magnet, not acceptance tests of "production magnets".
- **Corrected**: EAST 1066 s (20 Jan 2025) described as RF-sustained H-mode (at ~60 % Greenwald), not a reactor-grade "fully non-inductive" record; added WEST 1337 s (12 Feb 2025, 2 MW LHCD, not H-mode).
- **Corrected**: SPARC first plasma now 2027 (not late 2026); TF magnet installation behind plan (8/18 by Sept 2026); ARC early 2030s in Chesterfield County, Virginia, confirmed; added Google and Eni PPAs.
- **Added**: ITER 2024 re-baseline (SRO 2034, full magnetic energy 2036, DT 2039, ~€5 B extra); replaced "ITER first plasma 2033" in the conclusion.
- **Corrected**: IFE power balance — ηG ≈ 2.6 is engineering breakeven, economic plants need ηG ≳ 10; NIF wall-plug efficiency stated as well below 1 %; NIF-to-plant shot-rate gap corrected from ~60,000 to ~2 × 10⁵; LIFE gain arithmetic made consistent.
- **Corrected**: W7-X coils are 50 non-planar + 20 planar NbTi coils (not NbTi/Nb\(_3\)Sn), ~3.5 m tall; "OP3 from September 2026 for 30 minutes" replaced by OP2.4 (Aug–Dec 2026) / OP2.5 (Feb–May 2027) plan; W7-X density gap to reactor softened from "10×" to "a few times".
- **Softened**: SPARC quench stored-energy figure (3–6 GJ) given as an order-of-magnitude estimate, no official figure found.
- **Added**: HTS tape supply/price data; Tokamak Energy Demo4 (11.8 T); Proxima (€411 M, Alpha ~2031), Type One/TVA; Xcimer Phoenix and DOE Athena approval, Focused Energy (Biblis), Marvel (ATLAS), Pacific Fusion; Helion Orion/Polaris; TAE–TMTG merger; UK STEP £2.5 B; China BEST and CFEC; German action plan; DOE roadmap; NRC proposed rule (Feb 2026; final rule not confirmed published as of 2 Nov 2026); UK Energy Act s.156; EU DEMO timeline.
- **Unverified/dropped**: a reported Tennessee fusion byproduct licence for Type One and any 2026 NIF yield above 8.6 MJ could not be confirmed and are not stated as fact.
- **Added**: Risk Assessment (November 2026) section.

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

47. [ITER baseline 2024 — press conference summary (July 2024)](https://iter.org/sites/default/files/media/2024-07/baseline_press_conference_summary_july-2024_b.pdf)

48. [ITER fusion reactor hit by massive decade-long delay and €5bn price hike — Physics World](https://physicsworld.com/a/iter-fusion-reactor-hit-by-massive-decade-long-delay-and-e5bn-price-hike/)

49. [WEST sets a new plasma duration record — CEA-IRFM (February 2025)](https://irfm.cea.fr/en/2025/02/west-sets-a-new-plasma-duration-record/)

50. [China's Experimental Advanced Superconducting Tokamak smashes fusion confinement record — Physics World](https://www.physicsworld.com/a/chinas-experimental-advanced-superconducting-tokamak-smashes-fusion-confinement-record/)

51. [Commonwealth Fusion Systems on X: eight of 18 SPARC TF magnets installed (22 September 2026)](https://x.com/CFS_energy/status/2102395361390149897)

52. [Google to buy power from Chesterfield fusion plant — Greater Richmond Partnership](https://www.grpva.com/news/google-to-buy-power-from-chesterfield-fusion-plant/)

53. [Google-backed CFS signs PPA with Italian energy company Eni — DatacenterDynamics](https://www.datacenterdynamics.com/en/news/google-backed-fusion-firm-commonwealth-fusion-systems-signs-ppa-with-italian-energy-company-eni/)

54. [Tokamak Energy announces fusion power plant magnet technology breakthrough (November 2025)](https://tokamakenergy.com/2025/11/19/tokamak-energy-announces-fusion-power-plant-magnet-technology-breakthrough/)

55. [Commercial compact fusion triggered REBCO tape industry: pulsed laser deposition technology opportunities and challenges — EurekAlert (2025)](https://www.eurekalert.org/news-releases/1101339)

56. [Faraday Factory tightens grip on HTS supply chain — Commercial Fusion](https://www.commercial-fusion.com/p/faraday-factory-tightens-grip-on-hts-supply-chain)

57. [Proxima Fusion raises 411 million euros — Max Planck Society (July 2026)](https://www.mpg.de/26861952/proxima-fusion-raises-411-million-euros)

58. [TVA and Type One Energy to build 350 MW fusion plant — Neutron Bytes (September 2025)](https://neutronbytes.com/2025/09/20/tva-and-type-one-energy-to-build-350-mw-fusion-plant/)

59. [W7-X Task Force goals for OP2.4/OP2.5 — IPP](https://www.ipp.mpg.de/5229513/TFI_goals.pdf)

60. [DOE approves Xcimer's laser fusion power plant design — ANS Nuclear Newswire (June 2026)](https://www.ans.org/news/article-8111/doe-approves-xcimer-laser-fusion-power-plant-design/)

61. [Xcimer activates Phoenix fusion laser — Nuclear Engineering International](https://www.neimagazine.com/news/xcimer-activates-phoenix-fusion-laser/)

62. [Focused Energy: $240 million, the largest Series A financing in the global fusion industry — Focused Energy (May 2026)](https://www.focused-energy.co/news-release/focused-energy-sets-a-new-benchmark-240-million-for-the-largest-series-a-financing-in-the-global-fusion-industry)

63. [Marvel Fusion breaks ground on $150M laser facility in Colorado — The Next Web (October 2024)](https://thenextweb.com/news/marvel-fusion-breaks-ground-on-150m-laser-facility-in-colorado)

64. [Fusion simplification demonstrated by Pacific Fusion and Sandia — ANS Nuclear Newswire (2026)](https://www.ans.org/news/article-7739/fusion-simplification-demonstrated-by-pacific-fusion-and-sandia)

65. [Helion secures land and begins building on the site of world's first fusion power plant — Business Wire (July 2025)](https://www.businesswire.com/news/home/20250730326704/en/Helion-Secures-Land-and-Begins-Building-on-the-Site-of-Worlds-First-Fusion-Power-Plant)

66. [Helion achieves new industry-first fusion energy milestones — Helion (February 2026)](https://helionenergy.com/newsroom/helion-achieves-new-fusion-energy-milestones)

67. [Trump Media to merge with fusion startup TAE Technologies in $6B deal — ANS Nuclear Newswire (December 2025)](https://www.ans.org/news/article-7632/trump-media-to-merge-with-fusion-startup-tae-technologies-in-6b-deal/); [status update: closing targeted Q4 2026 — The Next Web](https://thenextweb.com/news/trump-media-drops-truth-social-spinoff-refocuses-on-6-billion-fusion-merger-with-tae-technologies)

68. [Regulatory Framework for Fusion Machines, proposed rule — Federal Register 91 FR 9476 (26 February 2026)](https://www.govinfo.gov/content/pkg/FR-2026-02-26/html/2026-03865.htm)

69. [Fusion machine rulemaking status — US NRC](https://www.nrc.gov/materials/fusion/rulemaking-status)

70. [Energy Act 2023, section 156: Fusion energy facilities — nuclear site licence not required](https://www.legislation.gov.uk/ukpga/2023/52/section/156)

71. [£2.5 billion for world-first prototype fusion energy plant — GOV.UK (June 2025)](https://www.gov.uk/government/news/25-billion-for-world-first-prototype-fusion-energy-plant)

72. [German government pledges more than €2 bln for nuclear fusion — Clean Energy Wire (October 2025)](https://www.cleanenergywire.org/news/german-government-pledges-more-eu2-bln-nuclear-fusion)

73. [China launches fusion-focused company — ANS Nuclear Newswire (July 2025)](https://www.ans.org/news/2025-07-30/article-7244/china-launches-fusionfocused-company/); [China sets out fusion progress, collaboration opportunities — World Nuclear News (January 2026)](https://www.world-nuclear-news.org/articles/china-sets-out-fusion-progress-collaboration-opportunities)

74. [Energy Department releases finalized Fusion Science and Technology Roadmap — US DOE (June 2026)](https://www.energy.gov/node/4858962)

75. [Euratom fusion programme — European Commission presentation at IEA (February 2025)](https://iea.blob.core.windows.net/assets/98a960b8-ec25-4e85-8e88-7beddf6cabd5/ElenaRighi_EURATOM.pdf)

76. [NIF status presentation, LSO workshop 2026 — LLNL (June 2026)](https://lasers.llnl.gov/sites/lasers/files/2026-06/lso-workshop-2026-wednesday-g-brunton.pdf)

77. [Biblis wird zum Laserfusions-Hub — TU Darmstadt (July 2026)](https://www.tu-darmstadt.de/universitaet/aktuelles_meldungen/einzelansicht_572032.de.jsp)

78. [The SPARC Toroidal Field Model Coil Program — Hartwig et al., arXiv:2308.12301](https://arxiv.org/pdf/2308.12301)

79. [Proxima Fusion seeks €2 billion to build a nuclear fusion test facility — The Next Web (February 2026)](https://thenextweb.com/news/proxima-fusion-seeks-e2-billion-to-build-a-nuclear-fusion-test-facility)
