# PRIMARINE — Changelog

All notable changes and consolidation milestones of the PRIMARINE / PRIMARINE platform are documented here.

## [1.0.0] - 2026-09-27
### Consolidated Release Gate
- **Scientific Freeze:** Completed empirical evaluations on Baltic Dry Index (2018–2024), Split-CQR finite-sample coverage ($q_{\text{calib}} = 0.8415$), and downstream fragility surfaces.
- **Selective Abstention:** Locked pre-calibrated threshold $\tau = 1.35 \times \text{validation median width}$, reducing observed false breakouts by 52.33% ($86 \rightarrow 41$) with Wilcoxon significance $p = 5.42 \times 10^{-11}$.
- **Negative Results Preserved:** Formally documented spot boundary crossing degeneracy ($\text{AUC} = 0.5025$) and sign error non-correlation ($\text{AUC} = 0.4487$).
- **Dual-Repository Architecture:** Staged `PRIMARINE_Research-` (Scientific core) and `PRIMARINE` (Product & Prototype demonstrator).
- **Google Drive Export:** Package structure `00_START_HERE` through `09_PUBLICATION` prepared.
