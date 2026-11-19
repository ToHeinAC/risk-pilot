# Nuclear Fusion — Deep Dive: Challenge 2
## Plasma-Facing Materials (PFMs) & Neutron Damage

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — June 2026; reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps gate MA to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

Plasma-facing materials and the neutron damage they sustain represent the most extreme materials engineering problem ever attempted. A commercial fusion reactor first wall must simultaneously withstand 14.1 MeV neutron bombardment at fluences reaching ~20 dpa per full power year **[unconfirmed 2026-11]** (upper end of published DEMO estimates; the repository's earlier review cites ~12–15 dpa/fpy for EU-DEMO front-wall steel — not re-verified), continuous steady-state heat fluxes of 1–10 MW m\(^{-2}\), intense helium and hydrogen ion bombardment from the plasma, and — in tokamaks — episodic ELM and disruption transients that transiently multiply heat loads by factors of 10–50. No material known today can meet all of these requirements simultaneously at reactor scale over the multi-year lifetimes required.[^1]

The fundamental difficulty is compounded by a critical epistemic gap: no facility in the world can yet expose materials simultaneously to fusion-relevant 14 MeV neutron fluxes and the full plasma environment. The IFMIF-DONES facility, whose international agreement was signed in November 2025, is the first dedicated attempt to close this gap — but it will not begin operations for years. Until then, all material qualification rests on extrapolation from ion-beam, fission-neutron, and separate plasma-exposure experiments, each of which captures only a subset of the true reactor environment.[^2][^3]

This report provides a deep-dive analysis of six interconnected sub-challenges: (1) neutron displacement damage and transmutation; (2) helium bubble formation, tungsten fuzz, and blistering; (3) tritium retention in PFMs; (4) erosion, redeposition, and impurity influx to the plasma; (5) structural material qualification for blankets and shielding; and (6) remote maintenance in the neutron-activated reactor environment. Each challenge is mapped across Tokamak, Stellarator, and Laser ICF pathways.

***

## Part I — Neutron Displacement Damage and Transmutation

### 1.1 The 14 MeV Neutron Problem

In a DT fusion reactor, 80% of fusion energy is carried by 14.1 MeV neutrons. This energy is far above the thresholds for nuclear reactions in structural materials. Unlike fission reactors, which produce neutrons with a mean energy of ~2 MeV, fusion neutrons have sufficient energy to:[^4]
- Create **primary knock-on atoms (PKA)** with energies up to several hundred keV, producing displacement damage cascades that generate thousands of Frenkel pairs per neutron interaction
- Transmute target nuclei through (n,p), (n,α), and (n,γ) reactions, generating helium, hydrogen, and new alloying species within the material lattice[^5][^2]

For tungsten armor on the divertor, the expected damage rate in DEMO is **3 dpa per full power year (fpy)** for the divertor armor, **6–9 dpa/fpy** for the first-wall armor, and **12–15 dpa/fpy** in the first-wall steel structure. Over a projected component lifetime of ~5 years, this accumulates to 40–70 dpa in the most exposed regions.[^6][^7][^8][^1]

### 1.2 Tungsten Transmutation: The Re/Os/Ta Problem

Tungsten is the reference plasma-facing armor material. Under 14 MeV neutron bombardment, W undergoes the following primary nuclear reactions:[^5][^2]

\[^{186}\text{W}(n,\gamma) \rightarrow ^{187}\text{W} \xrightarrow{\beta^-} ^{187}\text{Re}\]
\[^{187}\text{Re}(n,\gamma) \rightarrow ^{188}\text{Re} \xrightarrow{\beta^-} ^{188}\text{Os}\]

Over 10 full power years, these transmutation chains produce concentrations of approximately **10 at.% Re and 3 at.% Os** in the most neutron-exposed tungsten. This has several compounding consequences:[^5]
- **Phase precipitation**: at these concentrations, thermodynamically stable intermetallic Re\(_x\)W and Os\(_x\)W σ- and χ-phase precipitates form, even appearing experimentally at doses as low as 1.25 dpa at 800 °C. These phases are brittle and dramatically increase hardness[^9]
- **Ductile-to-brittle transition temperature (DBTT) increase**: neutron irradiation alone raises W's DBTT by 200–400 °C; combined Re/Os precipitation shifts it by an additional 100–200 °C, potentially raising the DBTT above 800 °C — well above the operating temperature of many coolant designs
- **Thermal conductivity degradation**: lattice defects and Re/Os solid-solution alloying reduce thermal conductivity by 30–60% from the unirradiated value, impairing the material's ability to conduct away plasma heat loads
- **Irradiation-induced void swelling**: vacancy clusters coalesce into nanoscale voids (10–65 nm diameter observed at 1.25 dpa at 800 °C), causing volumetric swelling and dimensional instability in precision-engineered components[^9]

The IAEA Coordinated Research Project on tungsten PFMs explicitly identified the simultaneous effects of plasma, neutrons, and transmutation as "the most serious impediment to the realization of fusion energy production". Critically, **the tritium retention behavior of pure W — which is inherently low — is dramatically worsened by neutron irradiation**, because transmutation-induced defects create trap sites for hydrogen isotopes that are absent in unirradiated W.[^10][^2]

### 1.3 Quantitative Damage Budget and Replacement Schedules

| Component | Material | Neutron Wall Load | Peak Damage (DEMO) | Replacement Frequency |
|---|---|---|---|---|
| First wall armor | Tungsten | 1.1–1.35 MW m\(^{-2}\) | 6–9 dpa/fpy[^1] | ~5 fpy (design target) |
| Divertor armor | Tungsten | Up to 20 MW m\(^{-2}\) peak | 3 dpa/fpy[^11] | 1–3 fpy (erosion-limited) |
| Blanket first wall | EUROFER97 (RAFM) | 1.3 MW m\(^{-2}\) | 12–15 dpa/fpy[^7] | ~4 fpy[^7] |
| Vacuum vessel | SS316 | Shielded | <2.75 dpa (lifetime limit)[^12] | End-of-life |
| Superconducting coils | REBCO/LTS | Shielded | <10\(^{-5}\) dpa (HTS sensitivity)[^8] | 30+ yr lifetime target |

For the EU DEMO starter blanket (EUROFER97), the design life is approximately **1.33 full power years or ~4 calendar years** before the damage dose reaches the design limit of ~20 dpa in the front-wall steel. This implies that the entire in-vessel component set — first wall, blanket modules, divertor cassettes — must be replaced multiple times over the reactor operational lifetime, each replacement operation conducted remotely in a high-radiation environment.[^7][^13][^14]

***

## Part II — Helium Embrittlement, Tungsten Fuzz, and Blistering

### 2.1 Helium Bubble Nucleation and Growth

In a DT fusion reactor, helium ash from the fusion reaction (\(\alpha\)-particles that have been thermalized) is pumped out through the divertor. However, a fraction of the helium that reaches the first wall and divertor is implanted directly into the tungsten lattice by charge-exchange neutral atoms and ion bombardment.

The consequences are severe:[^15][^16][^17]
- **Bubble nucleation**: Helium is nearly insoluble in the W lattice and immediately forms small complexes (He\(_n\)V\(_m\)) with vacancies. These serve as nuclei for bubble growth. Molecular dynamics simulations show that complex diffusivity has a complex non-monotonic dependence on He content, but that efficient diffusion pathways exist for bubble migration and coalescence[^16]
- **Blistering**: When a subsurface layer of He bubbles reaches a critical pressure (~GPa), interbubble fracture and crack propagation to the surface create dome-shaped blisters up to 20 µm high. Blistering is orientation-dependent: W{100} surfaces form larger blisters than W{110} or W{111}. Once blisters rupture, they release He and W dust/debris into the plasma, potentially destabilizing confinement[^18][^15]
- **Fuzz formation**: Under sustained He plasma bombardment (He energy >20 eV, fluence >10\(^{24}\) He m\(^{-2}\), surface temperature >700 °C), the W surface transforms into a tangled nanostructure of filaments called "fuzz". Fuzz formation has been confirmed on WEST tokamak divertor components under ITER-like He plasma conditions. Fuzz dramatically increases the surface area for further He implantation, accelerates erosion, and generates W nano-dust that can enter the plasma[^19][^20][^21]

### 2.2 Synergistic Neutron + Helium Damage

An important synergy exists between neutron displacement damage and helium implantation that is not captured by studying either effect in isolation:[^2][^10]
- Neutron-generated vacancies dramatically increase the sink density for He bubbles, accelerating bubble nucleation at lower He doses
- Pre-existing irradiation defect networks act as preferential nucleation sites for He clusters, moving bubble formation to shallower depths and higher temperatures
- The combined He bubble density in neutron-irradiated W is predicted to be **~50–100× higher** than in ion-irradiated W alone at equivalent fluence, greatly accelerating blistering kinetics
- Since no facility can apply both simultaneously at reactor-relevant flux levels, this synergy remains almost entirely uncharacterized experimentally[^2]

### 2.3 Tungsten Alternatives and Composite Approaches

Pure tungsten's brittleness and transmutation sensitivity have driven research into modified forms:[^22]
- **W-Re alloys**: improved ductility at low doses but accelerated Re precipitation under neutron irradiation, making them counterproductive for long-term operation
- **W + oxide particles (ODS-W)**: Yttria (Y\(_2\)O\(_3\)) or La\(_2\)O\(_3\) nano-dispersoids in the W matrix act as point-defect sinks, reducing radiation hardening and vacancy clustering. Oxide-dispersion strengthened W retains more thermal conductivity and shows reduced He bubble growth compared to pure W under ion irradiation[^22]
- **Tungsten-zirconium composites (porous surface layer)**: SPS-fabricated W-Zr composites can generate a controlled porous near-surface layer that allows He to escape rather than accumulate into blisters, but at the cost of reduced thermal conductivity[^22]
- **W fibre-reinforced W (Wf/W)**: analogous to carbon-fibre reinforced ceramics; the fibrous microstructure provides controlled crack deflection and pseudo-ductility, preventing brittle fracture at irradiated DBTT values. Still at laboratory TRL 3–4

None of these approaches has been validated under simultaneous fusion-relevant neutron and plasma conditions.

***

## Part III — Tritium Retention in Plasma-Facing Materials

### 3.1 Why Retention Matters

Tritium that becomes trapped in plasma-facing materials is lost from the fuel cycle, must be periodically removed by baking or isotopic exchange, and — if accumulated beyond a regulatory limit — can trigger a mandatory reactor shutdown for decontamination. In ITER, the in-vessel tritium inventory is limited to **700 g** by license for accident safety reasons. A DEMO reactor operating at 500 MW fusion power burns approximately **75 g T/day** **[corr. 2026-11]** (184 g/day would correspond to ~1.2 GW of fusion power); any steady accumulation in the first wall at a fractional rate would rapidly approach this limit.

### 3.2 Retention Mechanisms in Tungsten

In **unirradiated tungsten**, hydrogenic retention is intrinsically very low because W has a high activation energy for H diffusion and limited natural trapping sites. This was the primary motivation for selecting W over carbon for ITER's divertor. However:[^23][^10]

- **Irradiation-induced traps**: Neutron damage generates vacancy clusters and interstitial dislocation loops that act as strong trapping sites for hydrogen isotopes. The binding energy for T at radiation-induced traps (~1.5 eV) is much higher than at intrinsic lattice defects (~0.85 eV), greatly increasing retention depth and reducing thermal desorption effectiveness[^10]
- **Scaling with fluence**: Current experimental data suggest tritium retention in neutron-irradiated W follows a **t\(^{0.5}\) power law** (i.e., it does not saturate but keeps increasing with plasma exposure time). This is deeply concerning — if confirmed at reactor scale, it implies that in-vessel tritium inventory grows without bound during reactor operation, eventually hitting the safety limit[^10]
- **Temperature effects**: Retention is strongly temperature-dependent. At operating temperatures above 700–800 K (wall baking temperature), thermally activated detrapping reduces retained inventory significantly. Wall baking protocols (heating the first wall to 700–800 K under low-power plasmas) are the primary mechanism for tritium recovery in present devices, and their efficiency must be confirmed at ITER conditions[^24]

### 3.3 Mixed Materials: The Be/W Interaction

ITER's original design included a **beryllium first wall** (since replaced by full-W following the decision in 2024) combined with a tungsten divertor. Even in the full-W design, the transition produces a critical complication: beryllium eroded from wall regions can be transported to the divertor, where it co-deposits with tungsten and plasma-implanted hydrogen isotopes:[^25][^26][^23]
- Be co-deposited layers on W surfaces can trap tritium at significantly higher inventories than pure W
- Be-W alloying at the surface (forming intermetallic phases) can reduce the tungsten melting point to ~1500 °C, potentially causing structural compromise during ELM transients[^26]
- Mixed Be-C-W layers (if carbon is present from legacy components or diagnostics) have the highest tritium retention of all possible combinations[^23]

The multi-species plasma environment in any real tokamak creates a surface chemistry problem of enormous complexity that is not captured by single-species material testing.

***

## Part IV — Erosion, Redeposition, and Impurity Contamination

### 4.1 Physical Sputtering Mechanism and Net Erosion

The plasma bombards PFMs with energetic ions and charge-exchange neutrals. When the incident particle energy exceeds the surface binding energy of the target atom (~8 eV for W), **physical sputtering** occurs. The sputtering yield for W is extremely low (\(Y \sim 10^{-4}\) at relevant divertor conditions) compared to carbon, which was the original reason for selecting W. However:[^27]

- Under ELMs, transiently high particle energies increase sputtering yields by a factor of **5×** over the inter-ELM level, with intra-ELM sputtering dominating the total erosion budget[^27]
- Beryllium and other impurity ions, even at **0.1% concentration in the incident plasma**, produce the dominant W sputtering because their higher sputtering yield and lower mass create more efficient momentum transfer[^27]
- Under nitrogen impurity seeding (used for divertor detachment and heat load reduction), initial W sputtering **increases threefold** before the cooling effect of N lowers electron temperature enough to reduce sputtering below the nitrogen-free level[^27]
- **Prompt redeposition** — W sputtered from the surface that is immediately ionized and returned to the surface by the magnetic field within one gyro-orbit — accounts for **>50% of gross W erosion at high field**, significantly reducing net erosion. At ITER field (~5 T), prompt redeposition may reduce net erosion by 70–80% in normal operation. However, this benefit disappears during disruptions when prompt redeposition is disrupted by rapidly changing fields[^27]

### 4.2 Transport of Eroded W to the Plasma Core

Tungsten that escapes the divertor as W\(^{0}\) or low-ionization-state ions is swept toward the plasma core by SOL flows. In the hot core, high-Z W ions emit intense bremsstrahlung radiation that can cause core cooling and threaten plasma stability. Even **W concentrations of 2–5 × 10\(^{-5}\)** (relative to electron density) can cause significant core radiation losses in tokamaks.[^28][^29]

ITER's strategy to manage W influx involves:[^28][^25]
- Operating the divertor in **detached** plasma conditions, where the plasma temperature at the target is lowered to ~1–5 eV (vs. ~30 eV in attached conditions), reducing the kinetic energy of bombarding ions below the sputtering threshold
- **Boronization** of the first wall: deposition of thin boron coatings by glow-discharge in B-containing gases creates low-Z gettering layers that preferentially trap impurities and reduce W erosion rates. However, boron coatings erode rapidly in regions of direct plasma contact and must be periodically replenished — the required frequency and completeness on a full-tungsten ITER wall is essentially untested[^25]
- Active **impurity seeding** (Ne, Ar) to radiatively cool the SOL and divertor, reducing peak target temperatures below the W sputtering threshold. This competes with ELM suppression and power exhaust requirements, requiring sophisticated operational optimization

During ITER plasma start-up (the "limiter phase" before a diverted configuration is established), the plasma contacts the tungsten main chamber wall directly at elevated temperatures. ITER simulations show that in this configuration, W erosion produces "intolerable W plasma concentrations of several percent" in limiter geometry, which could prevent the establishment of the diverted plasma entirely. This is a critical operational risk.[^29]

### 4.3 Erosion in Laser ICF

In ICF, the material challenge for the first wall is qualitatively different from MCF. Each microexplosion (~10 kg TNT equivalent per target) generates:
- A pulse of 14 MeV neutrons and X-rays impacting the chamber wall within ~100 ns
- Energetic plasma debris at 100–1000 eV ionic charge states impacting the wall over ~1 µs
- Cyclic thermomechanical stress at 5–10 Hz repetition rate for the 30–40 year reactor lifetime (~10\(^{10}\) shots)

The **final optics** (fused silica or KDP frequency-conversion crystals) face an additional challenge: at NIF (single-shot operation), optics at the highest-used fluence of 8 J cm\(^{-2}\) show damage initiation that accumulates — optics must be removed for mitigation after ~100 shots at full energy. A power plant operating at 10 Hz would encounter this dose after ~10 seconds of operation. Novel final optics concepts using grazing incidence mirrors, gas final optics, or liquid film optical surfaces are under development but at TRL 1–2.[^30][^31]

***

## Part V — Structural Materials: RAFM Steels, ODS, and SiC/SiC

### 5.1 Reduced Activation Ferritic/Martensitic (RAFM) Steels

RAFM steels (EUROFER97 in Europe, F82H in Japan, China Low Activation Martensitic in China) are the reference structural material for fusion blankets. They were engineered by replacing high-activation alloying elements (Mo, Nb, Ni) in Mod9Cr-1Mo steel with low-activation alternatives (W, Ta, V), enabling shallow-land burial of activated components after a decay period of ~100 years rather than deep geological disposal.[^32][^33][^6]

**Property window and limitations**:
- **Minimum operating temperature**: ~350 °C, limited by irradiation-induced embrittlement — neutron-induced displacement damage causes DBTT shifts of 100–200 °C at doses above 5 dpa[^34][^6]
- **Maximum operating temperature**: ~550 °C, limited by creep strength loss and microstructural instability (M\(_{23}\)C\(_6\) coarsening and martensite recovery)[^34]
- **Helium limit**: ~400–500 appm He in 9%-Cr steels, corresponding to neutron doses of ~40–50 dpa, triggers void swelling onset — ODS variants can extend this limit[^35]
- **Irradiation data gap**: while EUROFER97 has been irradiated to ~70 dpa in fission reactors at ~300–325 °C, this is at a lower temperature than reactor operation and with a different neutron energy spectrum. Data at reactor-relevant conditions (350–550 °C, 14 MeV neutron spectrum) is absent[^6]

The temperature window of 350–550 °C imposes constraints on blanket coolant choice. Helium coolants at 8 MPa naturally operate within this range, but water-cooled blankets at ITER conditions (~3 MPa, ~300 °C) operate near or below the lower limit during some phases.[^12]

### 5.2 Oxide Dispersion Strengthened (ODS) Steels

ODS steels add nano-dispersed oxide particles (Y\(_2\)Ti\(_2\)O\(_7\), Y\(_2\)O\(_3\)-TiO\(_2\) mixed oxides) to a RAFM or 12–14%Cr ferritic matrix via mechanical alloying and hot isostatic pressing. The oxide nanoparticles act as **point-defect sinks** that:
- Capture vacancies and interstitials before they cluster into dislocation loops and voids
- Trap helium at the oxide interface rather than in the matrix, preventing large bubble formation at moderate He doses
- Provide dispersion strengthening that extends the maximum operating temperature to ~650–700 °C, opening higher Carnot-cycle efficiency potential[^35]

Recent high-temperature neutron irradiation studies of Fe-12Cr-YWT and Fe-14Cr-YWT ODS steels showed only minor changes to tensile properties, and Y-Ti-O nanoprecipitates remained largely unaffected by irradiation — a promising result. However, approximately **50% of the W alloying element migrated to grain boundaries** as W-rich Laves phase precipitates, representing a significant compositional redistribution that could affect long-term mechanical performance. Crucially, no ODS steel has yet been qualified to nuclear design codes (ASME, RCC-MRx) for use in fusion-relevant components.[^36][^37]

### 5.3 Silicon Carbide (SiC/SiC) Composites: The High-Temperature Frontier

SiC fiber-reinforced SiC matrix (SiC/SiC) composites offer the most attractive long-term material properties: operating temperatures up to ~1,000 °C (enabling Brayton cycle thermodynamic efficiency >45%), extremely low induced radioactivity (hands-on maintainability after ~50 years), and excellent radiation stability in the temperature range 800–1,100 °C.[^38][^37][^39]

Irradiation studies at doses of 28–41 dpa in Hi-Nicalon™ Type-S fiber / CVI SiC matrix composites confirm**no degradation** in swelling saturation, thermal conductivity saturation, elastic modulus, or flexural strength after initial dose-dependent saturation at low fluence. This is a critically important finding — it suggests that the radiation-induced property changes in advanced SiC/SiC are bounded and non-progressive.[^40]

Remaining barriers to deployment in fusion:[^37][^39][^38]
- **Joining technology**: reliable SiC/SiC joint methods for structural applications have not been developed. Mechanical designs currently avoid joints by relying on interlocking assembly — inadequate for complex blanket geometries
- **Transmutation chemistry**: C in SiC transmutes to He under 14 MeV neutrons and Si transmutes to Al and P. The consequences for long-term microstructure are not fully characterized at reactor-relevant fluences
- **High fabrication cost**: CVI/CVD production routes for SiC/SiC are extremely slow (weeks per part) and expensive compared to steel; industrial scale-up to reactor blanket quantities is undemonstrated
- **Lack of design codes**: SiC/SiC is not yet validated to any nuclear structural design code, blocking licensing even if material data existed

***

## Part VI — Remote Maintenance in Neutron-Activated Environments

### 6.1 The Radiation Environment After Shutdown

When a fusion reactor is shut down for maintenance, the neutron-activated structural materials become a distributed gamma-ray source whose intensity decays with complex multi-nuclide kinetics. For the ITER in-vessel components immediately after shutdown, calculated dose rates near first-wall and blanket modules in excess of **10\(^5\)–10\(^6\) Sv hr\(^{-1}\)** make any human approach impossible for decades. Workers in the ITER Tokamak Building must not exceed an integrated annual dose of 20 mSv — requiring that even transfer operations conducted via the remote-handling cask system undergo detailed radiation transport calculations to confirm worker and electronics protection.[^41][^42][^14]

Decay gamma transport modeling for ITER identifies:[^41]
- The dominant radiation source during component transfer is the activated first-wall and blanket modules, which are the most heavily irradiated components
- Photon-induced neutrons (from \(^{16}\)O in activated water coolant and \(^{9}\)Be) create a secondary neutron field that must be shielded separately
- Total dose rates at the transfer cask exterior exceed 0.1 Sv hr\(^{-1}\) during blanket transfers, requiring robot manipulators with radiation-hardened electronics rated to >10\(^6}\) Gy cumulative dose

