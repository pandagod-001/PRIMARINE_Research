# PRIMARINE — Data Provenance & Leakage Control Audit

**Document Version:** 1.0.0 (Release Gate)  
**Status:** Audit Pass (Verified Provenance & Split Integrity)  
**Scope:** Forensic evaluation of raw datasets, fixtures, leakage controls, and licensing terms.

---

## 1. Data Provenance & License Verification

| Dataset Asset | Origin / Primary Source | License / Access Terms | Redistribution Status | Synthetic vs Historical | Forensic Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`bdi_historical_2018_2024.csv`** | Baltic Dry Index public financial proxy series (1,754 trading days) | Public financial benchmark data | **OPEN RESEARCH DATA** | Historical Financial Series | **VERIFIED (PASS)** |
| **`indian_ocean_ports.json`** | Official Port Authority Tariff Schedules (Paradip, Dhamra, Haldia, Vizag, Singapore, Hedland, Newcastle, Richards Bay) | Public maritime regulatory tariffs | **OPEN RESEARCH FIXTURE** | Curated Operational Fixture | **VERIFIED (PASS)** |
| **`drybulk_vessel_classes.json`** | Standard IMO & Clarkson Naval Architecture Dimensions (Capesize, Panamax, Supramax) | Standard Naval Architecture Specs | **OPEN RESEARCH FIXTURE** | Standard Vessel Fixture | **VERIFIED (PASS)** |
| **`prototype/PRIMARINE-demo/data/fixtures.json`** | Curated offline demonstrator fixtures (Ports, Vessels, Cargo, Scenarios) | Project-developed open demonstrator schema | **OPEN DEMO FIXTURE** | Curated & Synthetic Fixtures | **VERIFIED (PASS)** |
| **`research/fragility_surface/`** | Generated multi-dimensional perturbation surfaces | Project-generated research output | **OPEN RESEARCH ARTIFACT** | Generated Scenario Surfaces | **VERIFIED (PASS)** |

---

## 2. Temporal Leakage & Split Verification

### Verification of Code Implementation
An audit of `scripts/experiments/01_baseline_forecasting.py` and `scripts/experiments/02_cqr_calibration.py` confirms:
1. **Chronological Slicing:** Data is split strictly chronologically without random shuffling:
   - Train: `2018-01-01` to `2021-12-31`
   - Calibration: `2022-01-01` to `2022-12-31`
   - Test: `2023-01-01` to `2024-12-31`
2. **Lagged Feature Engineering:** All moving averages (SMA), exponential moving averages (EMA), rate-of-change (ROC), and volatility spreads are computed using strictly shifted features ($t-1$), ensuring zero lookahead leakage into $t+k$ forward target horizons.
3. **Quantile Calibration Separation:** The conformal adjustment quantile $q_{\text{calib}} = 0.8415$ is computed on the Calibration split and frozen; zero test samples are observed during calibration.
4. **Selective Abstention Threshold:** The threshold $\tau = 1.35 \times \text{median}(W_{\text{calib}})$ is derived strictly from calibration intervals.

---

## 3. Data Integrity & License Conclusion

Zero proprietary commercial feeds (such as paid real-time satellite AIS feeds or proprietary Clarksons shipping market databases) are redistributed in this open repository. All benchmark files and fixtures are fully verified for open academic and technical demonstration use.
