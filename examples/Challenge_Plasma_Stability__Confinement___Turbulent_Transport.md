# Nuclear Fusion — Deep Dive: Challenge 1
## Plasma Stability, Confinement & Turbulent Transport

**Cross-pathway analysis: Tokamak · Stellarator · Laser ICF**
*Objective research report — June 2026; reviewed and updated 3 November 2026*

> **Review note (3 November 2026).** This report was checked for currency and for the soundness of its claims as of 3 November 2026. Corrections in the body are marked **[corr. 2026-11]**; statements that could not be confirmed are marked **[unconfirmed 2026-11]**. The section *Review & Model Update (November 2026)* before the references documents the check, splits laser ICF into direct and indirect drive, adds the licensing/permit and funding view, and maps gate PL to the risk-pilot model `kernfusion_gesamt.yaml` and its sub-models (`kernfusion_tokamak`, `_stellarator`, `_direct_drive`, `_indirect_drive`).

***

## Executive Summary

Plasma stability and confinement degradation represent the single most complex scientific challenge in fusion energy, encompassing at least four distinct but interacting physical problem classes: (1) macroscopic magnetohydrodynamic (MHD) instabilities that catastrophically terminate confinement in tokamaks; (2) microscale plasma turbulence that bleeds energy from the hot core in all magnetic confinement devices; (3) implosion hydrodynamic instabilities that degrade hot-spot formation in laser ICF; and (4) collective instabilities driven by fusion-born alpha particles that will emerge uniquely in burning plasmas. Each operates on different spatial scales, timescales, and physical mechanisms, yet all converge on the same outcome: the fusion plasma fails to sustain the triple product \(n \cdot T \cdot \tau_E\) required for ignition.

The scientific status in 2026 is mixed. Disruption prediction using AI has made substantial progress, and NIF has now achieved ignition ten times with yields reaching 8.6 MJ. However, no confirmed solution for disruption-free steady-state tokamak operation at Q > 1 exists, turbulent transport remains only partially understood even at the code level, and the alpha-particle stability problem has never been confronted in a burning plasma at ITER-relevant parameters.[^1][^2][^3][^4][^5]

***

## Part I — Tokamak: MHD Instabilities and Disruptions

### 1.1 What Is a Disruption?

A tokamak plasma is an inherently metastable system. At equilibrium, the plasma current density profile \(J(r)\), pressure profile \(P(r)\), and toroidal field \(B_\phi\) are locked in a configuration that satisfies the MHD force balance \(\mathbf{J} \times \mathbf{B} = \nabla P\). Perturbations in any of these quantities can trigger magnetohydrodynamic instabilities that grow until a **disruption** occurs: a sudden, irreversible collapse of the entire plasma current over milliseconds.

Disruptions involve two phases:
1. **Thermal quench** (~1 ms): plasma thermal energy (\(\sim\)350 MJ in ITER at full performance) is deposited on the first wall via radiation and particle transport, causing surface melting and ablation.
2. **Current quench** (~50–100 ms): the plasma current decays, inducing large halo currents in surrounding structures and potentially accelerating electrons to relativistic energies.[^6][^7]

The ITER engineering design currently allows for disruptions in approximately 10% of plasma pulses. The in-vessel components are designed to survive ~3,000 full-performance disruptions over their lifetime. However, this tolerance envelope was established for planned disruptions during operational development — any systematic mechanism that raises the disruption rate above design basis constitutes a machine-threatening risk.[^8]

### 1.2 Disruption Trigger Mechanisms

Disruptions are initiated by crossing stability boundaries defined by the MHD equilibrium. The primary triggers are:[^9]

**Operational limit violations:**
- **Greenwald density limit**: when the line-averaged electron density \(\bar{n}_e\) exceeds \(n_G = I_p/\pi a^2\) (in units of \(10^{20}\) m\(^{-3}\), MA, m), the plasma edge resistivity rises, current profile broadens, and locked modes are seeded
- **\(q\)-profile crossing**: the safety factor \(q = rB_\phi/R B_\theta\) profile must remain above \(q_{95} > 2\) at the edge; crossing below this induces the \(m=2, n=1\) tearing mode which is the most common disruption precursor
- **Pressure-driven ballooning modes**: when normalized pressure \(\beta_N = \beta a B / I_p\) exceeds the Troyon limit (\(\beta_N^{max} \approx 2.8 \ell_i + 1\)), ideal ballooning modes destabilize globally

**Intrinsic instabilities:**
- **Neoclassical Tearing Modes (NTMs)**: resistive instabilities that form magnetic islands at rational \(q\) surfaces; islands grow via a bootstrap current deficit in their O-points that reinforces the perturbation — this is the most dangerous non-ideal MHD instability in advanced tokamak scenarios[^10]
- **Resistive wall modes (RWMs)**: ideal external kink modes stabilized by a conducting wall only if the rotation is sufficient; at low rotation in burning plasma, RWMs may become unstable unless actively stabilized
- **Vertical displacement events (VDEs)**: elongated plasmas are vertically unstable; a VDE can drive the plasma into the wall, generating halo currents of up to 40% of the original plasma current in conducting structures[^9]

Historical disruption rates in operating tokamaks are instructive: in JET with an ITER-like wall, disruption rates of ~10% were typical; in JT-60U, the average disruption frequency during the plasma current flat-top was 9.6% across 7,039 shots. For ITER at high current, the target disruption rate is ≤1% for energy load and electromagnetic force reasons, and <<1% for runaway electron reasons — a factor of 10–100 lower than currently demonstrated in active research.[^11][^9]

### 1.3 Runaway Electrons: The Critical Sub-Problem

During the current quench, a fraction of thermal electrons is accelerated to relativistic energies rather than thermalizing. The **Dreicer mechanism** seeds runaways when the induced electric field \(E_{ind} > E_{Dreicer} = n_e e^3 \ln\Lambda / (4\pi \epsilon_0^2 m_e v_{te}^2)\), and the **avalanche mechanism** exponentially amplifies this seed population: each runaway electron, deflected during a close Coulomb collision, can generate additional runaways from the thermal bulk if the electric field exceeds the avalanche threshold.[^12]

In ITER, modeling predicts runaway currents of up to **12 MA** — the full plasma current — carried in a beam of multi-MeV electrons. The energy stored in such a beam is ~20–200 MJ, concentrated in an area of a few hundred cm². Impact of a full runaway beam on the first wall would cause local melting orders of magnitude deeper than thermal quench loads, potentially permanently damaging plasma-facing components.[^13][^14]

**ITER's Disruption Mitigation System (DMS)** passed its Final Design Review in March 2024 and uses **Shattered Pellet Injection (SPI)**: large cryogenic pellets of protium or neon-doped gas are shattered into fragments and injected into the pre-disruption or disrupting plasma in less than 5 ms. SPI can:[^15][^16][^17][^18]
- Radiate away thermal energy via impurity line radiation, reducing peak wall heat loads during the thermal quench
- Raise plasma density to collisionally suppress runaway electron avalanche formation
- Inject heavy material (neon, argon) into a fully formed RE beam to scatter runaways out of the beam via pitch-angle scattering

However, significant uncertainties remain. SPI neon injection produces ~20% pitch-angle scattering of incident runaway electrons per pellet cloud, but absorption and energy removal from the beam are negligible for neon. Tungsten pellets can terminate a RE beam by absorption, but their use must be optimized against wall contamination. The most recent DMS modeling for ITER in DT H-mode shows that nuclear Compton seed electrons (generated by fusion neutrons) can dominate the runaway seed in high-performance plasmas, making low-neon SPI alone insufficient. A consensus DMS workshop report concluded: "significant uncertainties exist as to whether the present baseline disruption mitigation system will offer sufficient protection to ITER from relativistic electron impacts".[^19][^20][^21]

