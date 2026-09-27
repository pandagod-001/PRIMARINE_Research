# PRIMARINE — Authoritative Source-of-Truth Specification

**Document:** `research/SOURCE_OF_TRUTH.md`  
**Classification:** Canonical Source-of-Truth Directory  
**Status:** Frozen & Audited  

---

## 1. Authoritative Document Registry

The following table defines the single authoritative canonical file for every functional, scientific, and architectural dimension of PRIMARINE:

| System Dimension | Authoritative File Path | Description / Scope |
|:---|:---|:---|
| **Central Research Contribution** | [`research/PRIMARINE_RESEARCH_PACKAGE/FINAL_RESEARCH_POSITION.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/FINAL_RESEARCH_POSITION.md) | Official publication position paper on conformal uncertainty gating and selective abstention. |
| **Research Abstract** | [`research/PRIMARINE_RESEARCH_PACKAGE/ABSTRACT.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/ABSTRACT.md) | Academic publication abstract with empirical numbers, negative results, and trade-offs. |
| **Scientific Claim Verification** | [`research/PRIMARINE_RESEARCH_PACKAGE/FINAL_CLAIM_MATRIX.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/FINAL_CLAIM_MATRIX.md) | Itemized matrix of all validated, negative, controlled simulation, and proposed claims. |
| **Literature & Prior-Art Audit** | [`research/PRIOR_ART_REVIEW.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIOR_ART_REVIEW.md) | Structured prior art review covering Makhado et al. (2026), Romano et al. (2019), and Elmachtoub & Grigas (2022). |
| **Original Product Vision** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/01_ORIGINAL_PRIMARINE_VISION.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/01_ORIGINAL_PRIMARINE_VISION.md) | Full 8-layer enterprise system vision, steel/power PSU industrial context, and end-to-end purpose. |
| **Technical Concept (SIH Document)** | [`SIH_PS26006_Comprehensive_Technical_Concept(2).md`](file:///c:/Users/Abhijay/PRIMARINE/SIH_PS26006_Comprehensive_Technical_Concept%282%29.md) | Consolidated 67-section SIH technical submission concept including latest empirical findings. |
| **Architecture Specification** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/06_COMPLETE_SYSTEM_ARCHITECTURE.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/06_COMPLETE_SYSTEM_ARCHITECTURE.md) | Microservice topology, 8-stage pipeline, and database/graph schemas. |
| **Unimplemented Capabilities Audit** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/03_WHAT_IS_NOT_IMPLEMENTED.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/03_WHAT_IS_NOT_IMPLEMENTED.md) | Forensic audit of missing live APIs, cloud databases, and RBAC authentication. |
| **Data & API Requirements Map** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/04_DATA_AND_API_REQUIREMENTS.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/04_DATA_AND_API_REQUIREMENTS.md) | Map of the 12 required data streams and provider-adapter interfaces. |
| **Research-to-Product Mapping** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/05_RESEARCH_TO_PRODUCT_MAPPING.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/05_RESEARCH_TO_PRODUCT_MAPPING.md) | Direct translation matrix connecting research discoveries to commercial UI features. |
| **Master Status Matrix** | [`docs/PRIMARINE_PRODUCT_BLUEPRINT/12_MASTER_STATUS_MATRIX.md`](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/12_MASTER_STATUS_MATRIX.md) | 11-component status audit across research, prototype, and production reality. |
| **Prototype Implementation** | [`prototype/PRIMARINE-demo/index.html`](file:///c:/Users/Abhijay/PRIMARINE/prototype/PRIMARINE-demo/index.html) | Local, self-contained interactive decision cockpit (HTML/CSS/JS). |
| **Core Research Figures Index** | [`research/PRIMARINE_RESEARCH_PACKAGE/FIGURE_INDEX.md`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/FIGURE_INDEX.md) | Complete index of all 10 publication-grade figures. |
| **Master Hero Figure** | [`research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png`](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png) | Master end-to-end decision pipeline diagram with metric annotations. |
| **Primary Real Market Dataset** | [`data/processed/freight_features_dataset.csv`](file:///c:/Users/Abhijay/PRIMARINE/data/processed/freight_features_dataset.csv) | 1,920 daily market rows (2018–2025) across BDRY, Brent, BHP, Vale, USD/INR, DXY. |

---

## 2. Research Metrics Authoritative Source

| Metric | Authoritative Value | Canonical Experiment File | Primary Data File |
|:---|:---|:---|:---|
| **Persistence Point MAE** | `0.4175` | [`results/PRIMARINE_FORECASTING_EXPERIMENT.md`](file:///c:/Users/Abhijay/PRIMARINE/results/PRIMARINE_FORECASTING_EXPERIMENT.md) | `results/model_comparison.csv` |
| **LightGBM Point MAE** | `0.4644` | [`results/PRIMARINE_FORECASTING_EXPERIMENT.md`](file:///c:/Users/Abhijay/PRIMARINE/results/PRIMARINE_FORECASTING_EXPERIMENT.md) | `results/model_comparison.csv` |
| **LightGBM Inflection F1** | `59.51%` | [`results/PRIMARINE_FORECASTING_EXPERIMENT.md`](file:///c:/Users/Abhijay/PRIMARINE/results/PRIMARINE_FORECASTING_EXPERIMENT.md) | `results/model_comparison.csv` |
| **AR(5) Inflection F1** | `27.18%` | [`results/PRIMARINE_FORECASTING_EXPERIMENT.md`](file:///c:/Users/Abhijay/PRIMARINE/results/PRIMARINE_FORECASTING_EXPERIMENT.md) | `results/model_comparison.csv` |
| **Split-CQR Test Coverage** | `88.19% to 95.83%` | [`research/experiments/08_fragility_surface.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/08_fragility_surface.py) | `research/fragility_surface/abstention_experiment.csv` |
| **Physical Decision Flip Rate** | `0.00%` | [`research/experiments/08_fragility_surface.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/08_fragility_surface.py) | `research/fragility_surface/fragility_surface.csv` |
| **Timing Decision Flip Rate** | `50.00% to 100.00%`| [`research/experiments/08_fragility_surface.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/08_fragility_surface.py) | `research/fragility_surface/fragility_surface.csv` |
| **CQR Width vs False Breakout**| $\text{AUC} = 0.6719$ | [`research/experiments/15_boundary_statistics.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/15_boundary_statistics.py) | `research/decision_boundary/bootstrap_statistics.csv` |
| **False Breakout Risk Diff** | `+16.86 pp [6.14, 28.52]` | [`research/experiments/15_boundary_statistics.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/15_boundary_statistics.py) | `research/decision_boundary/bootstrap_statistics.csv` |
| **Selective Abstention Cut** | `52.33%` ($86 \rightarrow 41$) | [`research/experiments/09_abstention_vs_forced.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/09_abstention_vs_forced.py) | `research/fragility_surface/abstention_experiment.csv` |
| **Nominal Cost Trade-Off** | `+0.453%` (`+$0.0334/MT`) | [`research/experiments/09_abstention_vs_forced.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/09_abstention_vs_forced.py) | `research/fragility_surface/abstention_experiment.csv` |
| **E5 vs E2 Paired Wilcoxon** | $W = 11530.0$, $p = 5.42\times 10^{-11}$ | [`research/experiments/value_of_information_v2_runner.py`](file:///c:/Users/Abhijay/PRIMARINE/research/experiments/value_of_information_v2_runner.py) | `research/fragility_surface/value_of_information_v2.csv` |
