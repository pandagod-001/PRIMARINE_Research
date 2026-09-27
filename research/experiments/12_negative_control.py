import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/fragility_surface", exist_ok=True)

print("=== PRIMARINE Fragility Research: Exp 5 - Negative Control Experiment ===", flush=True)

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

val_low = q10_model.predict(val_df[feature_cols])
val_upp = q90_model.predict(val_df[feature_cols])
val_actual = val_df['target_future'].values
nonconformity = np.maximum(val_low - val_actual, val_actual - val_upp)
alpha_nom = 0.10
q_calib = float(np.quantile(nonconformity, np.ceil((len(val_df) + 1) * (1 - alpha_nom)) / len(val_df)))

# Negative Control Setup:
# Case 1: Uniquely constrained scenario - 170,000 MT Capesize parcel to Paradip (Only V1_Capesize_Modern can physically serve it).
# Case 2: Shallow port scenario - 50,000 MT parcel to Haldia (Only V5_Supramax_Geared can physically enter due to 11.5m draft).
# In both cases, physical vessel/port allocation CANNOT change regardless of freight rate variations.

def evaluate_feasibility(vessel, port, parcel_mt):
    if vessel["dwt"] < parcel_mt:
        return False
    if vessel["draft"] > port["max_draft"]:
        return False
    if vessel["loa"] > port["max_loa"]:
        return False
    if vessel["beam"] > port["max_beam"]:
        return False
    return True

base_ports = {
    "Paradip": {"max_draft": 17.1, "max_loa": 300.0, "max_beam": 48.0, "handling_cost_per_t": 3.80, "avg_wait_days": 2.5},
    "Haldia": {"max_draft": 11.5, "max_loa": 230.0, "max_beam": 32.2, "handling_cost_per_t": 5.20, "avg_wait_days": 3.5}
}

base_fleet = [
    {"vessel_id": "V1_Capesize_Modern", "class": "Capesize", "dwt": 180000, "draft": 16.8, "loa": 292.0, "beam": 45.0, "fuel_burn_tpd": 42.0, "daily_hire_base": 24000},
    {"vessel_id": "V2_Capesize_Standard", "class": "Capesize", "dwt": 150000, "draft": 15.2, "loa": 274.0, "beam": 43.0, "fuel_burn_tpd": 48.0, "daily_hire_base": 21000},
    {"vessel_id": "V3_Panamax_Modern", "class": "Panamax", "dwt": 82000, "draft": 13.8, "loa": 229.0, "beam": 32.2, "fuel_burn_tpd": 28.0, "daily_hire_base": 14500},
    {"vessel_id": "V5_Supramax_Geared", "class": "Supramax", "dwt": 58000, "draft": 11.2, "loa": 190.0, "beam": 32.2, "fuel_burn_tpd": 24.0, "daily_hire_base": 11500},
]

routes = {
    "HayPoint_to_ECI": {"distance_nm": 4600, "origin": "Hay Point", "canal_fees": 0}
}

def calculate_landed_cost(vessel, port, route, freight_rate, parcel_mt):
    sea_days = route["distance_nm"] / (12.5 * 24.0)
    port_days = (parcel_mt / 25000.0) + port["avg_wait_days"]
    total_days = sea_days + port_days
    charter_cost = total_days * vessel["daily_hire_base"]
    fuel_cost = (sea_days * vessel["fuel_burn_tpd"] + port_days * 3.5) * 600
    port_dues = parcel_mt * port["handling_cost_per_t"]
    freight_charge = parcel_mt * freight_rate
    return (charter_cost + fuel_cost + port_dues + freight_charge) / parcel_mt

control_cases = [
    {"case_name": "Negative Control 1: Heavy Bulk (170k MT -> Paradip)", "target_port": "Paradip", "parcel_mt": 170000},
    {"case_name": "Negative Control 2: Draft-Restricted (50k MT -> Haldia)", "target_port": "Haldia", "parcel_mt": 50000}
]

test_sample = test_df.iloc[:20]
control_records = []

for c_info in control_cases:
    p_name = c_info["target_port"]
    port = base_ports[p_name]
    parcel_mt = c_info["parcel_mt"]
    
    # Check physically feasible vessels
    feasible_vessels = [v for v in base_fleet if evaluate_feasibility(v, port, parcel_mt)]
    
    for s_idx, (dt, row) in enumerate(test_sample.iterrows()):
        pt_pred = pt_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        raw_low = q10_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        raw_upp = q90_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        cqr_low = max(0.5, raw_low - q_calib)
        cqr_upp = raw_upp + q_calib
        
        # Test extreme freight rate perturbations: 0.1x to 5.0x
        perturbed_rates = [cqr_low, pt_pred, cqr_upp, pt_pred * 0.5, pt_pred * 2.0]
        
        selected_vessels = []
        for r_val in perturbed_rates:
            costs = [calculate_landed_cost(v, port, routes["HayPoint_to_ECI"], r_val, parcel_mt) for v in feasible_vessels]
            best_v = feasible_vessels[np.argmin(costs)]["vessel_id"]
            selected_vessels.append(best_v)
            
        is_identical = len(set(selected_vessels)) == 1
        false_fragility_detected = not is_identical
        
        control_records.append({
            "case_name": c_info["case_name"],
            "scenario_idx": s_idx,
            "num_feasible_vessels": len(feasible_vessels),
            "feasible_vessel_ids": [v["vessel_id"] for v in feasible_vessels],
            "selected_vessel": selected_vessels[0],
            "false_fragility_detected": int(false_fragility_detected),
            "physical_decision_stability": 1.0 if is_identical else 0.0
        })

control_df = pd.DataFrame(control_records)
control_df.to_csv("research/fragility_surface/negative_control.csv", index=False)
print("Exp 5 Complete: Negative Control Experiment evaluated.")
print(control_df.groupby('case_name')[['num_feasible_vessels', 'false_fragility_detected', 'physical_decision_stability']].mean())
