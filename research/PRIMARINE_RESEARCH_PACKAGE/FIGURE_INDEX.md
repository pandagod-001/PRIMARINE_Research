# PRIMARINE Research Package Figure Index

**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Document:** `research/PRIMARINE_RESEARCH_PACKAGE/FIGURE_INDEX.md`  

---

## Publication Figure Inventory

All figures are code-generated, reproducible, and stored in high-resolution PNG format.

| Figure ID | File Path | Scientific Purpose & Content | Source Script |
|:---|:---|:---|:---|
| **Hero Fig** | [`research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png) | **Master Hero Figure:** End-to-end decision pipeline integrating forecasting, CQR intervals, physical feasibility filtering, asymmetric fragility metrics, and selective abstention. | `generate_hero_figure.py` |
| **Fig 1** | [`research/fragility_surface/decision_fragility_heatmap.png`](file:///c:/Users/Abhijay/PRIMARINE/research/fragility_surface/decision_fragility_heatmap.png) | 2D Forecast-to-Decision Fragility Surface: Heatmap of Timing Flip Rate (%) across uncertainty scales ($0.5\times$ to $2.0\times$) and constraint tightness levels. | `08_fragility_surface.py` |
| **Fig 2** | [`research/fragility_surface/physical_flip_vs_uncertainty.png`](file:///c:/Users/Abhijay/PRIMARINE/research/fragility_surface/physical_flip_vs_uncertainty.png) | Asymmetric Fragility: Divergence between invariant physical vessel/port allocation ($0.0\%$) and acutely sensitive procurement timing ($50\%–100\%$). | `run_fragility_research.py` |
| **Fig 3** | [`research/fragility_surface/constraint_tightness_vs_fragility.png`](file:///c:/Users/Abhijay/PRIMARINE/research/fragility_surface/constraint_tightness_vs_fragility.png) | Constraint Regimes: Physical flip rate, timing flip rate, and feasible candidate count under Normal, Moderate, and Tight constraint regimes. | `11_constraint_fragility.py` |
| **Fig 4** | [`research/fragility_surface/cost_vs_abstention.png`](file:///c:/Users/Abhijay/PRIMARINE/research/fragility_surface/cost_vs_abstention.png) | Risk-Cost Trade-Off: Mean landed cost ($/MT) vs Conformal Abstention Rate across candidate threshold multipliers. | `09_abstention_vs_forced.py` |
| **Fig 5** | [`research/fragility_surface/negative_control.png`](file:///c:/Users/Abhijay/PRIMARINE/research/fragility_surface/negative_control.png) | Negative Control Sanity Check: Zero false fragility reported under uniquely constrained physical bulk fixtures. | `12_negative_control.py` |
| **Fig 6** | [`research/decision_boundary/decision_boundary_diagram.png`](file:///c:/Users/Abhijay/PRIMARINE/research/decision_boundary/decision_boundary_diagram.png) | Decision Boundary Crossing: Visualization of CQR intervals spanning the current spot price boundary ($L \le B \le U$). | `13_decision_boundary.py` |
| **Fig 7** | [`research/decision_boundary/width_vs_boundary_risk.png`](file:///c:/Users/Abhijay/PRIMARINE/research/decision_boundary/width_vs_boundary_risk.png) | Signal Separation: False breakout rate stratified by uncertainty signals (High Width vs Low Width vs Boundary Crossing). | `14_selective_boundary.py` |
| **Fig 8** | [`research/decision_boundary/risk_coverage_combined.png`](file:///c:/Users/Abhijay/PRIMARINE/research/decision_boundary/risk_coverage_combined.png) | Comparative Risk-Coverage: False breakout exposure under Width-Based vs Normalized-Margin selective abstention. | `14_selective_boundary.py` |
| **Fig 9** | [`research/decision_boundary/selective_policy_comparison.png`](file:///c:/Users/Abhijay/PRIMARINE/research/decision_boundary/selective_policy_comparison.png) | Policy Comparison: Abstention rate vs false breakout count across forced, width, boundary, and combined policies. | `14_selective_boundary.py` |
