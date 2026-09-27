import os
import json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

os.makedirs("research/decision_boundary", exist_ok=True)

print("=== PRIMARINE Decision Boundary: Exp 15 - Bootstrap & Association Statistics ===", flush=True)

db_df = pd.read_csv("research/decision_boundary/decision_boundary_analysis.csv")
N = len(db_df)

# 1. Association metrics: Pointwise Timing Error & False Breakout vs Signals
corr_w_err, p_w_err = stats.spearmanr(db_df['interval_width_W'], db_df['timing_error'])
corr_nm_err, p_nm_err = stats.spearmanr(db_df['norm_margin_NM'], db_df['timing_error'])
corr_bc_err, p_bc_err = stats.spearmanr(db_df['boundary_crossing'], db_df['timing_error'])

corr_w_fb, p_w_fb = stats.spearmanr(db_df['interval_width_W'], db_df['false_breakout'])
corr_nm_fb, p_nm_fb = stats.spearmanr(db_df['norm_margin_NM'], db_df['false_breakout'])
corr_bc_fb, p_bc_fb = stats.spearmanr(db_df['boundary_crossing'], db_df['false_breakout'])

auc_w_err = roc_auc_score(db_df['timing_error'], db_df['interval_width_W'])
auc_nm_err = roc_auc_score(db_df['timing_error'], -db_df['norm_margin_NM'])
auc_bc_err = roc_auc_score(db_df['timing_error'], db_df['boundary_crossing']) if len(db_df['boundary_crossing'].unique()) > 1 else 0.5

auc_w_fb = roc_auc_score(db_df['false_breakout'], db_df['interval_width_W'])
auc_nm_fb = roc_auc_score(db_df['false_breakout'], -db_df['norm_margin_NM'])
auc_bc_fb = roc_auc_score(db_df['false_breakout'], db_df['boundary_crossing']) if len(db_df['boundary_crossing'].unique()) > 1 else 0.5

print(f"AUC Timing Error: Width={auc_w_err:.4f}, NormMargin={auc_nm_err:.4f}, BoundaryCrossing={auc_bc_err:.4f}")
print(f"AUC False Breakout: Width={auc_w_fb:.4f}, NormMargin={auc_nm_fb:.4f}, BoundaryCrossing={auc_bc_fb:.4f}")

# 2. Bootstrap 95% Confidence Intervals (B = 1000)
np.random.seed(42)
B_boot = 1000

boot_stats = []
for b in range(B_boot):
    idx = np.random.choice(N, size=N, replace=True)
    samp = db_df.iloc[idx]
    
    # Stratified by high vs low width
    hw_mask = samp['high_width_flag'] == 1
    lw_mask = samp['high_width_flag'] == 0
    
    fb_hw = samp[hw_mask]['false_breakout'].mean() if hw_mask.sum() > 0 else 0.0
    fb_lw = samp[lw_mask]['false_breakout'].mean() if lw_mask.sum() > 0 else 0.0
    
    # Stratified by high vs low normalized margin
    lm_mask = samp['low_margin_flag'] == 1
    hm_mask = samp['low_margin_flag'] == 0
    
    fb_lm = samp[lm_mask]['false_breakout'].mean() if lm_mask.sum() > 0 else 0.0
    fb_hm = samp[hm_mask]['false_breakout'].mean() if hm_mask.sum() > 0 else 0.0
    
    err_hw = samp[hw_mask]['timing_error'].mean() if hw_mask.sum() > 0 else 0.0
    err_lw = samp[lw_mask]['timing_error'].mean() if lw_mask.sum() > 0 else 0.0
    
    err_lm = samp[lm_mask]['timing_error'].mean() if lm_mask.sum() > 0 else 0.0
    err_hm = samp[hm_mask]['timing_error'].mean() if hm_mask.sum() > 0 else 0.0
    
    boot_stats.append({
        "fb_hw": fb_hw, "fb_lw": fb_lw, "fb_diff_width": fb_hw - fb_lw,
        "fb_lm": fb_lm, "fb_hm": fb_hm, "fb_diff_margin": fb_lm - fb_hm,
        "err_hw": err_hw, "err_lw": err_lw, "err_diff_width": err_hw - err_lw,
        "err_lm": err_lm, "err_hm": err_hm, "err_diff_margin": err_lm - err_hm
    })

