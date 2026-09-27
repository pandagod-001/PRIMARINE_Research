import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open("results/metrics.json") as f:
    metrics = json.load(f)

# Figure: Model Metric Comparison (Judge Graph 2 - Fixed Layout)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300)

models_list = list(metrics.keys())
models_clean = ['Naive Persistence\n(Random Walk)', '5-Day Moving Avg\n(Technical)', 'AutoReg(5)\n(Statistical)', 'LightGBM\n(Multi-Modal)', 'XGBoost\n(Multi-Modal)']
mae_vals = [metrics[m]['MAE'] for m in models_list]
dir_acc_vals = [metrics[m]['Directional_Accuracy_Pct'] for m in models_list]

colors = ['#94a3b8', '#64748b', '#0284c7', '#2563eb', '#1d4ed8']

# MAE Comparison
bars1 = ax1.bar(models_clean, mae_vals, color=colors, width=0.55, edgecolor='#334155', linewidth=0.8)
ax1.set_title('Forecast Level Error (MAE - $/unit)\n[Lower is Better]', fontsize=11, fontweight='bold', color='#0f172a', pad=12)
ax1.set_ylabel('Mean Absolute Error ($/unit)', fontsize=10, fontweight='bold')
ax1.set_ylim(0, 0.60)
ax1.grid(True, linestyle=':', alpha=0.6, axis='y')
ax1.tick_params(axis='x', labelsize=9)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.015, f'{yval:.3f}', ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Directional Accuracy Comparison
bars2 = ax2.bar(models_clean, dir_acc_vals, color=colors, width=0.55, edgecolor='#334155', linewidth=0.8)
ax2.set_title('Directional Trend Accuracy (%)\n[Higher is Better — Key for Charter Timing Decision]', fontsize=11, fontweight='bold', color='#0f172a', pad=12)
ax2.set_ylabel('Directional Accuracy (%)', fontsize=10, fontweight='bold')
ax2.set_ylim(0, 80)
ax2.axhline(50, color='#ef4444', linestyle='--', linewidth=1.5, label='Random Chance Baseline (50%)')
ax2.grid(True, linestyle=':', alpha=0.6, axis='y')
ax2.tick_params(axis='x', labelsize=9)
ax2.legend(loc='lower left', frameon=True, framealpha=0.9, fontsize=9)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=9.5, fontweight='bold')

plt.suptitle('PRIMARINE Model Benchmark vs Classical Baselines (Strict Out-of-Sample Rolling Test)', fontsize=13, fontweight='bold', color='#0f172a', y=0.98)
plt.tight_layout(rect=[0, 0.05, 1, 0.94])
plt.savefig('results/figures/model_backtest_comparison.png')
plt.savefig('PRIMARINE_EVIDENCE/figures/model_backtest_comparison.png')
plt.close()
print("Regenerated clean model comparison graph.")
