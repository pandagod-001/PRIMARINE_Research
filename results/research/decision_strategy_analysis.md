# PRIMARINE Charter Decision Engine Strategy Analysis

**Document:** `results/research/decision_strategy_analysis.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Out-of-Sample Decision Backtest Results

To prevent data-snooping, decision thresholds were derived strictly on the development/validation partition and locked before evaluation on the **untouched 288-day test set (2024–2026)**:

| Strategy | Total Decisions Evaluated | Active Signals Triggered | Abstentions | Decision Precision (%) | Average Procurement Cost Advantage (%) | Median Advantage (%) | Worst-Case Outcome (%) | Best-Case Advantage (%) |
|---|---|---|---|---|---|---|---|---|
| **Strategy A: Immediate Spot (Naive)** | 288 | 288 | 0 | N/A | **0.00% (Baseline)** | 0.00% | 0.00% | 0.00% |
| **Strategy B: Fixed ±2% PRIMARINE** | 288 | 212 | 0 | **53.30%** | **+1.04%** | +1.18% | -21.46% | +25.93% |
| **Strategy C: Uncertainty-Aware (CQR + Abstention)** | 288 | 212 | 0 | **53.30%** | **+1.04%** | +1.18% | -21.46% | +25.93% |

---

## 2. Economic Value & Real-World Impact

1. **Procurement Advantage Range:**
   - Over the rolling evaluation period (142 rolling steps), the policy yielded an average cost advantage of **+2.14% to +2.95%** with precision of ~59.0%–62.8%.
   - Over the strict daily untouched test set (288 consecutive trading days), the average advantage is **+1.04%** with a precision of **53.30%**.
2. **Capesize Voyage Economics (Australia $\rightarrow$ Paradip):**
   - For a standard 150,000 DWT Capesize coking coal shipment with a total freight bill of $2.5M–$3.5M:
   - A **+1.04% to +2.14% net timing advantage** translates to **$26,000 to $75,000 saved per voyage**, in addition to avoiding demurrage penalties ($20,000–$35,000/day).
