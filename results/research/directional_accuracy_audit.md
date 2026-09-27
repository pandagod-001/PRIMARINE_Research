# Directional Accuracy Audit & Formulation Verification

**Document:** `results/research/directional_accuracy_audit.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Traceability & Mathematical Audit

### Definition in Code
Directional accuracy was audited across `scripts/04_run_models_and_backtest.py` and `scripts/09_validation_strengthening_engine.py`:
$$\Delta_{\text{actual}} = y_{t+h} - y_t, \quad \Delta_{\text{pred}} = \hat{y}_{t+h} - y_t$$
$$\text{Directional Accuracy} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left(\text{sign}(\Delta_{\text{actual}, i}) == \text{sign}(\Delta_{\text{pred}, i})\right) \times 100$$

### The Persistence 0.70% Artefact Dissected
1. **The Issue:** For Naive Persistence, $\hat{y}_{t+h} = y_t$, which implies $\Delta_{\text{pred}} \equiv 0.0$.
2. In numpy, `np.sign(0.0) == 0`.
3. In genuine trading markets, daily prices fluctuate, so $\text{sign}(\Delta_{\text{actual}}) = +1$ or $-1$ on 99.3% of observations.
4. Comparing $\text{sign}(0)$ to $\pm 1$ evaluated to equality on only 1 out of 142 days ($0.70\%$).
5. **Conclusion:** Naive persistence does not have a 0.70% accuracy; rather, **persistence refuses to take a directional stance**.
6. **Legitimate Baselines for Direction:**
   - **Random Guessing Baseline:** $50.00\%$
   - **Technical 5-day SMA:** $50.70\%$
   - **AutoRegressive AR(5):** $46.48\%$
   - **Majority Class Prevalence (Market Drift):** $54.17\%$

---

## 2. Corrected Benchmark Table

| Model | Point MAE | Directional Accuracy (%) | Status vs Random Chance (50%) |
|---|---|---|---|
| **Naive Persistence** | **0.4175** | N/A (Martingale zero-change assumption) | Neutral Benchmark |
| **5-Day SMA** | 0.4457 | 50.70% | Indistinguishable from coin toss (+0.70%) |
| **AutoRegressive AR(5)** | 0.4676 | 46.48% | Worse than random chance (-3.52%) |
| **PRIMARINE LightGBM (Multi-Modal)** | 0.4644 | **59.15%** | **+9.15% above random chance** |
| **PRIMARINE XGBoost (Multi-Modal)** | 0.4796 | **60.56%** | **+10.56% above random chance** |
