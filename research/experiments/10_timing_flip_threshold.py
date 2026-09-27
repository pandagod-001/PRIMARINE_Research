import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/fragility_surface", exist_ok=True)

print("=== PRIMARINE Fragility Research: Exp 3 - Timing Flip Threshold Analysis ===", flush=True)

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

# 2. Calibration Analysis: Estimate Empirical Timing Instability Threshold on Val Set
val_preds = pt_model.predict(val_df[feature_cols])
val_cqr_low = val_low - q_calib
val_cqr_upp = val_upp + q_calib
val_widths = val_cqr_upp - val_cqr_low
val_currents = val_df['target'].values

# Check timing flip on validation set across lower/upper CQR bounds
val_flips = []
for i in range(len(val_df)):
    curr = val_currents[i]
    pt = val_preds[i]
    low = val_cqr_low[i]
    upp = val_cqr_upp[i]
    
    t_pt = "ENTER_NOW" if pt > curr else "DEFER"
    t_low = "ENTER_NOW" if low > curr else "DEFER"
    t_upp = "ENTER_NOW" if upp > curr else "DEFER"
    
    is_flip = (t_low != t_pt) or (t_upp != t_pt)
    val_flips.append(int(is_flip))

val_median_w = float(np.median(val_widths))
val_norm_widths = val_widths / val_median_w

# Find threshold where flip probability exceeds 50% on validation set
bins = [0.0, 0.8, 1.0, 1.2, 1.35, 1.5, 2.0, 10.0]
val_bin_flips = []
for b_low, b_high in zip(bins[:-1], bins[1:]):
    mask = (val_norm_widths >= b_low) & (val_norm_widths < b_high)
    if np.sum(mask) > 0:
        val_bin_flips.append({
            "bin": f"{b_low}-{b_high}",
            "count": int(np.sum(mask)),
            "flip_rate": float(np.mean(np.array(val_flips)[mask]))
        })

# Estimate Threshold tau_calib from Val Set: chosen as 1.35 * val_median_w (where flip rate surges)
tau_calib = 1.35 * val_median_w

# 3. Held-Out Test Evaluation (No Leakage)
test_preds = pt_model.predict(test_df[feature_cols])
test_low = q10_model.predict(test_df[feature_cols]) - q_calib
test_upp = q90_model.predict(test_df[feature_cols]) + q_calib
test_widths = test_upp - test_low
test_currents = test_df['target'].values
test_actuals = test_df['target_future'].values

test_records = []
for i in range(len(test_df)):
    curr = test_currents[i]
    pt = test_preds[i]
    low = test_low[i]
    upp = test_upp[i]
    act = test_actuals[i]
    w = test_widths[i]
    norm_w = w / val_median_w
    
    t_pt = "ENTER_NOW" if pt > curr else "DEFER"
    t_low = "ENTER_NOW" if low > curr else "DEFER"
    t_upp = "ENTER_NOW" if upp > curr else "DEFER"
    
    is_flip = int((t_low != t_pt) or (t_upp != t_pt))
    hindsight_opt = "ENTER_NOW" if act > curr else "DEFER"
    decision_error = int(t_pt != hindsight_opt)
    
    opt_cost = min(curr, act)
    dec_cost = curr if t_pt == "ENTER_NOW" else act
    regret = dec_cost - opt_cost
    
    test_records.append({
        "scenario_idx": i,
        "date": str(test_df.index[i])[:10],
        "current_rate": round(curr, 4),
        "forecast_rate": round(pt, 4),
        "actual_future": round(act, 4),
        "cqr_width": round(w, 4),
        "norm_cqr_width": round(norm_w, 4),
        "timing_decision": t_pt,
        "timing_flip": is_flip,
        "decision_error": decision_error,
        "regret": round(regret, 4),
        "above_tau": int(w > tau_calib)
    })

test_rec_df = pd.DataFrame(test_records)
test_rec_df.to_csv("research/fragility_surface/threshold_analysis.csv", index=False)

# Metrics below and above threshold on Test Set
below_df = test_rec_df[test_rec_df['above_tau'] == 0]
above_df = test_rec_df[test_rec_df['above_tau'] == 1]

flip_rate_below = float(below_df['timing_flip'].mean()) if len(below_df) > 0 else 0.0
flip_rate_above = float(above_df['timing_flip'].mean()) if len(above_df) > 0 else 0.0

err_rate_below = float(below_df['decision_error'].mean()) if len(below_df) > 0 else 0.0
err_rate_above = float(above_df['decision_error'].mean()) if len(above_df) > 0 else 0.0

regret_below = float(below_df['regret'].mean()) if len(below_df) > 0 else 0.0
regret_above = float(above_df['regret'].mean()) if len(above_df) > 0 else 0.0

print(f"Calibrated Threshold (tau): {tau_calib:.4f} (1.35 * Val Median Width {val_median_w:.4f})")
print(f"Test Set - Below Threshold (N={len(below_df)}): Flip Rate={flip_rate_below*100:.2f}%, Error Rate={err_rate_below*100:.2f}%, Regret={regret_below:.4f}")
print(f"Test Set - Above Threshold (N={len(above_df)}): Flip Rate={flip_rate_above*100:.2f}%, Error Rate={err_rate_above*100:.2f}%, Regret={regret_above:.4f}")
