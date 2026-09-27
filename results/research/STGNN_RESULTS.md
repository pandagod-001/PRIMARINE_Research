# PRIMARINE ST-GNN Experimental Results & Structural Verification

**Document:** `results/research/STGNN_RESULTS.md`  
**Date:** 2026-09-24  
**Classification:** Controlled Simulation & Architectural Proof-of-Concept (Not Historical Telemetry)  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Graph Topology Definition (8 Maritime Nodes, 11 Corridors)

The proof-of-concept graph models critical dry-bulk trade lanes connecting Australia, Indonesia, and Indian East Coast discharge ports:

- **Node 0:** Hay Point (AU) — Primary Coking Coal Export Terminal
- **Node 1:** Gladstone (AU) — Coking Coal & Alumina Port
- **Node 2:** Newcastle (AU) — Thermal & Coking Coal Port
- **Node 3:** Samarinda (ID) — Thermal Coal Anchorage
- **Node 4:** Singapore Strait — Transit Chokepoint & Bunkering
- **Node 5:** Paradip (IN) — Primary East Coast Coking Coal Import
- **Node 6:** Visakhapatnam (IN) — Deepwater Bulk Import Port
- **Node 7:** Haldia (IN) — Draft-Restricted Riverine Bulk Port

**Corridors (11 Navigable Routes):**  
`Hay Point-Singapore`, `Gladstone-Singapore`, `Newcastle-Singapore`, `Samarinda-Singapore`, `Singapore-Paradip`, `Singapore-Visakhapatnam`, `Singapore-Haldia`, `Paradip-Visakhapatnam`, `Visakhapatnam-Haldia`, `Paradip-Haldia`, and `Hay Point-Paradip (Direct Capesize)`.

---

## 2. Controlled Counterfactual Scenario Results

All values generated via reproducible execution of [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py):

| Node ID | Port / Maritime Hub | Network Role | Scenario A: Baseline Risk (No Shock) | Scenario B: Moderate Shock ($\text{Sev}=1.0$) | $\Delta \text{Risk}$ (Scenario B) | Scenario C: Severe Shock ($\text{Sev}=1.5$) | $\Delta \text{Risk}$ (Scenario C) |
|---|---|---|---|---|---|---|---|
| **0** | **Hay Point (AU)** | Disruption Epicenter | 0.3547 | 0.5751 | **+0.2204** | 0.6799 | **+0.3251** |
| **4** | **Singapore Strait** | Transit Chokepoint | 0.4284 | 0.5655 | **+0.1371** | 0.6316 | **+0.2032** |
| **5** | **Paradip (IN)** | Direct Capesize Dest. | 0.3806 | 0.5525 | **+0.1719** | 0.6364 | **+0.2558** |
| **6** | **Visakhapatnam (IN)** | Secondary Dest. | 0.3663 | 0.4118 | **+0.0455** | 0.4351 | **+0.0688** |
| **7** | **Haldia (IN)** | Secondary Dest. | 0.3663 | 0.4118 | **+0.0455** | 0.4351 | **+0.0688** |
| **1** | **Gladstone (AU)** | Adjacent Origin | 0.3467 | 0.3707 | **+0.0239** | 0.3829 | **+0.0362** |
| **2** | **Newcastle (AU)** | Adjacent Origin | 0.3467 | 0.3707 | **+0.0239** | 0.3829 | **+0.0362** |
| **3** | **Samarinda (ID)** | Regional Origin | 0.3467 | 0.3707 | **+0.0239** | 0.3829 | **+0.0362** |

---

## 3. Spatial Distance Attenuation Breakdown

Under both moderate and severe shock scenarios, propagated disruption risk decays strictly with graph hop distance:

| Metric / Level | Graph Scope | Scenario B ($\text{Sev}=1.0$) | Scenario C ($\text{Sev}=1.5$) | Physical Behavior |
|---|---|---|---|---|
| **Hop 0** | Origin Epicenter (Hay Point) | **+0.2204** | **+0.3251** | Localized Port Stoppage / Cyclone Shock |
| **Hop 1** | Direct Corridors (Singapore, Paradip) | **+0.1545** | **+0.2295** | Primary Downstream Corridor Exposure |
| **Hop 2** | Secondary Destinations & Origins | **+0.0325** | **+0.0492** | Attenuated Secondary Port Exposure |
| **Control** | Disconnected Hubs (Rotterdam, Santos) | **0.0000** | **0.0000** | Strict Network Isolation (Zero Leakage) |

---

## 4. 5-Point Structural Sanity Check Suite

| Test ID | Description | Mathematical Condition | Observed Value | Status |
|---|---|---|---|---|
| **SANITY_01** | Graph Topology Integrity | $N = 8, E = 11$ | $N = 8, E = 11$ | **PASS** |
| **SANITY_02** | Zero Disruption Invariance | $\max |\text{Risk}(\text{Shock}=0) - \text{Base}| = 0.0$ | $\Delta = 0.000000$ | **PASS** |
| **SANITY_03** | Disruption Localization | $\text{argmax}(\Delta) = 0 \land \Delta[0] > 0.20$ | $\Delta = 0.2204$ (Rank 1 of 8) | **PASS** |
| **SANITY_04** | Spatial Distance Attenuation | $\text{Hop 0} > \text{Hop 1} > \text{Hop 2} > 0$ | $0.2204 > 0.1545 > 0.0325$ | **PASS** |
| **SANITY_05** | Disconnected Node Isolation | $\Delta(\text{Rotterdam}) = 0 \land \Delta(\text{Santos}) = 0$ | Rotterdam = 0.0, Santos = 0.0 | **PASS** |

---

## 5. Machine-Readable Outputs & Evidence Figures

- **Machine-Readable JSON Output:** [`results/research/STGNN_RESULTS.json`](file:///c:/Users/Abhijay/PRIMARINE/results/research/STGNN_RESULTS.json)
- **Scenario Data Table:** [`results/research/stgnn_scenario_results.csv`](file:///c:/Users/Abhijay/PRIMARINE/results/research/stgnn_scenario_results.csv)
- **Sanity Verification CSV:** [`results/research/stgnn_sanity_checks.csv`](file:///c:/Users/Abhijay/PRIMARINE/results/research/stgnn_sanity_checks.csv)
- **Counterfactual Presentation Chart:** [`results/research/stgnn_counterfactual_comparison.png`](file:///c:/Users/Abhijay/PRIMARINE/results/research/stgnn_counterfactual_comparison.png)
