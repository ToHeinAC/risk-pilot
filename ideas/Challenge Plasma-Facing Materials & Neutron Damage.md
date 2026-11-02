# Nuclear Fusion — Deep Dive: Challenge 2
## Plasma-Facing Materials (PFMs) & Neutron Damage

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — November 2026 update*

***

## Executive Summary

Plasma-facing materials and the neutron damage they sustain represent the most extreme materials engineering problem ever attempted. A commercial fusion reactor first wall must simultaneously withstand 14.1 MeV neutron bombardment producing ~10–15 dpa per full power year in the front-wall steel of a DEMO-class machine, continuous steady-state heat fluxes of 1–10 MW m\(^{-2}\), intense helium and hydrogen ion bombardment from the plasma, and — in tokamaks — episodic ELM and disruption transients that transiently multiply heat loads by factors of 10–50. No material known today can meet all of these requirements simultaneously at reactor scale over the multi-year lifetimes required.[^1]

The fundamental difficulty is compounded by a critical epistemic gap: no facility in the world can yet expose materials simultaneously to fusion-relevant 14 MeV neutron fluxes and the full plasma environment. The IFMIF-DONES facility in Granada is the first dedicated attempt to close this gap. Its Multilateral International DONES Agreement was signed in November 2025 with construction cost shares committed (Spain 55 %, EU via F4E 25 %, Italy 8 %, Japan 5.1 %, Croatia 5 %), and on-site works for the Main Building started in September 2026, with the building targeted for substantial completion in 2029. No official first-neutron date has been published; the older EU target of ~2034 remains the most-cited figure, and useful ≥10 dpa data are unlikely before the late 2030s (Section 7.1).[^2][^3][^53][^54] Until then, all material qualification rests on extrapolation from ion-beam, fission-neutron, and separate plasma-exposure experiments, each of which captures only a subset of the true reactor environment.[^2][^3]

This report provides a deep-dive analysis of six interconnected sub-challenges: (1) neutron displacement damage and transmutation; (2) helium bubble formation, tungsten fuzz, and blistering; (3) tritium retention in PFMs; (4) erosion, redeposition, and impurity influx to the plasma; (5) structural material qualification for blankets and shielding; and (6) remote maintenance in the neutron-activated reactor environment. Each challenge is mapped across Tokamak, Stellarator, and Laser ICF pathways.

***

## Part I — Neutron Displacement Damage and Transmutation

### 1.1 The 14 MeV Neutron Problem

In a DT fusion reactor, 80% of fusion energy is carried by 14.1 MeV neutrons. This energy is far above the thresholds for nuclear reactions in structural materials. Unlike fission reactors, which produce neutrons with a mean energy of ~2 MeV, fusion neutrons have sufficient energy to:[^4]
- Create **primary knock-on atoms (PKA)** with energies up to several hundred keV, producing displacement damage cascades that generate thousands of Frenkel pairs per neutron interaction
- Transmute target nuclei through (n,p), (n,α), and (n,γ) reactions, generating helium, hydrogen, and new alloying species within the material lattice[^5][^2]

For tungsten armor on the divertor, the expected damage rate in DEMO is **3 dpa per full power year (fpy)** for the divertor armor, **6–9 dpa/fpy** for the first-wall armor, and **12–15 dpa/fpy** in the first-wall steel structure. Over ~5 full power years these rates accumulate to ~30–45 dpa in first-wall tungsten armor and ~60–75 dpa in the first-wall steel. Note that fpy ≠ calendar years: at the ~30–50 % availability assumed for early DEMO phases, 5 fpy corresponds to 10–15 calendar years. The EU DEMO strategy therefore uses a **starter blanket limited to ~20 dpa** (steel) followed by a second blanket designed for ~50 dpa.[^6][^7][^8][^1]

### 1.2 Tungsten Transmutation: The Re/Os/Ta Problem

Tungsten is the reference plasma-facing armor material. Under 14 MeV neutron bombardment, W undergoes the following primary nuclear reactions:[^5][^2]

\[^{186}\text{W}(n,\gamma) \rightarrow ^{187}\text{W} \xrightarrow{\beta^-} ^{187}\text{Re}\]
\[^{187}\text{Re}(n,\gamma) \rightarrow ^{188}\text{Re} \xrightarrow{\beta^-} ^{188}\text{Os}\]

Over 5–10 full power years, these transmutation chains are calculated to produce **several at.% Re and of order 1–3 at.% Os** in the most neutron-exposed tungsten (inventory calculations vary strongly with position, spectrum and armor thickness; the frequently quoted "10 at.% Re" applies only to the most thermalised-spectrum locations and long exposures and could not be verified as a generic DEMO value). Because (n,γ) rates depend on the softened spectrum behind the armor, IFMIF-DONES reproduces DEMO transmutation reasonably well for EUROFER97 but shows "large discrepancies" for W and CuCrZr at the location studied — i.e. W transmutation effects will remain partly a modelling question even after DONES.[^5][^60] This has several compounding consequences:[^5]
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

For the EU DEMO starter blanket (EUROFER97), the design life is approximately **1.33–1.7 full power years (≈20 dpa ÷ 12–15 dpa/fpy), or ~4–5 calendar years at early-phase availability**, before the damage dose reaches the design limit of ~20 dpa in the front-wall steel. This implies that the entire in-vessel component set — first wall, blanket modules, divertor cassettes — must be replaced multiple times over the reactor operational lifetime, each replacement operation conducted remotely in a high-radiation environment.[^7][^13][^14]

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
- The combined He bubble density in neutron-damaged W is expected to be substantially higher than in He-only exposures at equivalent fluence, accelerating blistering kinetics (a specific "50–100×" factor quoted in earlier versions of this report could not be traced to a primary source and has been dropped)
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