### 1.4 Disruption Prediction with AI

Disruption prediction aims to give the plasma control system enough warning (typically tens to hundreds of milliseconds before the disruption) to either avoid the disruption by adjusting plasma parameters or execute a controlled shutdown via DMS. The field has transitioned from physics-based threshold monitors to data-driven machine learning.

Key developments (2022–2026):
- **Multi-task learning models** integrating disruption prediction with instability event classification (ELMs, NTMs, locking modes) have achieved Area Under the ROC Curve (AUC) of 0.940 on the HL-3 tokamak with limited training data[^22]
- **Hybrid physics/ML models** at JET combine self-organizing maps for unsupervised anomaly detection with decision-tree rule extraction, enabling interpretable prediction rules that can be cross-machine transferred[^23][^1]
- **Recurrent neural networks (LSTM-based)** from PPPL's FRNN package demonstrated multi-machine transfer learning between JET and DIII-D[^22]
- AI integration into the plasma control system loop — real-time inference with sub-ms latency — has been demonstrated on JET[^2]

The unresolved challenge is **distributional shift**: a disruption predictor trained on existing machines operates on data from ITER's new plasma-wall combinations, higher currents, and different heating profiles that have no historical precedent. ITER will face a cold-start problem: large margins of disruption avoidance must be imposed initially, sacrificing fusion performance, while operational experience accumulates.[^8]

***

## Part II — Tokamak: Edge-Localized Modes (ELMs)

### 2.1 The ELM Problem

High-confinement H-mode — the standard operating regime for ITER and most tokamak power plant concepts — is characterized by a **pedestal**: a region of steep pressure gradient at the plasma edge that acts as a transport barrier, elevating core pressure by a factor of ~2 over L-mode. The pedestal is bounded by the peeling-ballooning stability boundary, at which **Type-I ELMs** explosively erupt.

A single ITER Type-I ELM is expected to release ~10 MJ m\(^{-2}\) of energy fluence on the divertor in ~1 ms. This is comparable to the energy deposited by an arc welder per pulse, repeated every few seconds for years. Material studies show that tungsten divertor tiles begin to suffer surface melting above ~0.5 MJ m\(^{-2}\) for pulse widths typical of ELMs. The factor-20 excess means Type-I ELMs are fundamentally incompatible with ITER's tungsten divertor lifetime unless mitigated.[^24][^25][^26]

### 2.2 ELM Suppression: RMPs

**Resonant Magnetic Perturbations (RMPs)** are the leading ITER-approved approach to full ELM suppression. External coils add small, non-axisymmetric perturbations to the poloidal magnetic field that resonantly overlap with the pedestal rational surfaces, creating a stochastic layer at the edge that continuously bleeds particle content before pressure can build to the ballooning limit.

The experimental record as of 2026:
- Full Type-I ELM suppression first achieved on DIII-D using \(n=3\) RMPs in ITER-baseline conditions (\(I_p/aB = 1.41\), \(\beta_N \sim 1.8\), \(H_{98,y2} \sim 0.9\))[^27]
- Suppression maintained for ~3.5 s (~45 energy confinement times) with no ELM signature and maintained H-mode confinement[^27]
- Suppression demonstrated with n=4 RMPs on EAST under ITER-baseline conditions with tungsten divertors, requiring \(\beta_N > 1.8\)[^28]
- Suppression has been demonstrated with dominantly ECH heating on AUG, but ECH-dominated conditions (which are ITER-relevant since NBI will provide relatively less fraction than in present devices) reduce RMP penetration threshold, potentially complicating access[^29]

Key physics uncertainties that remain:[^30]
- Whether the RMP coil geometry of ITER will achieve the required resonance overlap in burning plasma conditions, which differ from current experiments in density, rotation profile, and bootstrap fraction
- The effect of neoclassical toroidal viscosity torque on pedestal rotation, which affects field penetration threshold
- Whether ELM suppression can be simultaneously maintained with pellet fueling (required to maintain core density in ITER)
- Whether the density pump-out accompanying RMP ELM suppression in present devices occurs at ITER-scale plasmas and degrades fusion performance

### 2.3 ELM-Free Operating Regimes

A growing body of experimental evidence suggests that ELMs may be avoidable altogether by operating in alternate confinement regimes, potentially making RMP reliance unnecessary. The EUROfusion tokamak exploitation program has systematically mapped eight ELM-free or ELM-tolerant regimes across AUG, JET, MAST-U, TCV, and WEST:[^31]

| Regime | ELM Status | Confinement | ITER/Reactor Relevance |
|---|---|---|---|
| Quiescent H-mode (QH) | ELM-free | H-mode quality | Requires low rotation; not yet at full ITER parameters[^32][^33] |
| I-mode | ELM-free | Sub-H-mode | Separated particle/energy barriers; attractive for exhaust[^34] |
| Negative Triangularity (NT) | Inherently ELM-free | L-mode quality | No pedestal; turbulence reduced by geometry; no high-density pedestal transport[^35][^36] |
| Quasi-Continuous Exhaust (QCE) | Small/no ELMs | ~H-mode | Demonstrated in DT on JET; minimum separatrix density requirement met in ITER baseline[^31] |
| X-point Radiator (XPR) | Small ELMs | H-mode | Radiative mantle suppresses edge pressure; novel regime[^31] |

**Negative triangularity (NT)** has attracted particular attention: by inverting the plasma cross-section shape (the outer edge is concave rather than convex), the bad-curvature region is moved from the outboard to the inboard side, fundamentally altering the linear drive of ballooning instabilities. NT plasmas naturally operate in L-mode with no pedestal, eliminating ELMs entirely. Gyrokinetic simulations and DIII-D experiments confirm that NT achieves superior L-mode confinement over positive triangularity — potentially sufficient for a fusion reactor if operated at sufficient magnetic field. The NT confinement advantage appears not to depend on machine scale, which is encouraging, but NT operation demands higher plasma current to achieve equivalent performance, and vertical stability control is more challenging.[^35][^36][^37][^38]

***

## Part III — All MCF Pathways: Anomalous Turbulent Transport

### 3.1 The Physical Origin: Why Turbulence Is Inevitable

Confinement of a hot plasma inherently creates large temperature and density gradients: the core operates at ~100–150 million °C while the edge is near room temperature over a distance of ~1–2 m. These gradients are the free-energy source for a hierarchy of microinstabilities that generate turbulence on scales from millimeters (ion-scale, \(k_\perp \rho_i \sim 1\)) to sub-millimeter (electron-scale, \(k_\perp \rho_e \sim 1\)).[^10]

The fundamental plasma-science reason transport exceeds classical predictions by two to three orders of magnitude is that charged particles in crossed electric and magnetic fields undergo \(\mathbf{E} \times \mathbf{B}\) drift motion. Turbulent fluctuations in the electric potential create a sea of eddies that carry plasma radially across field lines at rates far exceeding binary-collision diffusion.

### 3.2 The Ion Temperature Gradient (ITG) Mode: The Primary Driver

The most important instability for ion confinement is the **Ion Temperature Gradient (ITG) mode** (also called the \(\eta_i\) mode where \(\eta_i = L_{n_e}/L_{T_i}\)):[^39][^40]

**Physical mechanism**: The ion temperature gradient creates a pressure gradient in the direction of bad magnetic curvature on the outboard midplane of the tokamak. This is analogous to the Rayleigh-Taylor instability: heavier plasma is effectively "above" lighter plasma in the gravitational analogy of the centrifugal force from the curved field. Perturbations of this interface grow exponentially until non-linear saturation by zonal flows.[^39]