### 6.2 ITER and DEMO Remote Handling Systems

The ITER Remote Handling (RH) system uses a **comprehensive in-vessel viewing system**, a fixed-mounted blanket transfer system, a divertor remote handling system, and a tokamak services manipulator. These systems must:
- Disassemble and reassemble blanket module bolted connections using force-feedback robotic tools rated for >10\(^5\) Gy[^14]
- Transfer multi-tonne blanket modules (each ~4 tonnes for ITER) through 0.44 m × 1.68 m equatorial ports with sub-centimeter positioning accuracy[^13][^14]
- Inspect plasma-facing surfaces with sufficient spatial resolution to identify erosion, cracking, or blistering before it becomes a machine-risk

For DEMO, which will have longer pulses and higher neutron fluences, the RH challenge is substantially harder:[^13]
- DEMO blanket segments are expected to require replacement every ~4 calendar years, implying 5–7 full blanket change-outs over a 20-year reactor operational life[^7]
- Each change-out is a multi-month shutdown operation requiring thousands of individual robotic manipulations
- DEMO RH systems must be designed for **higher radiation hardness** (cumulative dose >10\(^7\)–10\(^8\) Gy for in-vessel electronics), higher force (larger, heavier blanket modules), and higher reliability (fewer humans available for recovery from failed manipulations) than ITER

