# PRIMARINE — Claim Registry & Scientific Boundaries

**Document Version:** 1.0.0 (Frozen Consolidation)  
**Status:** Canonical Reference  
**Purpose:** Formal specification of scientific boundaries, verified claims, controlled results, negative findings, prototype capabilities, and planned engineering.

---

## 1. Verified Scientific Claims (VALIDATED)

These claims are directly supported by empirical data, reproducible scripts, and verified statistical significance tests in the repository.

### Claim V-01: Point Forecast MAE Reality
- **Claim:** Single-step point forecasting models (LightGBM) do not achieve superior point MAE relative to a naive random-walk Persistence baseline on noisy daily freight price series.
- **Evidence:** Persistence MAE = `0.4175` vs LightGBM MAE = `0.4644`.
- **Reference:** [EV-001](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `scripts/experiments/01_baseline_forecasting.py`.

### Claim V-02: Turning-Point Inflection Detection
- **Claim:** Tree-based gradient boosted models (LightGBM) capture macro-regime inflection points ($\ge \pm 4\%$ rate movement over 7 days) significantly better than linear or autoregressive baselines.
- **Evidence:** LightGBM Inflection F1 = `59.51%` vs Persistence = `0.00%`, 5-Day SMA = `26.47%`, AR(5) = `27.18%` (+32.33 percentage point improvement).
- **Reference:** [EV-002](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `results/tables/inflection_metrics.csv`.

### Claim V-03: Marginal Finite-Sample Conformal Coverage
- **Claim:** Split Conformalized Quantile Regression (Split-CQR) provides distribution-free, finite-sample prediction intervals satisfying nominal 90% marginal coverage on held-out test splits under exchangeability.
- **Evidence:** Empirical coverage across held-out splits = `88.19% to 95.83%` ($q_{\text{calib}} = 0.8415$, mean interval width = `$5.76 to $7.62 / MT`).
- **Limitation:** Coverage drops under catastrophic macroeconomic regime shifts (e.g., COVID-19 pandemic stress test coverage = `50.59%`).
- **Reference:** [EV-004](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `scripts/experiments/02_cqr_calibration.py`.

### Claim V-04: Asymmetric Decision Fragility (Physical vs Timing)
- **Claim:** Physical vessel-to-port allocation decisions exhibit extreme robustness to price/rate uncertainty due to rigid draft/deadweight constraints (PDFR = 0.00% on tested dry-bulk fixtures), whereas procurement timing decisions exhibit severe fragility (TDFR = 50%–100% under uncertainty perturbations).
- **Evidence:** PDFR = `0.00%` across Capesize/Panamax/Supramax testbeds; TDFR ranges from `50.00% to 100.00%` across perturbation envelopes.
- **Reference:** [EV-005](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), [EV-006](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `research/fragility_surface/fragility_summary.csv`.

### Claim V-05: Downstream Decision Optimization Significance
- **Claim:** Incorporating conformal uncertainty gating into multi-stage procurement optimization produces decisions that are statistically distinguishable from unconstrained baseline optimization.
- **Evidence:** Paired Wilcoxon signed-rank test on 288 paired procurement decision cycles yields $W = 11530.0$, $p = 5.42 \times 10^{-11}$.
- **Reference:** [EV-011](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `results/tables/downstream_significance.csv`.

---

## 2. Controlled Experiment Claims (CONTROLLED_EXPERIMENT)

These claims hold strictly within the evaluated scenario testbeds and simulation parameters.

### Claim CE-01: Conformal Width as a Macro False-Breakout Filter
- **Claim:** High calibrated conformal interval width is observationally associated with greater false-breakout exposure during market breakouts.
- **Evidence:** High-width scenarios exhibited `40.25%` observed false-breakout rate vs `23.39%` in low-width scenarios (Risk Difference = `+16.86 percentage points`, 95% CI: `[+6.14, +28.52]`, $p < 0.01$, $\text{AUC} = 0.6719$).
- **Scientific Guardrail:** CQR interval width indicates regime-level volatility and forecast dispersion; it **DOES NOT** predict single-step market direction or forecast sign correctness.
- **Reference:** [EV-007](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `research/experiments/10_timing_flip_threshold.py`.

### Claim CE-02: Pre-Calibrated Selective Abstention
- **Claim:** Gating procurement timing with a pre-calibrated interval-width threshold ($\tau = 1.35 \times \text{validation median width}$) reduced observed false-breakout events by 52.33% (from 86 to 41 events) while retaining 61.11% decision coverage.
- **Economic Trade-off:** Incurs a nominal cost difference of `+$0.0334/MT` (`+0.453%`), functioning as an explicit risk-averse insurance policy.
- **Scientific Guardrail:** $\tau = 1.35\times$ is a **pre-calibrated threshold**, NOT an analytically optimal universal constant.
- **Reference:** [EV-010](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `research/experiments/09_abstention_vs_forced.py`.

---

## 3. Negative Findings (NEGATIVE_RESULT)

These findings represent disproven hypotheses and degenerate mechanisms that are explicitly preserved for scientific transparency.

### Finding NF-01: Spot Boundary-Crossing Degeneracy
- **Finding:** Abstaining when the prediction interval crosses the current spot price is degenerate and fails to provide discriminative decision support.
- **Evidence:** `99.65%` of evaluated intervals crossed the current spot boundary, yielding a random discrimination ROC $\text{AUC} = 0.5025$.
- **Conclusion:** Point-to-interval boundary crossing is useless in noisy daily freight series because normal volatility bounds encompass daily spot deltas.
- **Reference:** [EV-008](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `research/experiments/13_boundary_proximity.py`.

### Finding NF-02: Non-Monotonicity of Binary Directional Sign Error
- **Finding:** CQR interval width does NOT correlate with binary directional forecast sign errors.
- **Evidence:** Directional Error vs CQR Width ROC $\text{AUC} = 0.4487$.
- **Conclusion:** Wider uncertainty intervals reflect market volatility and model epistemic spread, not the binary sign correctness of the point forecast.
- **Reference:** [EV-009](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), `research/experiments/10_timing_flip_threshold.py`.

---

## 4. Prototype Claims (PROTOTYPE_IMPLEMENTATION)

These capabilities are demonstrated in the interactive local software prototype (`prototype/PRIMARINE-demo/`).

### Claim P-01: Interactive Vertical-Slice Demonstrator
- **Status:** Functional local demonstrator running on vanilla HTML5/CSS3/JavaScript.
- **Capabilities:**
  1. 8-node Indian Ocean dry-bulk network visualization with dynamic route rendering.
  2. Physical feasibility filtering (Draft, DWT, Beam, LOA constraints across Paradip, Dhamra, Haldia, Visakhapatnam, Singapore, Richards Bay, Newcastle, Port Hedland).
  3. Interactive Split-CQR uncertainty gating (`ENTER`, `DEFER`, `ABSTAIN`).
  4. Real-time disruption injection and adaptive re-ranking demonstration.
  5. Complete cryptographically hash-chained decision audit logging.
- **Boundary:** Uses curated local JSON fixtures and simulated telemetry; **NOT** a connected production backend.
- **Reference:** [prototype/README.md](file:///c:/Users/Abhijay/PRIMARINE/prototype/README.md).

---

## 5. Planned Engineering Claims (PLANNED_ENGINEERING)

These represent the designed production architecture documented in engineering blueprints, pending live enterprise deployment.

### Claim PE-01: Provider-Adapter Ingestion Architecture
- **Status:** Architecture fully specified with interfaces and mock adapters; live production subscriptions pending.
- **Scope:** Adapters designed for Baltic Exchange (Freight), MarineTraffic / Spire (AIS), ECMWF / Copernicus (ERA5 Weather), Port Community Systems (Berth Queues), and ERP / SAP (Cargo Ingestion).
- **Reference:** [docs/api/PROVIDER_ADAPTER_ARCHITECTURE.md](file:///c:/Users/Abhijay/PRIMARINE/docs/api/PROVIDER_ADAPTER_ARCHITECTURE.md).

### Claim PE-02: Production Data Layer
- **Status:** Schema specified; pending deployment to AWS/GCP cloud environment.
- **Scope:** TimescaleDB (Time-series telemetry), FalkorDB / Neo4j (Maritime Knowledge Graph), Redis (Live state caching).
- **Reference:** [docs/PRIMARINE_PRODUCT_BLUEPRINT/03_ENTERPRISE_SYSTEM_ARCHITECTURE.md](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/03_ENTERPRISE_SYSTEM_ARCHITECTURE.md).

---

## 6. Future Research Claims (FUTURE_RESEARCH)

These represent long-term research directions requiring multi-terabyte datasets and distributed GPU clusters.

### Claim FR-01: Global Real-AIS Spatio-Temporal Graph Neural Network
- **Status:** 8-node synthetic proof-of-concept completed; global real-AIS model is **NOT YET VALIDATED**.
- **Scope:** Training an ST-GNN on multi-billion message global terrestrial and satellite AIS streams for global delay propagation and maritime choke-point congestion prediction.
- **Reference:** [EV-013](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), [EV-014](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv).