**Critical gradient behavior**: The ITG drive is nearly zero below a critical value of \(\eta_i^{crit}\), above which turbulent transport rises steeply. This is the **stiff transport** or **critical gradient** property: the plasma self-organizes to maintain temperature profiles very close to the marginal stability gradient. It explains why external heating above a moderate level does not raise core temperature — all additional power is transported outward by increased turbulence until the edge temperature rises commensurately.[^41]

**Gyrokinetic simulation success**: Nonlinear gyrokinetic simulations (GENE, GS2, GYRO, CGYRO) now reproduce ITG-dominated transport in L-mode tokamak discharges within ±25% of experimental values in many cases. This represents a major scientific achievement. However, the computational cost of first-principles gyrokinetic simulation is extreme: a single flux-tube simulation of a 1 m radius plasma requires ~\(10^5\) CPU-hours on leadership-class computers. Real-time control applications require reduced models (e.g., TGLF, QuaLiKiz) that capture the essential physics with 6–7 orders-of-magnitude speedup, but at the cost of accuracy in nonlinear saturation and cross-scale coupling regimes.[^42][^43][^5]

### 3.3 The Multi-Scale Turbulence Problem

Real fusion plasmas contain turbulence at both ion scales (\(k_\perp \rho_i \sim 1\), driven by ITG and Trapped Electron Modes, TEM) and electron scales (\(k_\perp \rho_e \sim 1\), driven by Electron Temperature Gradient modes, ETG). The scale separation is \(\rho_i/\rho_e = (m_i/m_e)^{1/2} \approx 60\) for deuterium.[^43]

For years, these scales were simulated independently. **Multi-scale gyrokinetic simulations** — computationally feasible only at current supercomputer scales — have revealed significant **cross-scale coupling**:[^44][^45]

- Electron-scale (ETG) turbulence can **enhance** ion-scale transport when the ITG drive is near marginal stability — ETG streamers damp ion-scale zonal flows[^45]
- When the ITG drive is well above marginal, ion-scale turbulence **suppresses** ETG[^45]
- ETG turbulence is responsible for more than 50% of the turbulent electron heat flux in W7-X plasma cores[^46]
- Coupled ITG/TEM/ETG simulations show that TEM growth rates are reduced by effective diffusion from ETG but that zonal flow saturation mechanisms differ between the two modes[^47]

The critical implication is that **reduced transport models** that handle ion and electron scales separately are structurally incorrect in parameter regimes close to marginal stability — which is precisely where high-performance fusion reactors will operate. Building validated multi-scale transport models for ITER and DEMO is an open problem that will require exascale supercomputing and a new generation of gyrokinetic codes.[^5]

### 3.4 Zonal Flows: The Self-Regulation Mechanism

**Zonal flows** — poloidally and toroidally symmetric radial electric field perturbations — are generated by the turbulence itself via Reynolds stress and act as a feedback mechanism that partially suppresses turbulence. The ITG–zonal-flow system behaves as a **predator-prey cycle**: turbulence drives zonal flows, zonal flows shear and suppress turbulence, turbulence decays, zonal flows collapse, turbulence regrows.[^48][^49]

Zonal flows are the key mediator of **Internal Transport Barriers (ITBs)**. When the E×B shear rate from zonal or mean flows exceeds the maximum linear growth rate of the instability driving the turbulence, turbulence is locally suppressed and transport collapses, forming a barrier. ITBs have been observed in many tokamaks and offer a path to enhanced core confinement, but they are transient and difficult to sustain reliably. In toroidal geometry, geodesic curvature coupling depletes zonal flow energy into pressure sidebands, inhibiting the self-consistent formation of long-lived E×B shear layers that would fully quench turbulence.[^50][^51][^39]

### 3.5 Stellarator-Specific Turbulence Landscape

In W7-X, once neoclassical transport is suppressed, turbulence becomes the dominant loss channel. The distinctive findings are:[^52][^53]

- Core ion temperatures are **clamped at approximately 1.7 keV** in most W7-X scenarios, with turbulent transport dominating whenever this threshold is exceeded — consistent with ITG critical gradient behavior[^53]
- The turbulence regime depends strongly on the gradient ratio \(\eta_i = L_{n_e}/L_{T_i}\): when \(\eta_i\) falls below critical, an ITG→TEM regime transition occurs and turbulence amplitude drops[^53]
- **Density peaking** significantly suppresses turbulence in W7-X, likely by reducing \(\eta_i\) below the ITG threshold; confinement times can exceed 200 ms in peaked-density scenarios[^54][^52]
- Pellet fueling, by creating centrally peaked density profiles, enables turbulence suppression that has allowed W7-X to achieve profiles otherwise inaccessible[^54]
- Global gyrokinetic analysis confirms that ETG turbulence drives more than 50% of electron heat transport in the plasma core, while TEM drives ion transport[^46]

The key stellarator-specific challenge is that the complex 3D magnetic geometry creates mode structures that cannot be captured by simpler tokamak codes. The effect of **magnetic field ripple** on zonal flow amplitude — which is a 2D axisymmetric effect in tokamaks but is 3D in stellarators — can suppress zonal flows and thereby reduce their turbulence-regulatory effectiveness. Gyrokinetic codes such as GENE-3D, EUTERPE, and ORB5 have been adapted for 3D geometry but face validation gaps at W7-X reactor-scale parameters.[^55]

***

## Part IV — Laser ICF: Rayleigh–Taylor and Implosion Hydrodynamics

### 4.1 Implosion Dynamics and Stability Requirements

A NIF ignition experiment implodes a ~2 mm diameter spherical capsule filled with cryogenic DT ice, driven by ~2 MJ of X-rays from a laser-heated hohlraum. The capsule must be compressed by a factor of ~35 in radius (convergence ratio ~35×), achieving central fuel densities of ~1,000× liquid density and temperatures of 50–100 keV.[^56]

The Rayleigh-Taylor instability (RTI) grows whenever a high-density layer is accelerated by a lower-density layer — the fusion analogy to an inverted glass of water. In the ICF context, RTI operates at two distinct interfaces:[^57][^58]

**Acceleration phase (outer ablation surface)**: laser-imprinted non-uniformities and capsule surface roughness on the DT ice (required to be < 1 µm RMS) seed perturbations that grow during the acceleration as:[^59]
\[\delta(t) = \delta_0 e^{\gamma t}, \quad \gamma = \sqrt{Akg} - kV_{abl}\]
where \(A\) is the Atwood number, \(k\) the perturbation wavenumber, \(g\) the acceleration, and \(V_{abl}\) the ablation velocity (which provides a stabilizing term). Short-wavelength modes are stabilized by ablative mass flux, but long-wavelength modes grow freely.

**Deceleration phase (inner hot-spot surface)**: as the imploding shell decelerates against the stagnating hot-spot pressure, the outer cold shell and inner hot gas swap density positions, driving RTI again. This phase cannot benefit from ablative stabilization and is the dominant yield-degradation mechanism at high convergence.[^58][^57]

### 4.2 NIF Experimental Progress and Yield Degradation

NIF's path to ignition reveals the central importance of controlling implosion instabilities:
- The first shots in the 2011–2012 era produced yields only 10–20% of 1D simulation predictions; the primary degradation came from mix of high-Z ablator material into the hot spot and large low-mode asymmetries (\(\ell = 2, 4\) drive non-uniformities)[^60][^61]
- By systematically identifying and reducing mix mechanisms (fill tube size, surface roughness, drive symmetry), yields were raised to 80–85% of 1D predictions in some experiments[^62]
- **Ignition** (scientific breakeven) was first achieved on December 5, 2022 (3.15 MJ from 2.05 MJ laser), with subsequent experiments producing 3.88 MJ (July 2023), then 5.2 MJ (February 2024), and NIF has now achieved ignition **ten times with a record yield of 8.6 MJ** and target gain >4[^3][^63]
- However, large variability exists between shots: NIF implosions near ignition operate on the **ignition cliff** where yield is exponentially sensitive to hot-spot conditions. Repeats of the same design show yields varying by factors of 3–5x[^64][^65]