Pre-conceptual assessments confirm that the overall RH maintenance schedule is one of the main drivers of DEMO availability factor, and hence levelized cost of electricity. Remote maintenance is not a solved problem but an active engineering development that will consume a significant fraction of DEMO design effort.[^13]

### 6.3 Stellarator-Specific Remote Maintenance Penalties

For stellarators, the 3D coil geometry creates a fundamentally harder maintenance problem than tokamaks:[^43][^44][^45][^46]
- The plasma-bounding surface and the coils are non-axisymmetric; blanket modules must have complex 3D shapes to fill the non-uniform space between plasma and coils
- A single HELIAS 5-B stellarator reactor would require **hundreds of geometrically unique blanket modules** of varying shapes, each requiring a tailored robotic handling tool
- Port access is constrained to specific positions in the 3D structure; standard ITER-type large equatorial port access is not available in most stellarator designs
- Neutronics analysis of the HELIAS design shows that the current design **cannot fulfill the coil shielding limits** specified for DEMO in the most constrained areas due to limited radial space, requiring innovative compact shield solutions that have not yet been designed or tested[^45][^47]

The ITER/DEMO remote maintenance approach, which is already highly challenging for an axisymmetric tokamak, becomes qualitatively harder for a stellarator — and no prototype stellarator maintenance system has been demonstrated at reactor scale.

