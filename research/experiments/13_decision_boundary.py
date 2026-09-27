import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/decision_boundary", exist_ok=True)
os.makedirs("research/experiments", exist_ok=True)

print("=== PRIMARINE Decision Boundary: Exp 13 - Boundary Analysis ===", flush=True)

# 1. Load Data
df = pd.read_csv("data/processed/freight_features_dataset.csv", index_col="Date", parse_dates=True)
H = 7
df['target_future'] = df['target'].shift(-H)
clean_df = df.dropna().copy()
feature_cols = [c for c in clean_df.columns if c not in ['target', 'target_future']]

n_total = len(clean_df)
train_size = int(n_total * 0.70)
val_size = int(n_total * 0.15)
test_size = n_total - train_size - val_size

train_df = clean_df.iloc[:train_size]
val_df = clean_df.iloc[train_size:train_size + val_size]
test_df = clean_df.iloc[train_size + val_size:]

print(f"Data Split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}", flush=True)

# 2. Fit Point and Quantile LightGBM models
pt_model = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
pt_model.fit(train_df[feature_cols], train_df['target_future'])

q10_model = lgb.LGBMRegressor(objective='quantile', alpha=0.10, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q10_model.fit(train_df[feature_cols], train_df['target_future'])

q90_model = lgb.LGBMRegressor(objective='quantile', alpha=0.90, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q90_model.fit(train_df[feature_cols], train_df['target_future'])

# Calibration on validation set
val_low = q10_model.predict(val_df[feature_cols])
val_upp = q90_model.predict(val_df[feature_cols])
val_actual = val_df['target_future'].values
nonconformity = np.maximum(val_low - val_actual, val_actual - val_upp)
alpha_nom = 0.10
q_calib = float(np.quantile(nonconformity, np.ceil((len(val_df) + 1) * (1 - alpha_nom)) / len(val_df)))

# 3. Validation Analysis for Calibration of Thresholds (No test leakage)
val_pt = pt_model.predict(val_df[feature_cols])
val_L = np.maximum(0.5, val_low - q_calib)
val_U = val_upp + q_calib
val_W = val_U - val_L
val_B = val_df['target'].values
val_M = val_pt - val_B
val_NM = np.abs(val_M) / val_W
val_median_w = float(np.median(val_W))
tau_width = 1.35 * val_median_w

# Margin quantiles on validation set
tau_nm_val = float(np.quantile(val_NM, 0.35)) # 35th percentile of normalized margin as boundary threshold

# 4. Held-out Test Set Evaluation (N = 288)
test_pt = pt_model.predict(test_df[feature_cols])
test_L = np.maximum(0.5, q10_model.predict(test_df[feature_cols]) - q_calib)
test_U = q90_model.predict(test_df[feature_cols]) + q_calib
test_W = test_U - test_L
test_B = test_df['target'].values
test_act = test_df['target_future'].values

records = []
for i in range(len(test_df)):
    B = test_B[i]
    C = test_pt[i]
    L = test_L[i]
    U = test_U[i]
    W = test_W[i]
    act = test_act[i]
    
    M = C - B
    NM = np.abs(M) / W
    
    # Boundary crossing
    boundary_crossing = int(L <= B <= U)
    
    # Decision States
    if L > B:
        state = "ROBUST_ENTER"
    elif U < B:
        state = "ROBUST_DEFER"
    else:
        state = "BOUNDARY_CROSSING"
        
    timing_dec = "ENTER_NOW" if C > B else "DEFER"
    opt_dec = "ENTER_NOW" if act > B else "DEFER"
    timing_error = int(timing_dec != opt_dec)
    
    # False breakout: Decided ENTER_NOW because C > B, but market dropped (act < B)
    false_breakout = int(timing_dec == "ENTER_NOW" and act < B)
    
    # Regret
    opt_cost = min(B, act)
    dec_cost = B if timing_dec == "ENTER_NOW" else act
    regret = dec_cost - opt_cost
    
    # Realized adverse movement
    adverse_movement = max(0.0, dec_cost - opt_cost)
    
    records.append({
        "scenario_idx": i,
        "date": str(test_df.index[i])[:10],
        "current_rate_B": round(B, 4),
        "forecast_C": round(C, 4),
        "cqr_lower_L": round(L, 4),
        "cqr_upper_U": round(U, 4),
        "interval_width_W": round(W, 4),
        "decision_margin_M": round(M, 4),
        "norm_margin_NM": round(NM, 4),
        "boundary_crossing": boundary_crossing,
        "decision_state": state,
        "timing_decision": timing_dec,
        "actual_future": round(act, 4),
        "optimal_decision": opt_dec,
        "timing_error": timing_error,
        "false_breakout": false_breakout,
        "regret": round(regret, 4),
        "adverse_movement": round(adverse_movement, 4),
        "high_width_flag": int(W > tau_width),
        "low_margin_flag": int(NM < tau_nm_val)
    })

db_df = pd.DataFrame(records)
db_df.to_csv("research/decision_boundary/decision_boundary_analysis.csv", index=False)
print(f"Exp 13 Complete: Saved {len(db_df)} records to decision_boundary_analysis.csv")
print(db_df.groupby('decision_state')[['timing_error', 'false_breakout', 'regret', 'interval_width_W']].mean())
