# PRIMARINE Research Prototype — Traceability Matrix

**Document Version:** 1.0.0 (Clean Architecture)  
**Status:** Authoritative  

---

## 1. End-to-End Traceability

| UI Metric / Display Element | Sourced / Computed From | Evidence Registry ID | Source Artifact / Script |
| :--- | :--- | :--- | :--- |
| **Forecast ($/MT)** | `prototype/data/research_scenarios.json` (`forecast_rate`) | [EV-001](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv), [EV-002](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `scripts/experiments/01_baseline_forecasting.py` |
| **Prediction Interval ($/MT)** | `prototype/data/research_scenarios.json` (`cqr_lower_bound`, `cqr_upper_bound`) | [EV-004](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `scripts/experiments/02_cqr_calibration.py` ($q_{\text{calib}} = 0.8415$) |
| **Interval Width (W)** | Computed dynamically: `cqr_upper_bound - cqr_lower_bound` | [EV-007](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `prototype/logic/decisionEngine.js` |
| **Decision Threshold ($\tau = 5.9529$)** | `prototype/config/research_config.json` | [EV-010](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | Validation split median ($1.35 \times 4.4096$) |
| **Decision (`PROCEED` / `DEFER`)** | Computed dynamically: `width > threshold ? 'DEFER' : 'PROCEED'` | [EV-010](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `prototype/logic/decisionEngine.js` |
| **Explanation Text** | `prototype/config/research_config.json` (`explanation_templates`) | [EV-007](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | Derived from empirical association (AUC = 0.6719) |
| **Evidence Page Metrics** | `prototype/ui/research.html` | [EV-007](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv), [EV-010](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv), [EV-011](file:///c:/Users/Abhijay/MARINEX/research/EVIDENCE_REGISTRY.csv) | `results/tables/downstream_significance.csv`, `research/fragility_surface/abstention_frontier.csv` |
