# Conformal Uncertainty-Gated Decision Support for Maritime Freight Procurement
## Final Research Position Paper

**Project:** PRIMARINE — Uncertainty-Aware Maritime Freight Decision Intelligence  
**Problem Statement:** SIH 2026 PS-26006  
**Document:** `research/PRIMARINE_RESEARCH_PACKAGE/FINAL_RESEARCH_POSITION.md`  
**Classification:** **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**  

---

## 1. Selected Research Title

**Selected Title:**  
**"Conformal Uncertainty-Gated Decision Support for Maritime Freight Procurement"**

*Scientific Justification:*  
- Strongly aligns with the empirical findings without hyperbolic claims ("first", "novel", "guaranteed").
- Accurately captures the dual contribution: distribution-free conformal uncertainty intervals (Split-CQR) used as an operational gating mechanism for procurement decisions and physical feasibility validation.

---

## 2. Executive Research Story & Flow

```
+-----------------------------------------------------------------------------------+
| 1. Forward Point Forecast (LightGBM)                                              |
|    - Captures turning-point inflections (F1 = 59.51% vs AR(5) 27.18%)            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 2. Conformal Uncertainty Quantification (Split-CQR)                               |
|    - Provides finite-sample coverage guarantees (88.19% - 95.83% coverage)        |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 3. Physical Feasibility Filtering                                                  |
|    - Rigid draft, LOA, and deadweight constraints strictly bound physical vessel/ |
|      port choice (Physical Decision Flip Rate PDFR = 0.00% on tested fixtures)    |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 4. Decision Fragility Divergence                                                  |
|    - Physical allocation remains robust, while procurement timing is acutely      |
|      fragile (Timing Decision Flip Rate TDFR = 50% - 100%)                         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| 5. Macro-Regime Volatility Gating & Selective Abstention                          |
|    - High conformal width (W > tau) identifies false-breakout regimes (AUC=0.6719)|
|    - Selective abstention cuts false-breakout market entries by 52.33%             |
|    - Trades minor nominal cost (+0.453%) for major adverse positioning insurance   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Core Empirical Findings

1. **Asymmetric Decision Fragility:** Under empirical freight uncertainty, physical vessel/port allocations remain completely stable ($\text{PDFR} = 0.00\%$) because discrete physical constraints (e.g. Paradip $17.1\text{m}$ vs Haldia $11.5\text{m}$ draft) dominate continuous freight fluctuations. In contrast, procurement timing is acutely fragile ($\text{TDFR} \ge 50\%$).
2. **Predicting False Breakout Tail Events:** Conformal interval width ($W$) is an effective predictor of severe false-breakout positioning errors ($\text{AUC} = \mathbf{0.6719}$, Risk Difference $= \mathbf{+16.86\%}$, $95\%\text{ CI}: [+6.14\%, +28.52\%]$, $p < 0.01$).
3. **Selective Abstention Effectiveness:** Gating market entry on pre-calibrated conformal width ($\tau = 1.35 \times \text{Val Median Width}$) eliminates **$52.33\%$ of false breakout events** (from 86 down to 41) at a coverage of $61.11\%$.
4. **Risk-Cost Trade-Off:** Selective abstention accepts a modest nominal cost difference ($+\$0.0334/\text{MT}$ or $+0.453\%$) in exchange for substantial downside protection during volatile regime shifts.
5. **Downstream Optimization (E5 vs E2):** Coupling the full adaptive pipeline with physical constraints yields a statistically significant improvement over unconstrained point forecasts (Paired Wilcoxon $W = 11530.0$, $p = 5.42 \times 10^{-11}$).

---

## 4. Negative Results & Scientific Rigor

1. **Width vs Binary Direction Error:** Conformal interval width does *not* predict binary direction accuracy ($\text{AUC} = 0.4487$). Width measures macro-regime volatility and unconditional variance, not point forecast sign errors.
2. **Decision-Boundary Crossing:** Boundary crossing ($L \le B \le U$) is degenerate in this setting ($\text{AUC} = 0.5025$), as $99.65\%$ of $90\%$ conformal prediction intervals naturally encompass the current spot price.
3. **Normalized Decision Margin:** Normalized margin $|C - B| / W$ does not provide statistically significant risk separation ($\text{AUC} \approx 0.51$, Margin Risk Diff $= +0.70\%$, $95\%\text{ CI}: [-10.12\%, +11.53\%]$).
4. **ST-GNN Point Forecasting:** Spatial graph propagation does *not* improve univariate freight rate forecasting ($\text{MAE} \approx 0.46$ vs $0.42$ persistence); its utility is confined strictly to multi-hop spatial disruption detection.

---

## 5. Novelty Assessment & Candidate Research Contribution

- **Prior Art Context:** Makhado et al. (2026) established conformal prediction in container terminal operations. Therefore, PRIMARINE is not claimed as the "first" maritime conformal system.
- **Candidate Contribution:** PRIMARINE contributes an empirically validated, end-to-end framework demonstrating how distribution-free conformal prediction intervals (Split-CQR) interact with non-convex physical maritime berth/draft constraints to govern selective abstention, eliminating over $52\%$ of false-breakout chartering commitments.

---

## 6. Scientific Classification

### **POSSIBLE CONTRIBUTION / CONTROLLED EXPERIMENT SUPPORTED**

- **Validated Layer:** Econometric forecasting, LightGBM turning-point detection, Split-CQR calibration, selective abstention mechanics, and timing advantage.
- **Controlled Simulation Layer:** ST-GNN spatial shock propagation, 2D constraint tightness perturbations, and multi-port disruption recovery.
- **Proposed Future System:** Live broker negotiation, AIS telemetry streaming, and automated execution APIs.
