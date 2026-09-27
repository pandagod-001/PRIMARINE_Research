import os
import sys
import json
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# Ensure directories exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)
os.makedirs("PRIMARINE_EVIDENCE/figures", exist_ok=True)

print("Fetching genuine historical time-series data from public markets...")

# Tickers to fetch:
# 1. BDRY: Breakwave Dry Bulk Shipping ETF (Target Dry Bulk Freight Signal)
# 2. BZ=F: Brent Crude Oil Futures (Bunker fuel cost proxy)
# 3. BHP: BHP Group (Major Australian Coking Coal & Iron Ore Exporter to India)
# 4. VALE: Vale S.A. (Major Global Seaborne Iron Ore/Bulk Shipper)
# 5. DX-Y.NYB: US Dollar Index (Global Trade Currency / Macro purchasing power)
# 6. INR=X: USD to INR Exchange Rate (Currency impact for Indian Steel Mills)

tickers = {
    "target_bdry": "BDRY",
    "bunker_brent": "BZ=F",
    "miner_bhp": "BHP",
    "miner_vale": "VALE",
    "macro_dxy": "DX-Y.NYB",
    "macro_usdinr": "INR=X"
}

start_date = "2018-04-01"  # BDRY launched in March 2018
end_date = "2026-03-01"

raw_dfs = {}
for name, ticker in tickers.items():
    print(f"Downloading {ticker} ({name})...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not data.empty:
            # yfinance returns multi-index or single index depending on version
            if isinstance(data.columns, pd.MultiIndex):
                close_col = data['Close'][ticker]
                vol_col = data['Volume'][ticker] if 'Volume' in data else None
            else:
                close_col = data['Close']
                vol_col = data['Volume'] if 'Volume' in data else None
            
            df_single = pd.DataFrame(index=data.index)
            df_single[f"{name}_close"] = close_col
            if vol_col is not None and name == "target_bdry":
                df_single[f"{name}_volume"] = vol_col
            
            # Save raw csv
            raw_path = f"data/raw/{name}_{ticker.replace('=', '_').replace('^', '').replace('-', '_')}.csv"
            df_single.to_csv(raw_path)
            print(f"  -> Saved {len(df_single)} raw rows to {raw_path}")
            raw_dfs[name] = df_single
        else:
            print(f"  -> Warning: No data returned for {ticker}")
    except Exception as e:
        print(f"  -> Error fetching {ticker}: {e}")

# Merge into unified continuous business daily dataset
merged_df = pd.DataFrame()
for name, df in raw_dfs.items():
    if merged_df.empty:
        merged_df = df
    else:
        merged_df = merged_df.join(df, how="outer")

# Filter strictly to trading days where target (BDRY) has market trading history
merged_df = merged_df.dropna(subset=["target_bdry_close"]).copy()

# Forward fill minor holiday mismatches across international exchanges, then backward fill if start has NaNs
merged_df = merged_df.ffill().bfill()

print(f"\nConsolidated clean raw dataset: {merged_df.shape[0]} daily observations from {merged_df.index.min().strftime('%Y-%m-%d')} to {merged_df.index.max().strftime('%Y-%m-%d')}")
merged_df.to_csv("data/raw/consolidated_raw_freight_data.csv")
print("Saved data/raw/consolidated_raw_freight_data.csv successfully.")
