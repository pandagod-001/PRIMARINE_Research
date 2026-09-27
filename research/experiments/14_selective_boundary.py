import os
import json
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/decision_boundary", exist_ok=True)

print("=== PRIMARINE Decision Boundary: Exp 14 - Selective Boundary Policies & Risk-Coverage ===", flush=True)

db_df = pd.read_csv("research/decision_boundary/decision_boundary_analysis.csv")
N = len(db_df)

# Evaluate Signals:
# 1. Width-only: High vs Low width
# 2. Boundary crossing: Crossing vs No crossing
# 3. Normalized Margin: Low NM vs High NM
# 4. State: Robust Enter / Robust Defer vs Boundary Crossing

def get_signal_metrics(sub_df, name):
    n = len(sub_df)
    if n == 0:
        return {"Signal": name, "N": 0, "False_Breakout_Rate": 0, "Error_Rate": 0, "Mean_Regret": 0, "Median_Regret": 0}
    return {
        "Signal": name,
        "N": n,
        "False_Breakout_Count": int(sub_df['false_breakout'].sum()),
        "False_Breakout_Rate": round(float(sub_df['false_breakout'].mean()), 4),
        "Error_Count": int(sub_df['timing_error'].sum()),
        "Error_Rate": round(float(sub_df['timing_error'].mean()), 4),
        "Mean_Regret": round(float(sub_df['regret'].mean()), 4),
        "Median_Regret": round(float(sub_df['regret'].median()), 4)
    }

comp_rows = [
    get_signal_metrics(db_df[db_df['high_width_flag'] == 0], "Low Width (W <= tau)"),
    get_signal_metrics(db_df[db_df['high_width_flag'] == 1], "High Width (W > tau)"),
    get_signal_metrics(db_df[db_df['boundary_crossing'] == 1], "Boundary Crossing (L <= B <= U)"),
    get_signal_metrics(db_df[db_df['boundary_crossing'] == 0], "No Boundary Crossing (L > B or U < B)"),
    get_signal_metrics(db_df[db_df['decision_state'] == 'ROBUST_ENTER'], "State: Robust Enter (L > B)"),
    get_signal_metrics(db_df[db_df['decision_state'] == 'ROBUST_DEFER'], "State: Robust Defer (U < B)"),
    get_signal_metrics(db_df[db_df['low_margin_flag'] == 1], "Low Norm Margin (NM < tau_nm)"),
    get_signal_metrics(db_df[db_df['low_margin_flag'] == 0], "High Norm Margin (NM >= tau_nm)")
]

comp_df = pd.DataFrame(comp_rows)
comp_df.to_csv("research/decision_boundary/width_boundary_comparison.csv", index=False)
print("\n--- Signal Comparison Table ---")
print(comp_df.to_string())

# Selective Policies Evaluation
# Policy 1: Forced Point Forecast (Always Decide)
# Policy 2: Width-only Abstention (Abstain if W > tau_width)
# Policy 3: Boundary-Crossing Abstention (Abstain if L <= B <= U)
# Policy 4: Normalized-Margin Abstention (Abstain if NM < tau_nm)
# Policy 5: Combined Rule (Abstain if Boundary Crossing OR NM < tau_nm)

policies = {
    "1. Forced Point Forecast": lambda r: False,
    "2. Width-Only Abstention": lambda r: r['high_width_flag'] == 1,
    "3. Boundary-Crossing Abstention": lambda r: r['boundary_crossing'] == 1,
    "4. Normalized-Margin Abstention": lambda r: r['low_margin_flag'] == 1,
    "5. Combined Boundary + Margin": lambda r: (r['boundary_crossing'] == 1) or (r['low_margin_flag'] == 1)
}

pol_records = []
for p_name, p_fn in policies.items():
    abstained = []
    costs = []
    regrets = []
    fb_count = 0
    err_count = 0
    non_abstained_err = []
    
    for idx, r in db_df.iterrows():
        is_abs = p_fn(r)
        abstained.append(int(is_abs))
        curr = r['current_rate_B']
        act = r['actual_future']
        t_dec = r['timing_decision']
        
        if is_abs:
            cost = 0.5 * curr + 0.5 * act
            opt_cost = min(curr, act)
            regret = cost - opt_cost
        else:
            cost = curr if t_dec == "ENTER_NOW" else act
            opt_cost = min(curr, act)
            regret = cost - opt_cost
            if r['false_breakout'] == 1:
                fb_count += 1
            if r['timing_error'] == 1:
                err_count += 1
            non_abstained_err.append(r['timing_error'])
            
        costs.append(cost)
        regrets.append(regret)
        
    n_abs = sum(abstained)
    cov = (N - n_abs) / N
    sel_risk = np.mean(non_abstained_err) if len(non_abstained_err) > 0 else 0.0
    mean_c = np.mean(costs)
    mean_reg = np.mean(regrets)
    
    pol_records.append({
        "policy": p_name,
        "coverage": round(cov, 4),
        "abstention_rate": round(n_abs / N, 4),
        "false_breakouts": fb_count,
        "non_abstained_errors": err_count,
        "selective_risk": round(sel_risk, 4),
        "mean_landed_cost": round(mean_c, 4),
        "cost_diff_vs_forced": round(mean_c - db_df['current_rate_B'].mean(), 4),
        "mean_regret": round(mean_reg, 4)
    })

pol_df = pd.DataFrame(pol_records)
pol_df.to_csv("research/decision_boundary/selective_policy_comparison.csv", index=False)
print("\n--- Policy Comparison Table ---")
print(pol_df.to_string())

# Risk-Coverage Curves Generation
# Varying coverage thresholds for width, boundary margin, and normalized margin
rc_records = []
percentiles = np.linspace(0.05, 0.95, 19)

# 1. Width-based threshold curve
for p in percentiles:
    th = np.quantile(db_df['interval_width_W'], 1.0 - p)
    mask = db_df['interval_width_W'] <= th
    cov = mask.mean()
    sel_err = db_df[mask]['timing_error'].mean() if cov > 0 else 0.0
    fb_r = db_df[mask]['false_breakout'].mean() if cov > 0 else 0.0
    rc_records.append({"method": "Width-Based", "coverage": cov, "selective_risk": sel_err, "false_breakout_rate": fb_r})

# 2. Normalized-Margin threshold curve
for p in percentiles:
    th = np.quantile(db_df['norm_margin_NM'], 1.0 - p)
    mask = db_df['norm_margin_NM'] >= th
    cov = mask.mean()
    sel_err = db_df[mask]['timing_error'].mean() if cov > 0 else 0.0
    fb_r = db_df[mask]['false_breakout'].mean() if cov > 0 else 0.0
    rc_records.append({"method": "Normalized-Margin", "coverage": cov, "selective_risk": sel_err, "false_breakout_rate": fb_r})

rc_df = pd.DataFrame(rc_records)
rc_df.to_csv("research/decision_boundary/risk_coverage.csv", index=False)
print("\nExp 14 Complete: Risk-Coverage dataset generated.")
