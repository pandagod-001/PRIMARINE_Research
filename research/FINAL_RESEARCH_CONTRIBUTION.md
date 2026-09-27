# PRIMARINE Final Research Contribution & Scientific Synthesis

**Project:** PRIMARINE — Intelligent Freight Forecasting & Chartering Decision Support  
**Problem Statement:** SIH 2026 PS-26006 (Ministry of Steel, Government of India)  
**Date:** 2026-09-24  
**Audit Status:** Fully Verified, Corrected, and PPT-Ready  

---

## 1. Executive Research Framing

> **PRIMARINE: FROM PRICE PREDICTION TO FREIGHT DECISION INTELLIGENCE**  
> *"PRIMARINE shifts maritime freight intelligence from exact price prediction toward actionable freight decision intelligence: detecting major market inflections, quantifying predictive uncertainty, and supporting risk-aware charter timing."*
>
> *"PRIMARINE does not consistently outperform persistence in point MAE. Instead, its validated contribution is stronger inflection detection, uncertainty-aware forecasting, and conversion of market signals into charter decision support in markets where persistence is difficult to beat on raw point smoothing."*
>
> *"PRIMARINE combines temporal market intelligence with spatial maritime-network reasoning. The validated market layer detects freight inflections and quantifies uncertainty, while the ST-GNN proof-of-concept provides a pathway for modeling propagation of localized maritime disruptions across connected ports and routes."*

---

## 2. Core Empirical Findings & Verified Results

### 1. Point Forecasting Benchmark
- **Naive Persistence Baseline:** **0.4175 MAE**
- **PRIMARINE Multi-Modal LightGBM:** **0.4644 MAE**
- **Scientific Interpretation:** Persistence remains difficult to beat for raw daily point forecasting due to the near-martingale properties of daily freight markets.

### 2. Major Inflection & Turning-Point Detection
- **Naive Persistence Baseline:** F1 Score = **0.00%** (Precision = 0.0%, Recall = 0.0%)
- **5-Day Simple Moving Average:** F1 Score = **26.47%** (Precision = 61.36%, Recall = 16.88%)
- **AutoRegressive AR(5):** F1 Score = **27.18%** (Precision = 60.87%, Recall = 17.50%)
- **PRIMARINE Multi-Modal LightGBM:** F1 Score = **59.51%** (Precision = 58.43%, Recall = 60.62%)
- **Scientific Interpretation:** PRIMARINE improves turning-point F1 by **32.33 percentage points over AR(5)** (from 27.18% to 59.51%, representing a +118.9% relative improvement in detailed research audits) and provides substantially stronger 7-day early-warning detection of large cumulative freight movements ($\ge \pm 4.0\%$).

### 3. Directional Movement Accuracy
- **PRIMARINE LightGBM:** **59.15%** (XGBoost: **60.56%**) vs **50.70%** for 5-Day SMA.
- **Block-Bootstrap 95% CI:** [45.70%, 67.86%], $p = 0.138$.
- **Scientific Interpretation:** *Descriptive directional improvement was observed over random chance and moving averages, but formal statistical significance at $\alpha = 0.05$ was not established due to finite out-of-sample sample size.*

### 4. Split-Conformalized Quantile Regression (CQR) & Abstention
- **Overall Calibration:** Nominal 90.0% coverage yields **88.19% empirical coverage** on the untouched test split (Mean Width: 7.6262, Median Width: 7.4212).
- **Regime Performance:**
  - *Low Volatility / Range-bound:* 93.29% coverage (Mean Width: 7.48)
  - *Normal Volatility:* 85.59% coverage (Mean Width: 7.67)
  - *Tightening / High Surge:* 66.67% coverage (Mean Width: 8.46)
  - *COVID Historical Stress (2020):* 50.59% coverage (Mean Width: 8.30)
- **Scientific Interpretation:** Degraded uncertainty coverage during extreme regimes is used as a signal for **HIGH UNCERTAINTY / ABSTAIN** decisions rather than presenting false confidence.

### 5. Economic Decision Simulation & Scaled Impact
- **Observed Procurement Advantage:** **+1.04%** on the untouched test split (288 consecutive trading days, 53.30% precision); **+1.04% to +2.95%** across rolling evaluations.
- **Illustrative Economic Scaling:** For a standard 150,000 DWT Capesize shipment with a total freight bill of $2.5M–$3.5M, a 1.04% procurement advantage corresponds to approximately **$26K–$36K**. *(Note: This is illustrative scaling, not directly measured voyage savings).*

---

## 3. Verified Master Research Scorecard

| Model / Strategy | Point MAE ($/unit) | Directional Accuracy (%) | Turning-Point F1 (%) | 90% CQR Coverage (%) | Mean Interval Width ($) | Decision Precision (%) | Observed Procurement Advantage (%) |
|---|---|---|---|---|---|---|---|
| **Naive Persistence Baseline** | **0.4175** | N/A (Martingale) | 0.00% | N/A | N/A | N/A | 0.00% (Baseline) |
| **5-Day Moving Average** | 0.4457 | 50.70% | 26.47% | N/A | N/A | 48.20% | -0.85% |
| **AutoRegressive AR(5)** | 0.4676 | 46.48% | 27.18% | N/A | N/A | 45.60% | -1.20% |
| **PRIMARINE Multi-Modal (CQR)** | 0.4644 | **59.15%** | **59.51%** | **88.19%** | **7.6262** | **53.30%** | **+1.04% (Untouched) / +1.04%–+2.95% (Rolling)** |

---

## 4. Status Breakdown: Implemented vs Prototype vs Future

| Layer | Component | Status | Validation Basis |
|---|---|---|---|
| **1. Market Forecasting** | LightGBM + Multimodal Features | 🟢 **Implemented & Validated** | 1,920 daily public observations (2018–2026) |
| **2. Uncertainty Engine** | Split-Conformalized Quantile Regression | 🟢 **Implemented & Validated** | Calibration residuals (88.19% test coverage) |
| **3. Decision Engine** | Charter Timing & Economic Regret Optimizer | 🟢 **Implemented & Validated** | Untouched 288-day backtest (+1.04% advantage) |
| **4. Spatial Network** | Spatio-Temporal Graph Neural Network (ST-GNN) | 🟡 **Implemented as Prototype / POC** | 8-node controlled disruption simulation |
| **5. High-Frequency AIS** | Live Satellite Vessel & Port Stream Ingestion | ⚪ **Future Research Extension** | Commercial / paid API access required |
| **6. Command Center UI** | Deck.gl / Mapbox Live Fleet Tracking | ⚪ **Future Work / Next Phase** | Frontend UI milestone |
