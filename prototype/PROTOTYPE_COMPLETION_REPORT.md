# PRIMARINE Research Prototype — Completion & Verification Report

**Prototype Version:** 1.0.0 (Research Prototype Release)  
**Status:** Validated & Functioning  
**Verification Date:** 2026-09-27  

---

## 1. Prototype Objective & Research Alignment

The **PRIMARINE Uncertainty-Gated Procurement Research Prototype** has been implemented to provide an interactive, tangible demonstration of the validated scientific research chain:
- **Point Forecast Baseline Context:** Persistence MAE = `0.4175` vs LightGBM = `0.4644`; Turning-Point F1 = `59.51%` (+32.33 pp over AR-5).
- **Split-CQR Uncertainty Quantification:** Finite-sample non-parametric calibration at nominal 90% coverage.
- **Decision Gating:** Gating via pre-calibrated interval width threshold $\tau = 5.9529$ ($1.35 \times \text{validation median}$).
- **Selective Abstention Scorecard:** Demonstrates the 52.33% reduction in observed false breakouts ($86 \rightarrow 41$) with 61.11% coverage and +0.453% nominal cost trade-off.
- **Negative Results Preservation:** Displays degenerate spot boundary crossing ($\text{AUC} = 0.5025$) and directional sign error non-correlation ($\text{AUC} = 0.4487$).

---

## 2. Verification Checklist

- [x] Sourced directly from `research/decision_boundary/decision_boundary_analysis.csv` (288 observations).
- [x] Zero fabricated data or artificial smoothing.
- [x] Explicitly hedged scientific language ("associated with", "pre-calibrated threshold").
- [x] Negative results prominently displayed.
- [x] Clear scope demarcation (does NOT connect to live AIS or execute live trades).
- [x] Standalone, zero-dependency local browser execution.
