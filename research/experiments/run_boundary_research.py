import os
import sys
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("research/decision_boundary", exist_ok=True)

print("================================================================")
print("  PRIMARINE — DECISION-BOUNDARY AWARE SELECTIVE PREDICTION        ")
print("================================================================")

# 1. Run all experiments
scripts = [
    "research/experiments/13_decision_boundary.py",
    "research/experiments/14_selective_boundary.py",
    "research/experiments/15_boundary_statistics.py"
]

for s in scripts:
    print(f"\n--> Running {s}...")
    res = subprocess.run([sys.executable, s], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"ERROR in {s}:\n{res.stderr}")
    else:
        print(res.stdout.strip())

print("\n--> Generating Publication Figures in research/decision_boundary/...")

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

db_df = pd.read_csv("research/decision_boundary/decision_boundary_analysis.csv")
pol_df = pd.read_csv("research/decision_boundary/selective_policy_comparison.csv")
rc_df = pd.read_csv("research/decision_boundary/risk_coverage.csv")
margin_df = pd.read_csv("research/decision_boundary/margin_analysis.csv")

# 1. Figure: decision_boundary_diagram.png
plt.figure(figsize=(8, 4.5), dpi=300)
sample_pts = db_df.iloc[:40].copy()
x_idx = np.arange(len(sample_pts))
plt.errorbar(x_idx, sample_pts['forecast_C'],
             yerr=[sample_pts['forecast_C'] - sample_pts['cqr_lower_L'], sample_pts['cqr_upper_U'] - sample_pts['forecast_C']],
             fmt='o', color='#1f77b4', ecolor='#aec7e8', elinewidth=2, capsize=3, label='Forecast & CQR Interval [L, U]')
plt.plot(x_idx, sample_pts['current_rate_B'], color='#d62728', linestyle='--', linewidth=2, label='Current Market Rate (Decision Boundary B)')
for i, (_, r) in enumerate(sample_pts.iterrows()):
    if r['boundary_crossing'] == 1:
        plt.axvspan(i - 0.4, i + 0.4, color='#fee08b', alpha=0.3)
plt.title("Decision Boundary Crossing: Conformal Intervals Spanning Current Rate", fontweight='bold')
plt.xlabel("Test Scenario Index")
plt.ylabel("Freight Index Rate ($/MT)")
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig("research/decision_boundary/decision_boundary_diagram.png")
plt.close()

# 2. Figure: width_vs_boundary_risk.png
plt.figure(figsize=(7, 4.5), dpi=300)
width_comp = pd.read_csv("research/decision_boundary/width_boundary_comparison.csv")
bars = plt.barh(width_comp['Signal'], width_comp['False_Breakout_Rate'] * 100, color='#e67e22')
plt.title("False Breakout Rate Stratified by Uncertainty Signal", fontweight='bold')
plt.xlabel("Empirical False Breakout Rate (%)")
for bar in bars:
    w = bar.get_width()
    plt.text(w + 1, bar.get_y() + bar.get_height()/2.0, f"{w:.1f}%", va='center', fontweight='bold', fontsize=9)
plt.xlim(0, max(width_comp['False_Breakout_Rate']*100) + 10)
plt.tight_layout()
plt.savefig("research/decision_boundary/width_vs_boundary_risk.png")
plt.close()

# 3. Figure: risk_coverage_width.png
plt.figure(figsize=(7, 4.5), dpi=300)
w_rc = rc_df[rc_df['method'] == 'Width-Based']
plt.plot(w_rc['coverage'] * 100, w_rc['selective_risk'] * 100, marker='s', color='#2980b9', linewidth=2, label='Timing Error Rate')
plt.plot(w_rc['coverage'] * 100, w_rc['false_breakout_rate'] * 100, marker='o', color='#c0392b', linewidth=2, label='False Breakout Rate')
plt.title("Risk-Coverage Curve: Width-Based Abstention", fontweight='bold')
plt.xlabel("Decision Coverage (%)")
plt.ylabel("Selective Risk (%)")
plt.legend()
plt.tight_layout()
plt.savefig("research/decision_boundary/risk_coverage_width.png")
plt.close()