The dominant current yield-degradation mechanisms in igniting implosions include:[^66][^60][^56]
- **Hot-spot mix**: high-Z ablator material (diamond, HDC) injected into the hot spot by RTI-driven jets from fill tubes, surface defects, and crystallite boundaries degrades thermonuclear burn by increasing bremsstrahlung cooling and diluting fuel[^60]
- **Low-mode implosion asymmetries**: P2, P4 Legendre-mode asymmetries in the X-ray drive deform the hot spot into non-spherical shapes (prolate or oblate), reducing the minimum hot-spot dimension and thus the hydrodynamic disassembly time — yield degradation can reach ~45% for strongly deformed hot spots[^61]
- **Fill-tube perturbations**: even a 5 µm fill tube (required to inject DT gas during target fabrication) can seed a RTI jet during deceleration, contributing ~20% of hot-spot mix[^56]

Three-dimensional simulations that account for RTI growth seeded by long-wavelength surface defects degrade yield by ~60%, with short-wavelength drive asymmetry contributing an additional ~30% — combining to produce >70% yield reduction in worst-case scenarios. 3D effects are qualitatively captured only in 3D simulations; 2D simulations systematically underpredict yield degradation because they cannot model the full 3D mode structure of instability-driven mixing.[^66][^56]

### 4.3 Magnetic Mitigation of RTI in ICF

A non-standard approach to RTI mitigation is to embed a magnetic field in the implosion, which can reduce both electron thermal conductivity at the gas-ice interface (by trapping electrons on field lines, concentrating hot-spot heat) and damp short-wavelength RTI modes via magnetic tension. External fields of ~1,000 T at the onset of deceleration (corresponding to pre-implosion fields of ~50–100 T that are amplified by flux compression) can substantially slow RTI growth and reduce interface mixing area.[^67][^68]

The mechanism involves self-generated magnetic fields from the **Biermann battery effect** during ablation and RTI growth, supplemented by external applied fields. 3D simulations show that field alignment with the RTI interface reduces ablation near spikes and creates a more stabilized interface. Applied fields of 5 T are sufficient to provide net stabilization for short-wavelength modes where magnetic tension stabilization dominates over the reduced ablative stabilization.[^69][^70][^68]

Current experiments at NIF and Omega are developing the magnetized ICF platform, but applied fields have not yet been incorporated into igniting implosions.

***

## Part V — Burning Plasma: Alpha Particle Instabilities

### 5.1 The Burning Plasma Regime is Unexplored Territory

All existing confinement experiments, including JET's record DT campaign achieving Q ≈ 0.6 in 1997, are not burning plasmas. A **burning plasma** is one in which fusion-born alpha particles provide the dominant heating power. This requires Q ≥ 5, where alpha particle heating equals or exceeds external heating power.[^71]

In a burning plasma, 3.5 MeV alpha particles are born with velocities far exceeding the Alfvén velocity (\(v_\alpha/v_A \sim 3\)), creating an anisotropic fast-ion pressure gradient that can resonantly drive **shear Alfvén eigenmodes (AEs)**:[^72][^4]
- **Toroidal Alfvén Eigenmodes (TAEs)**: gap modes in the Alfvén continuum at \(q = (m + n/2)/(n)\) resonance; fastest-growing instabilities in ITER baseline scenario calculations have toroidal mode numbers \(n \approx 30\) with large growth rates[^73]
- **Reversed-shear Alfvén Eigenmodes (RSAEs)**: core-localized modes in reversed-shear \(q\)-profiles that are particularly problematic in steady-state advanced scenarios[^71]
- **Energetic Particle Modes (EPMs)**: non-linear modes whose frequency tracks the energetic particle population; can cause large radial excursions of fast ions

The critical concern is alpha particle redistribution: if Alfvénic modes scatter alpha particles to larger radii before they slow down and transfer energy to the bulk plasma, the fusion power gain is reduced and the escaped energetic particles load the first wall. Under some conditions, AE excitation could reduce alpha heating efficiency by 20–50%, a severe penalty to fusion performance.[^4][^72]

### 5.2 ITER as the First Burning Plasma Test

**No experiment has ever observed alpha-driven AEs with fusion-born alpha parameters**. JET's DT experiments observed Alfvénic activity driven by NBI fast ions and studied alpha-particle confinement, but alpha heating was always sub-dominant. The key issues that will be first addressed in ITER are:[^74][^4]

1. Whether alpha particle pressure behaves as a simple Maxwellian with respect to pressure-driven stability limits, or whether the non-Maxwellian slowing-down distribution function fundamentally changes MHD stability
2. Whether burning plasmas self-excite TAE/RSAE at amplitudes sufficient to cause significant alpha redistribution or loss
3. Whether the alpha particle profile and heating profile are robust against AE excitation, or whether AEs create a **self-limiting burn** where alpha losses reduce core pressure below the threshold for sustained fusion
4. Whether plasma turbulence is modified by alpha particle heating — alpha particles at Q ≈ 5–10 contribute to pressure-gradient-driven ITG modes and may simultaneously drive and damp turbulence in new parameter regimes[^4]

The alpha-particle problem represents a deep epistemic gap: current theory and experiments disagree on whether alpha-driven AEs will be benign or disruptive in burning plasma. First-principles simulations are computationally prohibitive at ITER scale for the relevant nonlinear AE saturation problem.[^73]

***

## Part VI — Mitigation Landscape and Technology Readiness

### 6.1 Cross-Pathway Comparison of Stability Challenges

| Sub-challenge | Tokamak | Stellarator | Laser ICF | TRL (2026) |
|---|---|---|---|---|
| Disruptions | Critical: 10% rate in present devices; <<1% needed for ITER[^11] | Not applicable: no large current | Not applicable | 4 (DMS designed, not validated) |
| Runaway electrons | Critical: 12 MA expected in ITER disruptions[^14] | Not applicable | Not applicable | 3–4 |
| ELMs (Type-I) | Critical: >20× over material limit[^24] | Absent (no pedestal) | Not applicable | 4 (RMPs demonstrated) |
| ELM-free regimes | Promising: NT, QH, QCE demonstrated[^31][^36] | Inherent (stellarator advantage) | Not applicable | 5 |
| ITG/TEM turbulence | Critical: dominant energy loss channel | Critical: dominant after neoclassical solved[^53] | Absent (ns burn time) | 4 (gyrokinetics partial) |
| Multi-scale turbulence | Partly understood: ETG enhances ITG near marginal stability[^45] | Partly understood: ETG dominates electron heat flux in W7-X[^46] | Not applicable | 3 |
| RTI / implosion instability | Peripheral (ELM physics shares some features) | Not applicable | Critical: primary yield degradation mechanism[^57][^60] | 5 (multiple ignitions achieved) |
| Alpha-particle AEs | Critical: untested in burning plasma[^4] | Moderate: no current-driven AEs; fast-ion AEs exist in LHD[^75] | Not applicable | 2–3 |

### 6.2 Quantitative Status of the Triple Product

The fusion power gain requires \(n T \tau_E \geq n T \tau_E^{ignition}\). Table of current best values vs. ITER/DEMO requirements:

