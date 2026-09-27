# PRIMARINE Data Quality & Empirical Validation Report

**Date:** 2026-09-24  
**Project:** PRIMARINE (SIH 2026 PS-26006)  
**Target Variable:** Breakwave Dry Bulk Shipping ETF (`BDRY` - Public Freight Proxy)  
**Dataset Path:** `data/processed/freight_features_dataset.csv`

---

## 1. Summary of Dataset Integrity

| Metric | Raw Ingested Data | Processed Feature Dataset |
|---|---|---|
| **Total Observations (Trading Days)** | 1989 | 1927 |
| **Date Range** | 2018-04-02 to 2026-02-27 | 2018-06-28 to 2026-02-27 |
| **Sampling Frequency** | Daily (Business/Trading Days) | Daily (Business/Trading Days) |
| **Missing Values (Target)** | 0 (after trading calendar alignment) | 0 |
| **Missing Values (Features)** | 0 | 0 |
| **Duplicates Detected** | 0 | 0 |
| **Total Feature Columns** | 7 raw market feeds | 31 engineered explanatory features + 1 target |

---

## 2. Target Variable Statistical Distribution (`BDRY`)

The primary target variable represents the unit level of the dry bulk freight futures index:

- **Mean Value:** 13.10
- **Standard Deviation:** 7.29
- **Median:** 10.44
- **Minimum Value:** 3.91 (Observed during COVID-19 pandemic shipping trough)
- **Maximum Value:** 41.51 (Observed during late 2021 post-pandemic supply chain super-spike)
- **Interquartile Range (25% - 75%):** 7.61 - 17.99
- **Skewness:** 1.02 (Typical heavy right tail reflecting severe freight market tightness during congestion regimes)
- **Kurtosis:** 0.26

---

## 3. Explanatory Feature Rationale & Data Health Check

All features in `freight_features_dataset.csv` were constructed with zero forward-looking leakage.

| Feature Category | Features Included | Physical / Economic Rationale | Verification Check |
|---|---|---|---|
| **Autoregressive Lags** | `freight_lag_1`, `2`, `3`, `5`, `10`, `21` | Captures strong persistence and multi-day fixture inertia in chartering fixtures. | Verified (No lookahead) |
| **Rate Momentum** | `freight_return_1d`, `5d`, `21d` | Quantifies velocity and acceleration in vessel supply tightening. | Verified |
| **Moving Averages & Ratio** | `freight_sma_5`, `21`, `63`, `freight_ratio_sma5_sma21` | Captures market regime (contango/backwardation, macro trend vs short noise). | Verified |
| **Rolling Volatility** | `freight_volatility_5d`, `21d` | Directly measures market uncertainty and sets predictive confidence bands. | Verified |
| **Bunker / Marine Fuel** | `bunker_price`, `bunker_return_5d`, `21d` | Fuel constitutes 40-60% of voyage operational costs; shifts shipowners' floor rates. | Verified (Brent crude proxy) |
| **Miner Supply Dynamics** | `bhp_price`, `vale_price`, returns | Captures upstream export cargo demand from Australia and Brazil. | Verified (Major miners) |
| **Macro / FX Dynamics** | `dxy_price`, `usdinr_price`, returns | Captures dollar liquidity and landed procurement cost impact for Indian mills. | Verified |
| **Seasonal / Calendar** | `sin_month`, `cos_month`, `quarter`, `dayofweek` | Encodes seasonal weather patterns (monsoons, holiday fixture cycles). | Verified |

---

## 4. Empirical Validity & Time-Series Rigor Guarantee

1. **No Synthetic / Fabricated Data:** Every single observation is derived directly from live exchange-traded market feeds.
2. **Calendar Alignment:** Cross-market holidays (e.g. US vs LSE vs Indian markets) are reconciled cleanly via forward-filling previous valid market close, maintaining strict temporal causality.
3. **Target Integrity:** The target variable exhibits genuine high-volatility dry bulk shipping cycles, making it the ideal benchmark for the SIH PS-26006 proof of concept.
