import os
import json
import numpy as np
import pandas as pd
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/fragility_surface", exist_ok=True)
os.makedirs("research/results", exist_ok=True)

print("=== PRIMARINE Fragility Research: Exp 1 - Decision Fragility Surface ===", flush=True)

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

# Physical Definitions
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
    "HayPoint_to_ECI": {"distance_nm": 4600, "speed_knots": 12.5, "origin": "Hay Point", "canal_fees": 0},
    "Newcastle_to_ECI": {"distance_nm": 4900, "speed_knots": 12.5, "origin": "Newcastle", "canal_fees": 0},
    "Samarinda_to_ECI": {"distance_nm": 2400, "speed_knots": 12.0, "origin": "Samarinda", "canal_fees": 0}
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
    sea_days = route["distance_nm"] / (vessel["speed_knots"] * 24.0) if "speed_knots" in vessel else route["distance_nm"] / (12.5 * 24.0)
    port_days = (parcel_mt / 25000.0) + port["avg_wait_days"]
    total_days = sea_days + port_days
    
    charter_cost = total_days * vessel["daily_hire_base"]
    fuel_cost = (sea_days * vessel["fuel_burn_tpd"] + port_days * 3.5) * bunker_price
    port_dues = parcel_mt * port["handling_cost_per_t"]
    freight_charge = parcel_mt * freight_rate
    
    total_usd = charter_cost + fuel_cost + port_dues + freight_charge + route["canal_fees"]
    return total_usd / parcel_mt

# Dimension A: Uncertainty Scale Factors
uncertainty_scales = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

# Dimension B: Constraint Tightness (Draft / Capacity perturbations)
# 1. Normal: 120k MT parcel, standard draft
# 2. Moderate: 120k MT parcel, -0.8m draft siltation
# 3. Tight: 140k MT parcel, -1.2m draft siltation
tightness_levels = {
    "Normal": {"parcel_mt": 120000, "draft_slack": 0.0},
    "Moderate": {"parcel_mt": 120000, "draft_slack": -0.8},
    "Tight": {"parcel_mt": 140000, "draft_slack": -1.2}
}

# Run 2D Grid Experiment across Test Scenarios
surface_records = []
test_sample = test_df.iloc[:20]

for s_idx, (dt, row) in enumerate(test_sample.iterrows()):
    curr_rate = row['target']
    pt_pred = pt_model.predict(pd.DataFrame([row[feature_cols]]))[0]
    raw_low = q10_model.predict(pd.DataFrame([row[feature_cols]]))[0]
    raw_upp = q90_model.predict(pd.DataFrame([row[feature_cols]]))[0]
    
    base_cqr_low = raw_low - q_calib
    base_cqr_upp = raw_upp + q_calib
    base_half_w = (base_cqr_upp - base_cqr_low) / 2.0
    
    for t_name, t_cfg in tightness_levels.items():
        parcel_mt = t_cfg["parcel_mt"]
        draft_slack = t_cfg["draft_slack"]
        
        # Central Decision (Baseline)
        central_feasible = []
        for v in base_fleet:
            for p_name, p in base_ports.items():
                is_f, _ = evaluate_feasibility(v, p, parcel_mt, draft_slack)
                if is_f:
                    for r_name, r in routes.items():
                        cost = calculate_landed_cost(v, p, r, pt_pred, parcel_mt)
                        central_feasible.append({
                            "vessel": v["vessel_id"], "port": p_name, "route": r_name,
                            "cost": cost, "rate": pt_pred
                        })
        
        if not central_feasible:
            continue
            
        central_opt = min(central_feasible, key=lambda x: x["cost"])
        
        for scale in uncertainty_scales:
            w_eff = base_half_w * scale
            low_rate = max(0.5, pt_pred - w_eff)
            upp_rate = pt_pred + w_eff
            
            # Scenarios: LOWER, CENTRAL, UPPER
            scen_decisions = []
            for rate_val, s_label in [(low_rate, "LOWER"), (pt_pred, "CENTRAL"), (upp_rate, "UPPER")]:
                f_list = []
                for v in base_fleet:
                    for p_name, p in base_ports.items():
                        is_f, _ = evaluate_feasibility(v, p, parcel_mt, draft_slack)
                        if is_f:
                            for r_name, r in routes.items():
                                cost = calculate_landed_cost(v, p, r, rate_val, parcel_mt)
                                f_list.append({
                                    "vessel": v["vessel_id"], "port": p_name, "route": r_name,
                                    "cost": cost, "scenario": s_label
                                })
                if f_list:
                    opt = min(f_list, key=lambda x: x["cost"])
                    scen_decisions.append(opt)
            
            # Check Physical Decision Flips across scenarios
            phys_flips = 0
            for d in scen_decisions:
                if d["vessel"] != central_opt["vessel"] or d["port"] != central_opt["port"] or d["route"] != central_opt["route"]:
                    phys_flips += 1
            
            phys_flip_rate = phys_flips / len(scen_decisions) if scen_decisions else 0.0
            
            # Timing Decision: If forecast delta is positive (rising), enter now; else defer
            # Under uncertainty: if width > 1.35 * median width (normalized), timing may abstain or flip
            timing_central = "ENTER_NOW" if pt_pred > curr_rate else "DEFER"
            timing_low = "ENTER_NOW" if low_rate > curr_rate else "DEFER"
            timing_upp = "ENTER_NOW" if upp_rate > curr_rate else "DEFER"
            
            timing_flips = 0
            for t_dec in [timing_low, timing_upp]:
                if t_dec != timing_central:
                    timing_flips += 1
            timing_flip_rate = timing_flips / 2.0
            
            surface_records.append({
                "scenario_idx": s_idx,
                "date": str(dt)[:10],
                "tightness": t_name,
                "uncertainty_scale": scale,
                "effective_width": round(w_eff * 2.0, 4),
                "num_feasible": len(central_feasible),
                "central_vessel": central_opt["vessel"],
                "central_port": central_opt["port"],
                "central_route": central_opt["route"],
                "central_cost": round(central_opt["cost"], 4),
                "physical_flip_rate": round(phys_flip_rate, 4),
                "timing_flip_rate": round(timing_flip_rate, 4),
                "fri": 1.0,
                "dfi": round(phys_flip_rate, 4)
            })

surface_df = pd.DataFrame(surface_records)
surface_df.to_csv("research/fragility_surface/fragility_surface.csv", index=False)
print(f"Exp 1 Complete: Generated {len(surface_df)} records across 2D grid.")
print(surface_df.groupby(['tightness', 'uncertainty_scale'])[['physical_flip_rate', 'timing_flip_rate', 'num_feasible']].mean())