Tritium that becomes trapped in plasma-facing materials is lost from the fuel cycle, must be periodically removed by baking or isotopic exchange, and — if accumulated beyond a regulatory limit — can trigger a mandatory reactor shutdown for decontamination. In ITER, the in-vessel tritium inventory is limited by the safety case to the order of **0.7–1 kg** (the exact figure depends on how measurement uncertainty is accounted). DT fusion consumes ~0.15 g of tritium per MW·day of fusion power (17.6 MeV per triton), i.e. **~76 g T/day at 500 MW** and **~300 g T/day for a ~2 GW EU DEMO**; a retention of even 0.1–1 % of the fuel throughput (which is far larger than the burn, given burn fractions of a few %) would approach such limits within months of full-power operation.

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

The plasma bombards PFMs with energetic ions and charge-exchange neutrals. **Physical sputtering** occurs when the energy transferred to a surface atom exceeds its surface binding energy (~8.8 eV for W); because of the poor mass match, the threshold *incident* energy for D on W is ~200 eV, so in practice W sputtering is dominated by heavier impurity and seeding ions (Be, C, N, Ne, Ar) and by W self-sputtering. The sputtering yield for W is extremely low (\(Y \sim 10^{-4}\) at relevant divertor conditions) compared to carbon, which was the original reason for selecting W. However:[^27]

- Under ELMs, transiently high particle energies increase sputtering yields by a factor of **5×** over the inter-ELM level, with intra-ELM sputtering dominating the total erosion budget[^27]
- Beryllium and other impurity ions, even at **0.1% concentration in the incident plasma**, produce the dominant W sputtering because their higher sputtering yield and lower mass create more efficient momentum transfer[^27]
- Under nitrogen impurity seeding (used for divertor detachment and heat load reduction), initial W sputtering **increases threefold** before the cooling effect of N lowers electron temperature enough to reduce sputtering below the nitrogen-free level[^27]
- **Prompt redeposition** — W sputtered from the surface that is immediately ionized and returned to the surface by the magnetic field within one gyro-orbit — accounts for **>50% of gross W erosion at high field**, significantly reducing net erosion. At ITER field (~5 T), prompt redeposition may reduce net erosion by 70–80% in normal operation. However, this benefit disappears during disruptions when prompt redeposition is disrupted by rapidly changing fields[^27]

### 4.2 Transport of Eroded W to the Plasma Core

Tungsten that escapes the divertor as W\(^{0}\) or low-ionization-state ions is swept toward the plasma core by SOL flows. In the hot core, partially ionised high-Z W ions emit intense line radiation (with smaller bremsstrahlung and recombination contributions) that can cause core cooling and threaten plasma stability. Even **W concentrations of 2–5 × 10\(^{-5}\)** (relative to electron density) can cause significant core radiation losses in tokamaks.[^28][^29]

ITER's strategy to manage W influx involves:[^28][^25]
- Operating the divertor in **detached** plasma conditions, where the plasma temperature at the target is lowered to ~1–5 eV (vs. ~30 eV in attached conditions), reducing the kinetic energy of bombarding ions below the sputtering threshold
- **Boronization** of the first wall: deposition of thin boron coatings by glow-discharge in B-containing gases creates low-Z gettering layers that preferentially trap impurities and reduce W erosion rates. However, boron coatings erode rapidly in regions of direct plasma contact and must be periodically replenished — the required frequency and completeness on a full-tungsten ITER wall is essentially untested[^25]
- Active **impurity seeding** (Ne, Ar) to radiatively cool the SOL and divertor, reducing peak target temperatures below the W sputtering threshold. This competes with ELM suppression and power exhaust requirements, requiring sophisticated operational optimization

During ITER plasma start-up (the "limiter phase" before a diverted configuration is established), the plasma contacts the tungsten main chamber wall directly at elevated temperatures. ITER simulations show that in this configuration, W erosion produces "intolerable W plasma concentrations of several percent" in limiter geometry, which could prevent the establishment of the diverted plasma entirely. This is a critical operational risk.[^29]

### 4.3 Erosion in Laser ICF

In ICF, the material challenge for the first wall is qualitatively different from MCF. Each microexplosion (a 40 MJ yield is ≈10 kg TNT equivalent at 4.184 MJ/kg; power-plant concepts with 100–1000 MJ yields correspond to ~25–240 kg TNT per shot) generates:
- A pulse of 14 MeV neutrons and X-rays impacting the chamber wall within ~100 ns
- Energetic ion debris (keV–MeV ions, including fast alphas and target material) impacting the wall over ~1 µs
- Cyclic thermomechanical stress at the repetition rate. **Shot-count arithmetic**: 5–10 Hz × 86 400 s/day = **4.3–8.6 × 10\(^5\) shots/day**, i.e. 1.6–3.2 × 10\(^8\) shots per calendar year at 100 % availability; over a 30-year life at ~85 % availability this is **~4–8 × 10\(^9\) shots** (order 10\(^{10}\) for 40 years at 10 Hz). Fatigue data in the 10\(^9\)–10\(^{10}\) cycle (very-high-cycle) regime under simultaneous irradiation do not exist for any candidate wall material.