| Machine | \(n T \tau_E\) (keV·s·m\(^{-3}\)) | Mode | Notes |
|---|---|---|---|
| JET (record DT) | ~5 × 10\(^{20}\) | H-mode, Q ≈ 0.6 | External heating dominant[^4] |
| JET (Q ≈ 0.67, 2022) | ~7 × 10\(^{20}\) | H-mode DT | All-time record for fusion power[^76] |
| ITER target | ~3 × 10\(^{21}\) | H-mode (Q ≥ 10) | Burning plasma target |
| DEMO requirement | ~10\(^{22}\) | Steady-state | Net electricity production |
| W7-X (neoclassical suppressed) | ~1–3 × 10\(^{20}\) | Low-density optimized | Limited by turbulence[^53] |
| NIF (2024 record) | N/A (ICF metric) | Ignition: Q_target > 4 | Yield 8.6 MJ[^3] |

ITER must achieve a 5–10× improvement in triple product over JET, operating in a qualitatively different burning plasma regime.

***

## Part VII — Open Research Questions and Analysis Entry Points

Each of the following constitutes a well-defined research program requiring focused experimental, theoretical, and computational investigation:

### Disruption Avoidance and Mitigation

- **Q1.1**: Can distributed machine learning disruption predictors trained on ITER operational data from the early low-performance phase transfer reliably to high-current burning-plasma conditions? What minimum number of disruptions must occur before reliable prediction is achievable?
- **Q1.2**: Is there a fundamentally disruption-free steady-state tokamak operating scenario (NT, advanced scenarios with broad current profiles) that combines sufficient performance with Q > 5?
- **Q1.3**: What is the maximum RE current that SPI can suppress in ITER under the full range of pre-disruption states, including nuclear Compton seeds in DT operation? Does the DMS need additional runaway mitigation hardware?

### ELM Control and ELM-Free Operation

- **Q2.1**: Does RMP ELM suppression scale to ITER 15 MA conditions with the ITER coil geometry? What is the accessible window in \(\beta_N\), \(q_{95}\), rotation, and collisionality?
- **Q2.2**: Can NT plasmas achieve confinement sufficient for net electricity at magnetically relevant scale (SPARC, ITER)? What is the minimum magnetic field and current for NT to reach ignition conditions in L-mode?
- **Q2.3**: What is the physics basis for the QCE minimum separatrix density criterion, and is it satisfied by ITER's baseline plasma?

### Turbulent Transport

- **Q3.1**: Do multi-scale gyrokinetic simulations with realistic plasma parameters converge to a predictive description of cross-scale coupling in ITER-grade plasmas (\(T_i = 20\) keV, \(\beta \sim 3\%\))? What computing resources are required?
- **Q3.2**: Can a reduced transport model (e.g., neural-network surrogate for nonlinear gyrokinetics) achieve <20% accuracy on turbulent fluxes at ITER-relevant gradients for use in integrated modeling?
- **Q3.3**: What is the stellarator-specific influence of magnetic field ripple on zonal flow amplitude and turbulence saturation? How does this scale with W7-X operational scenario space?
- **Q3.4**: Can density peaking via pellet fueling be used as an active turbulence-suppression actuator in W7-X and future stellarators, and what is its compatibility with tritium fueling requirements?

### Rayleigh-Taylor and ICF Stability

- **Q4.1**: What is the minimum surface roughness and fill-tube diameter compatible with achieving ignition robustly across shot-to-shot variability at NIF? What target fabrication processes can achieve these tolerances at scale?
- **Q4.2**: Can magnetized ICF (with ~100 T seed fields compressed to ~10,000 T at stagnation) reduce RTI-driven yield degradation sufficiently to change the shot-to-shot variability from 3–5× to <2×?
- **Q4.3**: Does the ICF scaling from NIF-level gain (Q_target ~ 3–5) to power-plant gain (Q_target ~ 50–100) require qualitatively different capsule designs, or is it a quantitative extension of the demonstrated ignition design?

### Burning Plasma Alpha Stability

- **Q5.1**: Will ITER's alpha population at Q = 10 drive TAEs at amplitudes sufficient to cause measurable alpha loss fractions (>1%)? What are the key dimensionless parameters controlling this?
- **Q5.2**: Can external NBI or ICRF actuators be used to seed coherent AEs at controlled amplitude to non-linearly suppress spontaneous TAE growth (active AE stabilization)?
- **Q5.3**: What is the effect of alpha heating profile modification (e.g., by core-localized AE-driven redistribution) on the ITG turbulence level in the burning plasma core? Is there a constructive or destructive interference between alpha heating and turbulence suppression?

***

## Conclusion: The Stability Challenge as a System Problem

The plasma stability and confinement challenge is not a single research question but a multi-decade scientific and engineering program spanning at least five distinct instability classes. The deepest open question is not whether each instability can be controlled individually — experiments have demonstrated disruption mitigation, ELM suppression, ITG turbulence reduction, and RTI control in isolation — but whether all mechanisms can be simultaneously managed in an integrated burning plasma at reactor scale.

The uniquely new physics of burning plasma (alpha heating, alpha-driven AEs, self-organized burn dynamics) remains entirely uncharacterized experimentally. ITER is not just a next-step machine; it is the only planned experiment capable of exploring this regime. Its operational success is therefore a prerequisite for any rational DEMO design that does not rest on extrapolation of uncertain physics. The scientific risk concentrated in ITER's burning plasma phase is arguably the highest uncertainty in the entire fusion development program.[^77][^4]

---

## Review & Model Update (November 2026)

Scope and model architecture are described in the overview report (section *Review & Model Update*). This
section covers what Challenge 1 contributes to gate **PL** (plasma/implosion performance).

### R.1 Currency and claim check

| ID | Location | Statement | Finding | Status |
|---|---|---|---|---|
| C1-01 | Executive summary | NIF ten ignitions, up to 8.6 MJ | Confirmed by LLNL [R15][R16] | confirmed |
| C1-02 | Executive summary | No MCF device at Q > 1 | Still true; SPARC first plasma now targeted for 2027 [R2] | confirmed |
| C1-03 | Part IV | Laser ICF treated as one pathway | Direct-drive status is missing: hot-spot gain > 1 [R23], hydro-equivalent burning plasma at ≥ ~1.7 MJ [R24], scaled Lawson > 0.9 [R25] | supplemented (R.2) |
| C1-04 | Part V | ITER as first burning-plasma test | Timing per Baseline 2024: DT from 2039 [R1]; SPARC and BEST may provide earlier alpha-heating data | context updated |
| C1-05 | Throughout | Physics claims (disruptions, ELMs, turbulence, RTI) | Not re-verified individually; they are consistent with the overview and do not depend on 2026 events | not re-verified |

### R.2 Direct vs. indirect drive for this challenge

- **Indirect drive.** Ignition is reproducible at NIF. The record of 8.6 MJ (gain 4.13) came with
  continuous-gradient-doped capsules [R15]. The Enhanced Yield Capability is expected to reach ~40 MJ [R16].
  The gate requires plant-consistent gains of about 30–50 with ηG ≳ 10. Hohlraum coupling losses keep this
  harder than the yield record suggests.
- **Direct drive.** No ignition has been achieved yet. OMEGA results scale to a burning plasma only at
  ≥ ~1.7 MJ [R24], and no such direct-drive facility exists or is funded. Theoretical gains are higher (better
  coupling), but imprint and laser-plasma instabilities are the dominant risks. This is reflected in a later
  PL gate and a higher show-stopper probability (0.25 vs. 0.15).

### R.3 TRL / licensing / funding view of Challenge 1