***

## Part VII — Technology Readiness Landscape

### 7.1 IFMIF-DONES: The Missing Cornerstone Facility

**IFMIF-DONES** (International Fusion Materials Irradiation Facility – DEMO-Oriented Neutron Source) is a planned accelerator-based neutron source in Granada, Spain, designed to deliver a 14 MeV neutron flux of ~10\(^{18}\) n m\(^{-2}\) s\(^{-1}\) in a 500 cm\(^3\) test volume, at temperatures of 250–550 °C. The Multilateral International DONES Agreement was signed in November 2025, marking a formal international commitment to the facility.[^48][^49][^3]

IFMIF-DONES will enable:[^49][^50][^48]
- Accumulation of ~20 dpa per full power year in the high-flux zone — the first time reactor-relevant fluences will be achievable in controlled experiments
- Simultaneous irradiation of EUROFER97, ODS steels, W alloys, and SiC/SiC at relevant temperatures and helium co-generation rates
- Production of the materials qualification database needed for DEMO licensing

IFMIF-DONES is **under construction** **[corr. 2026-11]**: the multilateral agreement was signed in November 2025, the building permit was granted on 16 June 2026 and preparatory works on the Main Building began in September 2026, with completion targeted for ~2029. First neutrons are not officially dated (~2033–2035 is most often cited), and ≥ 10 dpa data will follow some years later. This means DEMO — scheduled for operation ~2050 — will have only a narrow window for materials qualification before first-wall design must be frozen.

