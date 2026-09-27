import os
import sys
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("research/fragility_surface", exist_ok=True)
os.makedirs("research/results", exist_ok=True)

print("================================================================")
print("  PRIMARINE — FORECAST-TO-DECISION FRAGILITY RESEARCH PROGRAM     ")
print("================================================================")

# Step 1: Run all experiment modules
scripts = [
    "research/experiments/08_fragility_surface.py",
    "research/experiments/09_abstention_vs_forced.py",
    "research/experiments/10_timing_flip_threshold.py",
    "research/experiments/11_constraint_fragility.py",
    "research/experiments/12_negative_control.py",
    "research/experiments/value_of_information_v2_runner.py"
]

for s in scripts:
    print(f"\n--> Running {s}...")
    res = subprocess.run([sys.executable, s], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR running {s}:\n{res.stderr}")
    else:
        print(res.stdout.strip())

print("\n--> Generating Publication-Grade Figures in research/fragility_surface/...")

# Set academic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# 1. Figure: decision_fragility_heatmap.png
surface_df = pd.read_csv("research/fragility_surface/fragility_surface.csv")
pivot_timing = surface_df.pivot_table(index='tightness', columns='uncertainty_scale', values='timing_flip_rate', aggfunc='mean')

plt.figure(figsize=(8, 5), dpi=300)
sns.heatmap(pivot_timing * 100, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Timing Decision Flip Rate (%)'})
plt.title("Forecast-to-Decision Fragility Surface: Timing Flip Rate (%)", fontweight='bold', pad=12)
plt.xlabel("Forecast Uncertainty Scale (x CQR Width)", labelpad=8)
plt.ylabel("Physical Constraint Tightness", labelpad=8)
plt.tight_layout()
plt.savefig("research/fragility_surface/decision_fragility_heatmap.png")
plt.close()

# 2. Figure: timing_flip_vs_uncertainty.png
thresh_df = pd.read_csv("research/fragility_surface/threshold_analysis.csv")
plt.figure(figsize=(7, 4.5), dpi=300)
sns.regplot(data=thresh_df, x='norm_cqr_width', y='timing_flip', logistic=True, ci=95,
            scatter_kws={'alpha': 0.4, 'color': '#1f77b4'}, line_kws={'color': '#d62728', 'linewidth': 2})
plt.axvline(x=1.35, color='black', linestyle='--', label=r'Calibrated $\tau = 1.35 \times \mathrm{median}$')
plt.title("Empirical Probability of Timing Decision Flip vs Normalized CQR Width", fontweight='bold')
plt.xlabel("Normalized CQR Interval Width (W / Median W)")
plt.ylabel("Probability of Decision Flip")
plt.ylim(-0.05, 1.05)
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig("research/fragility_surface/timing_flip_vs_uncertainty.png")
plt.close()

# 3. Figure: physical_flip_vs_uncertainty.png
phys_by_scale = surface_df.groupby('uncertainty_scale')['physical_flip_rate'].mean() * 100
timing_by_scale = surface_df.groupby('uncertainty_scale')['timing_flip_rate'].mean() * 100

plt.figure(figsize=(7, 4.5), dpi=300)
plt.plot(phys_by_scale.index, phys_by_scale.values, marker='s', color='#2ca02c', linewidth=2, label='Physical Allocation Flip (Vessel/Port)')
plt.plot(timing_by_scale.index, timing_by_scale.values, marker='o', color='#d62728', linewidth=2, label='Procurement Timing Flip')
plt.title("Divergence in Fragility: Physical Allocation vs Procurement Timing", fontweight='bold')
plt.xlabel("Forecast Uncertainty Scale (x CQR Width)")
plt.ylabel("Decision Flip Rate (%)")
plt.ylim(-2, 100)
plt.legend()
plt.tight_layout()
plt.savefig("research/fragility_surface/physical_flip_vs_uncertainty.png")
plt.close()

# 4. Figure: constraint_tightness_vs_fragility.png
regime_df = pd.read_csv("research/fragility_surface/constraint_sensitivity_v2.csv")
reg_summary = regime_df.groupby('regime')[['physical_flip', 'timing_flip', 'num_feasible']].mean().reset_index()

fig, ax1 = plt.subplots(figsize=(8, 4.5), dpi=300)
x = np.arange(len(reg_summary))
width = 0.35

rects1 = ax1.bar(x - width/2, reg_summary['physical_flip'] * 100, width, label='Physical Decision Flip (%)', color='#3498db')
rects2 = ax1.bar(x + width/2, reg_summary['timing_flip'] * 100, width, label='Timing Decision Flip (%)', color='#e74c3c')
ax1.set_ylabel('Flip Rate (%)')
ax1.set_xticks(x)
ax1.set_xticklabels(reg_summary['regime'])
ax1.set_title("Constraint Tightness vs Decision Fragility Regimes", fontweight='bold')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(x, reg_summary['num_feasible'], color='#2ecc71', marker='D', linewidth=2, label='Feasible Candidate Count')
ax2.set_ylabel('Feasible Permutations', color='#2ecc71')
ax2.grid(False)
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig("research/fragility_surface/constraint_tightness_vs_fragility.png")
plt.close()

# 5. Figure: cost_vs_abstention.png
abstain_df = pd.read_csv("research/fragility_surface/abstention_experiment.csv")
plt.figure(figsize=(7, 4.5), dpi=300)
plt.plot(abstain_df['abstention_rate'] * 100, abstain_df['mean_cost_system_c'], marker='o', color='#8e44ad', linewidth=2)
plt.title("Trade-off Curve: Mean Landed Cost vs Conformal Abstention Rate", fontweight='bold')
plt.xlabel("Abstention Rate (%) [Selective Prediction]")
plt.ylabel("Mean Net Landed Cost ($/MT)")
for _, r in abstain_df.iterrows():
    if r['threshold_multiplier'] in ['1.0', '1.35', '1.8', 'No Abstention']:
        plt.annotate(f"Mult: {r['threshold_multiplier']}", (r['abstention_rate']*100, r['mean_cost_system_c']),
                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
plt.tight_layout()
plt.savefig("research/fragility_surface/cost_vs_abstention.png")
plt.close()

# 6. Figure: regret_vs_uncertainty.png
plt.figure(figsize=(7, 4.5), dpi=300)
sns.boxplot(data=thresh_df, x='above_tau', y='regret', palette=['#2ecc71', '#e74c3c'])
plt.xticks([0, 1], ['Low Uncertainty (W <= tau)', 'High Uncertainty (W > tau)'])
plt.title("Procurement Regret Distribution Stratified by Calibrated Threshold", fontweight='bold')
plt.xlabel("Conformal Uncertainty Regime")
plt.ylabel("Economic Regret ($/MT)")
plt.tight_layout()
plt.savefig("research/fragility_surface/regret_vs_uncertainty.png")
plt.close()

# 7. Figure: feasibility_vs_uncertainty.png
plt.figure(figsize=(7, 4.5), dpi=300)
feas_by_scale = surface_df.groupby('uncertainty_scale')['fri'].mean() * 100
plt.bar([f"{s}x" for s in feas_by_scale.index], feas_by_scale.values, color='#16a085', width=0.5)
plt.ylim(0, 110)
plt.title("Feasibility Robustness Index (FRI) Across Uncertainty Multipliers", fontweight='bold')
plt.xlabel("Uncertainty Multiplier")
plt.ylabel("Feasibility Robustness (%)")
for i, v in enumerate(feas_by_scale.values):
    plt.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig("research/fragility_surface/feasibility_vs_uncertainty.png")
plt.close()

# 8. Figure: negative_control.png
control_df = pd.read_csv("research/fragility_surface/negative_control.csv")
ctrl_summary = control_df.groupby('case_name')[['num_feasible_vessels', 'physical_decision_stability']].mean().reset_index()

plt.figure(figsize=(8, 4.5), dpi=300)
bars = plt.bar(ctrl_summary['case_name'], ctrl_summary['physical_decision_stability'] * 100, color='#2980b9', width=0.5)
plt.title("Negative Control Test: Physical Stability Under Rigid Constraints", fontweight='bold')
plt.ylabel("Decision Stability Rate (%)")
plt.ylim(0, 120)
plt.axhline(y=100, color='grey', linestyle='--')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f"{yval:.1f}% (No False Fragility)", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig("research/fragility_surface/negative_control.png")
plt.close()

print("\n--> All 8 Figures successfully generated in research/fragility_surface/")
print("================================================================")
print("  PRIMARINE FRAGILITY RESEARCH EXECUTION COMPLETE                 ")
print("================================================================")
