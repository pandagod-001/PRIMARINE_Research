# PRIMARINE: Uncertainty-Aware Maritime Freight Decision Intelligence

<div align="center">

![PRIMARINE Hero Banner](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png)

**Conformal Uncertainty-Gated Decision Support for Maritime Freight Procurement**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///c:/Users/Abhijay/PRIMARINE/LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Status: Frozen Research & Demo](https://img.shields.io/badge/Status-Consolidated%20%26%20Frozen-orange.svg)](file:///c:/Users/Abhijay/PRIMARINE/research/PRIMARINE_RESEARCH_PACKAGE/)
[![Evidence: 100% Traceable](https://img.shields.io/badge/Evidence-Audited%20Registry-success.svg)](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv)

</div>

---

## 1. What is PRIMARINE?

**PRIMARINE** is an **Uncertainty-Aware Maritime Freight Decision Intelligence Platform** designed to solve a multi-billion dollar vulnerability in commercial seaborne shipping: *the downstream failure of uncalibrated point-forecasts in high-stakes chartering under rigid physical vessel and port constraints.*

Commercial chartering desks traditionally rely on point estimates of spot freight rates. When sudden macro volatility induces a "false dip" (a *false breakout*), uncalibrated models recommend locking in expensive forward contracts. PRIMARINE introduces a distribution-free **Split Conformalized Quantile Regression (Split-CQR)** gating mechanism that quantifies forecast dispersion, guarantees finite-sample coverage, and selectively abstains from fragile procurement timing decisions under hard physical feasibility limits.

---

## 2. Four Reality States & System Status Matrix

To maintain strict scientific transparency, PRIMARINE explicitly separates its components into four reality states:

| Subsystem / Capability | Reality State | Scientific & Implementation Status | Authoritative Artifact |
| :--- | :--- | :--- | :--- |
| **Point Forecasting Benchmarks** | `1. VALIDATED RESEARCH` | LightGBM point MAE = `0.4644` vs Persistence = `0.4175` | [EV-001](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Turning-Point Inflection Detection** | `1. VALIDATED RESEARCH` | **F1 = 59.51%** (+32.33 pp over AR-5 baseline) | [EV-002](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Split-CQR Conformal Calibration** | `1. VALIDATED RESEARCH` | Nominal 90% coverage $\rightarrow$ **88.19%–95.83%** test coverage ($q = 0.8415$) | [EV-004](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Physical Feasibility Invariance** | `1. VALIDATED RESEARCH` | **PDFR = 0.00%** on tested dry-bulk draft/DWT constraints | [EV-005](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Asymmetric Timing Fragility** | `1. VALIDATED RESEARCH` | **TDFR = 50.00%–100.00%** under uncertainty perturbations | [EV-006](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **False-Breakout Risk Association** | `1. CONTROLLED EXPERIMENT` | High W = 40.25% vs Low W = 23.39% ($\text{AUC} = \mathbf{0.6719}$, $p < 0.01$) | [EV-007](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Selective Abstention Policy** | `1. CONTROLLED EXPERIMENT` | **-52.33% False Breakouts** ($86 \rightarrow 41$) at $\tau = 1.35\times$ (Coverage = 61.11%) | [EV-010](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Negative Results Preservation** | `1. NEGATIVE RESULT` | Boundary Crossing $\text{AUC} = 0.5025$; Sign Error $\text{AUC} = 0.4487$ | [EV-008](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv), [EV-009](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Interactive Demonstrator Cockpit** | `2. PROTOTYPE IMPLEMENTATION` | Functional local HTML5/CSS3/JS app on curated fixtures | [prototype/README.md](file:///c:/Users/Abhijay/PRIMARINE/prototype/README.md) |
| **Synthetic ST-GNN Disruption** | `2. PROOF OF CONCEPT` | 8-node synthetic graph cascade simulator ($r = 0.842$) | [EV-013](file:///c:/Users/Abhijay/PRIMARINE/research/EVIDENCE_REGISTRY.csv) |
| **Provider Adapter Architecture** | `3. PLANNED ENGINEERING` | Decoupled abstract adapters for Baltic, AIS, Weather, PCS | [docs/api/](file:///c:/Users/Abhijay/PRIMARINE/docs/api/) |
| **Production Cloud Backend** | `3. PLANNED ENGINEERING` | FastAPI microservices, TimescaleDB, FalkorDB Graph schema | [docs/PRIMARINE_PRODUCT_BLUEPRINT/](file:///c:/Users/Abhijay/PRIMARINE/docs/PRIMARINE_PRODUCT_BLUEPRINT/) |
| **Global Real-AIS ST-GNN** | `4. FUTURE RESEARCH` | Multi-billion message satellite AIS graph neural network | [Claim FR-01](file:///c:/Users/Abhijay/PRIMARINE/research/CLAIM_REGISTRY.md) |

---

## 3. What Did We Research and Find?

```
[ Research Question ]
  "How does forecast uncertainty propagate into discrete chartering choices,
   and can conformal prediction intervals serve as a risk gate?"
                          ↓
[ Positive Finding 1: Turning-Point Skill ]
  LightGBM achieves 59.51% F1 on 7-day inflection detection (+32.33 pp over AR).
                          ↓
[ Positive Finding 2: Asymmetric Fragility ]
  Physical vessel-port assignment is invariant (PDFR = 0.00%),
  while timing is acutely fragile (TDFR = 50%–100%).
                          ↓
[ Positive Finding 3: False-Breakout Gating ]
  Conformal interval width strongly associates with false-breakout exposure (AUC = 0.6719).
  Pre-calibrated abstention (tau = 1.35x) cuts false breakouts by 52.33% (p = 5.42e-11).
                          ↓
[ Negative Findings Preserved ]
  Naive spot boundary crossing is degenerate (AUC = 0.5025).
  CQR width does not predict single-step directional sign errors (AUC = 0.4487).
```

---

## 4. Quickstart: Running the Local Prototype Demonstrator

The local demonstrator is an interactive web cockpit that illustrates the complete vertical decision flow on curated dry-bulk scenarios.

```bash
# Clone the repository
git clone https://github.com/PRIMARINE-Maritime/PRIMARINE.git
cd PRIMARINE/prototype/PRIMARINE-demo

# Launch local HTTP server
python -m http.server 8000
```
Open **`http://localhost:8000`** in any modern web browser to explore:
- Interactive Indian Ocean port-vessel routing map.
- Real-time Split-CQR uncertainty gating slider.
- Feasibility filtering across draft, deadweight, and beam limits.
- Scenario disruption simulator (Red Sea closure, Cyclone warning).
- SHA-256 cryptographic audit drawer.

---

## 5. Quickstart: Reproducing the Scientific Experiments

To reproduce all published metrics and tables from source:

```bash
# Setup Python environment
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# 1. Baseline Forecasting & Inflection Detection (E1)
python scripts/experiments/01_baseline_forecasting.py

# 2. Split-CQR Conformal Calibration & Coverage (E2)
python scripts/experiments/02_cqr_calibration.py

# 3. Hard Physical Feasibility Invariance (E3)
python scripts/experiments/03_feasibility_invariance.py

# 4. Asymmetric Fragility Surface (E4)
python scripts/experiments/08_fragility_surface.py

# 5. Selective Abstention & Wilcoxon Significance (E5)
python scripts/experiments/09_abstention_vs_forced.py
python scripts/experiments/10_timing_flip_threshold.py

# 6. Spot Boundary Crossing Degeneracy (Negative Result)
python scripts/experiments/13_boundary_proximity.py
```
*Full instructions and environment details are documented in [REPRODUCIBILITY.md](file:///c:/Users/Abhijay/PRIMARINE/REPRODUCIBILITY.md).*

---

## 6. Repository Directory Structure

```
PRIMARINE/
├── README.md                               <-- Master Project Entry Point
├── LICENSE                                 <-- MIT Open Source License
├── CITATION.cff                            <-- Academic Citation Schema
├── REPRODUCIBILITY.md                      <-- Step-by-Step Reproduction Guide
│
├── docs/                                   <-- Project & Engineering Documentation
│   ├── 00_PROJECT_OVERVIEW.md              <-- Executive Orientation
│   ├── 01_ORIGINAL_SYSTEM_VISION.md        <-- 8-Stage Enterprise Blueprint
│   ├── 02_RESEARCH_QUESTION.md             <-- Formal Research Questions
│   ├── 03_RESEARCH_JOURNEY.md              <-- Chronological Evolution
│   ├── 04_WHAT_WE_FOUND.md                 <-- Comprehensive Findings Summary
│   ├── 05_CURRENT_STATUS.md                <-- Component Verification Matrix
│   ├── 06_LIMITATIONS.md                   <-- Methodological & Operational Boundaries
│   ├── RESEARCH_TO_PRODUCT_MAPPING.md      <-- Research-to-Product Matrix
│   ├── FINAL_PROJECT_STATUS.md             <-- Master 12-Section Status Audit
│   ├── api/                                <-- API Integration & Adapter Specs
│   └── PRIMARINE_PRODUCT_BLUEPRINT/          <-- 16 Comprehensive Product Blueprints
│
├── research/                               <-- Scientific Research & Evidence Core
│   ├── PRIMARINE_RESEARCH_PACKAGE/           <-- Official Frozen Research Package
│   ├── EVIDENCE_REGISTRY.csv               <-- 100% Traceable Claim-to-Code Matrix
│   ├── CLAIM_REGISTRY.md                   <-- Formal Scientific Boundary Registry
│   ├── MASTER_FILE_INVENTORY.csv           <-- 345-File Forensic Catalog
│   ├── SOURCE_OF_TRUTH.md                  <-- Authoritative Document Index
│   ├── CONFLICTS_AND_RECONCILIATION.md     <-- Discrepancy Reconciliation Log
│   └── MIGRATION_MAP.md                    <-- File Path Migration Index
│
├── data/                                   <-- Datasets & Fixtures
│   ├── README.md                           <-- Provenance, Splits & Licensing
│   ├── raw/                                <-- Historical BDI Series
│   └── fixtures/                           <-- Ports & Vessel Fleet Fixtures
│
├── scripts/                                <-- Python Code & Reproduction Scripts
│   ├── experiments/                        <-- E1 to E6 Experiment Scripts
│   └── evaluation/                         <-- Metric Evaluators & Backtests
│
├── results/                                <-- Generated Outputs
│   ├── tables/                             <-- Metrics & Significance Tables (CSV)
│   └── figures/                            <-- Visualizations & ROC Plots
│
├── prototype/                              <-- Standalone Interactive Prototype
│   └── PRIMARINE-demo/                       <-- Vertical-Slice Demonstrator Cockpit
│
└── PRIMARINE_GOOGLE_DRIVE_PACKAGE/           <-- Curated Presentation & Export Bundle
    ├── 00_START_HERE/                      <-- Plain-Language Orientation
    ├── 01_RESEARCH_REPORT/                 <-- PDF-Ready Publications
    ├── 02_RESEARCH_EVIDENCE/               <-- Registries & Conflict Logs
    ├── 03_DATASETS/                        <-- Data Dictionaries & Fixtures
    ├── 04_FIGURES/                         <-- High-Resolution Visuals
    ├── 05_CODE_AND_REPRODUCTION/           <-- Standalone Scripts
    ├── 06_PRODUCT_BLUEPRINT/               <-- System Architectures
    ├── 07_PRESENTATIONS/                   <-- SIH & Pitch Decks
    └── 08_PROTOTYPE_AND_DEMO/              <-- Prototype Package
```

---

## 7. Citation

If you use PRIMARINE research findings, code, or datasets in your academic work, please cite:

```bibtex
@article{PRIMARINE2026conformal,
  title={Conformal Uncertainty-Gated Decision Support for Maritime Freight Procurement},
  author={PRIMARINE Research Team},
  journal={Smart India Hackathon (SIH) Technical Concept Series},
  year={2026},
  url={https://github.com/PRIMARINE-Maritime/PRIMARINE}
}
```