The **final optics** (fused silica or KDP frequency-conversion crystals) face an additional challenge: at NIF (single-shot operation), optics at the highest-used fluence of 8 J cm\(^{-2}\) show damage initiation that accumulates and requires a recycle-and-mitigate loop; as an order of magnitude, ~100 full-energy shots — roughly NIF's annual cadence — would be reached by a 10 Hz plant in ~10 seconds. This is an illustrative comparison of laser-induced damage cadence, not a neutron-damage limit; neutron and gamma induced absorption (colour-centre formation in silica) adds a separate lifetime limit. Novel final optics concepts using grazing incidence metal mirrors, gas or plasma final optics, or liquid film optical surfaces are under development but at TRL 1–2.[^30][^31]

**2025–2026 developments (ICF).** NIF raised its record to **8.6 ± 0.45 MJ from 2.08 MJ on target (target gain ≈4.1)** in 2025, its eighth ignition shot; LLNL notes that a target gain approaching ~15 would be needed even for a zero-net-electric test facility, and plant designs assume gains of ~50–100 at several Hz.[^61] On the chamber side, the neutronics analysis of Xcimer Energy's **HYLIFE-III** thick-liquid-wall concept (FLiBe jets protecting the structural wall) reports a robust TBR > 1.2 and concludes that final optics can reach an adequate lifetime with moderate-temperature annealing — a modelling result, not experimental validation.[^62] Dry-wall assessments for HiPER-type chambers remain pessimistic: no dry first-wall material was found to withstand the ion pulses at reasonable repetition rates, and final lenses would not survive direct ion exposure.[^63] Thick liquid walls shift the problem from first-wall dpa to FLiBe chemistry, jet hydrodynamics at several Hz, and the activation and corrosion of the structure behind the jets.

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

### 5.4 HTS Tape Irradiation (as a Materials Question)

Compact high-field tokamaks and stellarators using REBCO tapes trade shield thickness for field, so the radiation tolerance of the tape sets the inboard shield and hence the machine size. Fission-reactor irradiations of commercial coated conductors (TU Wien, fast fluence up to 4.9 × 10\(^{22}\) m\(^{-2}\)) show a non-monotonic response: critical current first rises (radiation defects act as pinning centres) and then falls below its initial value at ~2 × 10\(^{22}\) m\(^{-2}\) (E > 0.1 MeV) at 50 K, with tapes containing artificial pinning centres degrading earlier.[^64] Open materials questions are (i) irradiation *at cryogenic temperature*, since defects frozen in at 20–30 K anneal differently from those created at room temperature — MIT's dedicated cryogenic neutron facility at the MIT reactor was still being commissioned in 2025 and no peer-reviewed results were found as of this update; and (ii) beam-heating artefacts in surrogate proton tests, which a 2025 study showed can masquerade as irradiation-induced I\(_c\) loss.[^65] The resulting fluence limit (~10\(^{22}\)–10\(^{23}\) m\(^{-2}\) fast neutrons over life) is a sizing constraint rather than a show-stopper, but it couples the materials gate to the magnet/compactness gate.

***

## Part VI — Remote Maintenance in Neutron-Activated Environments

### 6.1 The Radiation Environment After Shutdown

When a fusion reactor is shut down for maintenance, the neutron-activated structural materials become a distributed gamma-ray source whose intensity decays with complex multi-nuclide kinetics. In ITER, in-vessel remote-handling equipment is specified for gamma dose rates of order **~250 Gy h\(^{-1}\)** during maintenance; DEMO surface dose rates are estimated to be about two orders of magnitude higher, with blanket components at shutdown of order **13–17 kGy h\(^{-1}\)** (60 dpa steel) and divertor cassettes **9–12 kGy h\(^{-1}\)** (30 dpa), and roughly five years of cooling would be needed to reach ITER-like levels. Human in-vessel access is therefore excluded for the life of the plant; even after ~2.5 years cooling in a hot cell only remote or man-in-the-loop handling is feasible.[^55][^56] (An earlier version of this report quoted 10\(^5\)–10\(^6\) Sv h\(^{-1}\) for ITER; this is not supported by the sources and has been corrected.) Workers in the ITER Tokamak Building must not exceed an integrated annual dose of 20 mSv — requiring that even transfer operations conducted via the remote-handling cask system undergo detailed radiation transport calculations to confirm worker and electronics protection.[^41][^42][^14]

Decay gamma transport modeling for ITER identifies:[^41]
- The dominant radiation source during component transfer is the activated first-wall and blanket modules, which are the most heavily irradiated components
- Photon-induced neutrons (from \(^{16}\)O in activated water coolant and \(^{9}\)Be) create a secondary neutron field that must be shielded separately
- Total dose rates at the transfer cask exterior exceed 0.1 Sv hr\(^{-1}\) during blanket transfers, requiring robot manipulators with radiation-hardened electronics rated to >10\(^6\) Gy cumulative dose

### 6.2 ITER and DEMO Remote Handling Systems

The ITER Remote Handling (RH) system uses a **comprehensive in-vessel viewing system**, a fixed-mounted blanket transfer system, a divertor remote handling system, and a tokamak services manipulator. These systems must:
- Disassemble and reassemble blanket module bolted connections using force-feedback robotic tools rated for >10\(^5\) Gy[^14]
- Transfer multi-tonne blanket modules (up to ~4.5 tonnes each for ITER) through the equatorial ports with millimetre-level positioning accuracy[^13][^14]
- Inspect plasma-facing surfaces with sufficient spatial resolution to identify erosion, cracking, or blistering before it becomes a machine-risk

