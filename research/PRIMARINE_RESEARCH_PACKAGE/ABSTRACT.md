# Conformal Uncertainty-Gated Decision Support for Maritime Freight Procurement
## Scientific Abstract

**Authors:** PRIMARINE Research Team  
**Problem Statement:** SIH 2026 PS-26006  
**Document:** `research/PRIMARINE_RESEARCH_PACKAGE/ABSTRACT.md`  

---

### Abstract

Maritime freight rate forecasting models are traditionally evaluated on statistical accuracy metrics (e.g., MAE, RMSE) in isolation from downstream operations. In dry-bulk raw material chartering, freight forecasts directly inform discrete physical allocations (vessel deadweight, draft compatibility, discharge port) and market-entry timing commitments. This paper investigates the propagation of forecast uncertainty through non-convex physical maritime constraints and downstream chartering optimization. 

Using historical dry-bulk freight market data (2018–2025) and Conformalized Quantile Regression (Split-CQR), we conduct a structured computational experiment across 288 held-out test scenarios and 360 constraint perturbation fixtures. We demonstrate an asymmetric fragility phenomenon: while physical vessel and port allocations remain robustly invariant under tested fixtures (Physical Decision Flip Rate = 0.00%) due to dominant physical draft and capacity boundaries, procurement timing is acutely fragile to forward rate uncertainty (Timing Decision Flip Rate = 50%–100%). Furthermore, we find that while conformal interval width does not predict binary direction errors (AUC = 0.4487) and local decision-boundary crossing is degenerate (AUC = 0.5025), conformal width serves as an effective macro-volatility regime filter that strongly predicts severe false-breakout positioning events (AUC = 0.6719, Risk Difference = +16.86%, 95% CI: [+6.14%, +28.52%], p < 0.01). 

We propose a pre-calibrated selective abstention mechanism that gates charter commitments during high-uncertainty expansions. Across held-out test scenarios, selective abstention eliminates 52.33% of false-breakout capital commitments (41 vs. 86 forced errors) at 61.11% decision coverage, trading a modest nominal landed cost difference (+0.453%, +$0.0334/MT) for substantial downside risk mitigation. Finally, we show that the integrated adaptive uncertainty pipeline achieves statistically significant improvements over unconstrained point forecasts (paired Wilcoxon signed-rank test, W = 11530.0, p = 5.42e-11). This work establishes a candidate research contribution in uncertainty-gated decision support and selective prediction for maritime logistics.
