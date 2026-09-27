import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("figures/ideation_evidence", exist_ok=True)
os.makedirs("PRIMARINE_IDEATION_EVIDENCE/figures", exist_ok=True)

# Set global matplotlib styles for clean, academic aesthetic
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#94a3b8'
plt.rcParams['axes.linewidth'] = 0.8

print("=== Generating PRIMARINE Ideation Evidence Visualizations ===", flush=True)

# ----------------------------------------------------------------------
# FIGURE 01: SYSTEM ARCHITECTURE
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

# Main Header
ax.text(0.5, 0.95, "PRIMARINE — Decision Intelligence Architecture", ha='center', va='center', fontsize=15, fontweight='bold', color='#0f172a')
ax.text(0.5, 0.91, "Integration of Temporal Market Intelligence with Spatial Maritime-Network Reasoning", ha='center', va='center', fontsize=10, color='#475569')

# Box helper
def draw_box(x, y, w, h, title, subtitle, bg_color, border_color, badge=None):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor=bg_color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0f172a')
    ax.text(x + w/2, y + h*0.35, subtitle, ha='center', va='center', fontsize=8.5, color='#334155')
    if badge:
        ax.text(x + w/2, y + h*0.12, badge, ha='center', va='center', fontsize=7.5, fontweight='bold', color=border_color)

# 1. Market Layer
draw_box(0.08, 0.62, 0.38, 0.22, "1. TEMPORAL MARKET LAYER", "BDRY + Brent + Miners (BHP/Vale) + FX\nLightGBM 7-Day Turning-Point Forecaster", "#f0fdf4", "#16a34a", "[ VALIDATED EMPIRICAL CORE ]")

# 2. Network Layer
draw_box(0.54, 0.62, 0.38, 0.22, "2. SPATIAL NETWORK LAYER", "8-Node Dry Bulk Graph (11 Corridors)\nST-GNN Disruption Propagation Engine", "#eff6ff", "#2563eb", "[ CONTROLLED PROOF-OF-CONCEPT ]")

# 3. Uncertainty Layer
draw_box(0.08, 0.34, 0.38, 0.18, "3. UNCERTAINTY QUANTIFICATION", "Split-CQR Calibrated Prediction Bands (88.2%)\nStress Breakdown Monitoring", "#fefce8", "#ca8a04", "[ VALIDATED EMPIRICAL CORE ]")

# 4. Telemetry / Future Box
draw_box(0.54, 0.34, 0.38, 0.18, "4. MARITIME TELEMETRY INGESTION", "Live Satellite AIS Streams & Port EDI Queues\nDynamic Terminal Congestion Feeds", "#f8fafc", "#64748b", "[ FUTURE IMPLEMENTATION PHASE ]")

# 5. Decision Engine
draw_box(0.20, 0.08, 0.60, 0.18, "5. CHARTER PROCUREMENT DECISION ENGINE", "Synthesizes Market Outlook + Uncertainty Width + Route Disruption Exposure\nOutputs: ENTER_NOW / DEFER_ENTRY / MONITOR / HIGH UNCERTAINTY (ABSTAIN)", "#faf5ff", "#9333ea", "[ VALIDATED EMPIRICAL BACKTEST ]")

# Connecting Arrows
arrow_kw = dict(arrowstyle="->", lw=1.5, color="#64748b")
ax.annotate("", xy=(0.27, 0.52), xytext=(0.27, 0.62), arrowprops=arrow_kw)
ax.annotate("", xy=(0.73, 0.52), xytext=(0.73, 0.62), arrowprops=arrow_kw)
ax.annotate("", xy=(0.38, 0.26), xytext=(0.27, 0.34), arrowprops=arrow_kw)
ax.annotate("", xy=(0.62, 0.26), xytext=(0.73, 0.34), arrowprops=arrow_kw)