For DEMO, which will have longer pulses and higher neutron fluences, the RH challenge is substantially harder:[^13]
- DEMO blanket segments are expected to require replacement after the ~20 dpa starter-blanket phase (~4–5 calendar years) and then at ~50 dpa intervals; the number of change-outs over the plant life (several, the earlier "5–7" estimate assumed 20 dpa throughout) depends on whether higher-dose blankets can be qualified[^7]
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

**IFMIF-DONES** (International Fusion Materials Irradiation Facility – DEMO-Oriented Neutron Source) is an accelerator-based neutron source under construction in Escúzar (Granada), Spain. A 40 MeV, 125 mA continuous-wave deuteron beam (5 MW) strikes a 25 mm liquid-lithium jet flowing at ~15 m s\(^{-1}\), producing a broad neutron spectrum peaked near 14 MeV. The High-Flux Test Module (~850 specimens) is designed for **12–25 dpa/fpy**, with top-level requirements of >8–12 dpa/fpy in 0.3 L (20–30 dpa in < 2.5 years in ~300 cm³) and >16 dpa/fpy in 0.1 L (50 dpa in < 3 years), at 250–550 °C; the availability target is 70 % of calendar time. The DEMO first-wall flux it emulates is of order 10\(^{18}\) n m\(^{-2}\) s\(^{-1}\).[^48][^49][^3]

**Status (November 2026)**:[^3][^53][^54][^72][^73]
- **Agreement and funding**: the Multilateral International DONES Agreement (MIDA) was signed in Madrid in November 2025 by F4E (EU), Spain, Japan (QST), Croatia and Italy; cost shares are Spain 55 %, EU 25 % (€202 M, implying a construction budget of order €0.8 bn), Italy 8 %, Japan 5.1 %, Croatia 5 %. The earlier statement in this report that DONES was "not yet funded for construction" is no longer correct.
- **Construction**: the Escúzar building permit was granted in June 2026; the fourth Procurement Arrangement (buildings) was signed in August 2026 after arrangements for beam transport and the Test Cell; on-site preparatory works for the Main Building (accelerator and Test Cell) began in **September 2026**, excavation is planned before end-2026, foundations and structure in 2027, and the building is targeted to be **substantially complete in 2029**.
- **First neutrons**: no official date is published. F4E has cited operation "by 2034"; older plans (e.g. "first neutron early 2030s") have slipped. Given building completion in 2029, accelerator and lithium-loop installation and staged beam commissioning to 125 mA CW (which LIPAc in Rokkasho has demonstrated only in pulsed mode at 5 MeV so far, per available sources), **first neutrons in ~2033–2035** and full-power operation 1–2 years later is the realistic expectation used in this report.
- **Time to ≥10 dpa data**: at 12–25 dpa/fpy and ~70 % availability (lower during ramp-up), ~10 dpa takes ~1–1.5 calendar years of irradiation, followed by ~1 year of hot-cell post-irradiation examination. ≥10 dpa data are therefore expected **~2037–2039** (median), ~20 dpa data ~2039–2041.
- **Representativeness**: a 2026 JNM study finds DONES reproduces DEMO-like transmutation in EUROFER97 well, but not for W and CuCrZr at the position studied.[^60]

IFMIF-DONES will enable:[^49][^50][^48]
- Accumulation of >10 dpa per full power year in the high-flux zone — the first time reactor-relevant fluences with fusion-like He/dpa ratios will be achievable in controlled experiments
- Simultaneous irradiation of EUROFER97, ODS steels, W alloys, and SiC/SiC at relevant temperatures and helium co-generation rates
- Production of the materials qualification database needed for DEMO licensing (small-specimen test technique standards must be accepted by code bodies in parallel)

Even on the realistic schedule, EU DEMO — whose operation is now foreseen no earlier than the 2050s — has only a narrow window for materials qualification before first-wall design must be frozen, and private pilot plants targeting the 2030s will have to license **without** DONES data at the relevant dose.

### 7.1a Other Fusion-Relevant Neutron Sources and Test Stands (status Nov 2026)

| Facility | Type | Status (Nov 2026) | Relevance |
|---|---|---|---|
| LIPAc (Rokkasho, JP/EU) | DONES prototype accelerator (9 MeV, 125 mA) | 125 mA reached at 5 MeV in pulsed mode; CW and SRF-linac stages in progress (no confirmed CW full-current result found)[^58] | Key risk-reducer for DONES accelerator reliability |
| A-FNS (Rokkasho, JP) | D-Li source, 40 MeV/125 mA | Conceptual design complete; earlier "construction before 2025" target slipped; no construction decision found[^66] | Possible second DONES-class source; Japan now a MIDA partner instead |
| US FPNS | Fusion Prototypic Neutron Source | Risk-reduction activity final report to DOE (April 2025) found a D-Li stripping source sufficiently prototypic; DOE's June 2026 FS&T Roadmap commits to 3–5 years of R&D (D-Li, spallation, fusion-based, cyclotron options) and states FPNS access is "long-term of 5–10 years"; no construction decision[^59][^67] | Earliest plausible US data ~mid-2030s+ |
| MPEX (ORNL, US) | Linear plasma device, high-fluence PMI on (pre-)irradiated samples | Under construction, reported ~83 % complete (Jan 2026), operations planned 2027[^67] | Plasma + activated-sample synergy, not bulk neutron damage |
| HINEG / CFNS (Hefei, CN) | D-T neutron generator (HINEG ~6×10\(^{12}\) n/s) → proposed compact fusion neutron source | HINEG operating; CFNS described as a successor concept; no 2025–2026 construction confirmation found | 14 MeV spectrum but fluence orders of magnitude below DONES |
| Avalanche FusionWERX (Richland, US, private) | Orbitron-based D-T/D-D neutron test facility with hot cells and tritium licence | Launched 2025 with US$10 M Washington State grant; phased build; high-flux "uFPNS" stand only a future option[^68] | Low-dose component and blanket testing, not 10 dpa materials data |
| Kyoto Fusioneering UNITY-3 (ORNL, US, private–public) | Blanket/fuel-cycle test facility | Partnership announced Jan 2026; no schedule[^69] | Blanket integration, not high-dpa irradiation |
| Fission reactors (HFIR, BR2, MIT reactor) and ion beams | Surrogate | Operating; EUROfusion EUROFER97 qualification campaigns (incl. welds) currently cover 275–550 °C up to ~2 dpa[^70] | Bulk dpa without fusion He/dpa ratio |

