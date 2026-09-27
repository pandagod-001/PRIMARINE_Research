# PRIMARINE — Conflicts and Reconciliation Log

**Document Version:** 1.0.0 (Frozen Consolidation)  
**Status:** Canonical Reference  
**Scope:** Forensic reconciliation between legacy prototype drafts, early ideation documents, exploratory experimental branches, and the final frozen research package.

---

## 1. Principles of Reconciliation

To maintain scientific integrity across all public documentation, presentations, research publications, and code repositories, PRIMARINE follows strict precedence rules:

1. **Empirical Primacy:** Actual code execution outputs on disk (`research/fragility_surface/`, `results/`) supersede all narrative markdown summaries or preliminary slide decks.
2. **Four-Reality Separation:** Every artifact belongs strictly to one of:
   - `[1. VALIDATED RESEARCH]` — Empirically verified on benchmark data.
   - `[2. PROTOTYPE IMPLEMENTATION]` — Functional local code using fixtures.
   - `[3. PLANNED ENGINEERING]` — Architectural design not yet integrated.
   - `[4. FUTURE RESEARCH]` — Theoretical hypotheses requiring new experiments (e.g. real AIS ST-GNN).
3. **Negative Results Preservation:** Negative or degenerate findings (such as boundary-crossing non-discrimination) must NEVER be filtered, hidden, or smoothed.

---

## 2. Itemized Reconciliation Table

| Conflict ID | Topic / Metric | Conflicting Source A (Legacy / Preliminary) | Conflicting Source B (Canonical Frozen Package) | Root Cause Analysis | Canonical Resolution & Precedence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CR-01** | Point Forecasting MAE Superiority | Early ideation slides claimed *"LightGBM outperforms all baseline models in predicting freight rates."* | `research/PRIMARINE_RESEARCH_PACKAGE/FINAL_RESEARCH_POSITION.md` proves **Persistence MAE = 0.4175** vs **LightGBM MAE = 0.4644**. | LightGBM lags random-walk point forecasting on noisy step-ahead price levels, but captures regime dynamics. | **LightGBM DOES NOT win on point MAE.** The model's value is in **inflection detection (59.51% vs 0.00% F1)**. |
| **CR-02** | Split-CQR Coverage Guarantee | Preliminary notes referred to *"Guaranteed 90% empirical coverage under all market conditions."* | Empirical test coverage is **88.19% to 95.83%** ($q_{\text{calib}} = 0.8415$). Under COVID-19 stress, coverage drops to **50.59%**. | Split-CQR guarantees marginal finite-sample coverage under exchangeability. COVID-19 created extreme covariate shift. | **Use "Nominal 90% coverage with observed held-out test coverage of 88.19%–95.83%."** Note COVID-19 stress degradation. |
| **CR-03** | Directional Prediction Accuracy | Early exploratory drafts cited *"60.56% directional accuracy proves model reliably predicts market trends."* | `research/experiments/10_timing_flip_threshold.py` showed Directional Error vs Width has $\text{AUC} = 0.4487$. | Binary directional movement in raw prices has low signal-to-noise; width does not correlate with point-forecast sign error. | **CQR width is NOT a predictor of point-forecast direction or sign error.** It is a macro-volatility/spread uncertainty signal. |
| **CR-04** | Boundary Crossing as a Filter | Early hypothesis proposed *"Abstain whenever the prediction interval crosses the spot threshold."* | `research/experiments/13_boundary_proximity.py` demonstrated **99.65% interval crossing** ($\text{AUC} = 0.5025$). | Prediction intervals on noisy freight series are wide relative to day-to-day spot deltas, making crossing degenerate. | **Negative Result Locked.** Boundary crossing is degenerate ($\text{AUC} \approx 0.50$). Decision support relies on interval width ($\tau = 1.35\times$). |
| **CR-05** | False Breakout Reduction Claim | Draft presentation stated *"Selective prediction eliminates 52% of all false breakouts."* | At $\tau = 1.35\times$, false breakouts were reduced from **86 to 41 (52.33% reduction)** on held-out test scenarios. | Wording ambiguity: "eliminates 52%" implies eradicating all risk, whereas it reduced observed event counts by 52.33%. | **Use exact phrasing:** *"Reduced observed false-breakout events by 52.33% (86 to 41) under the tested held-out scenarios."* |
| **CR-06** | Threshold Optimality | Informal notes called $\tau = 1.35\times$ the *"Optimal universal threshold."* | $\tau = 1.35\times$ is a **pre-calibrated threshold** on validation split ($1.35 \times \text{median width}$), yielding a risk-coverage tradeoff. | Overclaiming universal optimality without out-of-distribution multi-commodity tuning. | **Labeled strictly as a "Pre-Calibrated Validation Threshold."** Economic trade-off is +0.453% nominal freight cost. |
| **CR-07** | Physical Feasibility Robustness | Early documentation claimed *"PRIMARINE guarantees 100% vessel feasibility across all global shipping."* | Experiments evaluated dry-bulk fixtures (Capesize/Panamax, Paradip/Dhamra/Haldia) yielding **PDFR = 0.00%**. | Fixture-specific structural invariance due to extreme draft/beam physical hard constraints. | **Constrained to tested dry-bulk fixtures.** *"Physical allocation remained invariant under the tested dry-bulk constraints."* |
| **CR-08** | ST-GNN Disruption Status | Architecture overview listed *"ST-GNN Disruption Propagation Engine with Live AIS Feed."* | Current status is an **8-node synthetic graph POC** (`research/experiments/07_stgnn_poc.py`). Live AIS integration is planned. | Confusing architectural vision with empirical deliverable. | **ST-GNN is classified strictly as PROOF OF CONCEPT (POC).** Live AIS ST-GNN is labeled as `FUTURE RESEARCH`. |
| **CR-09** | External API Connection Status | Prototype documentation mentioned *"Baltic Exchange, MarineTraffic, and ERA5 live integrations."* | The prototype (`prototype/PRIMARINE-demo/`) operates on **curated local fixture datasets and simulated adapter mocks**. | Prototype was built as a standalone offline demonstrator to ensure reproducibility without active paid API keys. | **All external data feeds are classified as `PLANNED ENGINEERING`.** Provider Adapter Architecture is fully documented. |
| **CR-10** | Economic Superiority Claim | Legacy pitch deck stated *"PRIMARINE strategy yields millions in cost savings over baseline."* | Untouched test savings were $+1.04\%$ to $+2.95\%$. With abstention, nominal procurement cost rose $+0.0334/\text{MT}$ ($+0.453\%$). | Abstention is an insurance mechanism (paying slight premium to avoid catastrophic tail risk/congestion). | **Explicitly NOT claiming unconditional cost minimization.** Frame as a **risk-averse downside protection mechanism**. |

---

## 3. Unresolved Items & Source Verification

*All historical conflicts identified in the forensic audit have been reconciled and verified against physical code execution artifacts.*  
No active unresolvable numerical discrepancies remain in the canonical codebase.