| Pathway | TRL | Licensing / permit | Funding |
|---|---|---|---|
| Tokamak | Disruption and runaway-electron control is the critical safety-relevant item. ITER DMS validation starts with operation from 2034 [R1]. | The disruption safety case (vessel loads, tritium mobilisation) is part of the licence application under Part 30 or national radiation-protection law [R5][R32]. | SPARC (private) and ITER (public) carry the burning-plasma evidence. A SPARC failure would hit the funding climate (scenario "funding weak"). |
| Stellarator | No disruptions. Turbulence and alpha confinement at reactor parameters are open; there is no DT stellarator. | No specific issue beyond the general framework. Tennessee precedent [R8]. | Alpha (Proxima) is the planned burning-plasma-relevant step; its federal co-funding is open [R13]. |
| Direct drive | Ignition not yet demonstrated (TRL 3). | Unclassified physics [R27]. | No public MJ-class direct-drive facility is funded. Private programmes plan their own implosion facilities (Focused Energy: first implosion 2033) [R22]. |
| Indirect drive | Ignition demonstrated; gain scaling open. | Classified elements of hohlraum design [R26][R27]. | NIF is funded by NNSA for weapons physics. Commercial work relies on private capital (Inertia) [R17]. |

### R.4 Mapping to the risk model (gate PL)

- **PL** — MCF: DT Q ≥ 10 (compact devices: alpha heating ≥ 2/3) sustained ≥ 300 s with disruption, runaway-electron and ELM control. ICF: target gain ≥ 30–50 with a plant-consistent driver.

| Pathway | Gate | P0 / P10 / P50 / P90 / P100 (year, conditional on success) | P(never by 2100) | Model nodes |
|---|---|---|---|---|
| Tokamak | PL – Plasma/implosion | 2031 / 2036 / 2044 / 2058 / 2080 | 0.05 | `tok_pl`, `tok_f_pl` |
| Stellarator | PL – Plasma/implosion | 2035 / 2042 / 2055 / 2078 / 2095 | 0.15 | `stl_pl`, `stl_f_pl` |
| Direct Drive | PL – Plasma/implosion | 2036 / 2042 / 2055 / 2080 / 2098 | 0.25 | `dir_pl`, `dir_f_pl` |
| Indirect Drive | PL – Plasma/implosion | 2033 / 2037 / 2048 / 2072 / 2095 | 0.15 | `ind_pl`, `ind_f_pl` |

Coupling of PL with the other gates (Spearman, within a pathway): MCF PL–EX 0.60, PL–DR 0.50, PL–TR 0.45,
PL–MA 0.30; ICF PL–DR 0.60, others 0.25–0.35. Across pathways, PL is coupled at 0.4 (tokamak–stellarator)
and 0.5 (direct–indirect).

Pathway scenarios touching PL:
- `sparc_erfolg`: PL ~3 years earlier, show-stopper 0.03.
- `iter_verzug`: +3 to 4 years.
- `dd_zuendanlage`: PL ~5 years earlier, show-stopper 0.18.
- `eyc_erfolg`: PL ~4 years earlier.

### Sources for this review

Accessed 3 November 2026. Secondary sources are marked as such; claims resting only on them are flagged in the tables above.

- **[R1]** ITER Organization via ANS Nuclear News, 'ITER begins operations at its magnet cold test facility' (1 Jun 2026) — Baseline 2024: SRO 2034, full magnetic energy 2036, DT 2039. <https://www.ans.org/news/article-8081/iter-begins-operations-at-its-magnet-cold-test-facility/>
- **[R2]** Nuclear News Network, SPARC project tracker (verified 11 Oct 2026) — ~75 % built by April 2026, first plasma target 2027 (secondary, cites CFS). <https://www.nuclearnewsnetwork.com/industry-trackers/fusion-energy-companies/cfs-sparc>
- **[R5]** US NRC, proposed rule 'Regulatory Framework for Fusion Machines', Federal Register 26 Feb 2026 (10 CFR Part 30). <https://www.federalregister.gov/documents/2026/02/26/2026-03865/regulatory-framework-for-fusion-machines>
- **[R8]** Tennessee Department of Environment and Conservation, press release (31 Aug 2026) — first fusion-specific byproduct material licence (Type One Energy). <https://www.tn.gov/environment/news/2026/8/31/first-license-commercial-fusion.html>
- **[R13]** Max Planck Society, 'Proxima Fusion raises 411 million euros' (8 Jul 2026) — federal share of EUR 1.2 bn for Alpha not yet committed. <https://www.mpg.de/26861952/proxima-fusion-raises-411-million-euros>
- **[R15]** LLNL, 'Target breakthrough enabled fusion record at NIF' (15 Apr 2026) — 8.6 MJ from 2.08 MJ. <https://lasers.llnl.gov/news/target-breakthrough-enabled-fusion-record-nif>
- **[R16]** LLNL, NIF overview, DOE Laser Safety Officer Workshop (20 May 2026) — ten ignitions, EYC ~40 MJ. <https://lasers.llnl.gov/sites/lasers/files/2026-06/lso-workshop-2026-wednesday-g-brunton.pdf>
- **[R17]** Nuclear Engineering International, 'Inertia secures Series A fusion funding' (Feb 2026) — USD 450 M, Thunderwall 10 kJ / 10 Hz / 10 % wall-plug. <https://www.neimagazine.com/news/inertia-secures-series-a-fusion-funding/>
- **[R22]** Runtime Wire, 'Focused Energy raises USD 240M Series A' (2026) — milestones 2028 laser, 2033 implosion, 2035 pilot, 2037 first grid MWh (secondary). <https://runtimewire.com/article/focused-energy-240m-series-a-laser-fusion>
- **[R23]** Williams et al., hot-spot fuel gain > 1 in direct-drive implosions, Nature Physics (2024). <https://www.nature.com/articles/s41567-023-02363-2>
- **[R24]** Gopalaswamy et al., hydrodynamically equivalent burning plasma in direct drive, Nature Physics (2024) — requires ≥ ~1.7 MJ laser energy. <https://doi.org/10.1038/s41567-023-02361-4>
- **[R25]** APS DPP 2025 invited talk, 'Optimization of laser direct-drive implosions … record performance on OMEGA' — scaled Lawson parameter > 0.9. <https://archive.aps.org/dpp/2025/bi02/4>
- **[R26]** National Research Council, 'An Assessment of the Prospects for Inertial Fusion Energy' (2013). <https://uwnxt.nationalacademies.org/read/18288/chapter/2>
- **[R27]** 'Nonproliferation and fusion power plants', arXiv:2207.14348 — direct-drive ICF largely declassified by 1974; export controls for indirect drive. <https://arxiv.org/pdf/2207.14348>
- **[R32]** Orrick, 'NRC proposed fusion rule further clarifies path for commercial deployment' (Mar 2026) — tritium/activation reporting, Part 51 environmental review. <https://www.orrick.com/en/Insights/2026/03/NRC-Proposed-Fusion-Rule-Further-Clarifies-Path-for-Commercial-Deployment>

---

## References