# 4. Figure: risk_coverage_margin.png
plt.figure(figsize=(7, 4.5), dpi=300)
m_rc = rc_df[rc_df['method'] == 'Normalized-Margin']
plt.plot(m_rc['coverage'] * 100, m_rc['selective_risk'] * 100, marker='s', color='#27ae60', linewidth=2, label='Timing Error Rate')
plt.plot(m_rc['coverage'] * 100, m_rc['false_breakout_rate'] * 100, marker='o', color='#e74c3c', linewidth=2, label='False Breakout Rate')
plt.title("Risk-Coverage Curve: Normalized-Margin Abstention", fontweight='bold')
plt.xlabel("Decision Coverage (%)")
plt.ylabel("Selective Risk (%)")
plt.legend()
plt.tight_layout()
plt.savefig("research/decision_boundary/risk_coverage_margin.png")
plt.close()

# 5. Figure: risk_coverage_combined.png
plt.figure(figsize=(7, 4.5), dpi=300)
plt.plot(w_rc['coverage'] * 100, w_rc['false_breakout_rate'] * 100, marker='s', color='#2980b9', label='Width-Based')
plt.plot(m_rc['coverage'] * 100, m_rc['false_breakout_rate'] * 100, marker='o', color='#27ae60', label='Normalized-Margin')
plt.title("Comparative Risk-Coverage: False Breakout Exposure", fontweight='bold')
plt.xlabel("Decision Coverage (%)")
plt.ylabel("False Breakout Rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig("research/decision_boundary/risk_coverage_combined.png")
plt.close()

# 6. Figure: margin_vs_regret.png
plt.figure(figsize=(8, 4.5), dpi=300)
valid_margins = margin_df[margin_df['N'] > 0]
plt.bar(valid_margins['margin_stratum'], valid_margins['Mean_Regret'], color='#8e44ad', width=0.5)
plt.title("Procurement Regret Across Decision Margin Strata", fontweight='bold')
plt.ylabel("Mean Economic Regret ($/MT)")
plt.xticks(rotation=15, ha='right')
for i, v in enumerate(valid_margins['Mean_Regret']):
    plt.text(i, v + 0.01, f"${v:.3f}", ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig("research/decision_boundary/margin_vs_regret.png")
plt.close()

# 7. Figure: boundary_crossing_vs_false_breakout.png
plt.figure(figsize=(6, 4.5), dpi=300)
bc_comp = db_df.groupby('boundary_crossing')['false_breakout'].mean() * 100
bars = plt.bar(['No Crossing (L>B or U<B)', 'Boundary Crossing (L<=B<=U)'], bc_comp.values, color=['#2ecc71', '#e74c3c'], width=0.45)
plt.title("False Breakout Probability by Boundary Crossing Status", fontweight='bold')
plt.ylabel("False Breakout Empirical Frequency (%)")
plt.ylim(0, max(bc_comp.values) + 15)
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y + 2, f"{y:.1f}%", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig("research/decision_boundary/boundary_crossing_vs_false_breakout.png")
plt.close()

# 8. Figure: selective_policy_comparison.png
plt.figure(figsize=(8, 4.5), dpi=300)
x = np.arange(len(pol_df))
width = 0.35
plt.bar(x - width/2, pol_df['abstention_rate'] * 100, width, label='Abstention Rate (%)', color='#34495e')
plt.bar(x + width/2, pol_df['false_breakouts'], width, label='False Breakout Count', color='#e74c3c')
plt.xticks(x, [p.split('. ')[-1] for p in pol_df['policy']], rotation=15, ha='right')
plt.title("Selective Policy Comparison: Abstention vs False Breakout Protection", fontweight='bold')
plt.ylabel("Metric Value")
plt.legend()
plt.tight_layout()
plt.savefig("research/decision_boundary/selective_policy_comparison.png")
plt.close()

print("\n--> All 8 Figures successfully generated in research/decision_boundary/")
print("================================================================")
print("  PRIMARINE DECISION-BOUNDARY RESEARCH COMPLETE                   ")
print("================================================================")