No facility other than DONES has a funded path to ≥10 dpa with a fusion-like spectrum before the late 2030s. This is the central fact behind the neutron-source row of the risk model below.

### 7.2 Material Candidates: Technology Readiness Summary

| Material | Application | Key Advantage | Critical Limitation | TRL |
|---|---|---|---|---|
| Pure W armor | First wall / divertor | Highest sputtering resistance, low T retention (unirradiated) | Brittle post-irradiation, transmutation; irradiated DBTT may exceed the operating temperature | 5–6 |
| ODS-W | First wall armor | Reduced void swelling, nano-bubble trapping | No nuclear code qualification, complex fabrication | 3 |
| W\(_f\)/W composite | First wall armor | Pseudo-ductility, crack arrest | Lab-scale only, no irradiation data at fusion fluence | 2–3 |
| EUROFER97 (RAFM) | Blanket structure | Industrial heats and RCC-MRx data base in preparation; fission data to ~70 dpa at low T | Narrow temperature window (350–550 °C), no fusion neutron data; not yet code-qualified for irradiated design | 5 |
| F82H (RAFM) | Blanket structure | Best-characterized RAFM globally | Same as EUROFER97 | 5 |
| ODS-EUROFER | Blanket structure | Extended T\(_{max}\), better He tolerance | No design code qualification, W redistribution concern[^36] | 3–4 |
| SiC/SiC composite | Advanced blanket | Ultra-high T, very low activation | No structural joints, no code qualification, cost | 3–4 |
| Liquid Li/Sn PFC | Divertor replacement | Renewing surface, high heat flux tolerance | Evaporation, tritium inventory, corrosion, MHD interaction[^51][^52] | 3 |

EUROfusion itself rates its baseline materials (EUROFER97, W, CuCrZr) at **Materials TRL ~4–5**, with MTRL 7 — which requires system-level integration and fusion-relevant post-irradiation testing, i.e. DONES data — as the target for DEMO.[^57]

### 7.3 Integrated PWI Evidence 2025–2026

Long-pulse operation with tungsten walls advanced markedly: WEST (CEA, all-W) held a 1337 s hydrogen plasma in February 2025 (2.6 GJ injected and extracted), after EAST's 1066 s in January 2025.[^71] These pulses provide the first steady-state PFC fluence and W-wall conditioning data relevant to ITER's 2024 decision to replace the Be first wall by W with boronization, but they are non-nuclear (no DT neutrons) and at low heating power (~2 MW), so they do not reduce the neutron-damage uncertainty.
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

The plasma-facing materials and neutron damage challenge is simultaneously a materials science problem, a nuclear engineering problem, and a facility problem. Progress on materials is blocked by the absence of a fusion-representative irradiation facility; the political and funding decision for the key facility was finally taken in November 2025 and construction started in 2026, but its schedule to useful dose now sets the pace; and the materials data needed to design DEMO is on the critical path for DEMO licensing — potentially the tightest timeline bottleneck in the entire fusion development program.

The most urgent single action is the on-schedule construction and commissioning of IFMIF-DONES — not because it will solve the materials problem, but because it is a prerequisite for even characterizing it. Without it, all DEMO first-wall and blanket material choices rest on extrapolations across three distinct unknowns: neutron spectrum, combined plasma+neutron environment, and fusion-relevant fluence. The risk of a late-stage materials failure discovery — after DEMO design is frozen and procurement has begun — is the scenario that most threatens the entire fusion development timeline.[^3]

***

## Risk Assessment (November 2026)

### Risk register

