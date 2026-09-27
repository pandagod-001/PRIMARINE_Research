# PRIMARINE Research Reproducibility Manifest

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Document:** `research/PRIMARINE_RESEARCH_PACKAGE/REPRODUCIBILITY_MANIFEST.md`  
**Date:** 2026-09-26  

---

## 1. Environment & Computational Dependencies

- **Operating System:** Windows 11 / Linux Compatible
- **Python Version:** 3.10+ / 3.13 tested
- **Key Libraries:**
  - `numpy >= 1.24.0`
  - `pandas >= 2.0.0`
  - `scipy >= 1.10.0`
  - `scikit-learn >= 1.2.0`
  - `lightgbm >= 4.0.0`
  - `matplotlib >= 3.7.0`
  - `seaborn >= 0.12.0`

---

## 2. Dataset & Temporal Splits

- **Raw Data Path:** `data/processed/freight_features_dataset.csv`
- **Total Market Observations:** 1,920 trading days (2018–2025)
- **Forecast Horizon:** $H = 7$ trading days ahead
- **Split Breakdown:**
  - **Training Set (70%):** 1,344 rows (2018-03-29 to 2023-07-28)
  - **Validation Set (15%):** 288 rows (2023-07-31 to 2024-09-18) — Used strictly for CQR nonconformity calibration ($q_{\text{calib}} = 0.8415$) and threshold pre-calibration ($\tau = 1.35 \times \text{median}$).
  - **Untouched Test Set (15%):** 288 rows (2024-09-19 to 2025-11-06) — Evaluated strictly once without data leakage.

---

## 3. Master Execution Commands

### A. Run Core Fragility Surface Research Suite:
```powershell
python research/experiments/run_fragility_research.py
```
*Executes:*
- `08_fragility_surface.py` (2D Fragility Surface Grid)
- `09_abstention_vs_forced.py` (Cost vs Abstention curves)
- `10_timing_flip_threshold.py` (Threshold stability & negative result check)
- `11_constraint_fragility.py` (Constraint perturbation regimes)
- `12_negative_control.py` (Sanity check on uniquely constrained fixtures)
- `value_of_information_v2_runner.py` (Paired VoI series)

### B. Run Decision Boundary & Selective Prediction Suite:
```powershell
python research/experiments/run_boundary_research.py
```
*Executes:*
- `13_decision_boundary.py` (Decision margins, boundary crossings, interval states)
- `14_selective_boundary.py` (Signal comparisons, policy evaluations, risk-coverage data)
- `15_boundary_statistics.py` (Bootstrap 95% CIs, ROC/AUC metrics, margin stratifications)

---

## 4. Generated Artifact Directory Structure

```
research/
├── PRIMARINE_RESEARCH_PACKAGE/
│   ├── ABSTRACT.md
│   ├── FINAL_RESEARCH_POSITION.md
│   ├── FINAL_CLAIM_MATRIX.md
│   ├── PRIOR_ART_REVIEW.md
│   ├── REPRODUCIBILITY_MANIFEST.md
│   └── FIGURE_INDEX.md
├── fragility_surface/
│   ├── fragility_surface.csv
│   ├── abstention_experiment.csv
│   ├── threshold_analysis.csv
│   ├── constraint_sensitivity_v2.csv
│   ├── negative_control.csv
│   ├── value_of_information_v2.csv
│   └── *.png (8 figures)
└── decision_boundary/
    ├── decision_boundary_analysis.csv
    ├── width_boundary_comparison.csv
    ├── risk_coverage.csv
    ├── margin_analysis.csv
    ├── selective_policy_comparison.csv
    ├── bootstrap_statistics.csv
    └── *.png (8 figures)
```
