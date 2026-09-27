import os
import pandas as pd
import numpy as np

# Load raw consolidated dataset
df = pd.read_csv("data/raw/consolidated_raw_freight_data.csv", index_col="Date", parse_dates=True)

print(f"Initial raw data shape: {df.shape}")

# 1. Feature Engineering with economic and maritime rationale:
# Target: BDRY Close (tracks Baltic Capesize/Panamax freight futures)
y = df['target_bdry_close']

features = pd.DataFrame(index=df.index)
features['target'] = y

# A. Freight Autoregressive Lags (Short-term momentum & memory)
# Rationale: Ship charter fixtures have strong autocorrelation over 1-day, 2-day, 5-day (1 week), 10-day (2 weeks), and 21-day (1 trading month)
for lag in [1, 2, 3, 5, 10, 21]:
    features[f'freight_lag_{lag}'] = y.shift(lag)

# B. Rate Momentum & Percentage Returns
# Rationale: Acceleration/deceleration in freight inquiries directly signals tightening vessel supply
features['freight_return_1d'] = y.pct_change(1)
features['freight_return_5d'] = y.pct_change(5)
features['freight_return_21d'] = y.pct_change(21)

# C. Moving Averages & Trend Indicators (Ratio of current freight to historical baseline)
# Rationale: Identifies whether the market is in a structural supercycle, contango, or backwardation
features['freight_sma_5'] = y.rolling(5).mean()
features['freight_sma_21'] = y.rolling(21).mean()
features['freight_sma_63'] = y.rolling(63).mean()  # ~1 quarter
features['freight_ratio_sma5_sma21'] = features['freight_sma_5'] / (features['freight_sma_21'] + 1e-6)

# D. Rolling Historical Volatility
# Rationale: Volatility spikes precede freight market regime changes and determine confidence bands
features['freight_volatility_5d'] = y.pct_change().rolling(5).std()
features['freight_volatility_21d'] = y.pct_change().rolling(21).std()

# E. Bunker / Fuel Price Dynamics (Brent Crude as VLSFO proxy)
# Rationale: Bunker represents 40-60% of vessel voyage operating cost; oil swings shift vessel owner floor prices
features['bunker_price'] = df['bunker_brent_close']
features['bunker_return_5d'] = df['bunker_brent_close'].pct_change(5)
features['bunker_return_21d'] = df['bunker_brent_close'].pct_change(21)

# F. Upstream Mining & Commodity Export Momentum (BHP & Vale)
# Rationale: Australian & Brazilian iron ore / coking coal fixture demand leads freight rate increases
features['bhp_price'] = df['miner_bhp_close']
features['bhp_return_5d'] = df['miner_bhp_close'].pct_change(5)
features['vale_price'] = df['miner_vale_close']
features['vale_return_5d'] = df['miner_vale_close'].pct_change(5)

# G. Macroeconomic Purchasing Power & FX Dynamics (DXY & USD/INR)
# Rationale: USD strength affects international charter contracting; USD/INR impacts Indian steel mill import margins
features['dxy_price'] = df['macro_dxy_close']
features['dxy_return_5d'] = df['macro_dxy_close'].pct_change(5)
features['usdinr_price'] = df['macro_usdinr_close']
features['usdinr_return_5d'] = df['macro_usdinr_close'].pct_change(5)

# H. Calendar / Seasonality Features
# Rationale: Dry bulk rates exhibit strong seasonal patterns (post-monsoon restocking, pre-Chinese New Year lulls)
features['month'] = df.index.month
features['quarter'] = df.index.quarter
features['dayofweek'] = df.index.dayofweek
# Sine/Cosine cyclical encoding for month
features['sin_month'] = np.sin(2 * np.pi * features['month'] / 12.0)
features['cos_month'] = np.cos(2 * np.pi * features['month'] / 12.0)

# Drop initial rows with NaNs resulting from maximum lag/rolling window (63 days)
clean_features = features.dropna().copy()

print(f"Processed clean dataset shape: {clean_features.shape}")
print(f"Date range: {clean_features.index.min().strftime('%Y-%m-%d')} to {clean_features.index.max().strftime('%Y-%m-%d')}")
print(f"Features count: {clean_features.shape[1] - 1} (excluding target)")

clean_features.to_csv("data/processed/freight_features_dataset.csv")
print("Saved data/processed/freight_features_dataset.csv successfully.")
