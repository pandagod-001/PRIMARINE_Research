# PRIMARINE Validation & Rigorous Research Audit Report

**Document:** `research/VALIDATION_AUDIT.md`  
**Date:** 2026-09-24  
**Auditor:** PRIMARINE Technical Team  
**Problem Statement:** SIH 2026 PS-26006  

---

## 1. Executive Summary: Verified Findings vs Discrepancies

This audit conducts a ruthless verification of all codebase metrics, scripts, and claim inconsistencies.

### Baseline & Point-Forecast Performance Verification
The historical out-of-sample backtest over the test split (Dec 2024 to Feb 2026, 142 evaluation points) produces the following verified metrics:

| Model | MAE ($/unit) | RMSE ($/unit) | Directional Accuracy (Initial Reported) | Directional Accuracy (Mathematically Corrected) | Point MAE Rank |
|---|---|---|---|---|---|
| **Naive Persistence Baseline** | **0.4175** | **0.5504** | 0.70% (Artefact) | **Undefined / Neutral (0% change)** | **#1 (Lowest Point Error)** |
| **5-Day Moving Average** | 0.4457 | 0.5980 | 50.70% | 50.70% | #2 |
| **LightGBM Multi-Modal** | 0.4644 | 0.5821 | 59.15% | 59.15% (on non-zero moves) | #3 |
| **AutoRegressive AR(5)** | 0.4676 | 0.6235 | 46.48% | 46.48% | #4 |
| **XGBoost Multi-Modal** | 0.4796 | 0.6090 | 60.56% | 60.56% | #5 |

---

## 2. Inconsistency Root-Cause Audit

### 1. Root Cause of "Naive Directional Accuracy = 0.70%"
- **In Code:** `pred_direction = np.sign(y_pred - y_baseline_lag)`. For Naive Persistence, `y_pred == y_baseline_lag`, so `pred_direction == 0`.
- **The Problem:** `actual_direction = np.sign(actual - lag)` is $+1$ or $-1$ on 99.3% of trading days (rarely exactly 0.0000). Thus `np.mean(actual_dir == 0)` evaluated to $1/142 = 0.70\%$.
- **Correction:** Naive persistence makes *no directional bet* ($\Delta = 0$). Comparing $\text{sign}(0)$ to $\text{sign}(\pm 1)$ creates a false metric artefact. The baseline for directional accuracy is **Random Chance ($50.0\%$)** or the **Majority Class Direction ($54.2\%$ Upwards)**.

### 2. Correction of Statistical Significance Claims
- The block-bootstrap 95% Confidence Interval for LightGBM directional accuracy is **[45.70% - 67.86%]** with a mean of **56.43%**.
- Because the 95% CI contains 50.0% ($p \approx 0.14$ for directional superiority under block dependency), we **cannot claim strict statistical significance at $\alpha = 0.05$**. We must state: *"The model exhibits a positive empirical directional tendency (~56%–60%), but statistical significance at the 95% level is not established due to sample size constraints in out-of-sample test windows."*

### 3. Conformal Prediction Method Classification
- **Initial POC:** Volatility-scaled empirical standard deviation ($y \pm 1.96 \cdot \sigma_{\text{res}} \cdot \text{vol\_factor}$).
- **Strengthened Module:** Split-Conformalized Quantile Regression (CQR) with calibration set non-conformity quantiles.
- **Audit Requirement:** Explicitly distinguish between the heuristic volatility band (99.3% coverage, high mean width) and genuine CQR (84.8%–93.3% coverage with sharp interval widths).

### 4. Market Pressure Index (MPI) Incremental Value
- Must be proven via a strictly controlled 4-step ablation under identical time-series splits to prevent multicollinearity leakage.
