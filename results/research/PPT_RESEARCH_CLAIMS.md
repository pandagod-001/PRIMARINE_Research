# PRIMARINE PPT Research Claims & Slide Narrative Guide

**Document:** `results/research/PPT_RESEARCH_CLAIMS.md`  
**Date:** 2026-09-24  
**Audience:** SIH Evaluation Panel / PPT Authors  

---

## Canonical Headline:
**PRIMARINE: FROM PRICE PREDICTION TO FREIGHT DECISION INTELLIGENCE**

---

### Core Verified Results:

#### 1. Point Forecast Reality
- **Naive Persistence Baseline:** `0.4175 MAE`
- **PRIMARINE Multi-Modal:** `0.4644 MAE`
- *Takeaway:* Raw point prediction in daily freight is near-martingale; persistence remains difficult to beat for raw flat price smoothing.

#### 2. Inflection & Turning-Point Early Warning (The Validated Edge)
- **PRIMARINE LightGBM:** `59.51% F1` (Precision: 58.4%, Recall: 60.6%)
- **AutoRegressive AR(5):** `27.18% F1`
- **5-Day Moving Average:** `26.47% F1`
- **Naive Persistence Baseline:** `0.00% F1`
- *Takeaway:* PRIMARINE improves turning-point F1 by **32.33 percentage points over AR(5)** (from 27.18% to 59.51%), successfully anticipating 7-day major cumulative freight shifts ($\ge \pm 4\%$).

#### 3. Calibrated Uncertainty Bands (Split-CQR)
- **Nominal Coverage:** `90.0%`
- **Empirical Test Coverage:** `88.19%`
- **Mean Interval Width:** `7.62 $/unit` (Median: `7.42`)
- *Takeaway:* Provides mathematically bounded, finite-sample calibrated prediction intervals instead of fragile single-point estimates.

#### 4. Actionable Charter Timing Decision
- **Untouched Out-of-Sample Test Advantage:** `+1.04%` (53.30% precision)
- **Rolling Evaluation Advantage:** `+1.04% to +2.95%`
- *Takeaway:* Observed procurement advantage: +1.04% on the untouched test split; +1.04%–+2.95% across rolling evaluations.
- *Illustrative Scaling:* A 1.04% procurement advantage on a $2.5M–$3.5M freight bill corresponds to approximately $26K–$36K *(illustrative scaling, not directly measured voyage savings)*.

#### 5. Stress Awareness & Abstention
- **Extreme Historical Stress (e.g. COVID 2020):** Coverage degrades to `50.59%`.
- *Takeaway:* Degraded uncertainty coverage during extreme regimes is used as a signal for **HIGH UNCERTAINTY / ABSTAIN** decisions rather than presenting false confidence.

#### 6. Future Research Extension
- **Spatio-Temporal Graph Neural Networks (ST-GNN):** Clearly labeled as **FUTURE WORK** for spatial network disruption propagation across global port hubs when high-frequency port graph telemetry becomes accessible.
