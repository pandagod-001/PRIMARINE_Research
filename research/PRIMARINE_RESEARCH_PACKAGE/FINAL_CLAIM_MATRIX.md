# Final Evidence & Scientific Claim Matrix

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Document:** `research/PRIMARINE_RESEARCH_PACKAGE/FINAL_CLAIM_MATRIX.md`  
**Date:** 2026-09-26  
**Status:** Frozen & Consolidated  

---

## 1. Consolidated Scientific Claim Matrix

| Claim Item | Exact Empirical Evidence / Metric | Evaluation Population / Setting | Scientific Status |
|:---|:---|:---|:---|
| **Physical Allocation Stability** | Physical Decision Flip Rate (PDFR) = **$0.00\%$** across 360 scenario evaluations on 120k MT bulk fixtures. | $N = 360$ Scenario perturbations (6 uncertainty scales $\times$ 3 constraint regimes). | **SUPPORTED WITH LIMITATION** (Conditional on testbed fixtures with distinct draft/deadweight gaps). |
| **Procurement Timing Fragility** | Timing Decision Flip Rate (TDFR) reaches **$50.00\%$ to $100.00\%$** across lower/upper CQR bounds. | $N = 288$ Held-out test scenarios ($2023$ onwards). | **SUPPORTED** (Timing is acutely fragile to forward rate bounds). |
| **CQR Interval Calibration** | Split-CQR achieves **$88.19\%$** test coverage (original untouched test) and **$95.83\%$** (extended test split) under nominal $90.0\%$ target ($q_{\text{calib}} = 0.8415$). | $N = 288$ Held-out test scenarios. | **SUPPORTED** (Distribution-free finite-sample coverage verified). |
| **Width vs False-Breakout Association** | Interval width predicts false breakout tail events with $\text{AUC} = \mathbf{0.6719}$. False breakout rate surges from $23.39\%$ (Low Width) to $40.25\%$ (High Width); Risk Diff = $+16.86\%$ ($95\%\text{ CI}: [+6.14\%, +28.52\%]$, $p < 0.01$). | $N = 288$ Held-out test scenarios ($B = 1000$ bootstrap iterations). | **SUPPORTED** (Width is a strong predictor of false breakout tail events). |
| **Width vs Directional Error Relationship** | Interval width does not predict binary direction error ($\text{AUC} = \mathbf{0.4487}$, Spearman $r = -0.103$). Timing error rate is $41.07\%$ for High Width vs $52.27\%$ for Low Width. | $N = 288$ Held-out test scenarios. | **NEGATIVE RESULT** (Width measures unconditional variance, not point prediction accuracy). |
| **Decision-Boundary Crossing** | $99.65\%$ ($287/288$) of 90% CQR intervals cross current spot price $B$ because mean width ($\$5.76/\text{MT}$) exceeds typical 7-day moves ($\$0.20–\$0.80/\text{MT}$). $\text{AUC} = 0.5025$. | $N = 288$ Held-out test scenarios. | **NEGATIVE RESULT / DEGENERATE** (Boundary crossing is uninformative on wide intervals). |
| **Normalized Decision Margin** | Normalized margin $|C - B| / W$ has $\text{AUC} = 0.5183$ (Error) and $\text{AUC} = 0.5066$ (False Breakout). Margin Risk Diff = $+0.70\%$ ($95\%\text{ CI}: [-10.12\%, +11.53\%]$). | $N = 288$ Held-out test scenarios. | **NEGATIVE RESULT / NON-SIGNIFICANT** (Secondary to macro width). |
| **Selective Abstention Performance** | Forced point forecasting incurred 86 false breakouts. Pre-calibrated width abstention ($\tau = 1.35 \times \text{Val Median Width}$) reduced false breakouts to 41. Exact reduction: **$52.33\%$** (Abstention rate = $38.89\%$, Coverage = $61.11\%$). | $N = 288$ Held-out test scenarios. | **SUPPORTED** (Selective abstention successfully filters high-risk entries). |
| **Economic Cost Trade-Off** | Mean landed cost: Forced = $\$7.3909/\text{MT}$ vs Abstention = $\$7.4243/\text{MT}$ ($+\$0.0334/\text{MT}$ or $+0.453\%$). | $N = 288$ Held-out test scenarios. | **SUPPORTED (RISK-COST TRADE-OFF)** (Abstention trades minor nominal cost for tail-risk reduction). |
| **Economic Superiority Claim** | Claim that abstention produces strictly cheaper landed costs under all market regimes. | $N = 288$ Held-out test scenarios. | **NOT SUPPORTED / REJECTED** (Abstention is an insurance policy, not an unconditional cost minimizer). |
| **Full Adaptive System (E5 vs E2)** | E5 Full Adaptive pipeline mean cost = $\$7.3649/\text{MT}$ vs E2 Point Forecast = $\$7.3909/\text{MT}$ ($-0.351\%$). Paired Wilcoxon $W = 11530.0$, **$p = 5.42 \times 10^{-11}$**. | $N = 288$ Paired test scenarios. | **SUPPORTED** (Statistically significant downstream optimization advantage). |
| **Baseline-Plan Feasibility Retention** | $\text{BPFR} = \mathbf{1.0}$ across rate and perturbation scenarios. | $N = 360$ Scenario evaluations. | **SUPPORTED WITH LIMITATION** (Measures baseline plan feasibility retention under tested fixtures). |
| **Negative Control Sanity Check** | Under uniquely constrained fixtures (170k MT Paradip and 50k MT Haldia), physical stability = $100.0\%$, false fragility = $0.0\%$. | Controlled synthetic fixtures. | **SUPPORTED / PASS** (Metric does not report false fragility when constraints uniquely force a single solution). |
| **ST-GNN Disruption Propagation** | Proactive spatial disruption warning saves an estimated $\$0.49/\text{MT}$ in congestion demurrage. ST-GNN does not improve univariate point forecasting ($\text{MAE} \approx 0.46$). | 8-node, 11-corridor maritime graph. | **CONTROLLED SIMULATION / POC** (Spatial routing proof-of-concept; negative result on point forecasting preserved). |
| **Adaptive Disruption Recovery** | Adaptive re-routing recovers an average of $\$3.90/\text{MT}$ under port siltation (+$14.79/MT$), congestion (+$0.49/MT$), and compound cyclone closures (+$12.01/MT$). | 7 Controlled disruption scenarios (D0–D6). | **CONTROLLED SIMULATION** (Quantifies algorithmic recovery under synthetic disruption shocks). |
| **Novelty / "First System" Claim** | Claim that PRIMARINE is the first system to combine conformal prediction and maritime optimization. | Global literature review (Makhado et al., 2026). | **NOT ESTABLISHED / REJECTED** (Makhado et al., 2026 established conformal container terminal scheduling). |
| **Candidate Research Contribution** | Conformal uncertainty-gated selective prediction and physical feasibility filtering for maritime dry-bulk procurement timing. | Entire experimental suite. | **CANDIDATE RESEARCH CONTRIBUTION** (Methodologically distinct and experimentally validated on held-out data). |

---

## 2. Formal Evidence Hierarchy

1. **VALIDATED EMPIRICAL EVIDENCE:** Historical freight market dataset ($2018–2025$), LightGBM point & quantile models, Split-CQR coverage guarantees, and held-out market-entry backtest results.
2. **CONTROLLED COMPUTATIONAL EXPERIMENT:** 2D Fragility Surface, Decision Margin analysis, ROC/AUC metrics, and paired Wilcoxon statistical tests on held-out test splits.
3. **CONTROLLED SIMULATION:** ST-GNN 8-node network shock propagation, synthetic draft cuts, and multi-port disruption recovery.
4. **PROPOSED / FUTURE ARCHITECTURE:** Real-time satellite AIS stream ingestion, live broker negotiation APIs, and automated multi-vessel execution engines.
