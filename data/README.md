# PRIMARINE — Dataset Inventory & Provenance Guide

**Document Version:** 1.0.0 (Frozen Consolidation)  
**Status:** Canonical Reference  
**Scope:** Complete catalog of all datasets, raw data sources, curated fixtures, split methodologies, leakage controls, and redistribution terms.

---

## 1. Dataset Classification & Redistribution Status

| Dataset Identifier | Domain / Description | Physical Path | Source / Origin | Sample Size / Window | Redistribution Status | Leakage Controls Enforced |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-BDI-HIST** | Baltic Dry Index (BDI) Historical Freight Rates | `data/raw/bdi_historical_2018_2024.csv` | Public Historical Financial Feeds / Baltic Exchange Archive | 1,754 Trading Days (2018–2024) | **OPEN RESEARCH ARCHIVE** | Strict chronological temporal train/calibration/test split; zero look-ahead bias. |
| **DS-FIXTURE-PORTS** | Indian Ocean Port & Berth Physical Constraints | `data/fixtures/indian_ocean_ports.json` | Published Port Authority Tariffs (Paradip, Dhamra, Haldia, Vizag, Singapore, Newcastle, Hedland, Richards Bay) | 8 Major Ports (24 Berths) | **OPEN REPRODUCIBLE FIXTURE** | Static physical constraints; deterministic rule engine. |
| **DS-FIXTURE-FLEET** | Dry-Bulk Vessel Class Particulars | `data/fixtures/drybulk_vessel_classes.json` | Clarkson / IMO Standard Dry-Bulk Vessel Specifications | 5 Classes (Capesize, Kamsarmax, Panamax, Ultramax, Supramax) | **OPEN REPRODUCIBLE FIXTURE** | Standard IMO Naval Architecture dimensions and deadweights. |
| **DS-FRAGILITY-EXP** | Perturbation Surfaces & Scenario Envelopes | `research/fragility_surface/` | Generated via Synthetic Scenario Injections (`08_fragility_surface.py`) | 288 Controlled Scenarios $\times$ 5 Perturbation Levels | **OPEN RESEARCH ARTIFACT** | Evaluated on held-out test splits; deterministic random seed 42. |
| **DS-DEMO-FIXTURES** | Consolidated Prototype Vertical-Slice Fixture | `prototype/PRIMARINE-demo/data/fixtures.json` | Curated multi-domain fixtures for standalone local demonstrator | Consolidated JSON (Ports, Vessels, Cargo, Disruption, Rates) | **OPEN DEMO FIXTURE** | Embedded in local UI demonstrator; no live credentials required. |

---

## 2. Temporal Train / Calibration / Test Split Protocol

To ensure rigorous non-asymptotic conformal validity and prevent data leakage in time-series forecasting, PRIMARINE enforces a strict three-way sequential chronological split:

```
[ 2018-01-01 to 2021-12-31 ]  -->  TRAINING SET (Model Weight Optimization)
                                           ↓
[ 2022-01-01 to 2022-12-31 ]  -->  CALIBRATION SET (Split-CQR Non-Conformity Scoring)
                                           ↓
[ 2023-01-01 to 2024-12-31 ]  -->  HELD-OUT TEST SET (Out-of-Sample Empirical Evaluation)
```

- **Feature Lagging:** All technical indicators, moving averages, and volatility spreads are lagged by $t-1$ or greater.
- **Conformal Calibration:** The non-conformity threshold $q_{\text{calib}} = 0.8415$ is computed exclusively on the Calibration set and frozen prior to Test set evaluation.
- **Selective Abstention Threshold:** The gating parameter $\tau = 1.35 \times \text{median}(W_{\text{calib}})$ is calculated on calibration/validation intervals without exposure to test outcomes.

---

## 3. Provenance & Integrity Statement

All synthetic fixtures and historical series in this repository are formatted as open CSV and JSON files for instant reproducibility. No private, confidential, or proprietary third-party commercial datasets are redistributed in violation of licensing terms.
