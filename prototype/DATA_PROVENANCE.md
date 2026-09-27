# PRIMARINE Research Prototype — Data Provenance

**Document Version:** 1.0.0 (Research Prototype)  
**Status:** Authoritative  

---

## 1. Primary Data Source

All 288 observation records loaded into `prototype/primarine_research_prototype/js/data.js` are directly exported from:
- **Physical File:** `research/decision_boundary/decision_boundary_analysis.csv`
- **Underlying Benchmark Dataset:** Baltic Dry Index Historical Daily Freight Series (2018–2024, 1,754 trading days).
- **Temporal Test Split:** Chronologically held-out test partition (`2023-01-01` to `2024-12-31`).

---

## 2. Feature & Metric Derivations

| Data Column | Derivation Method | Research Status |
| :--- | :--- | :--- |
| `current_rate_B` | Day $t$ spot freight index level ($/MT) | Observed historical price |
| `forecast_C` | LightGBM 7-day forward point forecast | Trained model output (zero lookahead) |
| `cqr_lower_L` | Split-CQR $\alpha=0.10$ lower bound with non-conformity calibration $q_{\text{calib}} = 0.8415$ | Conformal Quantile Regressor output |
| `cqr_upper_U` | Split-CQR $\alpha=0.10$ upper bound with non-conformity calibration $q_{\text{calib}} = 0.8415$ | Conformal Quantile Regressor output |
| `interval_width_W` | $W = U - L$ | Calculated spread metric |
| `actual_future` | Realized spot freight rate at day $t+7$ | Observed ground truth outcome |
| `false_breakout` | Flag = 1 if point forecast predicted $\Delta \ge +0.10$ (Enter) but price fell $\ge -0.10$ | Verified evaluation label |
| `timing_error` | Binary indicator of sub-optimal timing decision | Verified evaluation label |

---

## 3. Data Integrity Confirmation

- Zero records were manually fabricated or smoothed.
- 100% of data points correspond directly to physical Python experiment runs in `research/experiments/13_decision_boundary.py`.
