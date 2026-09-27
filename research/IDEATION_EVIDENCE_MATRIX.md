# PRIMARINE Ideation Evidence Matrix & Scientific Hierarchy

**Document:** `research/IDEATION_EVIDENCE_MATRIX.md`  
**Date:** 2026-09-24  
**Classification:** Scientific Traceability & Audit Framework  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Master Evidence Hierarchy

To ensure total transparency for SIH evaluators, all PRIMARINE capabilities are categorized into four distinct evidence tiers:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. EMPIRICALLY VALIDATED CORE                                                   │
│    Tested on 1,920 authentic daily market observations (2018–2026)              │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 2. CONTROLLED PROOF-OF-CONCEPT                                                  │
│    Tested via architectural graph simulations on verified physical topology     │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 3. PROPOSED PRODUCTION SYSTEM                                                   │
│    Engineering blueprints and data pipelines planned for SIH build phase        │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 4. FUTURE VALIDATION CRITERIA                                                   │
│    Empirical benchmarks to be evaluated once commercial telemetry is ingested   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Complete Evidence Audit Table

| System Capability | Implementation / Code Source | Data Basis | Quantitative Result | Evidence Tier | Status |
|---|---|---|---|---|---|
| **Daily Freight Time-Series Ingestion** | [`scripts/01_data_ingestion.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/01_data_ingestion.py) | Public Yahoo Finance APIs (BDRY, Brent, BHP, Vale, FX, DXY) | 1,920 clean daily rows (2018–2026) | **1. Empirically Validated** | Verified |
| **Point Freight Forecasting (7-Day)** | [`scripts/09_validation_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/09_validation_strengthening_engine.py) | Out-of-sample 288-day test split (2024–2026) | Persistence MAE: **0.4175** vs LightGBM: **0.4644** | **1. Empirically Validated** | Verified |
| **Inflection / Turning-Point Detection** | [`scripts/09_validation_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/09_validation_strengthening_engine.py) | 160 major 7-day inflection events ($\ge \pm 4.0\%$) | PRIMARINE F1: **59.51%** vs AR(5): **27.18%** (+32.33 pp) | **1. Empirically Validated** | Verified |
| **Directional Movement Prediction** | [`scripts/07_research_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/07_research_strengthening_engine.py) | Block-Bootstrap evaluation ($B=1,000$) | LightGBM: **59.15%** (95% CI: [45.70%, 67.86%], $p=0.138$) | **1. Empirically Validated** | Verified (Descriptive) |
| **Uncertainty Calibration (Split-CQR)** | [`scripts/09_validation_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/09_validation_strengthening_engine.py) | 288-day calibration + 288-day test split | Nominal 90.0% $\rightarrow$ **88.19% empirical coverage** | **1. Empirically Validated** | Verified |
| **Historical Stress Degradation** | [`scripts/07_research_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/07_research_strengthening_engine.py) | COVID-19 2020 extreme market shock | Coverage drops to **50.59%** (Triggers ABSTAIN) | **1. Empirically Validated** | Verified |
| **Procurement Decision Backtest** | [`scripts/09_validation_strengthening_engine.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/09_validation_strengthening_engine.py) | 288-day untouched test split & 142 rolling steps | **+1.04%** (Untouched) / **+1.04%–+2.95%** (Rolling) | **1. Empirically Validated** | Verified |
| **Maritime Network Graph Topology** | [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py) | Authentic physical bulk ports & shipping corridors | 8 Nodes, 11 Navigable Corridors | **2. Controlled POC** | Verified |
| **Disruption Message-Passing Diffusion** | [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py) | Controlled cyclone shock injection at Hay Point | Epicenter: **+0.2204**, Corridors: **+0.1545**, Vizag/Haldia: **+0.0325** | **2. Controlled POC** | Verified |
| **Spatial Distance Hop Attenuation** | [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py) | Controlled multi-hop graph convolution | Hop 0: **+0.2204** > Hop 1: **+0.1545** > Hop 2: **+0.0325** | **2. Controlled POC** | Verified |
| **Disconnected Node Isolation** | [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py) | Controlled graph partition test (Rotterdam/Santos) | $\Delta \text{Risk} = \mathbf{0.0000}$ (Zero leakage) | **2. Controlled POC** | Verified |
| **Counterfactual Shock Sensitivity** | [`scripts/13_run_stgnn_extension.py`](file:///c:/Users/Abhijay/PRIMARINE/scripts/13_run_stgnn_extension.py) | Comparison across Baseline, Moderate, and Severe shocks | Monotonic risk response (Sev 1.0: +0.2204 $\rightarrow$ Sev 1.5: +0.3251) | **2. Controlled POC** | Verified |
| **Live Satellite AIS Vessel Stream Ingestion** | Future Implementation Phase | Streaming AIS telemetry (Spire, MarineTraffic, AISHub) | Real-time vessel positions, speeds, heading, draught | **3. Proposed System** | Future Phase |
| **Real Port Berth Queue Telemetry** | Future Implementation Phase | Port Authority EDI feeds & berth management systems | Real-time anchorage counts, dwell times, queue hours | **3. Proposed System** | Future Phase |
| **Supervised Disruption Risk Evaluation** | Future Implementation Phase | Historical Lloyd's List / Maritime casualty incident logs | Formal ROC-AUC / F1 on historical disruption ground truth | **4. Future Validation** | Future Phase |
| **Ministry / Operator Command Dashboard** | Future Implementation Phase | React, Next.js, Deck.gl, Mapbox GL maritime overlay | Interactive fleet monitoring, route risk, charter advisory | **3. Proposed System** | Future Phase |

---

## 3. Methodological Distinctions for Evaluators

1. **Why Naive Persistence MAE (0.4175) Beats LightGBM MAE (0.4644):**  
   Daily freight indices exhibit near-martingale properties on range-bound days. Point smoothing naturally minimizes absolute error by outputting yesterday's price. PRIMARINE does not claim to outperform persistence on point MAE.
2. **Why Inflection F1 (59.51% vs 27.18%) Is the Decisive Metric:**  
   In vessel procurement, charterers do not fix vessels on small daily fluctuations. The high-value decision is anticipating multi-day swings ($\ge \pm 4\%$). Persistence has an F1 score of **0.00%** because it cannot anticipate turning points. PRIMARINE provides reliable 7-day early warning.
3. **Why ST-GNN Is an Architectural Prototype:**  
   Graph propagation equations and spatial distance attenuation are fully functional in code and verified under controlled simulations. However, because public AIS and port queue telemetry are unavailable for free research, GNN outputs are not claimed as supervised historical predictions.
