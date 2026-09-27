# PRIMARINE — Reproduction Audit & Execution Matrix

**Document Version:** 1.0.0 (Release Gate)  
**Status:** Audit Pass (100% Deterministic Reproducibility)  
**Scope:** Verification of all experimental reproduction scripts, inputs, configurations, seeds, and expected metrics.

---

## 1. Master Reproduction Audit Matrix

| Experiment ID | Script Path | Input Data Path | Random Seed | Leakage Controls | Output Path | Expected Key Metric | Reproducibility Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **E1: Baseline Forecasting** | `scripts/experiments/01_baseline_forecasting.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | Chronological temporal split; feature lagging $t-1$ | `results/tables/forecasting_metrics.csv` | LightGBM Inflection F1 = **59.51%**; Persistence MAE = **0.4175** | **VERIFIED (REPRODUCIBLE)** |
| **E2: Split-CQR Calibration** | `scripts/experiments/02_cqr_calibration.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | 3-way split: 2018-2021 train, 2022 calib, 2023-2024 test | `results/tables/cqr_coverage_results.csv` | $q_{\text{calib}} = \mathbf{0.8415}$; Empirical Coverage = **88.19%–95.83%** | **VERIFIED (REPRODUCIBLE)** |
| **E3: Physical Invariance** | `scripts/experiments/03_feasibility_invariance.py` | `data/fixtures/indian_ocean_ports.json` | N/A (Deterministic) | Fixed naval architecture & port berth constraints | `results/tables/feasibility_summary.csv` | Physical Decision Flip Rate ($\text{PDFR}$) = **0.00%** | **VERIFIED (REPRODUCIBLE)** |
| **E4: Fragility Surface** | `scripts/experiments/08_fragility_surface.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | Evaluated on held-out test splits | `research/fragility_surface/fragility_summary.csv` | Timing Decision Flip Rate ($\text{TDFR}$) = **50.00%–100.00%** | **VERIFIED (REPRODUCIBLE)** |
| **E5: Selective Abstention** | `scripts/experiments/09_abstention_vs_forced.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | Gating threshold $\tau = 1.35\times$ pre-calibrated on calib set | `research/fragility_surface/abstention_frontier.csv` | False-Breakout Reduction = **52.33%**; Wilcoxon $p = \mathbf{5.42 \times 10^{-11}}$ | **VERIFIED (REPRODUCIBLE)** |
| **E5: Boundary Correlation** | `scripts/experiments/10_timing_flip_threshold.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | Scenario rollouts on held-out testbed | `research/fragility_surface/threshold_roc_data.csv` | False-Breakout ROC $\text{AUC} = \mathbf{0.6719}$ ($p < 0.01$) | **VERIFIED (REPRODUCIBLE)** |
| **NF: Boundary Degeneracy** | `scripts/experiments/13_boundary_proximity.py` | `data/raw/bdi_historical_2018_2024.csv` | `seed=42` | Evaluated on testbed price deltas | `results/tables/boundary_proximity_metrics.csv` | Spot Crossing $\text{AUC} = \mathbf{0.5025}$ (99.65% cross) | **VERIFIED (REPRODUCIBLE)** |
| **E6: Synthetic ST-GNN POC** | `scripts/experiments/07_stgnn_poc.py` | Synthetic 8-Node Graph (11 Corridors) | `seed=42` | Controlled synthetic delay injections | `results/tables/stgnn_poc_metrics.csv` | Cascade Delay Correlation Pearson $r = \mathbf{0.842}$ | **VERIFIED (REPRODUCIBLE)** |

---

## 2. Environment Verification

- **Python Version:** Tested and verified on Python 3.10 and 3.11.
- **Dependencies:** Standard scientific stack (`numpy`, `pandas`, `scipy`, `scikit-learn`, `lightgbm`, `xgboost`, `matplotlib`).
- **Execution Speed:** Full test suite executes in $< 60$ seconds on a standard modern CPU.
