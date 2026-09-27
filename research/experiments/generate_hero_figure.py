import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig = plt.figure(figsize=(13, 7.5), dpi=300)
ax = fig.add_subplot(111)
ax.axis('off')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Colors
c_input = '#1f77b4'
c_cqr = '#2ca02c'
c_phys = '#3498db'
c_risk = '#e67e22'
c_abstain = '#e74c3c'
c_out = '#2c3e50'
c_box_bg = '#f8f9fa'

# Title
ax.text(50, 96, "PRIMARINE: Conformal Uncertainty-Gated Decision Pipeline", 
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1a252f')
ax.text(50, 92, "Empirical Evidence & Metric Flow Across Asymmetric Decision Layers", 
        ha='center', va='center', fontsize=11, fontstyle='italic', color='#555555')

def draw_box(ax, x, y, w, h, title, lines, color, bg='#ffffff', title_color='#ffffff'):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.5", 
                                  linewidth=1.8, edgecolor=color, facecolor=bg, zorder=2)
    ax.add_patch(rect)
    # Header bar
    hdr = patches.FancyBboxPatch((x, y + h - 3.5), w, 3.5, boxstyle="round,pad=0.5,rounding_size=1.0",
                                 linewidth=0, facecolor=color, zorder=3)
    ax.add_patch(hdr)
    ax.text(x + w/2, y + h - 1.8, title, ha='center', va='center', fontsize=10, fontweight='bold', color=title_color, zorder=4)
    
    # Body text
    y_text = y + h - 6.0
    for line in lines:
        ax.text(x + 1.5, y_text, line, ha='left', va='center', fontsize=8.5, color='#2c3e50', zorder=4)
        y_text -= 2.6

# 1. Prediction Layer (Top Center)
draw_box(ax, 35, 76, 30, 13, "1. FREIGHT FORECASTING", [
    "• Target: 7-Day Forward Spot Freight",
    "• Model: LightGBM Regressor",
    "• Metric: F1 = 59.51% (Turning Points)",
    "• Baseline: AR(5) F1 = 27.18%"
], c_input)

# 2. Conformal Quantification Layer
draw_box(ax, 35, 57, 30, 14, "2. CONFORMAL QUANTIFICATION", [
    "• Split-CQR (Nominal 90.0%)",
    "• Calibration: q_calib = 0.8415",
    "• Test Coverage: 88.19% - 95.83%",
    "• Mean Interval Width W = 5.76 $/MT"
], c_cqr)

# 3. Branch A: Physical Feasibility Layer (Left)
draw_box(ax, 5, 27, 38, 22, "3A. PHYSICAL FEASIBILITY FILTER", [
    "• Hard Constraints: Draft (17.1m vs 11.5m),",
    "  LOA, Beam & Deadweight (120k MT)",
    "• Result: Physical Allocation Invariance",
    "  --> PDFR = 0.00% across 360 scenarios",
    "• Feasibility Retention: BPFR = 1.0",
    "• Negative Control: 100% Stability",
    "• Insight: Discrete physical walls insulate",
    "  vessel/port selection from rate swings"
], c_phys)

# 4. Branch B: Uncertainty-Gated Risk & Selective Abstention (Right)
draw_box(ax, 57, 27, 38, 22, "3B. UNCERTAINTY-GATED TIMING", [
    "• Timing Fragility: TDFR = 50% - 100%",
    "• Macro-Regime Signal: CQR Width W",
    "  --> AUC = 0.6719 for False Breakouts",
    "  --> High W Rate: 40.25% vs Low W: 23.39%",
    "  --> Risk Diff = +16.86% [6.14%, 28.52%]",
    "• Negative Findings Preserved:",
    "  --> Boundary Crossing: Degenerate (AUC 0.50)",
    "  --> Direction Error: Uncorrelated (AUC 0.45)"
], c_risk)

# 5. Selective Abstention Mechanism (Sub-box in Right Branch)
draw_box(ax, 60, 9, 32, 13, "4. SELECTIVE ABSTENTION", [
    "• Pre-Calibrated Threshold: tau = 1.35x",
    "• False Breakouts: 86 --> 41 (52.33% Cut)",
    "• Decision Coverage = 61.11%",
    "• Trade-off: +0.453% (+0.0334 $/MT)"
], c_abstain)

# 6. Final Decision Integration (Bottom Center-Left)
draw_box(ax, 10, 9, 30, 13, "5. OPTIMAL CHARTER PLAN", [
    "• Full Adaptive Pipeline (E5)",
    "• Feasible Vessel & Berth Allocation",
    "• Paired Wilcoxon Test: p = 5.42e-11",
    "• Disruption Recovery: +3.90 $/MT"
], c_out)

# Connectors (Arrows)
def draw_arrow(ax, x1, y1, x2, y2, color='#7f8c8d'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, shrink=0.05), zorder=5)

# Forecast -> CQR
draw_arrow(ax, 50, 76, 50, 71, c_input)

# CQR -> Physical (Fork Left)
draw_arrow(ax, 40, 57, 24, 49, c_cqr)

# CQR -> Timing (Fork Right)
draw_arrow(ax, 60, 57, 76, 49, c_cqr)

# Timing -> Abstention
draw_arrow(ax, 76, 27, 76, 22, c_risk)

# Physical -> Final Plan
draw_arrow(ax, 24, 27, 24, 22, c_phys)

# Abstention -> Final Plan (Gating feedback)
ax.annotate('', xy=(40, 15), xytext=(60, 15),
            arrowprops=dict(facecolor=c_abstain, edgecolor=c_abstain, width=1.5, headwidth=6, shrink=0.05), zorder=5)
ax.text(50, 16.5, "Gated Commitment / Abstain", ha='center', va='center', fontsize=8, fontweight='bold', color=c_abstain)

plt.tight_layout()
plt.savefig("research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png", dpi=300, bbox_inches='tight')
plt.savefig("research/figures/hero_decision_pipeline.png", dpi=300, bbox_inches='tight')
print("Hero Decision Pipeline Diagram generated successfully in research/PRIMARINE_RESEARCH_PACKAGE/hero_decision_pipeline.png")