boot_df = pd.DataFrame(boot_stats)
boot_summary = {
    "metric": [
        "P(False Breakout | High Width)",
        "P(False Breakout | Low Width)",
        "Width False Breakout Risk Diff",
        "P(False Breakout | Low Norm Margin)",
        "P(False Breakout | High Norm Margin)",
        "Margin False Breakout Risk Diff",
        "P(Timing Error | High Width)",
        "P(Timing Error | Low Width)",
        "P(Timing Error | Low Norm Margin)",
        "P(Timing Error | High Norm Margin)"
    ],
    "mean": [
        boot_df['fb_hw'].mean(), boot_df['fb_lw'].mean(), boot_df['fb_diff_width'].mean(),
        boot_df['fb_lm'].mean(), boot_df['fb_hm'].mean(), boot_df['fb_diff_margin'].mean(),
        boot_df['err_hw'].mean(), boot_df['err_lw'].mean(),
        boot_df['err_lm'].mean(), boot_df['err_hm'].mean()
    ],
    "ci_lower": [
        np.percentile(boot_df['fb_hw'], 2.5), np.percentile(boot_df['fb_lw'], 2.5), np.percentile(boot_df['fb_diff_width'], 2.5),
        np.percentile(boot_df['fb_lm'], 2.5), np.percentile(boot_df['fb_hm'], 2.5), np.percentile(boot_df['fb_diff_margin'], 2.5),
        np.percentile(boot_df['err_hw'], 2.5), np.percentile(boot_df['err_lw'], 2.5),
        np.percentile(boot_df['err_lm'], 2.5), np.percentile(boot_df['err_hm'], 2.5)
    ],
    "ci_upper": [
        np.percentile(boot_df['fb_hw'], 97.5), np.percentile(boot_df['fb_lw'], 97.5), np.percentile(boot_df['fb_diff_width'], 97.5),
        np.percentile(boot_df['fb_lm'], 97.5), np.percentile(boot_df['fb_hm'], 97.5), np.percentile(boot_df['fb_diff_margin'], 97.5),
        np.percentile(boot_df['err_hw'], 97.5), np.percentile(boot_df['err_lw'], 97.5),
        np.percentile(boot_df['err_lm'], 97.5), np.percentile(boot_df['err_hm'], 97.5)
    ]
}

boot_res_df = pd.DataFrame(boot_summary)
boot_res_df.to_csv("research/decision_boundary/bootstrap_statistics.csv", index=False)
print("\n--- Bootstrap Confidence Intervals ---")
print(boot_res_df.to_string())

# 3. Margin Stratification Analysis (Experiment D)
# Bins based on decision margin M = C - B
m_bins = [-np.inf, -0.4, -0.1, 0.1, 0.4, np.inf]
m_labels = ["Strong Defer (M < -0.4)", "Weak Defer (-0.4 <= M < -0.1)", "Near-Zero (|M| <= 0.1)", "Weak Enter (0.1 < M <= 0.4)", "Strong Enter (M > 0.4)"]
db_df['margin_stratum'] = pd.cut(db_df['decision_margin_M'], bins=m_bins, labels=m_labels)

margin_strat_summary = db_df.groupby('margin_stratum', observed=False).agg(
    N=('scenario_idx', 'count'),
    False_Breakout_Rate=('false_breakout', 'mean'),
    Timing_Error_Rate=('timing_error', 'mean'),
    Mean_Regret=('regret', 'mean'),
    Median_Regret=('regret', 'median')
).reset_index()

margin_strat_summary.to_csv("research/decision_boundary/margin_analysis.csv", index=False)
print("\n--- Margin Stratum Analysis ---")
print(margin_strat_summary.to_string())