1. [A procedure for rule extraction from a Self-Organising plasma disruption predictor for JET](https://www.nature.com/articles/s41598-026-38318-9) - In a previous paper, a Self-Organizing Map had proven to be able to identify the regions of the plas

2. [Disruption prediction with artificial intelligence techniques in tokamak plasmas](https://www.nature.com/articles/s41567-022-01602-2) - Tokamak plasmas are prone to sudden collapses that terminate the nuclear fusion reactions. This pers...

3. [Achieving Fusion Ignition | National Ignition Facility & Photon ...](https://lasers.llnl.gov/science/achieving-fusion-ignition) - 4" data-caption="One of NIF’s key goals was to create self-sustaining thermonuclear fusion reactions...

4. [Read "Burning Plasma: Bringing a Star to Earth" at NAP.edu](https://www.nationalacademies.org/read/10816/chapter/4) - The plasma is said to be burning when alpha particles from the fusion reactions provide the dominant...

5. [Overview of multiscale turbulence studies covering ion-to - Pure](https://pure.tue.nl/ws/portalfiles/portal/354209897/Maeyama_2024_Nucl._Fusion_64_112007.pdf)

6. [[PDF] Disruption Mitigation in Tokamaks with Massive Material Injection](https://research.chalmers.se/publication/548917/file/548917_Fulltext.pdf) - In this thesis, we develop modeling tools for the various physical phenomena present during a tokama...

7. [Runaway electron generation in ITER mitigated disruptions with ...](https://arxiv.org/html/2602.22177v1)

8. [FAQs - ITER](https://www.iter.org/faqs?thematic=76) - Find answers to the most frequently asked questions about the ITER project.

9. [CHARACTERIZATION OF DISRUPTION PHENOMENOLOGY IN ITER](https://www-pub.iaea.org/MTCD/publications/PDF/csp_001c/pdf/itp1_14.pdf)

10. [arXiv:1903.10812v1  [physics.plasm-ph]  26 Mar 2019](https://arxiv.org/pdf/1903.10812.pdf)

11. [[PDF] Disruption Event Characterization of Global MHD Modes in NSTX ...](https://tsdw.pppl.gov/Talks/2016/Sabbagh.pdf)

12. [Disruption Mitigation in Tokamaks with Massive Material Injection](https://research.chalmers.se/publication/535522/file/535522_Fulltext.pdf)

13. [[PDF] Modelling runaway electrons - ITER](https://www.iter.org/sites/default/files/education/5_2_FulopRunawaysIIS2023.pdf) - ▷ Two-stage injection with 3 full pure H pellets followed by 1 Ne doped pellet after 5 ms. □ Two-sta...

14. [IAEA](https://arxiv.org/pdf/2105.04706.pdf)

15. [Microsoft Word - S_Jachmich_IAEA_2020_v3b.docx](https://www.osti.gov/servlets/purl/1856697)

16. [Pellet Fueling Technology Development for Efficient Fueling of Burning Plasmas in ITER](https://www-pub.iaea.org/mtcd/meetings/PDFplus/2010/cn180/cn180_papers/itr_p1-27.pdf)

17. [Print](https://www.iter.org/print/whatsnew/417)

18. [[PDF] ITER DISRUPTION MITIGATION SYSTEM DESIGN AND ...](https://conferences.iaea.org/event/392/contributions/35757/attachments/19779/33832/IAEA2025-synopsis_sjach_v3.pdf) - In this contribution we present an overview of the activities to validate the ITER DMS design and to...

19. [CoverSheet](https://mcnp.lanl.gov/pdf_files/TechReport_2023_LANL_LA-UR-23-30271Rev.1_LivelyPerezEtAl.pdf)

20. [Runaway electron dynamics in ITER shattered pellet injection ...](https://indico.global/event/13788/contributions/131661/attachments/62949/121481/Votta_EFTC_2025.pdf)

21. [[DOC] ITER Disruption Mitigation System (DMS) Workshop Report - FIRE](https://firefusionpower.org/executive_report_DMS_workshop_final.docx)

22. [kharitonov-ivan/awesome-ML-in-plasma-physics - GitHub](https://github.com/kharitonov-ivan/awesome-ML-in-plasma-physics) - Implementing deep learning-based disruption prediction in a drifting data environment of new tokamak...

23. [[PDF] A hybrid physics/data-driven logic to detect, classify, and predict ...](https://iris.cnr.it/retrieve/517bd9cb-066f-4605-b12a-c3f12b44d1a8/Rossi_2024_Nucl._Fusion_64_046017%20(1).pdf)

24. [[PDF] Experimental overview of ELM control using external magnetic ...](https://pls.llnl.gov/sites/pls/files/2024-11/pet13_presentations_joseph11_elmcontrol_overview.pdf)

25. [[PDF] Issues of tungsten as a plasma facing material for ITER and DEMO](http://www.eie.eng.osaka-u.ac.jp/~supraweb/PDF/ITC22_Ueda12R3.pdf)

26. [Divertor heat flux challenge and mitigation in SPARC - OSTI](https://www.osti.gov/biblio/1772637) - Owing to its high magnetic field, high power, and compact size, the SPARC experiment will operate wi...

27. [[PDF] ADVANCES IN THE PHYSICS UNDERSTANDING OF ELM ... - DIII-D](https://fusion.gat.com/pubs-ext/IAEA12/A27441.pdf)

28. [Suppression of Edge Localized Modes in ITER Baseline Scenario in EAST using Edge Localized Magnetic Perturbations](https://arxiv.org/abs/2408.03272) - We report the suppression of Type-I Edge Localized Modes (ELMs) in the EAST tokamak under ITER basel...

29. [2024 – Pursuing RMP ELM suppression in ECH dominated ITER ...](https://d3dfusion.org/2024-34-01/)

30. [2009 Pedestal and Edge Physics Ann Rep](https://www.iter.org/sites/default/files/media/2024-03/2009_pep_report.pdf)

31. [The physics of ELM-free regimes in EUROfusion tokamaks - arXiv](https://arxiv.org/abs/2604.20484) - The development of operational scenarios without large Type-I ELMs is of utmost importance for the s...

32. [Peeling-limited and high-pedestal ELM-free H-mode periods in](https://www.qst.go.jp/uploaded/attachment/40482.pdf)

33. [MHD simulations of formation, sustainment](http://arxiv.org/pdf/2301.07607.pdf)

34. [[PDF] access requirements for stationary elm-suppressed pedestals in diii ...](https://conferences.iaea.org/event/151/contributions/5642/attachments/6889/8346/Wilks_IAEA_Proceedings.pdf)

35. [Electromagnetic System Conceptual Design for a Negative Triangularity Tokamak](https://arxiv.org/abs/2501.14682) - Negative triangularity (NT) tokamak configurations have several key benefits including sufficient co...

36. [FES Inverting Fusion Plasmas Imp... | U.S. DOE Office of Science(SC)](https://science.osti.gov/fes/Highlights/2024/1a) - Plasmas with negative triangularity show reduced gradients that develop into instabilities, includin...

37. [Untitled Document](https://ar5iv.labs.arxiv.org/html/2402.16216) - In this work, we explore the triangularity effects on turbulent transport employing global gyrokinet...

38. [On the feasibility of Ohmically heated negative triangularity tokamak ...](https://arxiv.org/html/2407.06439v2)

39. [The Ion Temperature Gradient](https://w3.pppl.gov/~hammett/talks/2007/hammett_itginstability_lec.pdf)

40. [[PDF] Plasma Turbulence - UT Physics Department](https://w3fusion.ph.utexas.edu/old-site/ifs/ifsreports/Plasma_Turbulence_827.pdf)

41. [∇Ti](https://arxiv.org/pdf/1712.03587.pdf)

42. [[PDF] IAEA-CN-60ID-P6 - Princeton Plasma Physics Laboratory](https://w3.pppl.gov/~hammett/gyrofluid/iaea_dorland.pdf)

43. [A Scale-Separated Approach for Studying Coupled Ion and Electron Scale Turbulence](https://arxiv.org/abs/1901.07062v1) - Multiple space and time scales arise in plasma turbulence in magnetic confinement fusion devices bec...

44. [[PDF] Cross-‐Scale Coupling of Ion and Electron-‐Scale Turbulence in ...](https://www1.psfc.mit.edu/TTF2015/abstracts/Howard_TTF_abstract-2015.pdf)

45. [Cross-Scale Interactions between Electron and Ion Scale Turbulence in a Tokamak Plasma - PubMed](https://pubmed.ncbi.nlm.nih.gov/26197130/) - Multiscale gyrokinetic turbulence simulations with the real ion-to-electron mass ratio and β value a...

46. [[PDF] Global gyrokinetic analysis of Wendelstein 7-X discharge - Pure](https://pure.tue.nl/ws/portalfiles/portal/343589330/Wilms_2024_Nucl._Fusion_64_096040.pdf)

47. [8th Asia-Pacific Conference on Plasma Physics, 3-8 Nov, 2024 at Malacca](https://www.aappsdpp.org/DPP2024/html/3contents/pdf/5530.pdf)

48. [[PDF] TH/P2-11 Interplay between Zonal Flows/GAMs and ITG Turbulence ...](https://www-pub.iaea.org/mtcd/meetings/fec2006/th_p2-11.pdf) - Although conventional almost stationary zonal flows suppress the turbulent transport effectively, th...

49. [A27243 text](https://fusion.gat.com/pubs-ext/IAEA12/A27243.pdf)

50. [arXiv:physics/0208026v1  [physics.plasm-ph]  6 Aug 2002](https://arxiv.org/pdf/physics/0208026.pdf)

51. [[PDF] The role of flow shear in tokamak transport barriers](http://www-thphys.physics.ox.ac.uk/people/mbarnes/presentations/euromech2010.pdf) - Two types of sheared flow: 1) Zonal flows (generated by turbulence, radial wavelength ~ Larmor radiu...

52. [Overview of the first Wendelstein 7-X long pulse campaign ...](https://iris.unica.it/retrieve/136c5eb8-c22c-40a7-9765-1767a174d70c/Grulke_2024_Nucl._Fusion_64_112002.pdf)

53. [An experimental characterization of core turbulence regimes in Wendelstein 7-X](https://arxiv.org/abs/2105.05107) - First results from the optimized helias Wendelstein 7-X stellarator (W7-X) have shown that core tran...

54. [Experimental confirmation of efficient island divertor operation and successful neoclassical transport optimization in Wendelstein 7-X](https://arxiv.org/abs/2105.04002v1) - We present recent highlights from the most recent operation phases of Wendelstein 7-X, the most adva...

55. [International Atomic Energy Agency](https://physics.iisc.ac.in/~akuley/Papers/Tajinder22a.pdf)

56. [High-resolution modeling of indirectly driven high-convergence layered inertial confinement fusion capsule implosions](https://pubs.aip.org/aip/pop/article/24/5/052701/990207/High-resolution-modeling-of-indirectly-driven-high) - In this paper, we present the results of high-resolution simulations of the implosion of high-conver...

57. [Instabilities and Mixing in Inertial Confinement Fusion](https://www.annualreviews.org/content/journals/10.1146/annurev-fluid-022824-110008?crawler=true) - The main hydrodynamic instabilities that affect ICF are the Rayleigh–Taylor (RT) instability and the...

58. [A study of the Rayleigh-Taylor Instability during deceleration in ...](https://vtechworks.lib.vt.edu/items/b3c1f320-2bcb-44cb-9706-4c0e509da6dd) - The Rayleigh-Taylor instability (RTI) is one of the primary hydrodynamic instabilities that acts as ...

59. [[PDF] Target mass production for inertial fusion energy](https://lasers.llnl.gov/sites/lasers/files/2023-11/alexander-GA-IFE-workshop-2022-2.pdf) - Targets require high fabrication tolerance (~10 µm level), and large numbers if them are needed. (~5...

60. [Hot-spot mix in large-scale HDC implosions at NIF](https://pubs.aip.org/aip/pop/article/27/9/092709/263080/Hot-spot-mix-in-large-scale-HDC-implosions-at-NIF) - Mix of high-Z material from the capsule into the fuel can severely degrade the performance of inerti...

61. [This is the accepted manuscript made available via CHORUS. The article has been](https://link.aps.org/accepted/10.1103/PhysRevE.98.023203)

62. [Robustness to hydrodynamic instabilities in indirectly driven layered capsule implosions](https://pubs.aip.org/aip/pop/article/26/1/012707/367410/Robustness-to-hydrodynamic-instabilities-in) - We report on a high convergence ratio liquid layer capsule implosion performed on the National Ignit...

63. [National Ignition Facility - 2023 - Annual Report](https://annual.llnl.gov/fy-2023/national-ignition-facility-2023) - Supporting stockpile stewardship through a wide range of experiments including study of fusion ignit...

64. [[PDF] US program in laser fusion - ELI ERIC Indico Page](https://indico.eli-laser.eu/event/35/attachments/131/409/5_Betti_Prague-2023-v4.pdf)

65. [Three Peer-Reviewed Papers Highlight Scientific Results of NIF’s Record Shot](https://lasers.llnl.gov/news/three-peer-reviewed-papers-highlight-scientific-results-of-nifs-record-shot) - The scientific results of NIF’s record experiment that achieved a record fusion energy yield of more...

66. [Three-dimensional simulation strategy to determine the effects of turbulent mixing on inertial-confinement-fusion capsule performance - PubMed](https://pubmed.ncbi.nlm.nih.gov/25353910/) - In this paper, we present and justify an effective strategy for performing three-dimensional (3D) in...

67. [The mitigating effect of magnetic fields on Rayleigh-Taylor unstable inertial confinement fusion plasmas](https://pubs.aip.org/aip/pop/article-abstract/20/5/056307/109147/The-mitigating-effect-of-magnetic-fields-on?redirectedFrom=fulltext) - Rayleigh-Taylor (RT) instabilities at interfaces of disparate mass densities have long been known to...

68. [Magnetized Ablative Rayleigh-Taylor Instability in 3-D](https://www.osti.gov/servlets/purl/1860894)

69. [Self-generated magnetic field in three-dimensional ablative ...](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/selfgenerated-magnetic-field-in-threedimensional-ablative-rayleightaylor-instability/6B10BF7B24DC5E58D506510794FD50FC) - The Rayleigh–Taylor instability (RTI) (Rayleigh Reference Rayleigh1900; Taylor Reference Taylor1950)...

70. [Self-generated magnetic field in ablative Rayleigh–Taylor instability](https://pubs.aip.org/aip/pop/article/29/7/072702/2844212/Self-generated-magnetic-field-in-ablative-Rayleigh) - Self-generated magnetic fields in single-mode ablative Rayleigh–Taylor instability (ARTI) relevant t...

71. [Fast Ion Instabilities in Advanced Scenarios](http://www-thphys.physics.ox.ac.uk/research/plasma/reprints/sharapov25part1.pdf)

72. [Microsoft Word - SHARAPOV_final_CM_paper_corr1.doc](https://scientific-publications.ukaea.uk/wp-content/uploads/Published/FusionSTVOL57P156.pdf)

73. [Comprehensive evaluation of the linear stability of Alfvén eigenmodes driven by alpha particles in an ITER baseline scenario](https://arxiv.org/abs/1601.06621) - The linear stability of Alfvén eigenmodes in the presence of fusion-born alpha particles is thorough...

74. [UC Irvine](https://escholarship.org/content/qt4bc1z7q5/qt4bc1z7q5.pdf)

75. [Microsoft PowerPoint - L9_Toi_fin3.ppt](https://www.iter.org/sites/default/files/education/IISS2011_Toi.pdf)

76. [No Job Name](https://infoscience.epfl.ch/server/api/core/bitstreams/7102d40f-f3ce-4005-84cd-caaacd6dc6e0/content)

77. [[PDF] PPPL-3234 - Preprint: February 1997, UC-420, 421, 425, 426](https://bp-pub.pppl.gov/pub_report/1997/PPPL-3234.pdf)