### 7.2 Material Candidates: Technology Readiness Summary

| Material | Application | Key Advantage | Critical Limitation | TRL |
|---|---|---|---|---|
| Pure W armor | First wall / divertor | Highest sputtering resistance, low T retention (unirradiated) | Brittle post-irradiation, transmutation, DBTT >> 800 °C | 5–6 |
| ODS-W | First wall armor | Reduced void swelling, nano-bubble trapping | No nuclear code qualification, complex fabrication | 3 |
| W\(_f\)/W composite | First wall armor | Pseudo-ductility, crack arrest | Lab-scale only, no irradiation data at fusion fluence | 2–3 |
| EUROFER97 (RAFM) | Blanket structure | Qualified material, established production | Narrow temperature window (350–550 °C), no fusion neutron data | 5 |
| F82H (RAFM) | Blanket structure | Best-characterized RAFM globally | Same as EUROFER97 | 5 |
| ODS-EUROFER | Blanket structure | Extended T\(_{max}\), better He tolerance | No design code qualification, W redistribution concern[^36] | 3–4 |
| SiC/SiC composite | Advanced blanket | Ultra-high T, very low activation | No structural joints, no code qualification, cost | 3–4 |
| Liquid Li/Sn PFC | Divertor replacement | Renewing surface, high heat flux tolerance | Evaporation, tritium inventory, corrosion, MHD interaction[^51][^52] | 3 |

***

## Part VIII — Open Research Questions and Analysis Entry Points

### Tungsten Armor and Transmutation

- **Q1.1**: What is the actual microstructural evolution of W under simultaneous 14 MeV neutron, He, and D bombardment at 600–800 °C to doses of 20–50 dpa? Does the combined damage accelerate void swelling, He bubble formation, or brittle phase precipitation beyond predictions from separate irradiation campaigns?
- **Q1.2**: Can ODS-W or W\(_f\)/W composites suppress RTT-driven DBTT shift to below the minimum operating temperature (~400 °C) at 20+ dpa, while maintaining acceptable thermal conductivity (>40 W m\(^{-1}\) K\(^{-1}\))?
- **Q1.3**: At what W transmutation level (Re+Os at.%) do σ-phase or χ-phase precipitates appear in reactor conditions, and can phase stability be controlled by alloying additions or heat treatment protocols?

### Tritium Retention

- **Q2.1**: Does the \(t^{0.5}\) tritium retention scaling in irradiated W hold indefinitely, or does saturation occur at accessible exposure times? What is the steady-state tritium inventory prediction for a DEMO first wall over a 10 full-power-year operational period?
- **Q2.2**: What is the minimum wall temperature needed to prevent tritium accumulation beyond the DEMO safety limit? Is this compatible with blanket coolant design constraints?
- **Q2.3**: Can real-time tritium monitoring via laser-induced desorption spectroscopy or soft X-ray fluorescence provide actionable wall conditioning feedback in DEMO?

### Structural Materials and Qualification

- **Q3.1**: What is the DBTT shift in EUROFER97 and ODS-EUROFER irradiated to 40–70 dpa at 400–550 °C with the fusion neutron spectrum (he/dpa ratio ~10–15 appm He/dpa)? This is the single most critical missing data point for blanket design
- **Q3.2**: Is there a viable joining technique for SiC/SiC composites that survives 14 MeV neutron irradiation to 20 dpa at 900 °C without strength degradation?
- **Q3.3**: What is the minimum timeline from first IFMIF-DONES operation to a qualified DEMO structural materials database, and can design code qualification (RCC-MRx extension or ASME III) run in parallel?

### Remote Maintenance