# Source Footer
ax.text(0.5, 0.02, "Source: PRIMARINE Research Architecture Design — Not Claiming Live Commercial Telemetry", ha='center', va='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/01_PRIMARINE_system_architecture.png", dpi=300)
plt.close()
print("Saved 01_PRIMARINE_system_architecture.png")

# ----------------------------------------------------------------------
# FIGURE 02: POINT FORECAST REALITY
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
models = ['Naive Persistence Baseline\n(Yesterday\'s Close)', 'PRIMARINE Multi-Modal\n(LightGBM)']
maes = [0.4175, 0.4644]
colors = ['#10b981', '#3b82f6']

bars = ax.bar(models, maes, color=colors, width=0.45, edgecolor='#1e293b', linewidth=1.2)
ax.set_title("Point Forecasting: Persistence Remains Difficult to Beat", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "Untouched Out-of-Sample Evaluation (288 Daily Trading Observations)", transform=ax.transAxes, ha='center', fontsize=9, color='#64748b')
ax.set_ylabel("Mean Absolute Error (MAE) [$/unit]", fontsize=10, fontweight='bold', color='#1e293b')
ax.set_ylim(0, 0.60)
ax.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015, f"{y:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

# Honesty callout annotation
ax.annotate("PRIMARINE does NOT claim superiority in point MAE.\nDaily freight series exhibit near-martingale properties on flat days.",
            xy=(0.5, 0.44), xytext=(0.5, 0.52),
            ha='center', fontsize=8.5, fontweight='bold', color='#dc2626',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#fef2f2', edgecolor='#f87171'))

ax.text(0.5, -0.15, "Source: PRIMARINE public historical market-data evaluation", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/02_point_forecast_reality.png", dpi=300)
plt.close()
print("Saved 02_point_forecast_reality.png")

# ----------------------------------------------------------------------
# FIGURE 03: TURNING-POINT DETECTION
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
tp_models = ['Naive Persistence\nBaseline', '5-Day Simple\nMoving Average', 'AutoRegressive\nAR(5)', 'PRIMARINE Multi-Modal\n(LightGBM)']
tp_f1 = [0.00, 26.47, 27.18, 59.51]
tp_colors = ['#94a3b8', '#64748b', '#475569', '#2563eb']

bars = ax.bar(tp_models, tp_f1, color=tp_colors, width=0.50, edgecolor='#1e293b', linewidth=1.2)
ax.set_title("Major Freight-Market Inflection Detection", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "7-Day >= +/-4.0% Cumulative Turning-Point Classification (160 Test Events)", transform=ax.transAxes, ha='center', fontsize=9, color='#64748b')
ax.set_ylabel("Turning-Point F1 Score (%)", fontsize=10, fontweight='bold', color='#1e293b')
ax.set_ylim(0, 75)
ax.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 1.5, f"{y:.2f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Advantage bracket annotation
ax.annotate("+32.33 percentage points vs AR(5)",
            xy=(3, 59.51), xytext=(2.2, 66.0),
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#2563eb"),
            ha='center', fontsize=9, fontweight='bold', color='#1e40af',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#eff6ff', edgecolor='#93c5fd'))

ax.text(0.5, -0.18, "Source: PRIMARINE public historical market-data evaluation\nTest-set event definition and evaluation protocol fixed before final evaluation.", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/03_turning_point_f1.png", dpi=300)
plt.close()
print("Saved 03_turning_point_f1.png")

# ----------------------------------------------------------------------
# FIGURE 04: DIRECTIONAL ACCURACY
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
dir_models = ['5-Day Moving Average\n(Benchmark)', 'PRIMARINE Multi-Modal\n(LightGBM)', 'Gradient Boosted\n(XGBoost)']
dir_acc = [50.70, 59.15, 60.56]
dir_colors = ['#94a3b8', '#3b82f6', '#1d4ed8']

bars = ax.bar(dir_models, dir_acc, color=dir_colors, width=0.45, edgecolor='#1e293b', linewidth=1.2)
ax.axhline(50.0, color='#dc2626', linestyle='--', linewidth=1.2, label='Random Chance Baseline (50.0%)')
ax.set_title("Directional Movement Accuracy", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "Descriptive improvement observed; not statistically significant (p = 0.138)", transform=ax.transAxes, ha='center', fontsize=9, color='#64748b')
ax.set_ylabel("Out-of-Sample Directional Accuracy (%)", fontsize=10, fontweight='bold', color='#1e293b')
ax.set_ylim(40, 75)
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=8.5)

for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 1.0, f"{y:.2f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Statistical Callout Box
ax.text(0.5, 0.35, "Statistical Audit (Block-Bootstrap, B=1,000):\n95% CI: [45.70%, 67.86%] | p-value = 0.138\nFormal statistical significance is NOT established.",
        transform=ax.transAxes, ha='center', fontsize=8.5, color='#475569',
        bbox=dict(boxstyle="round,pad=0.4", facecolor='#f8fafc', edgecolor='#cbd5e1'))

ax.text(0.5, -0.16, "Source: PRIMARINE public historical market-data evaluation", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/04_directional_accuracy.png", dpi=300)
plt.close()
print("Saved 04_directional_accuracy.png")

# ----------------------------------------------------------------------
# FIGURE 05: CQR UNCERTAINTY & ABSTENTION
# ----------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2), dpi=300)

# Left: Coverage Bar
cov_labels = ['Nominal Target', 'Empirical Test\n(Normal Regime)', 'COVID-19 Stress\n(Extreme Regime)']
cov_vals = [90.00, 88.19, 50.59]
cov_cols = ['#94a3b8', '#16a34a', '#dc2626']
bars1 = ax1.bar(cov_labels, cov_vals, color=cov_cols, width=0.5, edgecolor='#1e293b', linewidth=1.2)
ax1.set_title("Split-CQR Empirical Coverage", fontsize=11, fontweight='bold', pad=10, color='#0f172a')
ax1.set_ylabel("Coverage Percentage (%)", fontsize=9.5, fontweight='bold')
ax1.set_ylim(0, 105)
ax1.grid(axis='y', linestyle=':', alpha=0.6)
for bar in bars1:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, y + 1.5, f"{y:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Right: Decision Rule Diagram
ax2.set_facecolor('#f8fafc')
ax2.axis('off')
ax2.text(0.5, 0.90, "HIGH UNCERTAINTY / ABSTAIN RULE", ha='center', va='center', fontsize=11, fontweight='bold', color='#0f172a')

rule_text = (
    "Operational Uncertainty Logic:\n\n"
    "1. Mean Calibrated Interval Width = 7.62 $/unit\n"
    "2. Median Calibrated Width = 7.42 $/unit\n\n"
    "Deterministic Decision Trigger:\n"
    "IF Interval Width > 1.35 × Median Width\n"
    "THEN Trigger: ABSTAIN_HIGH_UNCERTAINTY\n\n"
    "Stress Awareness:\n"
    "Coverage degradation during black-swan regimes\n"
    "is an active warning signal, not an algorithm defect."
)
ax2.text(0.5, 0.45, rule_text, ha='center', va='center', fontsize=8.5, color='#1e293b',
         bbox=dict(boxstyle="round,pad=0.6", facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1.2))

fig.suptitle("Conformalized Quantile Regression (CQR) & Abstention Logic", fontsize=12, fontweight='bold', y=0.98, color='#0f172a')
fig.text(0.5, 0.02, "Source: PRIMARINE public historical market-data evaluation", ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout(rect=[0, 0.04, 1, 0.95])
plt.savefig("figures/ideation_evidence/05_cqr_uncertainty.png", dpi=300)
plt.close()
print("Saved 05_cqr_uncertainty.png")

# ----------------------------------------------------------------------
# FIGURE 06: MARITIME GRAPH (8 NODES, 11 CORRIDORS)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor('#f8fafc')
fig.patch.set_facecolor('#ffffff')

# Node Positions (Schematic Topological Representation)
pos = {
    0: (0.15, 0.75), # Hay Point
    1: (0.15, 0.50), # Gladstone
    2: (0.15, 0.25), # Newcastle
    3: (0.35, 0.15), # Samarinda
    4: (0.50, 0.50), # Singapore Strait
    5: (0.85, 0.75), # Paradip
    6: (0.85, 0.50), # Visakhapatnam
    7: (0.85, 0.25)  # Haldia
}

node_names_map = {
    0: "Hay Point (AU)\n[Coking Coal Origin]",
    1: "Gladstone (AU)\n[Coking Coal/Alumina]",
    2: "Newcastle (AU)\n[Thermal/Coking Coal]",
    3: "Samarinda (ID)\n[Thermal Coal]",
    4: "Singapore Strait\n[Transit Chokepoint]",
    5: "Paradip (IN)\n[Primary Import Port]",
    6: "Visakhapatnam (IN)\n[Deepwater Import]",
    7: "Haldia (IN)\n[Riverine Import]"
}

# Draw 11 Edges
edges = [
    (0, 4), (1, 4), (2, 4), (3, 4),
    (4, 5), (4, 6), (4, 7),
    (5, 6), (6, 7), (5, 7),
    (0, 5) # Direct Capesize Route
]

for u, v in edges:
    x_coords = [pos[u][0], pos[v][0]]
    y_coords = [pos[u][1], pos[v][1]]
    if (u, v) == (0, 5) or (v, u) == (0, 5):
        ax.plot(x_coords, y_coords, color='#dc2626', linestyle='--', linewidth=2.0, zorder=1, label='Direct Capesize Corridor' if u==0 else "")
    elif u == 4 or v == 4:
        ax.plot(x_coords, y_coords, color='#3b82f6', linestyle='-', linewidth=1.8, zorder=1)
    else:
        ax.plot(x_coords, y_coords, color='#64748b', linestyle=':', linewidth=1.5, zorder=1)

# Draw Nodes
for node_id, (x, y) in pos.items():
    bg = '#dc2626' if node_id == 0 else ('#f97316' if node_id == 4 else ('#2563eb' if node_id in [5,6,7] else '#475569'))
    ax.scatter(x, y, s=600, color=bg, edgecolor='#0f172a', linewidth=1.5, zorder=2)
    ax.text(x, y, str(node_id), ha='center', va='center', fontsize=9.5, fontweight='bold', color='#ffffff', zorder=3)
    
    # Label placement
    x_offset = -0.02 if x < 0.4 else (0.02 if x > 0.6 else 0.0)
    ha_align = 'right' if x < 0.4 else ('left' if x > 0.6 else 'center')
    y_offset = -0.08 if node_id == 4 else 0.0
    ax.text(x + x_offset, y + y_offset, node_names_map[node_id], ha=ha_align, va='center', fontsize=8, fontweight='bold', color='#0f172a')

ax.set_title("CONTROLLED MARITIME NETWORK — ARCHITECTURAL POC\n(8 Physical Nodes & 11 Navigable Corridors)", fontsize=11, fontweight='bold', pad=12, color='#0f172a')
ax.set_xlim(0.0, 1.05)
ax.set_ylim(0.05, 0.95)
ax.axis('off')
ax.text(0.5, 0.02, "Source: PRIMARINE controlled architectural simulation — not historical AIS validation", ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/06_maritime_graph.png", dpi=300)
plt.close()
print("Saved 06_maritime_graph.png")

# ----------------------------------------------------------------------
# FIGURE 07: ST-GNN HOP PROPAGATION ATTENUATION
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
hops = ['Hop 0: Epicenter\n(Hay Point Shock)', 'Hop 1: Direct Corridors\n(Singapore & Paradip Mean)', 'Hop 2: Secondary Hubs\n(Vizag, Haldia, Origins Mean)']
hop_deltas = [0.2204, 0.1545, 0.0325]
hop_cols = ['#dc2626', '#f97316', '#3b82f6']

bars = ax.bar(hops, hop_deltas, color=hop_cols, width=0.45, edgecolor='#1e293b', linewidth=1.2)
ax.set_title("ST-GNN Spatial Disruption Attenuation Across Graph Hops", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "Controlled Cyclone Shock at Hay Point (Queensland, Australia)", transform=ax.transAxes, ha='center', fontsize=9, color='#64748b')
ax.set_ylabel("Mean Propagated Risk Score $\\Delta$ [0, 1]", fontsize=10, fontweight='bold', color='#1e293b')
ax.set_ylim(0, 0.28)
ax.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.008, f"+{y:.4f}", ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Attenuation decay arrow
ax.annotate("HOP 0  →  HOP 1  →  HOP 2\n+0.2204 → +0.1545 → +0.0325\n(Monotonic Spatial Decay)",
            xy=(1, 0.1545), xytext=(1.8, 0.22),
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#0f172a"),
            ha='center', fontsize=8.5, fontweight='bold', color='#0f172a',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#f8fafc', edgecolor='#cbd5e1'))

ax.text(0.5, -0.16, "Source: PRIMARINE controlled architectural simulation — not historical AIS validation", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/07_stgnn_hop_propagation.png", dpi=300)
plt.close()
print("Saved 07_stgnn_hop_propagation.png")

# ----------------------------------------------------------------------
# FIGURE 08: COUNTERFACTUAL SHOCK EXPERIMENT
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=300)
scenarios = ['Scenario A\n(Baseline: No Shock)', 'Scenario B\n(Moderate Shock: Sev=1.0)', 'Scenario C\n(Severe Shock: Sev=1.5)']
hp_risks = [0.3547, 0.5751, 0.6799]
pdp_risks = [0.3806, 0.5525, 0.6364]

x = np.arange(len(scenarios))
w = 0.32

b1 = ax.bar(x - w/2, hp_risks, w, label='Hay Point (AU) — Epicenter Origin', color='#dc2626', edgecolor='#1e293b', linewidth=1.1)
b2 = ax.bar(x + w/2, pdp_risks, w, label='Paradip (IN) — Primary Discharge Port', color='#2563eb', edgecolor='#1e293b', linewidth=1.1)

ax.set_title("Controlled Counterfactual: Increasing Shock Severity", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "Monotonic downstream response under controlled simulation (Architectural ST-GNN POC)", transform=ax.transAxes, ha='center', fontsize=8.8, color='#64748b')
ax.set_ylabel("Computed Risk Score [0, 1]", fontsize=10, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=9, fontweight='bold')
ax.set_ylim(0, 0.85)
ax.grid(axis='y', linestyle=':', alpha=0.6)
ax.legend(loc='upper left', fontsize=9)

for bar in b1:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015, f"{y:.4f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
for bar in b2:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015, f"{y:.4f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

ax.text(0.5, -0.16, "Source: PRIMARINE controlled architectural simulation — not historical AIS validation", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/08_stgnn_counterfactual.png", dpi=300)
plt.close()
print("Saved 08_stgnn_counterfactual.png")

# ----------------------------------------------------------------------
# FIGURE 09: CONNECTED VS ISOLATED NODES
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.2), dpi=300)
test_nodes = ['Hay Point (AU)\n[Epicenter Shock]', 'Paradip (IN)\n[Connected Dest.]', 'Singapore\n[Connected Hub]', 'Rotterdam (NL)\n[Isolated Control]', 'Santos (BR)\n[Isolated Control]']
deltas = [0.2204, 0.1719, 0.1371, 0.0000, 0.0000]
colors = ['#dc2626', '#2563eb', '#f97316', '#94a3b8', '#94a3b8']

bars = ax.bar(test_nodes, deltas, color=colors, width=0.48, edgecolor='#1e293b', linewidth=1.2)
ax.set_title("Network-Topology Sanity Check", fontsize=12, fontweight='bold', pad=12, color='#0f172a')
ax.text(0.5, 1.02, "Controlled Structural Experiment: Connected Corridors vs Isolated Control Hubs", transform=ax.transAxes, ha='center', fontsize=9, color='#64748b')
ax.set_ylabel("Propagated Risk Score $\\Delta$", fontsize=10, fontweight='bold')
ax.set_ylim(-0.02, 0.28)
ax.grid(axis='y', linestyle=':', alpha=0.6)

for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, max(y, 0) + 0.008, f"+{y:.4f}" if y>0 else "0.0000", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.annotate("ISOLATED CONTROL EXPERIMENT\nZero energy leakage to unconnected Atlantic ports",
            xy=(3.5, 0.00), xytext=(3.5, 0.12),
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#64748b"),
            ha='center', fontsize=8.5, color='#334155',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#f1f5f9', edgecolor='#94a3b8'))

ax.text(0.5, -0.18, "Source: PRIMARINE controlled architectural simulation — not historical AIS validation", transform=ax.transAxes, ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/09_connected_vs_isolated.png", dpi=300)
plt.close()
print("Saved 09_connected_vs_isolated.png")

# ----------------------------------------------------------------------
# FIGURE 10: EVIDENCE BOUNDARY
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

ax.text(0.5, 0.95, "What PRIMARINE Has Demonstrated vs What Comes Next", ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
ax.text(0.5, 0.90, "Definitive Scientific & Implementation Boundaries for SIH 2026", ha='center', va='center', fontsize=9.5, color='#64748b')

def draw_tier_box(x, y, w, h, title, items, bg_col, border_col, header_col):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", facecolor=bg_col, edgecolor=border_col, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.06, title, ha='center', va='center', fontsize=11, fontweight='bold', color=header_col)
    text_body = "\n\n".join(items)
    ax.text(x + 0.02, y + h*0.45, text_body, ha='left', va='center', fontsize=8.5, color='#1e293b', linespacing=1.3)

tier1_items = [
    "• 1,920 Daily Market Data Rows (2018–2026)",
    "• LightGBM Turning-Point F1 (59.51%)",
    "• Persistence MAE (0.4175 vs 0.4644)",
    "• Split-CQR Uncertainty (88.19% Test Cov)",
    "• Decision Backtest (+1.04% Untouched)"
]
draw_tier_box(0.04, 0.12, 0.28, 0.72, "1. VALIDATED EMPIRICAL", tier1_items, "#f0fdf4", "#22c55e", "#15803d")

tier2_items = [
    "• 8-Node Maritime Graph (11 Corridors)",
    "• ST-GNN Message-Passing Equation",
    "• Cyclone Shock Spatial Attenuation",
    "• Monotonic Counterfactual Simulation",
    "• Disconnected Control Isolation"
]
draw_tier_box(0.36, 0.12, 0.28, 0.72, "2. CONTROLLED POC", tier2_items, "#eff6ff", "#3b82f6", "#1d4ed8")

tier3_items = [
    "• Live Streaming Satellite AIS Feeds",
    "• Port Authority EDI Berth Queues",
    "• Historical Disruption Incident Labels",
    "• 50+ Node Production ST-GNN Model",
    "• Enterprise React/Mapbox Command UI"
]
draw_tier_box(0.68, 0.12, 0.28, 0.72, "3. FUTURE SYSTEM", tier3_items, "#f8fafc", "#94a3b8", "#475569")

ax.text(0.5, 0.04, "Source: PRIMARINE Ideation Evidence Classification Framework", ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/10_evidence_boundary.png", dpi=300)
plt.close()
print("Saved 10_evidence_boundary.png")

# ----------------------------------------------------------------------
# FIGURE 11: DECISION INTELLIGENCE
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

ax.text(0.5, 0.94, "PRIMARINE Charter Decision Intelligence Framework", ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
ax.text(0.5, 0.89, "Synthesis of Market Momentum, Predictive Uncertainty, and Spatial Disruption Risk", ha='center', va='center', fontsize=9.5, color='#64748b')

# 3 Input Pillars
draw_box(0.06, 0.60, 0.26, 0.20, "MARKET FORECAST", "7-Day Rate Movement\nInflection Warning (F1: 59.5%)", "#f0fdf4", "#16a34a")
draw_box(0.37, 0.60, 0.26, 0.20, "CQR UNCERTAINTY", "Finite-Sample Width\nInterval Breadth Monitoring", "#fefce8", "#ca8a04")
draw_box(0.68, 0.60, 0.26, 0.20, "ST-GNN NETWORK RISK", "Corridor Disruption Index\nSpatial Shock Propagation", "#eff6ff", "#2563eb")

# Decision Core
draw_box(0.20, 0.30, 0.60, 0.18, "CHARTER DECISION & REGRET OPTIMIZER", "Deterministic Rules: Evaluates Expected Freight Shift vs Uncertainty Risk Threshold\nProcurement Advantage: +1.04% Untouched (+1.04%–+2.95% Rolling)", "#faf5ff", "#9333ea")

# Action Outputs
draw_box(0.06, 0.08, 0.20, 0.14, "ENTER_NOW", "Rising Market Ahead\nLow Route Risk", "#dcfce7", "#16a34a")
draw_box(0.29, 0.08, 0.20, 0.14, "DEFER_ENTRY", "Softening Market Ahead\nCost Savings from Delay", "#e0f2fe", "#0284c7")
draw_box(0.52, 0.08, 0.20, 0.14, "MONITOR", "Range-bound Market\nStable Shipping Rates", "#f1f5f9", "#64748b")
draw_box(0.75, 0.08, 0.20, 0.14, "HIGH UNCERTAINTY\n/ ABSTAIN", "Stress Regime / Wide CQR\nHalts Auto-Guidance", "#fee2e2", "#dc2626")

# Arrows
ax.annotate("", xy=(0.35, 0.48), xytext=(0.19, 0.60), arrowprops=arrow_kw)
ax.annotate("", xy=(0.50, 0.48), xytext=(0.50, 0.60), arrowprops=arrow_kw)
ax.annotate("", xy=(0.65, 0.48), xytext=(0.81, 0.60), arrowprops=arrow_kw)

ax.annotate("", xy=(0.16, 0.22), xytext=(0.35, 0.30), arrowprops=arrow_kw)
ax.annotate("", xy=(0.39, 0.22), xytext=(0.45, 0.30), arrowprops=arrow_kw)
ax.annotate("", xy=(0.62, 0.22), xytext=(0.55, 0.30), arrowprops=arrow_kw)
ax.annotate("", xy=(0.85, 0.22), xytext=(0.65, 0.30), arrowprops=arrow_kw)

ax.text(0.5, 0.02, "Source: PRIMARINE Decision-support prototype — not autonomous charter execution", ha='center', fontsize=7.5, color='#94a3b8')
plt.tight_layout()
plt.savefig("figures/ideation_evidence/11_decision_intelligence.png", dpi=300)
plt.close()
print("Saved 11_decision_intelligence.png")

print("\n=== All 11 Evidence Visualizations Successfully Generated! ===", flush=True)
