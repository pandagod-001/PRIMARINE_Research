# PRIMARINE Research Prototype — Research Traceability Matrix

**Document Version:** 1.0.0 (Research Prototype)  
**Status:** Authoritative  

---

## 1. Feature-to-Evidence Mapping

| Prototype Interface Element | Corresponding Research Claim | Evidence Registry ID | Source Experiment Script | Canonical Result CSV / Output |
| :--- | :--- | :--- | :--- | :--- |
| **Point Forecast & Inflection Bar** | LightGBM captures 7-day inflection detection with F1 = 59.51% (Persistence MAE: 0.4175 vs LightGBM: 0.4644) | [EV-001](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv), [EV-002](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `scripts/experiments/01_baseline_forecasting.py` | `results/tables/forecasting_metrics.csv`, `results/tables/inflection_metrics.csv` |
| **Conformal Prediction Interval Fan** | Split-CQR finite-sample coverage at nominal 90% (Empirical test coverage = 88.19%) | [EV-004](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `scripts/experiments/02_cqr_calibration.py` | `results/tables/cqr_coverage_results.csv` |
| **Elevated vs Lower Width Gating** | High interval width associates with false-breakout exposure (Risk Diff = +16.86 pp, AUC = 0.6719, $p < 0.01$) | [EV-007](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/10_timing_flip_threshold.py` | `research/fragility_surface/threshold_roc_data.csv` |
| **Pre-Calibrated Threshold ($\tau = 5.9529$)** | Threshold derived from validation split median ($\tau = 1.35 \times 4.4096$) | [EV-010](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/09_abstention_vs_forced.py` | `research/fragility_surface/abstention_frontier.csv` |
| **Selective Abstention Scorecard** | Gating reduces false breakouts by 52.33% (86 $\rightarrow$ 41) with 61.11% coverage (+0.453% cost premium) | [EV-010](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/09_abstention_vs_forced.py` | `research/fragility_surface/abstention_frontier.csv` |
| **Downstream Wilcoxon Test** | Statistically significant downstream optimization divergence ($p = 5.42 \times 10^{-11}$, $W = 11530.0$) | [EV-011](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/09_abstention_vs_forced.py` | `results/tables/downstream_significance.csv` |
| **Spot Boundary Crossing Degeneracy** | 99.65% interval crossing yields random discrimination ($\text{AUC} = 0.5025$) | [EV-008](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/13_boundary_proximity.py` | `results/tables/boundary_proximity_metrics.csv` |
| **Directional Sign Error Non-Correlation** | CQR width does not correlate with point-forecast sign error ($\text{AUC} = 0.4487$) | [EV-009](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `research/experiments/10_timing_flip_threshold.py` | `results/tables/directional_error_correlation.csv` |