| ID | Risk | Pathway(s) | Likelihood | Impact on schedule (years) / on feasibility | Early indicator | Mitigation |
|---|---|---|---|---|---|---|
| MA-1 | IFMIF-DONES first neutrons slip beyond 2035 (accelerator CW reliability at 125 mA, Li-loop, licensing, cost growth) | All | med | +3–5 y on all gates / none | Main Building not substantially complete in 2029; LIPAc fails to show CW high-current operation; further MIDA partners not joining | Staged commissioning at reduced current; parallel FPNS/A-FNS; keep LIPAc running |
| MA-2 | EUROFER97 shows unacceptable embrittlement or swelling at 10–20 dpa with fusion He/dpa, forcing an alloy change | Tokamak, Stellarator | low–med | +6–10 y / design margins shrink, plant availability falls | First DONES 5–10 dpa PIE; fission-plus-He-implantation tests | Qualify ODS-EUROFER and advanced RAFM in parallel; design starter blanket at low dose |
| MA-3 | Tungsten armor/divertor: irradiation and Re/Os transmutation embrittlement causes cracking under ELM/thermal cycling | Tokamak (Stellarator less, no ELMs in optimised configs) | med | +2–5 y / lower divertor lifetime, more remote maintenance | Cracking in ITER/WEST high-fluence campaigns; DONES W results (spectrum not fully representative) | Wf/W, W-laminates, liquid-metal divertor back-up, conservative heat-flux design |
| MA-4 | Tritium retention in neutron-damaged W exceeds inventory limits | Tokamak, Stellarator | med | +2–4 y / operating limits, baking requirements | Retention data on neutron-damaged W; ITER DT operation (~2039+) | Hot walls (>500 °C), periodic baking, isotope exchange, W-based alloys with fewer traps |
| MA-5 | Design-code qualification (RCC-MRx, ASME III Div. 4) lags data by >5 y; small-specimen techniques not accepted | All | med–high | +3–6 y / none | Code-body acceptance of DONES small-specimen standards; NRC/ONR guidance on fusion structural codes | Start code cases now with fission data; regulators' proportionate fusion frameworks |
| MA-6 | Remote maintenance cannot meet availability target (change-out > 6–12 months, RH equipment failure at kGy/h) | Tokamak, Stellarator (higher) | med | +3–8 y / economic feasibility | ITER RH commissioning and first in-vessel interventions; DEMO RH mock-ups; stellarator 3D module studies | Large vertical ports, segmented blankets, rad-hard electronics, shielding of RH tools |
| MA-7 | Stellarator 3D blanket/shield cannot satisfy coil-shielding and maintainability simultaneously | Stellarator | med | +5–10 y / possible show-stopper for compact designs | Integrated neutronics + RH designs from Type One, Proxima, Thea, IPP | Larger coil–plasma distance, simplified coil designs, liquid blankets |
| MA-8 | ICF first wall / liquid-jet chamber fails very-high-cycle (10\(^9\)–10\(^{10}\)) fatigue or jet re-establishment at ≥ 5 Hz | Laser ICF | med–high | +5–10 y / feasibility | Rep-rated chamber test stands; jet re-formation data at Hz rates | Thick liquid walls (HYLIFE-III), larger chambers, lower rep-rate/higher yield |
| MA-9 | ICF final optics: neutron/gamma-induced absorption and debris damage limit lifetime below economic replacement interval | Laser ICF | high | +3–8 y / feasibility at high rep-rate | Irradiated silica/grazing-mirror data; annealing demonstrations | Grazing-incidence metal mirrors, gas/plasma optics, in-situ annealing, magnetic debris deflection |
| MA-10 | HTS tape degradation at cryogenic irradiation is worse than room-temperature data imply, forcing thicker shields | Tokamak, Stellarator (compact HTS) | low–med | +2–4 y / larger, costlier machines | MIT cryogenic neutron irradiation results | Thicker inboard shield (WC, metal hydrides), lower field, annealing |
| MA-11 | Waste/activation: impurities (Nb, Mo, Ag, Co) in industrial heats prevent low-level-waste classification | All | low–med | +1–3 y / licensing and cost | Industrial-scale RAFM/W heats; regulator waste classification for fusion | Tight impurity specs, recycling and clearance strategy |

### Gate definition

**Gate (as used in this assessment):** a pathway passes the gate in the first calendar year in which **all** of the following are true for at least one plant design of that pathway that is credibly heading to construction:
1. The structural material of the first wall/blanket (or, for ICF, the chamber structure and its protective wall) and the plasma-facing armor have **irradiation data with a fusion-relevant spectrum (14 MeV-dominated, He/dpa ≈ 10 appm/dpa in steel) to ≥ ~20 dpa** at the design temperatures, either from IFMIF-DONES or an equivalent source (a fission/ion-beam data set alone does not count; it may supplement);
2. These data have been **accepted by the licensing authority** in the plant's jurisdiction as the basis of the safety case — via a recognised design code (RCC-MRx, ASME III Div. 4 or equivalent) or an explicit code case — for a starter blanket/first wall at ≈20 dpa end-of-life;
3. The **remote maintenance concept** for replacing that blanket/first-wall/divertor (ICF: chamber liners and final optics) has been validated on full-scale mock-ups under representative loads and, for MCF, by at least one in-vessel remote intervention in an activated DT device (ITER or equivalent) or a regulator-accepted equivalent demonstration.

A pathway whose design deliberately avoids high-dpa structures (e.g. thick liquid walls in ICF) passes condition 1 for the protected structure at its actual end-of-life dose, but must then qualify its alternative life-limiting component (final optics, jets) under condition 3.

**Neutron-source milestone — "IFMIF-DONES (or equivalent) delivers first irradiation data at ≥ ~10 dpa"** (calendar year when post-irradiation results of specimens irradiated to ≥ 10 dpa are available to designers):

| P0 | P10 | P50 | P90 | P100 |
|---|---|---|---|---|
| 2033 | 2036 | 2038 | 2043 | 2060 |

Basis: Main Building substantially complete 2029 → installation/commissioning → first neutrons ~2033–2035 → ~1–1.5 years to 10 dpa at 12–25 dpa/fpy and ~70 % availability (lower during ramp-up) → ~1 year PIE. P0 assumes a near-perfect schedule; the tail reflects first-of-a-kind accelerator and lithium-target risks (MA-1) and a small chance of programme collapse.

### Model parameters

*These are calibrated expert judgments by the author of this report, grounded in the evidence above (DONES schedule, current MTRL 4–5 of baseline materials, code-qualification lead times, ITER RH timeline). They are not outputs of a formal model and should be treated as subjective priors.*

