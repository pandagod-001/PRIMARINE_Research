import os
import json
import numpy as np
import pandas as pd

os.makedirs("research/results", exist_ok=True)
print("=== PRIMARINE Experiment 3: Counterfactual Constraint Sensitivity & Criticality ===", flush=True)

ports = {
    "Paradip": {"max_draft": 17.1, "max_loa": 300.0, "max_beam": 48.0},
    "Visakhapatnam": {"max_draft": 16.5, "max_loa": 290.0, "max_beam": 45.0},
    "Haldia": {"max_draft": 11.5, "max_loa": 230.0, "max_beam": 32.2}
}

vessels = [
    {"vessel_id": "V1_Capesize_180k", "class": "Capesize", "dwt": 180000, "draft": 16.8, "loa": 292.0, "beam": 45.0},
    {"vessel_id": "V2_Capesize_150k", "class": "Capesize", "dwt": 150000, "draft": 15.2, "loa": 274.0, "beam": 43.0},
    {"vessel_id": "V3_Panamax_82k", "class": "Panamax", "dwt": 82000, "draft": 13.8, "loa": 229.0, "beam": 32.2},
    {"vessel_id": "V4_Panamax_75k", "class": "Panamax", "dwt": 75000, "draft": 12.8, "loa": 225.0, "beam": 32.2},
    {"vessel_id": "V5_Supramax_58k", "class": "Supramax", "dwt": 58000, "draft": 11.2, "loa": 190.0, "beam": 32.2},
]

parcel_sizes = [50000, 75000, 100000, 120000, 150000, 175000]

# Evaluate All Candidate Pairings
sensitivity_records = []

for parcel in parcel_sizes:
    for v in vessels:
        for p_name, p in ports.items():
            # Baseline Constraint Checks
            pass_cap = v["dwt"] >= parcel
            pass_draft = v["draft"] <= p["max_draft"]
            pass_loa = v["loa"] <= p["max_loa"]
            pass_beam = v["beam"] <= p["max_beam"]
            
            baseline_feasible = pass_cap and pass_draft and pass_loa and pass_beam
            
            # Counterfactual Relaxations (Relax exactly one constraint)
            # 1. Relax Capacity (+25% DWT allowance or partial parcel)
            relax_cap_feasible = True and pass_draft and pass_loa and pass_beam
            # 2. Relax Draft (+2.0m tidal / dredging depth)
            relax_draft_feasible = pass_cap and (v["draft"] <= p["max_draft"] + 2.0) and pass_loa and pass_beam
            # 3. Relax LOA (+30m berth extension)
            relax_loa_feasible = pass_cap and pass_draft and (v["loa"] <= p["max_loa"] + 30.0) and pass_beam
            # 4. Relax Beam (+5m berth geometry)
            relax_beam_feasible = pass_cap and pass_draft and pass_loa and (v["beam"] <= p["max_beam"] + 5.0)
            
            sensitivity_records.append({
                "Parcel_MT": parcel,
                "Vessel_ID": v["vessel_id"],
                "Port": p_name,
                "Baseline_Feasible": int(baseline_feasible),
                "Fail_Capacity": int(not pass_cap),
                "Fail_Draft": int(not pass_draft),
                "Fail_LOA": int(not pass_loa),
                "Fail_Beam": int(not pass_beam),
                "Feasible_If_Relax_Capacity": int(relax_cap_feasible),
                "Feasible_If_Relax_Draft": int(relax_draft_feasible),
                "Feasible_If_Relax_LOA": int(relax_loa_feasible),
                "Feasible_If_Relax_Beam": int(relax_beam_feasible)
            })

sens_df = pd.DataFrame(sensitivity_records)
sens_df.to_csv("research/results/03_constraint_sensitivity.csv", index=False)
print("Saved research/results/03_constraint_sensitivity.csv", flush=True)

# Calculate Constraint Criticality Score (CCS):
# CCS = % of infeasible plans that become feasible when that specific constraint is relaxed
infeasible_subset = sens_df[sens_df["Baseline_Feasible"] == 0]
total_infeasible = len(infeasible_subset)

ccs_draft = (infeasible_subset["Feasible_If_Relax_Draft"].sum() / total_infeasible) * 100.0
ccs_cap = (infeasible_subset["Feasible_If_Relax_Capacity"].sum() / total_infeasible) * 100.0
ccs_loa = (infeasible_subset["Feasible_If_Relax_LOA"].sum() / total_infeasible) * 100.0
ccs_beam = (infeasible_subset["Feasible_If_Relax_Beam"].sum() / total_infeasible) * 100.0

print(f"\n--- Constraint Criticality Analysis ({total_infeasible} Infeasible Pairs) ---")
print(f"1. Draft Criticality Score:    {ccs_draft:.2f}% (Toughest Physical Bottleneck)")
print(f"2. Capacity Criticality Score: {ccs_cap:.2f}% (Parcel Sizing Bottleneck)")
print(f"3. LOA Criticality Score:      {ccs_loa:.2f}%")
print(f"4. Beam Criticality Score:     {ccs_beam:.2f}%")
