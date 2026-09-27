# PRIMARINE Scientific Audit & Final Claim Verification Matrix

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Document:** `research/FINAL_CLAIMS_AUDIT.md`  
**Date:** 2026-09-26  
**Status:** Forensic Audit Complete  

---

## 1. Executive Summary of Audit

This document records the rigorous forensic verification of all mathematical definitions, empirical results, threshold calibration procedures, and statistical claims in the PRIMARINE Forecast-to-Decision Fragility extension.

---

## 2. Forensic Claims & Evidence Audit Matrix

| Claim | Verified Evidence / Mathematical Truth | Status | Corrective Action Taken |
|:---|:---|:---|:---|
| **Physical Allocation Stability** | Across 360 scenario evaluations on fixed 120k MT bulk fixtures, physical vessel/port choice remained unchanged (PDFR = 0.00%). | **SUPPORTED (CONDITIONAL ON TEST FIXTURES)** | Explicitly noted that stability is conditional on test fixtures with distinct draft/deadweight gaps. |
| **Procurement Timing Sensitivity** | Timing flip rate across lower/upper CQR bounds reached 50.0% to 100.0% (TDFR >= 0.50). | **SUPPORTED** | Retained as empirical evidence of asymmetric decision fragility. |
| **Conformal Prediction Calibration** | Split-CQR achieved 95.83% coverage on test set (nominal target 90.0%, q_calib = 0.8415). | **SUPPORTED** | Verified without data leakage. |
| **Abstention Reduces False Breakouts** | Forced point forecasting incurred 86 false breakouts; abstention with tau=1.35 reduced this to 41. (86 - 41)/86 = 52.33%. | **SUPPORTED** | Validated; exact reduction is 52.33% in false breakout risk. |
| **Abstention Reduces Nominal Economic Cost** | Forced decision landed cost = $7.3909/MT; tau=1.35 landed cost = $7.4243/MT (+$0.0334/MT or -0.453%). | **NOT SUPPORTED (TRADE-OFF ONLY)** | Corrected claim: Selective abstention trades a slight nominal cost increase for a 52.3% reduction in false breakout exposure. |
| **Threshold tau=1.35 is "Optimal"** | Threshold was selected on validation set based on where timing flips surged; no formal global utility function was optimized. | **NOT SUPPORTED (RENAMED TO PRE-CALIBRATED)** | Renamed from "optimal threshold" to "pre-calibrated abstention threshold". |
| **Threshold Predicts Higher Timing Error** | Below tau error = 52.27% (N=176); Above tau error = 41.07% (N=112). Error rate does not monotonically increase above threshold. | **NEGATIVE RESULT / AUDITED** | Documented negative result: CQR interval width reflects macro volatility, not pointwise direction error rate. |
| **FRI = 1.0 Proves Universal Robustness** | FRI measured whether the baseline plan remained feasible under rate/draft perturbations. | **RENAMED TO BASELINE FEASIBILITY RETENTION** | Renamed metric to "Baseline-Plan Feasibility Retention" to avoid overclaiming. |
| **Full Adaptive System Advantage (E5 vs E2)** | Mean E2 = $7.3909/MT vs Mean E5 = $7.3649/MT (-0.351%). Paired Wilcoxon W = 11530.0, p = 5.42e-11 (N=288). | **SUPPORTED (STATISTICALLY SIGNIFICANT)** | Confirmed with exact paired non-parametric test. |
| **Novelty Claim** | Literature confirms candidate gap in coupling CQR intervals with physical maritime feasibility and selective abstention. | **CANDIDATE GAP / POSSIBLE CONTRIBUTION** | Maintained disciplined framing as an investigated research hypothesis. |

---

## 3. Detailed Audit Findings

### 3.1 DFI vs Decision Diversity Correction
The previous expression reporting $DFI = 0.00$ while defining $DFI = \text{unique decisions} / \text{total scenarios}$ was mathematically invalid.
- Corrected Metric: **Physical Decision Flip Rate (PDFR)** = $\frac{\text{Flips}}{\text{Scenarios}} = 0.00\%$.
- Corrected Metric: **Timing Decision Flip Rate (TDFR)** = $\frac{\text{Timing Flips}}{\text{Scenarios}} \ge 50.0\%$.

### 3.2 Threshold tau = 1.35 Calibration Audit
- Selected on validation set where normalized width exceeded $1.35 \times \text{median}$.
- When applied to the untouched test set ($N=288$), abstention rate was **$38.89\%$**, cutting false breakouts from **$86$** down to **$41$** ($52.33\%$ reduction).
- However, timing direction error rate above threshold ($41.07\%$) was lower than below threshold ($52.27\%$). This demonstrates that conformal width measures **unconditional forecast variance** rather than pointwise binary direction accuracy.

### 3.3 Economic Trade-off
- System A (Forced Point Forecast): $\$7.3909/\text{MT}$
- System C (Abstention at $\tau=1.35$): $\$7.4243/\text{MT}$
- Difference: $+0.0334/\text{MT}$ ($+0.45\%$).
- **Scientific Verdict:** Selective abstention acts as an insurance mechanism, accepting a minor expected cost penalty to guard against volatile regime shifts and false-breakout capital commitments.
