import os
import json
import numpy as np
import pandas as pd
from scipy import stats
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, precision_recall_fscore_support
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/results", exist_ok=True)
os.makedirs("research/experiments", exist_ok=True)

print("=== PRIMARINE Experiment 1: Decision Fragility & Uncertainty Propagation ===", flush=True)

# 1. Load Data
df = pd.read_csv("data/processed/freight_features_dataset.csv", index_col="Date", parse_dates=True)
H = 7

# Construct Target
df['target_future'] = df['target'].shift(-H)
clean_df = df.dropna().copy()
feature_cols = [c for c in clean_df.columns if c not in ['target', 'target_future']]

# Split: Train (70%), Val (15%), Test (15% Untouched)
n_total = len(clean_df)
train_size = int(n_total * 0.70)
val_size = int(n_total * 0.15)
test_size = n_total - train_size - val_size

train_df = clean_df.iloc[:train_size]
val_df = clean_df.iloc[train_size:train_size + val_size]
test_df = clean_df.iloc[train_size + val_size:]

print(f"Dataset Split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}", flush=True)

# 2. Train Point and Quantile LightGBM Models
pt_model = lgb.LGBMRegressor(n_estimators=60, learning_rate=0.05, num_leaves=12, random_state=42, verbose=-1, n_jobs=1)
pt_model.fit(train_df[feature_cols], train_df['target_future'])

