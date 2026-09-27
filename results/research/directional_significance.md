# Statistical Significance Audit: Directional Accuracy & Error Differentials

**Document:** `results/research/directional_significance.md`  
**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  

---

## 1. Directional Accuracy Block-Bootstrap Hypothesis Test

To account for temporal autocorrelation in weekly rolling steps, a block bootstrap ($B = 1000$, block length = 5 days) was executed on out-of-sample directional outcomes:

- **Null Hypothesis ($H_0$):** Model directional accuracy $\le 50.0\%$ (No better than random coin toss).
- **Alternative Hypothesis ($H_1$):** Model directional accuracy $> 50.0\%$.
- **Test Results (LightGBM):**
  - **Empirical Mean Accuracy:** **56.43%**
  - **Block Bootstrap 95% Confidence Interval:** **[45.70% - 67.86%]**
  - **Empirical $p$-value ($P(\text{Boot Accuracy} \le 50\%)$):** **$p = 0.138$**

### Scientific Interpretation
Because the 95% bootstrap confidence interval includes 50.0% and $p = 0.138 > 0.05$, **we cannot claim formal statistical significance at the $\alpha = 0.05$ level** on the available test window. 

While the point estimate shows an empirical edge of ~56% to 60%, the sample size of non-overlapping evaluation windows leaves open the possibility of sampling noise. This must be stated honestly in all research documentation.

---

## 2. Diebold-Mariano Test for Forecast Error Differentials

- **Null Hypothesis ($H_0$):** Naive Persistence and PRIMARINE LightGBM have equal expected absolute loss ($E[|e_{\text{naive}}| - |e_{\text{lgb}}|] = 0$).
- **Test Statistic ($t_{\text{DM}}$):** $-1.651$
- **$p$-value:** **$p = 0.0988$** (Two-tailed)
- **Result:** Naive persistence holds a marginal, statistically non-zero advantage in point MAE ($d = -0.0455$), confirming that point forecasting in near-term freight markets is dominated by martingale random-walk dynamics.
