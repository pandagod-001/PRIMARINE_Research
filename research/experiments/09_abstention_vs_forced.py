import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/fragility_surface", exist_ok=True)

print("=== PRIMARINE Fragility Research: Exp 2 - Abstention vs Forced Decision ===", flush=True)

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

# Train Point and Quantile Models
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

# Compute validation CQR interval widths to determine calibration threshold without test leakage
val_cqr_w = (val_upp + q_calib) - (val_low - q_calib)
val_median_w = float(np.median(val_cqr_w))

# Test Set Evaluation across Candidate Threshold Multipliers
# Threshold = mult * val_median_w
threshold_multipliers = [0.8, 1.0, 1.2, 1.35, 1.5, 1.8, 2.0, 999.0] # 999.0 corresponds to forced decision (no abstention)

test_preds = pt_model.predict(test_df[feature_cols])
test_low = q10_model.predict(test_df[feature_cols]) - q_calib
test_upp = q90_model.predict(test_df[feature_cols]) + q_calib
test_widths = test_upp - test_low
test_actuals = test_df['target_future'].values
test_currents = test_df['target'].values

results_by_thresh = []

for mult in threshold_multipliers:
    tau = mult * val_median_w
    
    costs_forced_a = []
    costs_cqr_b = []
    costs_abstain_c = []
    
    abstention_count = 0
    false_breakouts = 0
    missed_opps = 0
    regrets = []
    
    for i in range(len(test_df)):
        curr = test_currents[i]
        pt = test_preds[i]
        act = test_actuals[i]
        w = test_widths[i]
        
        # System A: Always Decide on Point Forecast
        dec_a = "ENTER_NOW" if pt > curr else "DEFER"
        cost_a = curr if dec_a == "ENTER_NOW" else act
        costs_forced_a.append(cost_a)
        
        # System B: Uncertainty Aware (uses point forecast if width within bounds)
        dec_b = dec_a
        costs_cqr_b.append(cost_a)
        
        # System C: Uncertainty + Abstention
        # If width > tau -> ABSTAIN (default to dollar-cost averaging / neutral spot rate: 0.5*curr + 0.5*act)
        if w > tau:
            dec_c = "ABSTAIN"
            abstention_count += 1
            cost_c = 0.5 * curr + 0.5 * act
        else:
            dec_c = dec_a
            cost_c = curr if dec_c == "ENTER_NOW" else act
            
            # False breakout check: Decided ENTER_NOW because pt > curr, but market actually dropped (act < curr)
            if dec_c == "ENTER_NOW" and act < curr:
                false_breakouts += 1
            elif dec_c == "DEFER" and act > curr:
                missed_opps += 1
                
        costs_abstain_c.append(cost_c)
        
        # Hindsight optimal cost
        opt_cost = min(curr, act)
        regrets.append(cost_c - opt_cost)
        
    abstention_rate = abstention_count / len(test_df)
    mean_cost_a = float(np.mean(costs_forced_a))
    mean_cost_c = float(np.mean(costs_abstain_c))
    mean_regret = float(np.mean(regrets))
    
    # Coverage on test set
    covered = np.sum((test_actuals >= test_low) & (test_actuals <= test_upp))
    coverage_rate = float(covered / len(test_df))
    
    results_by_thresh.append({
        "threshold_multiplier": mult if mult < 999 else "No Abstention",
        "threshold_val": round(tau, 4) if mult < 999 else "Inf",
        "abstention_rate": round(abstention_rate, 4),
        "mean_cost_system_a": round(mean_cost_a, 4),
        "mean_cost_system_c": round(mean_cost_c, 4),
        "cost_advantage_c_vs_a_pct": round(((mean_cost_a - mean_cost_c) / mean_cost_a) * 100, 3),
        "mean_regret": round(mean_regret, 4),
        "false_breakouts": false_breakouts,
        "missed_opps": missed_opps,
        "coverage_rate": round(coverage_rate, 4),
        "mean_interval_width": round(float(np.mean(test_widths)), 4)
    })

abstain_df = pd.DataFrame(results_by_thresh)
abstain_df.to_csv("research/fragility_surface/abstention_experiment.csv", index=False)
print("Exp 2 Complete: Abstention vs Forced Decision evaluated.")
print(abstain_df[['threshold_multiplier', 'abstention_rate', 'mean_cost_system_c', 'cost_advantage_c_vs_a_pct', 'false_breakouts']])
