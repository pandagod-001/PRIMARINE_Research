# PRIMARINE Ideation Phase Limitations & Boundaries

**Document:** `research/IDEATION_LIMITATIONS.md`  
**Date:** 2026-09-24  
**Classification:** Research Boundaries & Engineering Transparency  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Executive Framing: Scientific Honesty as a Strength

PRIMARINE maintains a strict boundary between **empirically validated evidence** and **future implementation capabilities**. This document outlines the explicit technical boundaries of the ideation-phase prototype and explains how each will be addressed during the SIH implementation phase.

---

## 2. Comprehensive Limitations & Scope Disclosures

### 1. Market Data Proxy (`BDRY`) vs Proprietary Route Assessments
- **Current Scope:** Because commercial freight benchmarks (e.g., Baltic Exchange C5 Capesize index, Platts assessment) require paid institutional licensing, PRIMARINE utilizes `BDRY` (Breakwave Dry Bulk Shipping ETF) as an authentic, publicly accessible daily proxy tracking Baltic Capesize and Panamax futures contracts.
- **Next Phase Action:** Integrate official Baltic Exchange / S&P Platts API feeds to produce route-specific USD/tonne freight rate forecasts for Paradip, Visakhapatnam, and Haldia.

### 2. Spatio-Temporal Graph Neural Network (ST-GNN) as an Architectural Prototype
- **Current Scope:** The ST-GNN is an architectural proof-of-concept demonstrating how spatial network reasoning and message-passing propagate localized shocks across shipping lanes. It is evaluated under controlled, physically structured simulations (e.g., cyclone shock at Hay Point).
- **Explicit Disclosure:** The GNN is **not** trained on real-world historical disruption labels, and simulation outputs are not claimed as measured historical telemetry.
- **Next Phase Action:** Ingest streaming AIS data and historical maritime casualty/strike logs to train and benchmark the GNN using supervised classification metrics (ROC-AUC, Precision-Recall).

### 3. Point Forecast Error vs Turning-Point Early Warning
- **Current Scope:** Naive Persistence achieves a lower point MAE (**0.4175**) than PRIMARINE LightGBM (**0.4644**) because daily freight rates exhibit near-martingale properties during flat market regimes.
- **Explicit Disclosure:** PRIMARINE does not claim to beat persistence on point MAE. Its validated advantage is **turning-point detection** (**59.51% F1** vs **27.18%** for AR(5) and **0.00%** for Persistence on major $\ge \pm 4\%$ inflections).

### 4. Directional Accuracy Significance
- **Current Scope:** Out-of-sample directional accuracy is **59.15%** for LightGBM and **60.56%** for XGBoost (vs **50.70%** for Moving Average).
- **Explicit Disclosure:** Block-bootstrap analysis ($B=1,000$, 95% CI: $[45.70\%, 67.86\%]$, $p=0.138$) confirms that this directional improvement is **descriptive** and not statistically significant at $\alpha = 0.05$ over a 288-day sample.

### 5. Uncertainty Degradation During Historical Stress Regimes
- **Current Scope:** Conformalized Quantile Regression (Split-CQR) achieves **88.19% empirical coverage** at a 90% nominal level across normal trading periods. However, during extreme historical shocks (e.g., COVID-19 in 2020), empirical coverage drops to **50.59%**.
- **Explicit Disclosure:** PRIMARINE treats coverage breakdown not as a defect to conceal, but as an explicit risk signal that triggers **HIGH UNCERTAINTY / ABSTAIN** advisory modes in the decision engine.

### 6. Economic Procurement Advantage Scaling
- **Current Scope:** The decision engine achieves an average procurement timing advantage of **+1.04%** on the untouched 288-day test set and **+1.04% to +2.95%** across rolling evaluation windows.
- **Explicit Disclosure:** These are **simulated backtest evaluation results**, not guaranteed financial savings. Illustrative scaling ($26K–$36K on a $2.5M–$3.5M freight bill) demonstrates the operational leverage of timing optimization.

---

## 3. Road to Implementation Phase

| Current Ideation Proof-of-Concept | Post-Selection Implementation Milestone |
|---|---|
| Public market ETF proxy (`BDRY`) | Direct integration of Baltic Exchange C5 & Platts Coking Coal freight indices |
| Controlled 8-node ST-GNN simulation | 50+ node global maritime graph powered by live streaming AIS (Spire / AISHub) |
| Localized Python execution pipeline | Scalable microservice architecture with automated daily model retraining |
| Static presentation figures & markdown | Interactive React/Mapbox command center for port authority & steel procurement officers |
