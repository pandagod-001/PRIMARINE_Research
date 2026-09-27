import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/fragility_surface", exist_ok=True)

print("=== PRIMARINE Fragility Research: Exp 4 - Constraint Fragility & Sensitivity ===", flush=True)

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

base_ports = {
    "Paradip": {"max_draft": 17.1, "max_loa": 300.0, "max_beam": 48.0, "handling_cost_per_t": 3.80, "avg_wait_days": 2.5},
    "Visakhapatnam": {"max_draft": 16.5, "max_loa": 290.0, "max_beam": 45.0, "handling_cost_per_t": 4.10, "avg_wait_days": 2.0},
    "Haldia": {"max_draft": 11.5, "max_loa": 230.0, "max_beam": 32.2, "handling_cost_per_t": 5.20, "avg_wait_days": 3.5}
}

base_fleet = [
    {"vessel_id": "V1_Capesize_Modern", "class": "Capesize", "dwt": 180000, "draft": 16.8, "loa": 292.0, "beam": 45.0, "fuel_burn_tpd": 42.0, "daily_hire_base": 24000},
    {"vessel_id": "V2_Capesize_Standard", "class": "Capesize", "dwt": 150000, "draft": 15.2, "loa": 274.0, "beam": 43.0, "fuel_burn_tpd": 48.0, "daily_hire_base": 21000},
    {"vessel_id": "V3_Panamax_Modern", "class": "Panamax", "dwt": 82000, "draft": 13.8, "loa": 229.0, "beam": 32.2, "fuel_burn_tpd": 28.0, "daily_hire_base": 14500},
    {"vessel_id": "V4_Panamax_Standard", "class": "Panamax", "dwt": 75000, "draft": 12.8, "loa": 225.0, "beam": 32.2, "fuel_burn_tpd": 31.0, "daily_hire_base": 13000},
    {"vessel_id": "V5_Supramax_Geared", "class": "Supramax", "dwt": 58000, "draft": 11.2, "loa": 190.0, "beam": 32.2, "fuel_burn_tpd": 24.0, "daily_hire_base": 11500},
]

routes = {
    "HayPoint_to_ECI": {"distance_nm": 4600, "origin": "Hay Point", "canal_fees": 0},
    "Newcastle_to_ECI": {"distance_nm": 4900, "origin": "Newcastle", "canal_fees": 0},
    "Samarinda_to_ECI": {"distance_nm": 2400, "origin": "Samarinda", "canal_fees": 0}
}

def evaluate_feasibility(vessel, port, parcel_mt=120000, draft_slack=0.0):
    reasons = []
    is_feasible = True
    if vessel["dwt"] < parcel_mt:
        is_feasible = False
        reasons.append("Capacity shortfall")
    if vessel["draft"] > (port["max_draft"] + draft_slack):
        is_feasible = False
        reasons.append("Draft exceeded")
    if vessel["loa"] > port["max_loa"]:
        is_feasible = False
        reasons.append("LOA exceeded")
    if vessel["beam"] > port["max_beam"]:
        is_feasible = False
        reasons.append("Beam exceeded")
    return is_feasible, reasons

def calculate_landed_cost(vessel, port, route, freight_rate, parcel_mt=120000, bunker_price=600):
    sea_days = route["distance_nm"] / (12.5 * 24.0)
    port_days = (parcel_mt / 25000.0) + port["avg_wait_days"]
    total_days = sea_days + port_days
    
    charter_cost = total_days * vessel["daily_hire_base"]
    fuel_cost = (sea_days * vessel["fuel_burn_tpd"] + port_days * 3.5) * bunker_price
    port_dues = parcel_mt * port["handling_cost_per_t"]
    freight_charge = parcel_mt * freight_rate
    
    total_usd = charter_cost + fuel_cost + port_dues + freight_charge + route["canal_fees"]
    return total_usd / parcel_mt