- **Q4.1**: What is the optimal stellarator blanket module design strategy — maximizing coverage while enabling robotic replacement — for a HELIAS-type reactor with fixed coil topology?
- **Q4.2**: Can radiation-hardened electronics at >10\(^8\) Gy cumulative tolerance be developed using SiC or diamond-based semiconductor technology for in-vessel DEMO robotic systems?
- **Q4.3**: What is the DEMO availability factor achievable with the current blanket replacement frequency (~4 fpy) and RH system maintenance scheduling, and what availability is required for economic electricity generation?

### ICF-Specific Wall and Optics

- **Q5.1**: What first-wall material or geometry (dry wall, wetted wall, liquid jet blanket) can survive \(10^{10}\) microexplosion shots while maintaining the geometric precision needed for target injection alignment?
- **Q5.2**: Can grazing-incidence metal mirrors or gas final optics schemes survive IFE-relevant 14 MeV neutron fluences while maintaining sufficient reflectivity and optical figure quality for coherent beam delivery?

***

## Conclusion

The plasma-facing materials and neutron damage challenge is simultaneously a materials science problem, a nuclear engineering problem, and a facility problem. Progress on materials is blocked by the absence of a fusion-representative irradiation facility; progress on facility construction is dependent on political and funding decisions; and the materials data needed to design DEMO is on the critical path for DEMO licensing — potentially the tightest timeline bottleneck in the entire fusion development program.

The most urgent single action is the construction and operation of IFMIF-DONES — not because it will solve the materials problem, but because it is a prerequisite for even characterizing it. Without it, all DEMO first-wall and blanket material choices rest on extrapolations across three distinct unknowns: neutron spectrum, combined plasma+neutron environment, and fusion-relevant fluence. The risk of a late-stage materials failure discovery — after DEMO design is frozen and procurement has begun — is the scenario that most threatens the entire fusion development timeline.[^3]

---

## Review & Model Update (November 2026)

Scope and model architecture are described in the overview report. This section covers gate **MA**
(materials qualified for licensing) and the shared IFMIF-DONES node.

### R.1 Currency and claim check

| ID | Location | Statement | Finding | Status |
|---|---|---|---|---|
| C2-01 | Executive summary | DONES agreement signed Nov 2025 | Consistent with later milestones: building permit 16 Jun 2026 [R29]; Main Building preparatory works since Sep 2026, completion ~2029 [R30] (secondary) | confirmed |
| C2-02 | Part VII 7.1 | "DONES not yet funded for construction as of 2026" | Contradicted by C2-01 and by the report's own executive summary | corrected |
| C2-03 | Part III 3.1 | 500 MW DEMO burns "184 g T/day" | Arithmetic error: 500 MW ≈ 75 g/day (1 GW ≈ 150 g/day) | corrected |
| C2-04 | Executive summary | "~20 dpa per full power year" | Upper end of estimates; not re-verified | flagged |
| C2-05 | Part III 3.3 | ITER switched to a full-W first wall (2024) | Confirmed: Baseline 2024 uses tungsten instead of beryllium [R33] | confirmed |
| C2-06 | Throughout | Laser ICF as one pathway | Split in R.2 | supplemented |

### R.2 Direct vs. indirect drive for this challenge

