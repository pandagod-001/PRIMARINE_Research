# Decision-Boundary Aware Selective Prediction Audit Matrix

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Document:** `research/DECISION_BOUNDARY_CLAIMS_AUDIT.md`  
**Date:** 2026-09-26  
**Status:** Audit Complete  

---

## 1. Executive Summary & Verification Matrix

This audit verifies whether decision-boundary proximity ($M = C - B$, $NM = |C - B| / W$, or boundary crossing $L \le B \le U$) explains timing fragility better than conformal prediction interval width ($W$) alone.

| Research Question / Claim | Empirical Evidence (N = 288 Held-Out Scenarios) | Scientific Status |
|:---|:---|:---|
| **1. Does interval width predict timing error?** | AUC = 0.4487, Spearman r = -0.103. Error rate is 41.07% (High W) vs 52.27% (Low W). | **NEGATIVE RESULT / NOT SUPPORTED** (Width does not predict binary direction error). |
| **2. Does interval width predict false breakout risk?** | AUC = 0.6719. High Width has 40.25% false breakout rate vs 23.39% for Low Width (Risk diff = +16.86%, 95% CI: [+6.14%, +28.52%]). | **SUPPORTED** (Width is a strong predictor of false breakout tail events). |
| **3. Does boundary crossing predict timing risk?** | In 287/288 scenarios (99.65%), the calibrated 90% CQR interval spanned the current spot price ($L \le B \le U$). AUC = 0.5033 (Error), AUC = 0.5025 (False Breakout). | **NOT SUPPORTED (DEGENERATE ON BROAD INTERVALS)** (CQR width exceeds typical 7-day rate shifts). |
| **4. Does normalized margin predict timing risk?** | AUC = 0.5183 (Error), AUC = 0.5066 (False Breakout). Low NM error = 50.0% vs High NM error = 44.83%. | **WEAK PREDICTOR** (Slight directional correlation, but secondary to macro width). |
| **5. Does width-based abstention reduce false breakouts?** | Reduces false breakouts from 86 down to 41 (52.33% reduction) with an abstention rate of 38.89%. | **SUPPORTED** |
| **6. What is the economic cost trade-off?** | Forced: $7.3909/MT vs Width Abstention: $7.4243/MT (+$0.0334/MT or +0.453%). | **RISK-COST TRADE-OFF SUPPORTED** |
| **7. Does the negative control behave correctly?** | In synthetic test fixture with wide intervals safely detached from the boundary (e.g., $L > B$), boundary-aware logic preserves 100% decision coverage without spurious abstention. | **PASS / SUPPORTED** |
| **8. Overall Research Hypothesis** | *Finding:* Decision-boundary crossing is degenerate for wide distribution-free prediction intervals (span > weekly move). Conformal width $W$ remains the primary, empirical predictor of large false-breakout capital risk. | **PARTIALLY SUPPORTED (WIDTH REMAINS SUPERIOR FOR RISK MITIGATION)** |

---

## 2. Answers to Specific Evaluation Questions

1. **Does interval width predict timing risk?**  
   *No for binary error direction (AUC = 0.45), but YES for severe false breakout positioning (AUC = 0.67).*
2. **Does CQR boundary crossing predict timing risk?**  
   *No (AUC = 0.50).* Because 90% conformal bands have a mean width of 5.76 $/MT while weekly freight moves are typically 0.20–0.80 $/MT, the interval spans the boundary in 99.65% of scenarios.
3. **Does normalized margin predict timing risk?**  
   *Weakly (AUC = 0.518).* Does not outperform calibrated interval width.
4. **Does boundary-aware abstention outperform width-only abstention on selective risk?**  
   *No.* Pure boundary-crossing abstention abstains in 99.65% of scenarios, rendering it operationally unusable. Normalized-margin abstention achieves selective risk of 44.83% with 59.72% abstention, but width-based abstention remains the cleanest operational policy (38.89% abstention, 52.33% false breakout elimination).
5. **Does it reduce false-breakout exposure?**  
   *Yes, width-based abstention eliminates 52.33% of false breakouts.*
6. **What is the cost trade-off?**  
   *Trades a +0.453% nominal landed cost difference (+$0.0334/MT) for a 52.33% reduction in adverse positioning risk.*
7. **Does the negative control behave correctly?**  
   *Yes (Pass).*
8. **Does this provide a stronger candidate research contribution than width-only abstention?**  
   *It provides a crucial scientific clarification:* It proves that the value of conformal prediction in freight logistics is **not** local boundary thresholding, but **macro-volatility regime gating** that prevents false-breakout commitments during regime shifts.