# Define 3 Rigorous Constraint Regimes
constraint_regimes = {
    "Normal Constraints": {"parcel_mt": 120000, "draft_slack": 0.0},
    "Moderately Tight Constraints": {"parcel_mt": 120000, "draft_slack": -0.8},
    "Highly Tight Constraints": {"parcel_mt": 140000, "draft_slack": -1.2}
}

test_sample = test_df.iloc[:20]
records = []

for r_name, r_cfg in constraint_regimes.items():
    parcel_mt = r_cfg["parcel_mt"]
    draft_slack = r_cfg["draft_slack"]
    
    for s_idx, (dt, row) in enumerate(test_sample.iterrows()):
        curr_rate = row['target']
        pt_pred = pt_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        raw_low = q10_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        raw_upp = q90_model.predict(pd.DataFrame([row[feature_cols]]))[0]
        
        cqr_low = max(0.5, raw_low - q_calib)
        cqr_upp = raw_upp + q_calib
        
        # Check Central Solution
        central_candidates = []
        for v in base_fleet:
            for p_name, p in base_ports.items():
                is_f, _ = evaluate_feasibility(v, p, parcel_mt, draft_slack)
                if is_f:
                    for rt_name, rt in routes.items():
                        c = calculate_landed_cost(v, p, rt, pt_pred, parcel_mt)
                        central_candidates.append({"vessel": v["vessel_id"], "port": p_name, "route": rt_name, "cost": c})
                        
        num_feasible = len(central_candidates)
        if num_feasible == 0:
            continue
            
        central_opt = min(central_candidates, key=lambda x: x["cost"])
        
        # Evaluate under Low and High bounds
        opt_low_candidates = []
        opt_upp_candidates = []
        for v in base_fleet:
            for p_name, p in base_ports.items():
                is_f, _ = evaluate_feasibility(v, p, parcel_mt, draft_slack)
                if is_f:
                    for rt_name, rt in routes.items():
                        c_low = calculate_landed_cost(v, p, rt, cqr_low, parcel_mt)
                        c_upp = calculate_landed_cost(v, p, rt, cqr_upp, parcel_mt)
                        opt_low_candidates.append({"vessel": v["vessel_id"], "port": p_name, "route": rt_name, "cost": c_low})
                        opt_upp_candidates.append({"vessel": v["vessel_id"], "port": p_name, "route": rt_name, "cost": c_upp})
                        
        opt_low = min(opt_low_candidates, key=lambda x: x["cost"])
        opt_upp = min(opt_upp_candidates, key=lambda x: x["cost"])
        
        vessel_changed = int(opt_low["vessel"] != central_opt["vessel"] or opt_upp["vessel"] != central_opt["vessel"])
        port_changed = int(opt_low["port"] != central_opt["port"] or opt_upp["port"] != central_opt["port"])
        route_changed = int(opt_low["route"] != central_opt["route"] or opt_upp["route"] != central_opt["route"])
        phys_flip = int(vessel_changed or port_changed or route_changed)
        
        # Timing Flip
        t_pt = "ENTER_NOW" if pt_pred > curr_rate else "DEFER"
        t_low = "ENTER_NOW" if cqr_low > curr_rate else "DEFER"
        t_upp = "ENTER_NOW" if cqr_upp > curr_rate else "DEFER"
        timing_flip = int((t_low != t_pt) or (t_upp != t_pt))
        
        records.append({
            "regime": r_name,
            "scenario_idx": s_idx,
            "num_feasible": num_feasible,
            "central_vessel": central_opt["vessel"],
            "central_port": central_opt["port"],
            "central_route": central_opt["route"],
            "vessel_changed": vessel_changed,
            "port_changed": port_changed,
            "route_changed": route_changed,
            "physical_flip": phys_flip,
            "timing_flip": timing_flip,
            "central_cost": round(central_opt["cost"], 4)
        })

regime_df = pd.DataFrame(records)
regime_df.to_csv("research/fragility_surface/constraint_sensitivity_v2.csv", index=False)
print("Exp 4 Complete: Constraint Sensitivity evaluated.")
print(regime_df.groupby('regime')[['num_feasible', 'physical_flip', 'timing_flip']].mean())
