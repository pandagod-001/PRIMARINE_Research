import os
import json
import numpy as np
import pandas as pd

os.makedirs("research/results", exist_ok=True)
print("=== PRIMARINE Experiment 4: Adaptive Disruption Recovery & Impact Re-Optimization ===", flush=True)

# Define Base Parameters
base_freight = 18.50 # $/unit
bunker_price = 550.0 # $/MT
parcel_mt = 120000

ports = {
    "Paradip": {"max_draft": 17.1, "max_loa": 300.0, "handling_cost_per_t": 3.80, "avg_wait_days": 2.5},
    "Visakhapatnam": {"max_draft": 16.5, "max_loa": 290.0, "handling_cost_per_t": 4.10, "avg_wait_days": 2.0},
    "Haldia": {"max_draft": 11.5, "max_loa": 230.0, "handling_cost_per_t": 5.20, "avg_wait_days": 3.5}
}

vessels = {
    "V1_Capesize_180k": {"class": "Capesize", "dwt": 180000, "draft": 16.8, "loa": 292.0, "fuel_burn": 42.0, "daily_hire": 24000, "avail": True},
    "V2_Capesize_150k": {"class": "Capesize", "dwt": 150000, "draft": 15.2, "loa": 274.0, "fuel_burn": 48.0, "daily_hire": 21000, "avail": True},
    "V3_Panamax_82k": {"class": "Panamax", "dwt": 82000, "draft": 13.8, "loa": 229.0, "fuel_burn": 28.0, "daily_hire": 14500, "avail": True},
    "V4_Panamax_75k": {"class": "Panamax", "dwt": 75000, "draft": 12.8, "loa": 225.0, "fuel_burn": 31.0, "daily_hire": 13000, "avail": True},
}

def solve_optimal_plan(vessel_dict, port_dict, freight, parcel):
    plans = []
    for v_id, v in vessel_dict.items():
        if not v.get("avail", True):
            continue
        for p_id, p in port_dict.items():
            if v["dwt"] < parcel or v["draft"] > p["max_draft"] or v["loa"] > p["max_loa"]:
                continue
            sailing_days = 4200.0 / (12.5 * 24.0)
            tot_days = sailing_days + p["avg_wait_days"] + (parcel / 25000.0)
            tot_cost = (freight * parcel) + (sailing_days * v["fuel_burn"] * bunker_price) + (tot_days * v["daily_hire"]) + (parcel * p["handling_cost_per_t"])
            unit_cost = tot_cost / parcel
            plans.append({
                "plan_id": f"{v_id}_at_{p_id}",
                "unit_cost": unit_cost,
                "vessel": v_id,
                "port": p_id,
                "tot_days": tot_days
            })
    plans.sort(key=lambda x: x["unit_cost"])
    return plans[0] if len(plans) > 0 else None

# Baseline D0 Plan
base_plan = solve_optimal_plan(vessels, ports, base_freight, parcel_mt)
base_cost = base_plan["unit_cost"]

# Disruption Scenarios
disruptions = [
    {"Scenario": "D0_Baseline", "Desc": "Nominal Operating State", "Freight": base_freight, "Ports": ports, "Vessels": vessels},
    {"Scenario": "D1_Freight_Spike_10pct", "Desc": "Market Surge (+10% Freight)", "Freight": base_freight * 1.10, "Ports": ports, "Vessels": vessels},
    {"Scenario": "D2_Freight_Spike_20pct", "Desc": "Market Shock (+20% Freight)", "Freight": base_freight * 1.20, "Ports": ports, "Vessels": vessels},
    {"Scenario": "D3_Paradip_Draft_Cut", "Desc": "Siltation Cuts Paradip Draft to 15.0m", "Freight": base_freight, 
     "Ports": {**ports, "Paradip": {**ports["Paradip"], "max_draft": 15.0}}, "Vessels": vessels},
    {"Scenario": "D4_Primary_Vessel_Unavailable", "Desc": "Selected V1 Fixed by Third Party", "Freight": base_freight, "Ports": ports,
     "Vessels": {**vessels, "V1_Capesize_180k": {**vessels["V1_Capesize_180k"], "avail": False}}},
    {"Scenario": "D5_Port_Congestion_Surge", "Desc": "Paradip Anchorage Queue +4 Days", "Freight": base_freight,
     "Ports": {**ports, "Paradip": {**ports["Paradip"], "avg_wait_days": 6.5}}, "Vessels": vessels},
    {"Scenario": "D6_Compound_Cyclone_Disruption", "Desc": "Cyclone Shock: +15% Freight, V1 Unavailable, Paradip Closed", "Freight": base_freight * 1.15,
     "Ports": {**ports, "Paradip": {**ports["Paradip"], "max_draft": 0.0}}, # Closed
     "Vessels": {**vessels, "V1_Capesize_180k": {**vessels["V1_Capesize_180k"], "avail": False}}}
]

