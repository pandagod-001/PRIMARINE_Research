# PRIMARINE — Intelligent Freight Forecasting & Chartering Decision Support

**Problem Statement:** SIH 2026 PS-26006  
**Organization:** Ministry of Steel, Government of India  
**System Status:** Research Validated & PPT-Ready (Empirical Data Freeze)  

---

## 1. Project Overview
PRIMARINE is an intelligent maritime freight decision-support framework designed to assist Indian steel manufacturing organizations (such as SAIL) in timing overseas bulk raw material procurement (coking coal, thermal coal, iron ore) and optimizing vessel charter contracts.

---

## 2. Problem Statement & Operational Challenge
Raw material procurement to India's East Coast ports (e.g. Hay Point $\rightarrow$ Paradip) represents hundreds of millions of dollars in volatile freight commitments. Freight rates fluctuate unpredictably, and daily market movements follow near-martingale properties where naive flat persistence is difficult to beat on single-point MAE. However, persistence is completely blind to major rate surges and crashes, leading to severe commercial regret and demurrage penalties.

---

## 3. Current Validated Architecture
The validated prototype is structured into four integrated layers:
1. **Multimodal Data Ingestion Layer:** Ingests genuine exchange-traded freight futures proxies (`BDRY`), marine bunker proxies (`BZ=F`), upstream miner demand (`BHP`, `VALE`), macroeconomic purchasing power (`DX-Y.NYB`), and FX rates (`INR=X`).
2. **Market Pressure Index (MPI) & Regime Segmentation:** Quantifies market velocity and segments conditions into Stable, Normal, and Surge volatility states.
3. **Split-Conformalized Quantile Regression (CQR):** Generates distribution-free, finite-sample calibrated prediction intervals (nominal 90% coverage).
4. **Uncertainty-Aware Charter Timing Engine:** Translates probability distributions and rate momentum into actionable charter timing decisions (`ENTER_NOW`, `DEFER_ENTRY`, `MONITOR`, `ABSTAIN`).

---

## 4. Dataset & Data Source Limitations
- **Target Variable:** Breakwave Dry Bulk Shipping ETF (`BDRY`), an exchange-traded proxy reflecting near-dated Baltic Capesize (50%), Panamax (40%), and Supramax (10%) freight futures.
- **Explicit Proxy Notice:** *PUBLIC PROXY — NOT THE PROPRIETARY ROUTE-SPECIFIC FREIGHT ASSESSMENT.* Commercial route assessments (e.g. Platts Hay Point to Paradip $/tonne) require paid institutional subscriptions.
- **Dataset Size:** 1,920 clean daily observations across ~7.7 years (2018–2026).

---

## 5. Experimental Methodology & Validation Rigor
- **Zero Future-Leakage Guarantee:** Chronological partitioning into Training (1,344 days, ~70%), Calibration/Validation (288 days, ~15%), and an Untouched Out-of-Sample Test Set (288 days, ~15%, Dec 2024 to Feb 2026).
- **No Test-Set Threshold Snooping:** Decision and turning-point thresholds ($\pm 2.0\%$ charter trigger, $\pm 4.0\%$ inflection trigger) were locked on validation data prior to test set evaluation.

---

## 6. Final Master Research Scorecard

| Model / Strategy | Point MAE ($/unit) | Directional Accuracy (%) | Turning-Point F1 (%) | 90% CQR Coverage (%) | Mean Interval Width ($) | Decision Precision (%) | Observed Procurement Advantage (%) |
|---|---|---|---|---|---|---|---|
| **Naive Persistence Baseline** | **0.4175** | N/A (Martingale) | 0.00% | N/A | N/A | N/A | 0.00% (Baseline) |
| **5-Day Moving Average** | 0.4457 | 50.70% | 26.47% | N/A | N/A | 48.20% | -0.85% |
| **AutoRegressive AR(5)** | 0.4676 | 46.48% | 27.18% | N/A | N/A | 45.60% | -1.20% |
| **PRIMARINE Multi-Modal (CQR)** | 0.4644 | **59.15%** | **59.51%** | **88.19%** | **7.6262** | **53.30%** | **+1.04% (Untouched) / +1.04%–+2.95% (Rolling)** |

---

