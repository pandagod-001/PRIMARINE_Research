# PRIMARINE Research Prototype — Data Provenance

**Document Version:** 1.0.0  
**Status:** Authoritative  

---

## 1. Provenance of Scenario Dataset

All scenarios in `prototype/data/research_scenarios.json` are extracted directly from:
- **Source File:** `research/decision_boundary/decision_boundary_analysis.csv`
- **Underlying Series:** Baltic Dry Index (2018–2024, 1,754 trading days).
- **Evaluation Split:** Chronologically held-out test split (`2023-01-01` to `2024-12-31`).

---

## 2. Derivation Script

The JSON data was generated via `scripts/export_scenarios.py` with the following field mapping:
- `observed_spot_rate` $\longleftarrow$ `current_rate_B`
- `forecast_rate` $\longleftarrow$ `forecast_C`
- `cqr_lower_bound` $\longleftarrow$ `cqr_lower_L`
- `cqr_upper_bound` $\longleftarrow$ `cqr_upper_U`
- `realized_future_rate` $\longleftarrow$ `actual_future`
- `actual_false_breakout` $\longleftarrow$ `false_breakout`

Zero values were manually fabricated, modified, or artificially adjusted.
