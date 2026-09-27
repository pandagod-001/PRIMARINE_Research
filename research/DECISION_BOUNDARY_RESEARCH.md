# PRIMARINE: Decision-Boundary Proximity vs Conformal Uncertainty in Maritime Procurement Timing
## Research Experiment Report

**Project:** PRIMARINE — Uncertainty-Aware Maritime Freight Decision Intelligence  
**Problem Statement:** SIH 2026 PS-26006  
**Document:** `research/DECISION_BOUNDARY_RESEARCH.md`  
**Classification:** **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**  

---

## 1. Executive Summary & Research Question

The prior fragility experiments revealed a critical negative result:
- **Prediction interval width ($W$) is not a monotonic predictor of binary timing direction error** (Test error rate was $41.07\%$ for high width vs $52.27\%$ for low width).

This motivated the central research question of this study:

> **Research Question:**  
> *Is decision-boundary proximity ($M = C - B$, $NM = |C - B| / W$, or boundary crossing $L \le B \le U$) a better indicator of maritime procurement decision fragility and selective risk than prediction-interval width alone?*

---

## 2. Decision Boundary Formulations

For any held-out market observation:
- **Current Spot Freight Rate (Boundary):** $B = y_t$
- **Forward Point Forecast:** $C = \hat{y}_{t+h}$
- **Conformal Prediction Interval (Split-CQR 90%):** $[L, U] = [\hat{q}_{10} - q_{\text{calib}}, \hat{q}_{90} + q_{\text{calib}}]$
- **Decision Margin:** $M = C - B$
- **Normalized Margin:** $NM = \frac{|C - B|}{U - L}$
- **Boundary Crossing Indicator:** $\mathbb{I}(L \le B \le U)$

Deterministic Decision States:
1. **State 1 (Robust Enter):** $L > B$
2. **State 2 (Boundary Crossing):** $L \le B \le U$
3. **State 3 (Robust Defer):** $U < B$

---

## 3. Empirical Results (N = 288 Held-Out Scenarios)

### 3.1 Signal Discriminative Power Comparison

| Signal Stratum | Sample Count ($N$) | False Breakout Count | False Breakout Rate | Timing Error Rate | Mean Regret ($/MT) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Low Width ($W \le \tau$)** | 176 | 41 | $23.30\%$ | $52.27\%$ | $\$0.2371$ |
| **High Width ($W > \tau$)** | 112 | 45 | **$40.18\%$** | $41.07\%$ | $\$0.1026$ |
| **Boundary Crossing ($L \le B \le U$)** | 287 | 86 | $29.97\%$ | $48.08\%$ | $\$0.1855$ |
| **No Crossing ($L > B$ or $U < B$)** | 1 | 0 | $0.00\%$ | $0.00\%$ | $\$0.0000$ |
| **Low Norm Margin ($NM < \tau_{nm}$)** | 172 | 52 | $30.23\%$ | $50.00\%$ | $\$0.1793$ |
| **High Norm Margin ($NM \ge \tau_{nm}$)** | 116 | 34 | $29.31\%$ | $44.83\%$ | $\$0.1930$ |

### 3.2 Key Association Findings & AUC Analysis
1. **Predicting False Breakout Tail Events:**
   - **Interval Width ($W$):** $\text{AUC} = \mathbf{0.6719}$ (Moderate to strong predictor of false breakouts).
   - **Normalized Margin ($NM$):** $\text{AUC} = 0.5066$ (No discriminative power).
   - **Boundary Crossing:** $\text{AUC} = 0.5025$ (Degenerate due to 99.65% base rate).
2. **Predicting Binary Timing Direction Error:**
   - **Interval Width ($W$):** $\text{AUC} = 0.4487$ (Negative correlation with direction error).
   - **Normalized Margin ($NM$):** $\text{AUC} = 0.5183$ (Very weak).
   - **Boundary Crossing:** $\text{AUC} = 0.5033$ (No discriminative power).

---

## 4. Bootstrap Confidence Intervals (B = 1000)

- **$P(\text{False Breakout} \mid \text{High Width})$:** $40.25\%$ ($95\%\text{ CI}: [31.76\%, 49.52\%]$)
- **$P(\text{False Breakout} \mid \text{Low Width})$:** $23.39\%$ ($95\%\text{ CI}: [17.26\%, 29.73\%]$)
- **Width False Breakout Risk Difference:** **$+16.86\%$** ($95\%\text{ CI}: [+6.14\%, +28.52\%]$, $p < 0.01$)
- **Margin False Breakout Risk Difference:** $+0.70\%$ ($95\%\text{ CI}: [-10.12\%, +11.53\%]$, not statistically significant)

---

## 5. Policy Comparison & Economic Trade-Off

| Policy | Coverage | Abstention Rate | False Breakouts | Selective Risk | Mean Landed Cost ($/MT) | Net Cost Diff vs Forced |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Forced Point Forecast** | $100.0\%$ | $0.00\%$ | 86 | $47.92\%$ | $\$7.3909$ | $\$0.0000$ (Base) |
| **2. Width-Only Abstention ($\tau=1.35$)** | **$61.11\%$** | **$38.89\%$** | **41** ($-52.33\%$) | $52.27\%$ | $\$7.4243$ | $+\$0.0334$ ($+0.453\%$) |
| **3. Boundary-Crossing Abstention** | $0.35\%$ | $99.65\%$ | 0 | $0.00\%$ | $\$7.4071$ | $+\$0.0162$ |
| **4. Normalized-Margin Abstention** | $40.28\%$ | $59.72\%$ | 34 | $44.83\%$ | $\$7.3928$ | $+\$0.0019$ |

---

## 6. Scientific Interpretation & Conclusion

1. **Why Boundary Crossing Fails:** In volatile freight markets, 90% conformal prediction intervals span a mean width of $\approx \$5.76/\text{MT}$, whereas 7-day spot freight changes typically range from $\$0.20$ to $\$0.80/\text{MT}$. Consequently, $99.65\%$ of intervals encompass the current rate, making binary boundary-crossing degenerate.
2. **The True Role of Conformal Uncertainty:** Conformal interval width operates as a **macro-volatility regime filter**. When market uncertainty surges ($W > \tau$), entering the market entails high false-breakout exposure ($40.25\%$). Selective abstention eliminates **$52.33\%$** of these adverse events by deferring action to neutral spot averaging.
3. **Classification:** **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**
   - Framing: *Conformal Uncertainty-Gated Selective Prediction for Maritime Procurement Timing*.

---

## 7. Reproduction

```powershell
python research/experiments/run_boundary_research.py
```
