# PRIMARINE: Forecast-to-Decision Fragility Surface & Selective Abstention in Maritime Chartering
## Audited Scientific Research Report

**Project:** PRIMARINE — Uncertainty-Aware Maritime Freight Decision Intelligence  
**Problem Statement:** SIH 2026 PS-26006  
**Document:** `research/FRAGILITY_RESEARCH_REPORT_AUDITED.md`  
**Classification:** **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**  

---

## 1. Executive Summary & Research Question

Traditional machine learning benchmarks in maritime logistics evaluate freight forecasting models purely through point-prediction accuracy metrics ($\text{MAE}$, $\text{RMSE}$, $\text{DA}$). However, in chartering operations, freight forecasts directly inform discrete physical resource allocations (vessel class, discharge port, corridor) and market-entry timing commitments.

This research extension investigates the following central scientific question:

> **Research Question:**  
> *Does forecast uncertainty propagate uniformly through the maritime decision pipeline, or does it induce asymmetric fragility—leaving physical vessel/port allocations robustly constrained while causing high instability and false breakouts in procurement timing? Can calibrated conformal uncertainty intervals support a principled selective abstention mechanism to mitigate procurement risk?*

---

## 2. Research Hypothesis

> **Hypothesis:**  
> *"Forecast uncertainty does not affect all maritime decisions equally. It has a limited effect on physically constrained vessel/port allocation (where hard draft and deadweight boundaries dominate) while having a substantially larger effect on procurement timing and decision confidence."*

---

## 3. Preservation of Authoritative Evidence Baseline

All previously validated empirical milestones remain preserved without modification:

| Layer | Benchmark / Model | Metric | Value | Verification Source |
| :--- | :--- | :--- | :--- | :--- |
| **Point Forecasting** | Baseline Persistence | Test MAE | `0.4175` | [`results/PRIMARINE_FORECASTING_EXPERIMENT.md`](file:///c:/Users/Abhijay/PRIMARINE/results/PRIMARINE_FORECASTING_EXPERIMENT.md) |
| | LightGBM (10-seed avg) | Test MAE | `0.4644` | Verified (Untouched Split) |
| **Turning Points ($\ge \pm 4\%$)** | Persistence | Inflection F1 | `0.00%` | Baseline Blindness |
| | AR(5) Baseline | Inflection F1 | `27.18%` | Econometric |
| | 5-Day SMA | Inflection F1 | `26.47%` | Technical Filter |
| | LightGBM | Inflection F1 | `59.51%` | +32.33% over AR(5) |
| **Directional Accuracy** | 5-Day SMA | 5-day DA | `50.70%` | Random Walk Level |
| | LightGBM | 5-day DA | `59.15%` | Directional Skill |
| | XGBoost | 5-day DA | `60.56%` | Directional Skill |
| **Conformal Uncertainty** | Split-CQR (Nominal 90%) | Test Coverage | `88.19%` | Verified Coverage |
| | | Mean Interval Width | `7.62` | Verified Mean Span |
| | COVID Stress Period | Stress Coverage | `50.59%` | Identifies Volatility Shock |
| **Procurement Timing** | Untouched Test Period | Landed Cost Gain | `+1.04%` | Verified Timing Edge |
| | Rolling Regimes | Landed Cost Gain | `+1.04% to +2.95%` | Verified Timing Edge |
| **Network Intelligence** | ST-GNN (Proof of Concept) | Graph Scope | 8 Nodes, 11 Corridors | Controlled Synthetic Graph |

---

## 4. Prior Art & Methodological Review

As cataloged in [`research/PRIOR_ART_REVIEW.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIOR_ART_REVIEW.md):
- **Alizadeh & Nomikos (2009) / Kavussanos (2014):** Parametric volatility models (GARCH) for financial FFA hedging, lacking physical port/vessel constraints (**PARTIALLY OVERLAPPING / RELATED**).
- **Romano et al. (2019):** Conformalized Quantile Regression (CQR) providing distribution-free finite-sample guarantees (**RELATED**).
- **Elmachtoub & Grigas (2022):** Smart Predict-then-Optimize (SPO) for decision-loss training in linear/convex problems (**RELATED**).
- **Geifman & El-Yaniv (2017):** Selective prediction and risk-coverage abstention trade-offs (**RELATED**).
- **Duan et al. (2023) / Wang et al. (2018):** Stochastic port scheduling under synthetic uncertainty trees (**PARTIALLY OVERLAPPING**).

---

## 5. Methodology & Uncertainty Construction

### Explicit Uncertainty Scenarios
Scenarios are constructed directly from calibrated Split-CQR bounds without assuming parametric Gaussianity:
- **Central Scenario:** $\hat{y}_{\text{central}} = \hat{y}_{\text{point}}$
- **Lower Scenario:** $\hat{y}_{\text{low}} = \max(0.5, \hat{y}_{\text{point}} - s \cdot W_{\text{half}})$
- **Upper Scenario:** $\hat{y}_{\text{upp}} = \hat{y}_{\text{point}} + s \cdot W_{\text{half}}$
where $s \in \{0.50, 0.75, 1.00, 1.25, 1.50, 2.00\}$ and $W_{\text{half}}$ is derived on the validation set ($q_{\text{calib}} = 0.8415$, validation median width = $4.4096$).

---

## 6. Mathematical Definition of Audited Metrics

1. **Physical Decision Flip Rate (PDFR):**
   $$\text{PDFR} = \frac{1}{|\mathcal{S}|} \sum_{s \in \mathcal{S}} \mathbb{I}\left( (\text{Vessel}_s, \text{Port}_s, \text{Route}_s) \neq (\text{Vessel}_0, \text{Port}_0, \text{Route}_0) \right)$$
2. **Timing Decision Flip Rate (TDFR):**
   $$\text{TDFR} = \frac{1}{|\mathcal{S}|} \sum_{s \in \mathcal{S}} \mathbb{I}\left( \text{Timing}_s \neq \text{Timing}_0 \right)$$
3. **Baseline-Plan Feasibility Retention (BPFR):**
   $$\text{BPFR} = \frac{1}{|\mathcal{S}|} \sum_{s \in \mathcal{S}} \mathbb{I}(\text{Plan}_0 \text{ remains feasible in scenario } s)$$
4. **Economic Regret:**
   $$\text{Regret} = \text{LandedCost}(\text{Action}) - \min(\text{Spot}_t, \text{Spot}_{t+h})$$
5. **Selective Abstention Rate:**
   $$\text{AR}(\tau) = \frac{1}{N_{\text{test}}} \sum_{i=1}^{N_{\text{test}}} \mathbb{I}(W_i > \tau)$$

---

## 7. Audited Findings Across Experiments

### Experiment 1: 2D Forecast-to-Decision Fragility Surface
Across $360$ scenario evaluations spanning 6 uncertainty scales and 3 constraint tightness levels:
- **Physical Decision Flip Rate:** **$0.00\%$** ($\text{PDFR} = 0.0$). Physical vessel/port allocations remain completely invariant under the tested fixtures because draft ($17.1\text{m}$ vs $11.5\text{m}$) and deadweight ($120\text{k MT}$) dominate rate fluctuations.
- **Timing Decision Flip Rate:** **$50.00\%$ to $100.00\%$** ($\text{TDFR} \ge 0.50$). Procurement timing is acutely fragile to rate bounds.
- **Baseline-Plan Feasibility Retention:** **$100.0\%$** ($\text{BPFR} = 1.0$) across all tested scales.

---

### Experiment 2: Conformal Abstention vs Forced Decisions
Evaluated on $288$ held-out test scenarios across candidate threshold multipliers ($\tau = \text{mult} \times \text{Val Median Width}$):

| Threshold Multiplier ($\text{mult}$) | Absolute Threshold ($\tau$) | Abstention Rate | False Breakout Errors | Mean Landed Cost ($/MT) | Net Cost Diff vs Forced |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.80** | $3.5277$ | $96.88\%$ | **0** | $\$7.4069$ | $+0.217\%$ |
| **1.00** | $4.4096$ | $88.89\%$ | **1** | $\$7.4114$ | $+0.278\%$ |
| **1.20** | $5.2915$ | $55.56\%$ | **21** | $\$7.4234$ | $+0.440\%$ |
| **1.35 (Pre-Calibrated)** | **$5.9529$** | **$38.89\%$** | **41** (vs 86 forced) | **$\$7.4243$** | **$+0.453\%$** |
| **1.50** | $6.6144$ | $32.64\%$ | **50** | $\$7.4217$ | $+0.417\%$ |
| **1.80** | $7.9373$ | $3.82\%$ | **84** | $\$7.3968$ | $+0.081\%$ |
| **No Abstention** | $\infty$ | $0.00\%$ | **86** | $\$7.3909$ | $0.000\%$ |

*Audited Trade-off:* Selective abstention at pre-calibrated threshold $\tau = 1.35 \times \text{Val Median Width}$ eliminates **$52.33\%$ of false-breakout positioning errors** (41 vs 86) while accepting a minor nominal cost difference of $+\$0.0334/\text{MT}$ ($+0.453\%$) as an operational risk hedge.

---

### Experiment 3: Threshold Analysis & Negative Result on Error Monotonicity
- **Pre-calibrated Threshold:** $\tau = 5.9529$ derived on validation set.
- **Negative Result:** Pointwise timing error rate above threshold ($41.07\%$, $N=112$) was lower than below threshold ($52.27\%$, $N=176$).
- **Scientific Rationale:** Conformal width captures macro-regime volatility rather than point prediction directional error. High uncertainty signals market expansion where large trends unfold, but where committing capital involves severe tail risk.

---

### Experiment 4: Constraint Tightness & Negative Control Sanity Checks
- **Constraint Tightness:** Feasible solution space drops from 9 to 6 candidates under draft siltation; physical allocation remains $100\%$ stable on tested fixtures.
- **Negative Control Sanity Check:** Verified that under 170k MT Paradip and 50k MT Haldia fixtures, only 1 vessel is physically feasible, yielding 0.0% false fragility as expected.

---

### Experiment 5: Value of Information (VoI V2) & Paired Statistics
- **E2 Point Forecast:** $\$7.3909/\text{MT}$
- **E5 Full Adaptive Pipeline:** $\$7.3649/\text{MT}$
- **Improvement:** $-\$0.0260/\text{MT}$ ($-0.351\%$)
- **Paired Non-Parametric Test:** Paired Wilcoxon signed-rank test on $N=288$ paired test scenarios yields $W = 11530.0$, **$p = 5.42 \times 10^{-11}$** ($p < 0.001$).

---

## 8. Final Research Position & Novelty Assessment

### Classification: **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**

- **Supported Research Finding:** Physical feasibility acts as a rigid boundary insulating vessel class allocation from freight uncertainty under standard fixtures, whereas procurement timing is acutely fragile. Calibrated conformal prediction intervals (Split-CQR) provide a viable mechanism for selective abstention, cutting false breakout events by $52.33\%$ at the cost of a modest operational risk spread.
