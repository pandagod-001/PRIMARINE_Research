import os
import json
import numpy as np
import pandas as pd
from scipy import stats
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/results", exist_ok=True)
print("=== PRIMARINE Experiment 2: Uncertainty Propagation Through Constraints & Optimization ===", flush=True)

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

# Train Point and Quantile LightGBM
pt_model = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
pt_model.fit(train_df[feature_cols], train_df['target_future'])

q10_model = lgb.LGBMRegressor(objective='quantile', alpha=0.10, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q10_model.fit(train_df[feature_cols], train_df['target_future'])

q90_model = lgb.LGBMRegressor(objective='quantile', alpha=0.90, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q90_model.fit(train_df[feature_cols], train_df['target_future'])

val_low = q10_model.predict(val_df[feature_cols])
val_upp = q90_model.predict(val_df[feature_cols])
nonconformity = np.maximum(val_low - val_df['target_future'].values, val_df['target_future'].values - val_upp)
q_calib = float(np.quantile(nonconformity, np.ceil((len(val_df) + 1) * 0.90) / len(val_df)))

ports = {
    "Paradip": {"max_draft": 17.1, "max_loa": 300.0, "max_beam": 48.0, "handling_cost_per_t": 3.80, "avg_wait_days": 2.5},
    "Visakhapatnam": {"max_draft": 16.5, "max_loa": 290.0, "max_beam": 45.0, "handling_cost_per_t": 4.10, "avg_wait_days": 2.0},
    "Haldia": {"max_draft": 11.5, "max_loa": 230.0, "max_beam": 32.2, "handling_cost_per_t": 5.20, "avg_wait_days": 3.5}
}

vessel_fleet = [
    {"vessel_id": "V1_Capesize_Modern", "class": "Capesize", "dwt": 180000, "draft": 16.8, "loa": 292.0, "beam": 45.0, "fuel_burn_tpd": 42.0, "cii_rating": "A", "daily_hire_base": 24000},
    {"vessel_id": "V2_Capesize_Standard", "class": "Capesize", "dwt": 150000, "draft": 15.2, "loa": 274.0, "beam": 43.0, "fuel_burn_tpd": 48.0, "cii_rating": "C", "daily_hire_base": 21000},
    {"vessel_id": "V3_Panamax_Modern", "class": "Panamax", "dwt": 82000, "draft": 13.8, "loa": 229.0, "beam": 32.2, "fuel_burn_tpd": 28.0, "cii_rating": "B", "daily_hire_base": 14500},
    {"vessel_id": "V4_Panamax_Standard", "class": "Panamax", "dwt": 75000, "draft": 12.8, "loa": 225.0, "beam": 32.2, "fuel_burn_tpd": 31.0, "cii_rating": "D", "daily_hire_base": 13000},
    {"vessel_id": "V5_Supramax_Geared", "class": "Supramax", "dwt": 58000, "draft": 11.2, "loa": 190.0, "beam": 32.2, "fuel_burn_tpd": 24.0, "cii_rating": "B", "daily_hire_base": 11500},
]

def eval_plan(vessel, port, freight_rate, parcel_mt=120000):
    if vessel["dwt"] < parcel_mt or vessel["draft"] > port["max_draft"] or vessel["loa"] > port["max_loa"]:
        return None
    sailing_days = 4200.0 / (12.5 * 24.0)
    total_days = sailing_days + port["avg_wait_days"] + (parcel_mt / 25000.0)
    total_cost = (freight_rate * parcel_mt) + (sailing_days * vessel["fuel_burn_tpd"] * 550.0) + (total_days * vessel["daily_hire_base"]) + (parcel_mt * port["handling_cost_per_t"])
    return total_cost / parcel_mt

test_dates = test_df.index
prop_records = []

for i in range(0, len(test_dates), 2):
    date = test_dates[i]
    curr_feat = pd.DataFrame([test_df.loc[date, feature_cols]])
    actual_future = float(test_df.loc[date, 'target_future'])
    curr_spot = float(test_df.loc[date, 'target'])
    
    p_pt = float(pt_model.predict(curr_feat)[0])
    p10 = float(q10_model.predict(curr_feat)[0]) - q_calib
    p90 = float(q90_model.predict(curr_feat)[0]) + q_calib
    width = p90 - p10
    
    # Evaluate across 3 modes
    for p_mt in [50000, 75000, 120000]:
        cost_pt_candidates = []
        cost_p10_candidates = []
        cost_p90_candidates = []
        cost_act_candidates = []
        
        for v in vessel_fleet:
            for p_name, p_spec in ports.items():
                c_pt = eval_plan(v, p_spec, p_pt, p_mt)
                c_p10 = eval_plan(v, p_spec, p10, p_mt)
                c_p90 = eval_plan(v, p_spec, p90, p_mt)
                c_act = eval_plan(v, p_spec, actual_future, p_mt)
                
                if c_pt is not None:
                    cost_pt_candidates.append((c_pt, f"{v['vessel_id']}_{p_name}"))
                if c_p10 is not None:
                    cost_p10_candidates.append((c_p10, f"{v['vessel_id']}_{p_name}"))
                if c_p90 is not None:
                    cost_p90_candidates.append((c_p90, f"{v['vessel_id']}_{p_name}"))
                if c_act is not None:
                    cost_act_candidates.append((c_act, f"{v['vessel_id']}_{p_name}"))
                    
        cost_pt_candidates.sort(key=lambda x: x[0])
        cost_p10_candidates.sort(key=lambda x: x[0])
        cost_p90_candidates.sort(key=lambda x: x[0])
        cost_act_candidates.sort(key=lambda x: x[0])
        
        best_pt = cost_pt_candidates[0][1] if cost_pt_candidates else "NONE"
        best_p10 = cost_p10_candidates[0][1] if cost_p10_candidates else "NONE"
        best_p90 = cost_p90_candidates[0][1] if cost_p90_candidates else "NONE"
        best_act = cost_act_candidates[0][1] if cost_act_candidates else "NONE"
        
        # Objective Sensitivity: Spread between best cost under P90 vs P10 ($/MT)
        cost_spread = (cost_p90_candidates[0][0] - cost_p10_candidates[0][0]) if (cost_p90_candidates and cost_p10_candidates) else 0.0
        
        # Regret of point forecast decision evaluated under actual realized market
        actual_dict = dict([(x[1], x[0]) for x in cost_act_candidates])
        realized_cost_pt = actual_dict.get(best_pt, np.nan)
        realized_cost_optimal = cost_act_candidates[0][0] if cost_act_candidates else np.nan
        regret_pmt = realized_cost_pt - realized_cost_optimal if (not np.isnan(realized_cost_pt) and not np.isnan(realized_cost_optimal)) else 0.0
        
        prop_records.append({
            "Date": date.strftime('%Y-%m-%d'),
            "Parcel_MT": p_mt,
            "Spot": round(curr_spot, 4),
            "Forecast_Pt": round(p_pt, 4),
            "CQR_P10": round(p10, 4),
            "CQR_P90": round(p90, 4),
            "Uncertainty_Width": round(width, 4),
            "Optimal_Decision_Point": best_pt,
            "Optimal_Decision_P10": best_p10,
            "Optimal_Decision_P90": best_p90,
            "Optimal_Decision_Actual": best_act,
            "Decision_Flipped_Under_Uncertainty": int(best_p10 != best_p90),
            "Objective_Sensitivity_Spread_pmt": round(cost_spread, 4),
            "Downstream_Regret_pmt": round(regret_pmt, 4)
        })

prop_df = pd.DataFrame(prop_records)
prop_df.to_csv("research/results/02_uncertainty_propagation.csv", index=False)
print("Saved research/results/02_uncertainty_propagation.csv", flush=True)