| Pathway | P0 | P10 | P50 | P90 | P100 | P(never by 2100, show-stopper) | Rationale |
|---|---|---|---|---|---|---|---|
| Tokamak | 2036 | 2040 | 2046 | 2057 | 2085 | 0.05 | Best-characterised (EUROFER97/F82H, W); gate needs DONES ~20 dpa data (~2039–2041) + 3–5 y code/licensing acceptance + ITER-era RH validation; early tail from regulators accepting lifetime-limited starter blankets for private pilots |
| Stellarator | 2038 | 2043 | 2050 | 2063 | 2095 | 0.10 | Same materials as tokamak, but 3D blanket modules, constrained ports and coil-shielding space make RH validation later and riskier (MA-6, MA-7); no stellarator DT device planned to test RH in activated conditions |
| Laser ICF | 2037 | 2042 | 2050 | 2065 | 2100 | 0.15 | Thick liquid walls can keep structural dpa low, but final-optics lifetime, 10\(^9\)–10\(^{10}\)-cycle chamber fatigue and jet behaviour at Hz rates lack any integrated test; needs a rep-rated facility not yet funded (MA-8, MA-9) |
| Neutron source data (DONES or equivalent, ≥ 10 dpa) | 2033 | 2036 | 2038 | 2043 | 2060 | 0.03 | DONES funded (MIDA 2025), site works since Sep 2026, building 2029; first neutrons ~2033–2035; FPNS/A-FNS/private sources unlikely to beat DONES to 10 dpa |