Both drive types load the chamber wall with the same 14 MeV neutron spectrum and with X-ray and ion pulses
from each shot (~10⁹–10¹⁰ shots over a plant's life). The differences:
- **Indirect drive** adds the hohlraum: several hundred milligrams of high-Z material (e.g. gold or lead) per
  shot that must be removed from the chamber and recovered. This raises erosion/redeposition and waste
  questions.
- **Direct drive** needs more symmetric illumination and therefore usually more beam ports and more final
  optics close to the chamber.
- Both are modelled with the same MA distribution; the coupling between direct and indirect MA is set to
  ρ = 0.7.

### R.3 TRL / licensing / funding view of Challenge 2

| Pathway | TRL | Licensing / permit | Funding |
|---|---|---|---|
| All pathways | Baseline materials (EUROFER97, W) are at materials-TRL ~4–5, without fusion-spectrum data. DONES is the gating facility [R29][R30]. | Activated components are the main waste and decommissioning topic. The NRC proposal opens a low-level-waste disposal path [R5]. In Germany, critics argue the Radiation Protection Act lacks comprehensive waste and decommissioning rules [R34]; the ReFus project is drafting application guidance [R12]. | DONES is publicly funded (Spain majority, EU, Italy, Japan, Croatia) [R30]. There are no private irradiation facilities at comparable scale. |
| Tokamak | Divertor erosion and remote-handling port access are manageable. | Standard. | — |
| Stellarator | 3D blanket and remote maintenance are harder (model: later MA gate). | Standard. | — |
| Direct / indirect drive | Final optics lifetime and chamber wall fatigue under 5–10 Hz pulsed loads; there is no rep-rated test chamber. | Indirect drive: high-Z debris recycling. | Private programmes fund chamber work only after the driver and implosion milestones. |

### R.4 Mapping to the risk model (gate MA)

- **MA** — Fusion-spectrum irradiation data to ≥ ~20 dpa accepted by the regulator; remote maintenance validated (ICF: chamber wall and final optics).

`<p>_ma = max(<p>_ma_eigen, g_dones + g_qual)`. DONES ≥ 10 dpa data: P0/P10/P50/P90/P100 =
2033/2035/2038/2043/2055 (`g_dones`, now partly verified, see C2-01). Qualification lag `g_qual` = 5 years.
Common show-stopper `g_f_material` = 0.02 (no economically durable structural material).

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | MA – Materials (pathway-specific) | 2034 / 2040 / 2046 / 2057 / 2080 | 0.05 | `tok_ma_eigen`, `tok_f_ma` |
| Stellarator | MA – Materials (pathway-specific) | 2036 / 2043 / 2050 / 2063 / 2090 | 0.10 | `stl_ma_eigen`, `stl_f_ma` |
| Direct Drive | MA – Materials (pathway-specific) | 2036 / 2042 / 2050 / 2065 / 2090 | 0.15 | `dir_ma_eigen`, `dir_f_ma` |
| Indirect Drive | MA – Materials (pathway-specific) | 2036 / 2042 / 2050 / 2065 / 2090 | 0.15 | `ind_ma_eigen`, `ind_f_ma` |

### R.5 Open items

- dpa rates and replacement intervals were not re-verified.
- The DONES first-neutron date is unofficial.
- The EU-funded share of DONES construction is reported only in a secondary summary [R30].

### Sources for this review

Accessed 3 November 2026. Secondary sources are marked as such; claims resting only on them are flagged in the tables above.

- **[R5]** US NRC, proposed rule 'Regulatory Framework for Fusion Machines', Federal Register 26 Feb 2026 (10 CFR Part 30). <https://www.federalregister.gov/documents/2026/02/26/2026-03865/regulatory-framework-for-fusion-machines>
- **[R12]** GRS, ReFus status report (draft for comment, status June 2026; published Aug 2026). <https://www.grs.de/de/aktuelles/refus-statusbericht>
- **[R29]** IFMIF-DONES España, building permit granted 16 Jun 2026. <https://ifmif-dones.es/?p=23730>
- **[R30]** Lovguiden summary of F4E news (21 Oct 2026) — first EU procurement arrangements; Main Building preparatory works since Sep 2026, completion ~2029 (secondary). <https://www.lovguiden.dk/en/det-offentlige/fusion-for-energy/2026-10-21-f4e-underskriver-de-foerste-to-indkoebsaftaler-for-ifmif-dones>
- **[R33]** ITER Organization, Baseline 2024 press conference summary (Jul 2024) — tungsten instead of beryllium first wall. <https://iter.org/sites/default/files/media/2024-07/baseline_press_conference_summary_july-2024_b.pdf>
- **[R34]** .ausgestrahlt, 'Kernfusion im Strahlenschutzgesetz – reicht das?' (15 Jul 2026) — NGO critique: waste and decommissioning gaps (position source). <https://www.ausgestrahlt.de/blog/2026/07/15/kernfusion-im-strahlenschutzgesetz-reicht-das/>

---

## References

1. [Journal of Nuclear Materials - UKAEA Scientific Publications](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss38.pdf)

2. [Studying the Interaction of Plasma with Irradiated Tungsten and ...](https://www.iaea.org/newscenter/news/studying-the-interaction-of-plasma-with-irradiated-tungsten-and-tungsten-alloys-in-fusion-devices-f43021) - Controlled nuclear fusion is widely accepted as one of the best long-term hopes for meeting the worl...

3. [International agreement signed for fusion materials research facility](https://www.world-nuclear-news.org/articles/international-agreement-signed-for-fusion-materials-research-facility) - Fusion for Energy, representing the European Commission and Member States' contribution, together wi...

4. [[PDF] ITER and DEMO – Technology Challenges on the Way to Fusion ...](https://publikationen.bibliothek.kit.edu/1000162053/155551872) - According to momentum conversation, 80% of the reaction energy (i.e., 14.1 MeV) is carried by the ne...

5. [1](https://ftg.demokritos.gr/sites/default/files/publications/chatzikos_exp_neutron_w_fusengdes_2024.pdf)

6. [[PDF] 1 Recent Status and Improvement of Reduced-Activation Ferritic ...](https://www.osti.gov/servlets/purl/1286969) - Reduced-activation ferritic-martensitic (RAFM) steels, candidate structural materials for fusion rea...

7. [PowerPoint-Präsentation](https://iea.blob.core.windows.net/assets/imports/events/333/Item_5_M._RIETH_.pdf)

8. [[PDF] Materials for DEMO and Reactor Applications - Boundary Conditions ...](https://pure.mpg.de/rest/items/item_2242719_4/component/file_2461513/content)

9. [New insights into microstructure of neutron-irradiated tungsten - Scientific Reports](https://www.nature.com/articles/s41598-021-86746-6) - The development of appropriate materials for fusion reactors that can sustain high neutron fluence a...

10. [the challenges of plasma material interactions in nuclear ...](https://www.osti.gov/servlets/purl/1394140)

11. [Post Neutron Irradiation Recovery and Recrystallization of ...](https://ftg.demokritos.gr/sites/default/files/publications/papadakis_metals-15-00172_2025.pdf)

12. [[PDF] Neutronic Performance Issues of the Breeding Blanket Options ... - KIT](https://publikationen.bibliothek.kit.edu/230102188/3816906) - Displacement damage rate to steel [dpa/fp y]. Radial distance from FW [cm]. (*)fpy = full power year...

13. [[PDF] Pre-conceptual design assessment of DEMO remote maintenance](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss125.pdf)

14. [Remote Handling Systems](https://www.vltfusion.org/areas-of-research/remote-handling-systems/)

15. [Mechanisms of helium irradiation blistering and surface deformation in tungsten](https://www.sciencedirect.com/science/article/pii/S1359645423003245) - Helium irradiation blistering in tungsten is of intense interest for plasma-facing materials under f...

16. [The mobility of small vacancy/helium complexes in tungsten and its impact on retention in fusion-relevant conditions - PubMed](https://pubmed.ncbi.nlm.nih.gov/28559588/) - Tungsten is a promising plasma facing material for fusion reactors. Despite many favorable propertie...

17. [[PDF] §27. Bubble Formation in Tungsten Material under Helium Plasma ...](https://www.nifs.ac.jp/report/annrep16/pdf/383.pdf) - Many experimental studies reported bubble formation on the surface of tungsten materials under heliu...

18. [Plasma and Fusion Research,ISSN 1880-6821](https://www.jstage.jst.go.jp/article/pfr/13/0/13_1205084/_pdf)

19. [[PDF] INVESTIGATION OF PLASMA WALL INTERACTIONS BETWEEN ...](https://pure.mpg.de/rest/items/item_3383795_4/component/file_3385859/content)

20. [Fuzz formation on grain-refined bulk tungsten surfaces after low energy helium plasma exposure](https://www.sciencedirect.com/science/article/abs/pii/S0167577X21016189)

21. [Tungsten fuzz: Deposition effects and influence to fusion devices](https://www.sciencedirect.com/science/article/pii/S2352179120300995) - Helium (He) plasma irradiation to tungsten leads to formation of He bubbles and fiberform nanostruct...

22. [Discovering tungsten-based composites as plasma facing materials for future high-duty cycle nuclear fusion reactors - Scientific Reports](https://www.nature.com/articles/s41598-024-64614-3) - Despite of excellent thermal properties and high sputtering resistance, pure tungsten cannot fully s...

23. [Recent Advances on Hydrogen Retention in ITER’s Plasma-Facing Materials: Beryllium, Carbon, and Tungsten](https://www.tandfonline.com/doi/full/10.13182/FST54-891) - Management of tritium inventory remains one of the grand challenges in the development of fusion ene...

24. [Retention of Fuel Hydrogen Retention of Tungsten Plasma Facing ...](https://www.scientific.net/MSF.721.211) - In-vessel tritium inventory in fusion reactors has to be reduced from a view point of safety in fusi...

25. [Print](https://www.iter.org/print/whatsnew/409)

26. [IT/P3-18](https://www-pub.iaea.org/MTCD/Meetings/PDFplus/fusion-20-preprints/IT_P3-18.pdf)

27. [[PDF] Tungsten divertor erosion in all metal devices: lessons from the ITER ...](https://pure.mpg.de/rest/items/item_2145197_1/component/file_2145196/content) - Nitrogen seeding initially increased the tungsten sputtering threefold due to higher extrinsic impur...

28. [[PDF] PHYSICS BASIS, IMPLICATIONS FO - iaea-indico](https://conferences.iaea.org/event/392/papers/35653/files/13834-Loarte_FEC_2025_revised_final.pdf)

29. [[PDF] P3-29 DIVIMP modelling of tungsten impurity transport in ITER](https://pure.mpg.de/rest/items/item_2143211/component/file_2143210/content)

30. [The National Ignition Facility - International Atomic Energy ...](https://www-pub.iaea.org/MTCD/publications/PDF/csp_008c/pdf/if_3.pdf)

31. [[PDF] Gas and Plasma Final Optics for Inertial Fusion Energy Lasers](https://lasers.llnl.gov/sites/lasers/files/2023-11/edwards-LLNL-IFE-workshop-2022.pdf)

32. [Effect of Processing on Microstructural ...](https://scipub.euro-fusion.org/wp-content/uploads/eurofusion/WPMATPR17_17182_submitted.pdf)

33. [[PDF] Development of Reduced Activation Ferritic/Martensitic Steel - iferc](https://www.iferc.org/wp/wp-content/uploads/2021/03/news-2013-11.pdf) - Reduced activation ferritic/martensitic (RAFM) steels have been developed as structural materials fo...

34. [paper.v1.pdf](https://www-pub.iaea.org/mtcd/publications/pdf/csp_019c/pdf/ft1_1rb.pdf)

35. [28th IAEA Fusion Energy Conference (FEC 2020)](https://conferences.iaea.org/event/214/contributions/17100/contribution.pdf)

36. [High-Cr ODS Steels Perform Well under Neutron Irradiation - LinkedIn](https://www.linkedin.com/posts/prof-amy-gandy-66807362_performance-of-high-cr-ods-steels-under-high-temperature-activity-7396549055419412480-58Te) - I'd like to highlight a recent publication by Viacheslav Kuksenko with Alex Dickinson-Lomas, Murthy ...

37. [Silicon carbide composites as fusion power reactor structural materials](https://www.sciencedirect.com/science/article/abs/pii/S0022311511002637) - Silicon carbide was first proposed as a low activation fusion reactor material in the mid 1970s. How...

38. [(FT/P1-03) Neutron Tolerance of Advanced SiC-Fiber / CVI-SiC ...](https://www-pub.iaea.org/mtcd/publications/pdf/csp_019c/html/node345.htm) - Fusion blankets employing a silicon carbide (SiC) fiber-reinforced SiC matrix composite (SiC/SiC com...

39. [Microsoft Word - CN69FTP37.doc](https://www.osti.gov/etdeweb/servlets/purl/20261801)

40. [Stability of SiC and its composites at high neutron fluence](https://impact.ornl.gov/en/publications/stability-of-sic-and-its-composites-at-high-neutron-fluence/) - The Hi-Nicalon™ Type-S, CVI SiC composite retained the pre-irradiation strength and the non-linear f...

41. [Assessment of ITER radiation environment during the remote-handling operation of In-Vessel components with D1SUNED - Scientific Reports](https://www.nature.com/articles/s41598-023-30534-x) - During ITER operational life, a remote-handled cask will be used to transfer In-Vessel components to...

42. [Neutronic Activation Analysis for ITER Fusion Reactor](https://static.sif.it/SIF/resources/public/files/congr14/ip/Caiffi.pdf)

43. [STELLARATOR FUSION REACTORS –– AN OVERVIEW](https://fire.pppl.gov/itc12_wobig_paper.pdf)

44. [1](https://www-pub.iaea.org/mtcd/meetings/fec2008/ft_p3-13.pdf)

45. [Use of Mesh based Variance Reduction Technique for ...](https://pure.mpg.de/rest/items/item_3155049_3/component/file_3156251/content)

46. [High-temperature superconducting strong-field stellarator with precise ...](https://www.sciencedirect.com/science/article/pii/S2666675823001650)

47. [Technical Meeting on Tritium Breeding Blankets and Associated Neutronics](https://conferences.iaea.org/event/406/contributions/37082/contribution.pdf)

48. [The IFMIF-DONES Project: Design Status and Main Achievements ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC9596351/) - IFMIF-DONES is a high-intensity neutron irradiation facility for qualification of fusion reactor mat...

49. [[PDF] IFMIF-DONES Project, Status and Opportunities - CDTI](https://www.cdti.es/sites/default/files/2023-12/230224dones-v3.pdf) - What is IFMIF-DONES? A fusion-like neutron source required for the qualification of the materials to...

50. [20250122_Early Neutron Source IFMIF-DONES_Synopses-IAEA-FEC_DJR](https://conferences.iaea.org/event/392/contributions/35649/attachments/19723/33771/Synopsis_Jimenez-Rey_IAEA-FEC-2025.V1.1.pdf)

51. [Plasma Facing Components Beyond ITER – Liquid Materials](https://www.iter.org/sites/default/files/education/%5B5-2%5D25JAN2019_Andruczyk.pdf)

52. [Liquid Metal Plasma Facing Component Research for the ...](https://fire.pppl.gov/FESAC_WP_LiqMetalPFC_Jaworski.pdf)
