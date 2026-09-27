# PRIMARINE — Master Reproducibility Guide

**System Version:** 1.0.0 (Frozen Consolidation)  
**Status:** Canonical Reference  
**Scope:** Step-by-step instructions to reproduce all empirical experiments, metrics, figures, and launch the local prototype demonstrator.

---

## 1. Environment & Setup

### Requirements
- **Python:** 3.10 or 3.11 (Recommended)
- **Node.js:** v18+ (Optional, for running local HTTP servers)
- **Operating System:** Linux, macOS, or Windows (PowerShell/WSL)

### Virtual Environment Setup
```bash
# Clone the repository
git clone https://github.com/PRIMARINE-Maritime/PRIMARINE.git
cd PRIMARINE

# Create and activate Python virtual environment
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install core scientific and ML dependencies
pip install -r requirements.txt
```

---

## 2. Reproducing Empirical Research Experiments

All experimental scripts are deterministic with fixed random seeds (`seed=42`). Run the following commands from the repository root:

### Step 1: Baseline Forecasting & Inflection Detection (E1)
Evaluates Persistence, 5-Day SMA, AR(5), LightGBM, and XGBoost on Baltic Dry Index data.
```bash
python scripts/experiments/01_baseline_forecasting.py
```
- **Outputs:** `results/tables/forecasting_metrics.csv`, `results/tables/inflection_metrics.csv`
- **Expected Key Metrics:** LightGBM Inflection F1 = `59.51%`, Persistence MAE = `0.4175`, LightGBM MAE = `0.4644`.

### Step 2: Split-CQR Conformal Calibration & Coverage (E2)
Calibrates quantile regressors and computes empirical finite-sample coverage.
```bash
python scripts/experiments/02_cqr_calibration.py
```
- **Outputs:** `results/tables/cqr_coverage_results.csv`, `results/figures/uncertainty/cqr_interval_fan.png`
- **Expected Key Metrics:** $q_{\text{calib}} = 0.8415$, Empirical Test Coverage = `88.19%–95.83%`.

### Step 3: Hard Physical Feasibility Invariance (E3)
Tests vessel-to-port allocation stability under rate perturbations across Paradip, Dhamra, and Haldia berths.
```bash
python scripts/experiments/03_feasibility_invariance.py
```
- **Outputs:** `results/tables/feasibility_summary.csv`
- **Expected Key Metrics:** Physical Decision Flip Rate ($\text{PDFR}$) = `0.00%`.

### Step 4: Decision Fragility & Perturbation Surface (E4)
Generates multi-dimensional fragility surfaces across uncertainty perturbations.
```bash
python scripts/experiments/08_fragility_surface.py
```
- **Outputs:** `research/fragility_surface/fragility_summary.csv`
- **Expected Key Metrics:** Timing Decision Flip Rate ($\text{TDFR}$) = `50.00%–100.00%`.

### Step 5: Decision-Boundary & Selective Abstention Policy (E5)
Evaluates false-breakout risk correlation, selective abstention threshold ($\tau = 1.35\times$), and paired Wilcoxon test.
```bash
python scripts/experiments/09_abstention_vs_forced.py
python scripts/experiments/10_timing_flip_threshold.py
```
- **Outputs:** `research/fragility_surface/abstention_frontier.csv`, `results/tables/downstream_significance.csv`
- **Expected Key Metrics:** False-Breakout Reduction = `52.33%` (86 $\rightarrow$ 41), Decision Coverage = `61.11%`, Cost Premium = `+$0.0334/MT` (+0.453%), Wilcoxon $p = 5.42 \times 10^{-11}$.

### Step 6: Negative Controls & Boundary Degeneracy (NF)
Verifies spot boundary-crossing degeneracy and directional sign error non-correlation.
```bash
python scripts/experiments/13_boundary_proximity.py
```
- **Outputs:** `results/tables/boundary_proximity_metrics.csv`
- **Expected Key Metrics:** Boundary-Crossing $\text{AUC} = 0.5025$, Directional Error $\text{AUC} = 0.4487$.

---

## 3. Running the Interactive Prototype Demonstrator

The PRIMARINE local demonstrator is an interactive single-page application requiring zero complex server setup.

```bash
# Navigate to the prototype directory
cd prototype/PRIMARINE-demo

# Launch a lightweight local HTTP server (Python 3)
python -m http.server 8000
```
- **Open Browser:** Navigate to `http://localhost:8000` to interact with the full cockpit:
  - Dynamic Indian Ocean map and route renderer.
  - Physical feasibility filtering across 8 ports and 5 vessel classes.
  - Interactive Split-CQR uncertainty gating slider.
  - Scenario-based disruption simulator (Red Sea closure, Cyclone warning).
  - Cryptographic SHA-256 decision audit drawer.