**Coupling to other challenges** (suggested Spearman rank correlation with this challenge's gate years):
- **Tritium / breeding blanket: ρ ≈ +0.6** — same structural steel, same DONES dependence, same blanket remote maintenance; a materials slip almost always slips blanket qualification.
- **Power exhaust / divertor: ρ ≈ +0.5** — W armor and CuCrZr heat sink are shared; neutron-induced embrittlement and conductivity loss define the divertor's usable heat-flux margin.
- **Plasma burning performance: ρ ≈ +0.3** — ITER DT operation provides the first activated-environment RH and PFC data; delays in burning-plasma programmes delay condition 3 of the gate.
- **Driver / magnets / steady-state: ρ ≈ +0.25** — HTS irradiation limits set shield thickness (MCF); for ICF the final-optics problem couples to the driver (ρ ≈ +0.35 for the Laser ICF pathway).

**Discrete events** (applied on top of the distributions above):
- **Setback — DONES commissioning delay ≥ 3 years** (CW accelerator or Li target problems): p = 0.30 by 2035; +3 to +5 years on the neutron-source row and ~+3 years on all pathway gates.
- **Setback — EUROFER97 found unsuitable at 10–20 dpa** (He embrittlement/DBTT): p = 0.12; +6 to +10 years on Tokamak and Stellarator gates (alloy re-qualification).
- **Breakthrough — second high-flux fusion-spectrum source** (US FPNS via cyclotron route or private high-flux source) delivers ≥ 10 dpa data before DONES: p = 0.10; −2 years on the neutron-source row and ~−1 year on pathway gates.
- **Breakthrough — regulatory acceptance of surveillance-based, lifetime-limited licensing** using fission/ion data plus early (≤ 5 dpa) DONES data for first plants: p = 0.35; −3 years on Tokamak and Stellarator gates (−2 years on Laser ICF).
- **Setback — rep-rated ICF chamber/optics test reveals sub-year optics lifetime with no annealing remedy**: p = 0.20; +5 years on Laser ICF gate.

***

## Changelog (2026-11)

- Header updated to "November 2026 update".
- **IFMIF-DONES status corrected**: was "not yet funded for construction"; now MIDA signed Nov 2025 with cost shares, building permit (Jun 2026), fourth Procurement Arrangement (Aug 2026), Main Building site works started Sep 2026, building completion targeted 2029. No official first-neutron date; ~2034 most-cited, ~2033–2035 used here.
- DONES performance figures corrected: HFTM 12–25 dpa/fpy (top-level >8–12 dpa/fpy in 0.3 L, >16 dpa/fpy in 0.1 L) replaces "~20 dpa/fpy in 500 cm³"; ~10\(^{18}\) n m\(^{-2}\) s\(^{-1}\) is the DEMO first-wall reference flux.
- DEMO dpa arithmetic corrected: 5 fpy gives ~30–45 dpa (W armor) and ~60–75 dpa (steel), not a single "40–70 dpa"; executive-summary "~20 dpa/fpy" replaced by ~10–15 dpa/fpy in front-wall steel; starter blanket 20 dpa ≈ 1.33–1.7 fpy.
- W transmutation: "10 at.% Re, 3 at.% Os after 10 fpy" softened to "several at.% Re, ~1–3 at.% Os after 5–10 fpy" (position-dependent, generic value not verified); added DONES/DEMO transmutation comparison (JNM 2026).
- Tritium burn rate corrected: 500 MW consumes ~76 g T/day (not 184 g); ~300 g/day for 2 GW. ITER in-vessel limit given as ~0.7–1 kg.
- Dose rates corrected: ITER "10\(^5\)–10\(^6\) Sv/h" removed; ITER in-vessel RH ~250 Gy/h, DEMO blanket ~13–17 kGy/h at shutdown.
- ICF shot arithmetic made explicit (5–10 Hz ≈ 4.3–8.6 × 10\(^5\) shots/day; ~4–8 × 10\(^9\) shots over 30 y at 85 % availability); TNT equivalence tied to yield; debris energy description corrected; NIF optics "10 seconds" comparison qualified.
- Sputtering threshold (D on W ~200 eV) and W core radiation (line radiation dominant) corrected; unsupported "50–100× bubble density" and ITER port dimensions removed; EUROFER97 no longer labelled "qualified".
- Added: Section 5.4 HTS tape irradiation; Section 7.1a other neutron sources (LIPAc, A-FNS, US FPNS and DOE June 2026 Roadmap, MPEX, HINEG/CFNS, Avalanche FusionWERX, Kyoto Fusioneering UNITY-3, fission campaigns ≤2 dpa); Section 7.3 WEST/EAST long-pulse results; ICF 2025–2026 developments (NIF 8.6 MJ, HYLIFE-III); EUROfusion MTRL 4–5; Risk Assessment section.
- Not verified and therefore not asserted: a 2026 construction decision for China's CFNS or Japan's A-FNS; CW full-current LIPAc operation; final status of US FPNS funding.

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


53. [IFMIF-DONES construction enters a new phase with the start of site works (17 Sep 2026)](https://ifmif-dones.es/dones-updates/ifmif-dones-construction-enters-a-new-phase-with-the-start-of-site-works/)

54. [Escúzar Town Council grants building permit for IFMIF-DONES](https://ifmif-dones.es/dones-updates/escuzar-town-council-grants-building-permit-for-ifmif-dones-paving-the-way-for-construction-to-begin-this-summer/)

55. [DEMO Hot Cell and Ex-Vessel Remote Handling (UKAEA/CCFE)](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/Miss29.pdf) - shutdown dose rates 13.1–17.4 kGy/h (blanket, 60 dpa) and 8.8–11.6 kGy/h (divertor, 30 dpa)

56. [QST repository: DEMO in-vessel component replacement and maintenance-port dose rates](https://repo.qst.go.jp/records/48891) - ITER in-vessel RH limit 250 Gy/h; DEMO surface dose rates two orders higher

57. [Pintsuk et al., EUROfusion material development and qualification roadmap, 4th DONES Users Workshop, Oct 2026](https://indico.ifmif-dones.es/event/92/contributions/1385/)

58. [Europe and Japan celebrate major milestone in validating LIPAc (F4E)](https://fusionforenergy.europa.eu/news/europe-and-japan-celebrate-major-milestone-in-validating-lipac)

59. [Lumsdaine, US FPNS risk reduction activity, IAEA presentation 2025](https://conferences.iaea.org/event/425/contributions/37857/attachments/21714/37327/Arnie%20Lumsdaine.pdf)

60. [Álvarez et al., Assessment of EUROFER97, tungsten and CuCrZr transmutation effects under IFMIF-DONES and DEMO conditions, J. Nucl. Mater. 618 (2026) 156228](https://publikationen.bibliothek.kit.edu/1000189111)

61. [LLNL experts foster national fusion-energy ecosystem at IFE-STAR Conference (8.6 MJ shot)](https://www.llnl.gov/article/52906/llnl-experts-foster-national-fusion-energy-ecosystem-ife-star-conference)

62. [Ogando et al., Preliminary nuclear analysis of HYLIFE-III, Fusion Eng. Des. 202 (2024) 114333](https://e-spacio.uned.es/entities/publication/47efc0de-9730-422f-b38b-aabedeef764d/full)

63. [Materials research for HiPER laser fusion facilities: chamber wall, structural material and final optics (arXiv:2405.01542)](https://arxiv.org/abs/2405.01542)

64. [TU Wien repository: neutron irradiation of commercial coated conductors](https://repositum.tuwien.at/handle/20.500.12708/11493)

65. [Fischer et al., irradiation temperature effects on REBCO, RADSUM 2025 (CERN Indico)](https://indico.cern.ch/event/1450988/contributions/6259629/attachments/2997460/5281386/RADSUM2025%20David%20Fischer.pdf)

66. [A-FNS presentation at DONES info day (CDTI)](https://cdti.es/sites/default/files/2023-12/dones_infoday_a-fnsr3.pdf)

67. [US DOE Fusion Science and Technology Roadmap (published June 2026)](https://www.energy.gov/documents/fusion-st-roadmap-060926pdf) and [FES presentation to SC advisory committee, 27 Mar 2026 (MPEX status)](https://science.osti.gov/-/media/About/pdf/scac/meetings/2026/FES-SCAC-03272026.pdf)

68. [Avalanche Energy awarded $10 million grant from Washington State to develop FusionWERX](https://www.avalanchefusion.com/news-release/avalanche-energy-awarded-10-million-grant-from-washington-state-to-develop-fusionwerx-neutron-factory)

69. [ORNL, Kyoto Fusioneering to develop Tenn. fusion testing facility (ANS, 30 Jan 2026)](https://www.ans.org/news/2026-01-30/article-7722/ornl-kyoto-fusioneering-to-develop-tenn-fusion-testing-facility/)

70. [Serrano et al., Qualification of EUROFER97 within EUROfusion, 4th DONES Users Workshop, Oct 2026](https://indico.ifmif-dones.es/event/92/contributions/1464/)

71. [WEST sets a new plasma duration record (CEA-IRFM, Feb 2025)](https://irfm.cea.fr/en/2025/02/west-sets-a-new-plasma-duration-record/)

72. [Fourth DONES Procurement Arrangement signed for the IFMIF-DONES buildings](https://ifmif-dones.es/dones-updates/fourth-dones-procurement-arrangement-signed-for-the-ifmif-dones-buildings/)

73. [DONES Programme collaboration takes shape (F4E, Apr 2024: "could be operational by 2034")](https://fusionforenergy.europa.eu/news/dones-programme-collaboration-takes-shape/)
