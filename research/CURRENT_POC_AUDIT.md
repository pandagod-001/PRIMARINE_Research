# Brutal Technical Audit of Existing PRIMARINE POC

**Date:** 2026-09-24  
**Audit Purpose:** Uncompromising factual review of the code, data, baselines, and claims in the initial PRIMARINE proof-of-concept.

---

## 1. Summary of Baseline Metrics vs ML Claims

A full verification of `results/metrics.json` and `results/model_comparison.csv` reveals the ground truth of the initial experiment:

| Model | MAE ($/unit) | RMSE ($/unit) | Directional Accuracy (%) | Status in POC |
|---|---|---|---|---|
| **Naive Persistence Baseline** | **0.4175** | **0.5504** | 0.70% (No movement predicted) | **Lowest Point Error** |
| **5-Day Moving Average** | 0.4457 | 0.5980 | 50.70% (Equivalent to coin toss) | Technical benchmark |
| **AutoRegressive AR(5)** | 0.4676 | 0.6235 | 46.48% | Statistical benchmark |
| **LightGBM (Multi-Modal)** | 0.4644 | 0.5821 | **59.15%** | ML Model |
| **XGBoost (Multi-Modal)** | 0.4796 | 0.6090 | **60.56%** | ML Model |

---

## 2. Inconsistencies & Weaknesses Identified

### Weakness 1: Point Forecast Error (The Martingale / Random-Walk Trap)
- **Fact:** The Naive Persistence model achieved an MAE of `0.4175`, whereas LightGBM achieved `0.4644` (+11.2% higher error) and XGBoost achieved `0.4796` (+14.8% higher error).
- **Audit Verdict:** Claiming that ML models "beat" the baseline in general point-forecasting accuracy is scientifically false. In financial and near-term freight markets, daily levels follow near-martingale properties where yesterday's price is the minimum-variance point estimator.

### Weakness 2: Erroneous Claim of ">65% Directional Accuracy"
- **Fact:** In `PRIMARINE_EVIDENCE/claims.md`, it was stated that ML models achieve `>65%` directional accuracy.
- **Audit Verdict:** The actual calculated numbers are **59.15% (LightGBM)** and **60.56% (XGBoost)**. This discrepancy must be explicitly corrected. While ~60% directional accuracy is statistically non-trivial in financial time series (random chance = 50%), it must be reported exactly without inflation.

### Weakness 3: Conformal Prediction Misnomer
- **Fact:** The uncertainty interval in the POC used empirical standard deviation of residuals multiplied by a rolling volatility ratio.
- **Audit Verdict:** While empirically effective (achieving 99.30% coverage), this is a **volatility-scaled residual heuristic**, not a mathematically rigorous conformalized quantile regression (CQR) or split-conformal calibration with guaranteed finite-sample coverage bounds.

### Weakness 4: Target Selection & Proxy Limitations
- **Fact:** The target is `BDRY` (Breakwave Dry Bulk ETF).
- **Audit Verdict:** BDRY is an aggregate financial proxy tracking Baltic freight futures, not the physical voyage freight rate ($/tonne) for the Australia (Hay Point) $\rightarrow$ East Coast India (Paradip) coking coal corridor.

### Weakness 5: Heuristic Market-Entry Rule
- **Fact:** The `ENTER_NOW` / `DEFER` decision rule used a fixed, arbitrarily chosen $\pm 2.0\%$ threshold.
- **Audit Verdict:** Fixed thresholds do not account for voyage-specific economics, fuel bunker shifts, daily demurrage penalties, or predictive uncertainty.

---

## 3. Scientific Pivot: Where the Real Novelty Lies

The audit shows that **trying to beat Naive Persistence on single-point MAE is a dead end.** 

The true scientific value of PRIMARINE lies in:
1. **Regime Detection & Heterogeneous Performance:** Identifying market conditions (surges, regime shifts, volatile supply squeezes) where baseline models catastrophically fail and ML models provide early directional warnings.
2. **True Probabilistic Quantile & Conformal Forecasting:** Estimating the full distribution $P(y_{t+h})$ rather than a fragile single-point number.
3. **Economic Chartering Decision Engine:** Deriving optimal charter timing ($ENTER$, $DEFER$, $MONITOR$, $NO\_CONFIDENCE$) based on expected economic regret, voyage duration, and risk tolerance rather than arbitrary percentage thresholds.
