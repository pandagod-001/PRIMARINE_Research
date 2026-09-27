# Turning-Point Detection & Inflection Analysis

**Document:** `results/research/turning_point_analysis.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Operational Definition & Mathematical Formulation

In commercial dry bulk chartering, minor day-to-day noise does not warrant adjusting vessel fixture timing. The primary operational objective is detecting **major 7-day freight inflections** ($\ge \pm 4.0\%$).

- **Exact Formulation at Date $t$:**
  $$\Delta_{\text{pct}}(t) = \frac{y(t+7) - y(t)}{y(t)} \times 100$$
  - **Class $+1$ (Major Upward Surge):** $\Delta_{\text{pct}}(t) \ge +4.0\%$
  - **Class $-1$ (Major Downward Drop):** $\Delta_{\text{pct}}(t) \le -4.0\%$
  - **Class $0$ (Range-bound / Noise):** $|\Delta_{\text{pct}}(t)| < 4.0\%$
- **Temporal Causality & Zero Lookahead:** Predictions are generated strictly at time $t$ using information $\le t$ to predict the condition at $t+7$ (7-day positive lead time).
- **Threshold Integrity:** The $\pm 4.0\%$ threshold was fixed during the development phase prior to running evaluation on the untouched out-of-sample test split.

---

## 2. Test-Set Event Distribution Audit ($N = 288$ Days)

A strict audit of the untouched test split (Dec 31, 2024 to Feb 27, 2026) reveals:

| Category | Count | Percentage of Test Set |
|---|---|---|
| **Total Test Observations** | **288** | **100.00%** |
| **Major Upward Surges ($\ge +4\%$)** | 102 | 35.42% |
| **Major Downward Drops ($\le -4\%$)** | 58 | 20.14% |
| **Total Major Inflection Events** | **160** | **55.56%** |
| **Range-bound / Noise (Class 0)** | 128 | 44.44% |

> **Methodological Note on Event Prevalence:**  
> The 55.56% event rate reflects the characteristic high volatility of the underlying Baltic dry bulk freight futures market (BDRY proxy) over multi-day (7-day) cumulative horizons, where cumulative multi-day rate swings frequently exceed $\pm 4\%$.

---

## 3. Benchmarking Inflection Detection Performance

| Model | Total Events | Predicted Events | Precision (%) | Recall (%) | F1 Score (%) | Accuracy (%) |
|---|---|---|---|---|---|---|
| **Naive Persistence Baseline** | 160 | 0 | 0.00% | 0.00% | **0.00%** | 44.44% |
| **5-Day Simple Moving Average** | 160 | 44 | 61.36% | 16.88% | **26.47%** | 47.92% |
| **AutoRegressive AR(5)** | 160 | 46 | 60.87% | 17.50% | **27.18%** | 47.92% |
| **PRIMARINE Multi-Modal (LightGBM)** | 160 | 166 | 58.43% | 60.62% | **59.51%** | **54.17%** |

---

## 4. Key Scientific Conclusion

- **Percentage Point Improvement:** PRIMARINE improves turning-point F1 by **32.33 percentage points over AR(5)** (from 27.18% to 59.51%) and by **33.04 percentage points over 5-Day SMA** (from 26.47% to 59.51%).
- **Relative Improvement:** This corresponds to a **+118.9% relative increase in F1 score over AR(5)** and a **+124.8% relative increase over SMA**.
- **Persistence Failure:** Naive persistence achieves an F1 score of **0.00%** because it assumes zero price change ($\Delta = 0$). While persistence minimizes point MAE during flat days, it is blind to large market turns. PRIMARINE provides reliable 7-day early warning of major market inflections.