## 7. Turning-Point Detection Findings
- **Persistence Failure:** Naive persistence achieves an F1 score of **0.00%** (Precision: 0.0%, Recall: 0.0%) as it predicts zero deviation from spot rates.
- **PRIMARINE Performance:** Captures 60.62% of major $\ge \pm 4.0\%$ rate inflections with 58.43% precision (**F1 = 59.51%**).
- **Improvement:** PRIMARINE improves turning-point F1 by **32.33 percentage points over AR(5)** (from 27.18% to 59.51%, representing a +118.9% relative increase).

---

## 8. Split-CQR Uncertainty Results
- **Overall Calibration:** Nominal 90.0% coverage $\rightarrow$ **88.19% empirical coverage** on the untouched test split (Mean Width: 7.6262, Median Width: 7.4212).
- **Regime Breakdown:** Low Volatility: 93.29% coverage | Normal Volatility: 85.59% | High Surge: 66.67% | COVID Stress (2020): 50.59%.

---

## 9. Charter Decision Results & Scaled Impact
- **Procurement Advantage:** Observed procurement advantage: **+1.04% on the untouched test split; +1.04%–+2.95% across rolling evaluations**.
- **Illustrative Economic Scaling:** A 1.04% procurement advantage on a $2.5M–$3.5M freight bill corresponds to approximately **$26K–$36K**. *(Illustrative scaling, not directly measured voyage savings).*

---

## 10. Abstention & Uncertainty Behavior
Degraded uncertainty coverage during extreme regimes is used as a signal for **HIGH UNCERTAINTY / ABSTAIN** decisions rather than presenting false confidence.

---

## 11. Limitations
1. Does not beat persistence on point MAE during flat range-bound markets.
2. Descriptive directional improvement (~59%–60%) is observed, but formal statistical significance at $\alpha = 0.05$ is not established.
3. BDRY is an aggregate futures proxy, not physical voyage assessments.

---

## 12. Future Research Extension — Spatio-Temporal GNN
- **Concept:** Spatio-temporal graph neural network over port nodes (Hay Point, Paradip, Vizag) and shipping routes to model spatial network disruption propagation.
- **Validation Boundary:** *ST-GNN is a future extension and is not included in the current validated experimental results because the required high-frequency port/AIS graph telemetry is not currently part of the validated public dataset.*

---

## 13. Exact Distinction: Implemented vs Future

| Implemented & Validated in POC | Future Conceptual Extensions |
|---|---|
| 🟢 Multi-modal daily time-series ingestion (1,920 obs) | ⚪ Full Spatio-Temporal GNN across 20+ port nodes |
| 🟢 Rolling forward backtesting engine (zero leakage) | ⚪ High-frequency satellite/terrestrial AIS telemetry |
| 🟢 Split-Conformalized Quantile Regression (CQR) | ⚪ Automated live Notice of Readiness (NOR) Go engine |
| 🟢 Turning-point detection & charter timing simulation | ⚪ Interactive Deck.gl / Mapbox Command Center UI |

---

## 14. Reproducibility Instructions
```bash
# 1. Ingest authentic market data
python scripts/01_data_ingestion.py

# 2. Generate engineered multimodal features
python scripts/02_feature_engineering.py

# 3. Run validation and research strengthening engine
python scripts/09_validation_strengthening_engine.py

# 4. Run final verification and language audit
python scripts/10_final_shortcoming_fix.py
python scripts/11_check_language.py
```

---

## 15. Final PPT Central Slide
**Headline:** PRIMARINE: FROM PRICE PREDICTION TO FREIGHT DECISION INTELLIGENCE  
1. **Point Forecasting:** Persistence (0.4175 MAE) vs PRIMARINE (0.4644 MAE).  
2. **Inflection Early Warning:** PRIMARINE (59.51% F1) vs AR(5) (27.18% F1) vs Persistence (0.00% F1).  
3. **Calibrated Uncertainty:** 90% nominal CQR $\rightarrow$ 88.19% empirical coverage.  
4. **Charter Decision:** +1.04% untouched-test procurement advantage (+1.04%–+2.95% rolling).  
5. **Stress Awareness:** Extreme stress $\rightarrow$ degraded coverage $\rightarrow$ HIGH UNCERTAINTY / ABSTAIN.  
6. **Future Extension:** Spatio-Temporal GNN for spatial network disruption cascades.