disruption_results = []

for sc in disruptions:
    # 1. Evaluate Static Plan (What happens if we stubbornly stick to baseline choice)
    static_vessel = vessels.get(base_plan["vessel"])
    static_port = sc["Ports"].get(base_plan["port"])
    
    # Check if static plan is still feasible
    static_feas = False
    if static_vessel.get("avail", True) and static_port:
        if static_vessel["dwt"] >= parcel_mt and static_vessel["draft"] <= static_port["max_draft"] and static_vessel["loa"] <= static_port["max_loa"]:
            static_feas = True
            
    if static_feas:
        sailing_days = 4200.0 / (12.5 * 24.0)
        tot_days = sailing_days + static_port["avg_wait_days"] + (parcel_mt / 25000.0)
        static_cost = ((sc["Freight"] * parcel_mt) + (sailing_days * static_vessel["fuel_burn"] * bunker_price) + 
                       (tot_days * static_vessel["daily_hire"]) + (parcel_mt * static_port["handling_cost_per_t"])) / parcel_mt
    else:
        # Demurrage / Emergency Spot Penalty ($15/MT chartering penalty)
        static_cost = base_cost + 15.00 
        
    # 2. Adaptive Re-Optimization Plan
    adapt_plan = solve_optimal_plan(sc["Vessels"], sc["Ports"], sc["Freight"], parcel_mt)
    adapt_cost = adapt_plan["unit_cost"] if adapt_plan else (base_cost + 20.00)
    
    # Measure Degradation and Adaptive Recovery
    cost_degradation = adapt_cost - base_cost
    static_loss = static_cost - base_cost
    adaptive_savings = static_cost - adapt_cost
    
    disruption_results.append({
        "Scenario": sc["Scenario"],
        "Description": sc["Desc"],
        "Original_Plan": base_plan["plan_id"],
        "Static_Feasible": int(static_feas),
        "Static_Cost_pmt": round(static_cost, 4),
        "Adapted_Plan": adapt_plan["plan_id"] if adapt_plan else "INFEASIBLE",
        "Adapted_Cost_pmt": round(adapt_cost, 4),
        "Cost_Degradation_pmt": round(cost_degradation, 4),
        "Adaptive_Benefit_pmt": round(adaptive_savings, 4),
        "Decision_Adapted": int(base_plan["plan_id"] != (adapt_plan["plan_id"] if adapt_plan else "NONE"))
    })

disrupt_df = pd.DataFrame(disruption_results)
disrupt_df.to_csv("research/results/04_adaptive_disruption.csv", index=False)
print("Saved research/results/04_adaptive_disruption.csv", flush=True)

print(f"\n--- Adaptive Disruption Experiment Results ---")
for _, r in disrupt_df.iterrows():
    print(f"[{r['Scenario']}] Static Feas: {r['Static_Feasible']} | Adapted Plan: {r['Adapted_Plan']} | Adapt Savings: ${r['Adaptive_Benefit_pmt']:.2f}/MT")