q10_model = lgb.LGBMRegressor(objective='quantile', alpha=0.10, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q10_model.fit(train_df[feature_cols], train_df['target_future'])

q25_model = lgb.LGBMRegressor(objective='quantile', alpha=0.25, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q25_model.fit(train_df[feature_cols], train_df['target_future'])

q50_model = lgb.LGBMRegressor(objective='quantile', alpha=0.50, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q50_model.fit(train_df[feature_cols], train_df['target_future'])

q75_model = lgb.LGBMRegressor(objective='quantile', alpha=0.75, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q75_model.fit(train_df[feature_cols], train_df['target_future'])

q90_model = lgb.LGBMRegressor(objective='quantile', alpha=0.90, n_estimators=80, learning_rate=0.04, num_leaves=15, random_state=42, verbose=-1, n_jobs=1)
q90_model.fit(train_df[feature_cols], train_df['target_future'])

# Split-CQR calibration on validation set
val_low = q10_model.predict(val_df[feature_cols])
val_upp = q90_model.predict(val_df[feature_cols])
val_actual = val_df['target_future'].values
nonconformity = np.maximum(val_low - val_actual, val_actual - val_upp)
alpha_nom = 0.10
q_calib = float(np.quantile(nonconformity, np.ceil((len(val_df) + 1) * (1 - alpha_nom)) / len(val_df)))

# 3. Canonical Fleet Candidates and Destination Ports
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

# Physical Feasibility Function
def evaluate_feasibility(vessel, port, parcel_mt=120000):
    reasons = []
    is_feasible = True
    
    # 1. Capacity check
    if vessel["dwt"] < parcel_mt:
        is_feasible = False
        reasons.append(f"Capacity shortfall: DWT {vessel['dwt']} < Parcel {parcel_mt}")
        
    # 2. Draft check
    if vessel["draft"] > port["max_draft"]:
        is_feasible = False
        reasons.append(f"Draft exceeded: Vessel {vessel['draft']}m > Port {port['max_draft']}m")
        
    # 3. LOA check
    if vessel["loa"] > port["max_loa"]:
        is_feasible = False
        reasons.append(f"LOA exceeded: Vessel {vessel['loa']}m > Port {port['max_loa']}m")
        
    # 4. Beam check
    if vessel["beam"] > port["max_beam"]:
        is_feasible = False
        reasons.append(f"Beam exceeded: Vessel {vessel['beam']}m > Port {port['max_beam']}m")
        
    return is_feasible, reasons

# Multi-Objective Cost & Ranking Function
def evaluate_charter_plan(vessel, port, freight_rate, bunker_price=550.0, distance_nm=4200.0, speed_knots=12.5, parcel_mt=120000, mode="balanced"):
    is_feas, reasons = evaluate_feasibility(vessel, port, parcel_mt)
    if not is_feas:
        return None
        
    sailing_days = distance_nm / (speed_knots * 24.0)
    total_days = sailing_days + port["avg_wait_days"] + (parcel_mt / 25000.0) # 25k T/day discharge
    
    # Financial Cost Model ($)
    freight_cost = freight_rate * parcel_mt
    bunker_cost = sailing_days * vessel["fuel_burn_tpd"] * bunker_price
    hire_cost = total_days * vessel["daily_hire_base"]
    port_dues = parcel_mt * port["handling_cost_per_t"]
    
    total_financial_cost = freight_cost + bunker_cost + hire_cost + port_dues
    unit_cost_pmt = total_financial_cost / parcel_mt
    
    # Carbon / CII Penalty ($)
    co2_mt = (sailing_days * vessel["fuel_burn_tpd"] * 3.114) # 3.114 MT CO2 per MT bunker
    carbon_tax_rate = 50.0 # $50 / MT CO2
    cii_multiplier = {"A": 0.85, "B": 1.0, "C": 1.15, "D": 1.30}[vessel["cii_rating"]]
    carbon_penalty = co2_mt * carbon_tax_rate * cii_multiplier
    
    green_landed_cost_pmt = unit_cost_pmt + (carbon_penalty / parcel_mt)
    
    # Objective Value by Mode
    if mode == "cost_saver":
        score = unit_cost_pmt
    elif mode == "green":
        score = green_landed_cost_pmt
    else: # balanced
        # Combines landed cost, schedule risk (wait days), and carbon
        score = unit_cost_pmt * 0.70 + (green_landed_cost_pmt - unit_cost_pmt) * 0.20 + (port["avg_wait_days"] * 1.5) * 0.10
        
    return {
        "vessel_id": vessel["vessel_id"],
        "port": port,
        "score": score,
        "unit_cost_pmt": unit_cost_pmt,
        "green_cost_pmt": green_landed_cost_pmt,
        "total_days": total_days,
        "co2_mt": co2_mt
    }

# 4. Run Decision Fragility Across Untouched Test Set
print("Executing Decision Fragility & Uncertainty Propagation across Test Windows...", flush=True)

fragility_results = []
test_dates = test_df.index
eval_step = 2

# We test 3 procurement requirement sizes: Small (50k MT), Medium (75k MT), Large (120k MT)
parcels = [50000, 75000, 120000]

for p_mt in parcels:
    for i in range(0, len(test_dates), eval_step):
        date = test_dates[i]
        curr_feat = pd.DataFrame([test_df.loc[date, feature_cols]])
        curr_spot = float(test_df.loc[date, 'target'])
        actual_future = float(test_df.loc[date, 'target_future'])
        
        # Predictions across quantiles
        p_pt = float(pt_model.predict(curr_feat)[0])
        p10 = float(q10_model.predict(curr_feat)[0]) - q_calib
        p25 = float(q25_model.predict(curr_feat)[0])
        p50 = float(q50_model.predict(curr_feat)[0])
        p75 = float(q75_model.predict(curr_feat)[0])
        p90 = float(q90_model.predict(curr_feat)[0]) + q_calib
        
        uncertainty_width = p90 - p10
        
        scenarios = {
            "Point_Forecast": p_pt,
            "CQR_P10_Low": p10,
            "CQR_P25": p25,
            "CQR_P50_Median": p50,
            "CQR_P75": p75,
            "CQR_P90_High": p90
        }
        
        # Optimize across scenarios
        scenario_decisions = {}
        scenario_feasible_counts = {}
        
        for sc_name, sc_freight in scenarios.items():
            valid_plans = []
            for v in vessel_fleet:
                for port_name, p_spec in ports.items():
                    plan = evaluate_charter_plan(v, p_spec, freight_rate=sc_freight, parcel_mt=p_mt, mode="balanced")
                    if plan is not None:
                        plan["port_name"] = port_name
                        valid_plans.append(plan)
                        
            scenario_feasible_counts[sc_name] = len(valid_plans)
            
            if len(valid_plans) > 0:
                # Rank by score (lower is better)
                valid_plans.sort(key=lambda x: x["score"])
                best_plan = valid_plans[0]
                scenario_decisions[sc_name] = f"{best_plan['vessel_id']}_at_{best_plan['port_name']}"
            else:
                scenario_decisions[sc_name] = "NO_FEASIBLE_PLAN"
                
        # Fragility Metrics for this date
        central_decision = scenario_decisions["CQR_P50_Median"]
        point_decision = scenario_decisions["Point_Forecast"]
        
        unique_decisions = list(set([scenario_decisions[k] for k in ["CQR_P10_Low", "CQR_P25", "CQR_P50_Median", "CQR_P75", "CQR_P90_High"]]))
        dfi = len(unique_decisions) / 5.0 # Decision Fragility Index over 5 quantiles
        
        # Feasibility Robustness Index: Fraction of scenarios where the central plan remains feasible
        central_vessel_id = central_decision.split("_at_")[0] if "_at_" in central_decision else None
        central_port_name = central_decision.split("_at_")[1] if "_at_" in central_decision else None
        
        fri_count = 0
        for sc_name, sc_freight in scenarios.items():
            if sc_name == "Point_Forecast": continue
            if central_vessel_id and central_port_name:
                v_obj = [v for v in vessel_fleet if v["vessel_id"] == central_vessel_id][0]
                p_obj = ports[central_port_name]
                is_f, _ = evaluate_feasibility(v_obj, p_obj, parcel_mt=p_mt)
                if is_f: fri_count += 1
                
        fri = fri_count / 5.0
        
        # Decision flip relative to central
        flips = sum([1 for k in ["CQR_P10_Low", "CQR_P25", "CQR_P75", "CQR_P90_High"] if scenario_decisions[k] != central_decision])
        flip_rate = flips / 4.0
        
        fragility_results.append({
            "Date": date.strftime('%Y-%m-%d'),
            "Parcel_MT": p_mt,
            "Current_Spot": round(curr_spot, 4),
            "Point_Forecast": round(p_pt, 4),
            "CQR_P10": round(p10, 4),
            "CQR_P50": round(p50, 4),
            "CQR_P90": round(p90, 4),
            "Uncertainty_Width": round(uncertainty_width, 4),
            "Point_Decision": point_decision,
            "Central_Decision": central_decision,
            "P10_Decision": scenario_decisions["CQR_P10_Low"],
            "P90_Decision": scenario_decisions["CQR_P90_High"],
            "DFI": round(dfi, 4),
            "FRI": round(fri, 4),
            "Flip_Rate": round(flip_rate, 4),
            "Feasible_Plan_Count_P50": scenario_feasible_counts["CQR_P50_Median"]
        })

frag_df = pd.DataFrame(fragility_results)
frag_df.to_csv("research/results/01_decision_fragility.csv", index=False)
print("Saved research/results/01_decision_fragility.csv", flush=True)

# Generate Summary Stats
overall_dfi = float(frag_df["DFI"].mean())
overall_fri = float(frag_df["FRI"].mean())
overall_flip_rate = float(frag_df["Flip_Rate"].mean()) * 100.0

print(f"\n--- Decision Fragility Experiment Results ---")
print(f"Mean Decision Fragility Index (DFI): {overall_dfi:.4f}")
print(f"Mean Feasibility Robustness Index (FRI): {overall_fri:.4f}")
print(f"Mean Decision Flip Rate: {overall_flip_rate:.2f}%")

fragility_summary = {
    "Overall_DFI": round(overall_dfi, 4),
    "Overall_FRI": round(overall_fri, 4),
    "Overall_Flip_Rate_Pct": round(overall_flip_rate, 2),
    "By_Parcel_Size": {
        str(p): {
            "DFI": round(float(frag_df[frag_df["Parcel_MT"] == p]["DFI"].mean()), 4),
            "FRI": round(float(frag_df[frag_df["Parcel_MT"] == p]["FRI"].mean()), 4),
            "Flip_Rate_Pct": round(float(frag_df[frag_df["Parcel_MT"] == p]["Flip_Rate"].mean()) * 100.0, 2)
        } for p in parcels
    }
}

with open("research/results/decision_fragility_summary.json", "w") as f:
    json.dump(fragility_summary, f, indent=2)

print("Saved research/results/decision_fragility_summary.json", flush=True)
